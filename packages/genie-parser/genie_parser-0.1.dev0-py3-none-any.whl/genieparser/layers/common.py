# Copyright 2017 The Board of Trustees of the Leland Stanford Junior University
#
# Author: Giovanni Campagna <gcampagn@cs.stanford.edu>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>. 
'''
Created on Dec 22, 2017

@author: gcampagn
'''

import tensorflow as tf
from tensorflow.python.util import nest
from tensor2tensor.layers import common_layers
from tensor2tensor.layers import common_attention
from tensor2tensor.utils import beam_search

from tensorflow.contrib.seq2seq import LuongAttention, AttentionWrapper

from collections import namedtuple
import numpy as np

StackRNNState = namedtuple('StackRNNState', ('hidden_state', 'stacks'))

class StackRNNCell(tf.contrib.rnn.RNNCell):
    '''
    Stack-Augmented RNN Cell, from:
    "Inferring Algorithmic Patterns with Stack-Augmented Recurrent Nets"
    '''
    
    def __init__(self, num_units, num_stacks=2, stack_size=50, stack_top_k=2, activation=tf.sigmoid):
        super().__init__()
        
        self._num_units = num_units
        self._num_stacks = num_stacks
        self._stack_size = stack_size
        self._stack_top_k = stack_top_k

        self._action_layers = [tf.layers.Dense(3, activation=tf.nn.softmax, name=('action_layer_%d' % i)) for i in range(self._num_stacks)] # push, pop, nop
        self._push_layers = [tf.layers.Dense(self._num_units, activation=tf.sigmoid, use_bias=False, name=('push_layer_%d' % i)) for i in range(self._num_stacks)]
        self._cell_layer = tf.layers.Dense(self._num_units, activation=activation, name='cell_layer')
        
    def call(self, input, state):
        batch_size = tf.shape(input)[0]
             
        new_stacks = []
        for i in range(self._num_stacks):
            with tf.name_scope('stack_%d' % i):
                action = self._action_layers[i](state.hidden_state)
                push_prob = tf.expand_dims(action[:,0], axis=1)
                pop_prob = tf.expand_dims(action[:,1], axis=1)
                nop_prob = tf.expand_dims(action[:,2], axis=1)
                
                stack = tf.reshape(state.stacks[i], (batch_size, self._stack_size, self._num_units))
                
                stack_0 = stack[:,0]
                stack_1 = stack[:,1]
                with tf.name_scope('new_stack_0'): 
                    new_stack_0 = tf.expand_dims(push_prob * self._push_layers[i](state.hidden_state) +
                                                 pop_prob * stack_1 + nop_prob * stack_0, axis=1)
                with tf.name_scope('new_stack_i'):
                    stack_push = (stack[:,:-1])
                    stack_pop = tf.concat((stack[:,2:], tf.zeros((batch_size, 1, self._num_units), dtype=tf.float32)), axis=1)
                    stack_nop = stack[:,1:]
                    
                    new_stack_i = tf.expand_dims(push_prob, axis=1) * stack_push + \
                        tf.expand_dims(pop_prob, axis=1) * stack_pop + \
                        tf.expand_dims(nop_prob, axis=1) * stack_nop
                new_stack = tf.concat((new_stack_0, new_stack_i), axis=1)
                new_stacks.append(new_stack)
        
        stack_tops = [tf.reshape(stack[:,:self._stack_top_k], (batch_size, self._stack_top_k * self._num_units)) for stack in new_stacks]
        flat_input = tf.concat([input, state.hidden_state] + stack_tops, axis=1)
        new_hidden_state = self._cell_layer(flat_input)

        return new_hidden_state, StackRNNState(hidden_state=new_hidden_state,
                                               stacks=tuple(tf.reshape(stack, (batch_size, self._stack_size * self._num_units)) for stack in new_stacks))
    
    @property
    def output_size(self):
        return self._num_units
    
    @property
    def state_size(self):
        return StackRNNState(hidden_state=tf.TensorShape((self._num_units,)),
                             stacks=tuple(tf.TensorShape((self._stack_size * self._num_units)) for _ in range(self._num_stacks)))

def make_rnn_cell(cell_type, hidden_size, dropout):
    if cell_type == "lstm":
        cell = tf.contrib.rnn.LSTMBlockCell(hidden_size)
    elif cell_type == "gru":
        cell = tf.contrib.rnn.GRUBlockCellV2(hidden_size)
    elif cell_type == "basic-tanh":
        cell = tf.contrib.rnn.BasicRNNCell(hidden_size)
    elif cell_type == 'stackrnn':
        cell = StackRNNCell(hidden_size)
    else:
        raise ValueError("Invalid RNN Cell type")
    cell = tf.contrib.rnn.DropoutWrapper(cell,
                                         variational_recurrent=True,
                                         output_keep_prob=dropout,
                                         state_keep_prob=dropout if cell_type != 'gru' else 1.0,
                                         dtype=tf.float32)
    return cell

def make_multi_rnn_cell(num_layers, cell_type, hidden_size, dropout):
    return tf.contrib.rnn.MultiRNNCell([make_rnn_cell(cell_type, hidden_size, dropout) for _ in range(num_layers)])


class DotProductLayer(tf.layers.Layer):
    def __init__(self, against):
        super().__init__()
        self._against = against
        self._depth_size = self._against.get_shape()[1]
        self._output_size = self._against.get_shape()[0]
    
    def build(self, input_shape):
        input_shape = tf.TensorShape(input_shape)
        if input_shape[-1].value is None:
            raise ValueError("Input to DotProductLayer must have the last dimension defined")
        if input_shape[-1].value != self._depth_size:
            self._space_transform = self.add_variable('kernel',
                                                      shape=(input_shape[-1].value, self._depth_size),
                                                      dtype=self.dtype,
                                                      trainable=True)
        else:
            self._space_transform = None
        self.built = True
    
    def call(self, inputs):
        inputs = tf.convert_to_tensor(inputs, dtype=self.dtype)
        shape = inputs.get_shape().as_list()
        if len(shape) > 2:
            # Broadcasting is required for the inputs.
            if self._space_transform is not None:
                inputs = tf.tensordot(inputs, self._space_transform, [[len(shape) - 1], [0]])
            outputs = tf.tensordot(inputs, self._against, [[len(shape) - 1], [1]])
            
            # Reshape the output back to the original ndim of the input.
            output_shape = tf.TensorShape(shape[:-1] + [self._output_size])
            assert output_shape.is_compatible_with(outputs.shape)
            outputs.set_shape(output_shape)
            return outputs
        else:
            if self._space_transform is not None:
                inputs = tf.matmul(inputs, self._space_transform)
        
            # input is batch by depth
            # self._against is output by depth
            # result is batch by output
            return tf.matmul(inputs, self._against, transpose_b=True)

    def _compute_output_shape(self, input_shape):
        input_shape = tf.TensorShape(input_shape)
        input_shape = input_shape.with_rank_at_least(2)
        return input_shape[:-1].concatenate(self._output_size)


class EmbeddingPointerLayer(tf.layers.Layer):
    """
    A pointer layer that chooses from an embedding matrix (of size O x D, where
    D is the depth of the embedding and O the space of choices), using an MLP
    """
    def __init__(self, hidden_size, embeddings, activation=tf.tanh, dropout=1):
        super().__init__()
        
        self._embeddings = embeddings
        self._embedding_size = embeddings.shape[-1]
        self._hidden_size = hidden_size
        self._activation = activation
        self._dropout = dropout
        
    def build(self, input_shape):
        input_shape = tf.TensorShape(input_shape)
        
        self.kernel1 = self.add_variable('kernel1', shape=(self._embedding_size, self._hidden_size), dtype=self.dtype)
        self._matmul1 = tf.tensordot(self._embeddings, self.kernel1, [[1], [0]])

        self.kernel2 = self.add_variable('kernel2', shape=(input_shape[-1], self._hidden_size), dtype=self.dtype)
        self.bias = self.add_variable('bias', shape=(self._hidden_size,), dtype=self.dtype)
        self.output_projection = self.add_variable('output_projection', shape=(self._hidden_size,), dtype=self.dtype)
        self.built = True

    def call(self, inputs):
        with tf.name_scope('EmbeddingPointerLayer', (inputs,)):
            input_shape = inputs.shape
            matmul2 = tf.tensordot(inputs, self.kernel2, [[input_shape.ndims-1], [0]])
            
            matmul1 = self._matmul1
            for _ in range(input_shape.ndims-1):
                matmul1 = tf.expand_dims(matmul1, axis=0)
            
            matmul2 = tf.expand_dims(matmul2, axis=input_shape.ndims-1)
            
            neuron_input = matmul1 + matmul2
            neuron_input = tf.nn.bias_add(neuron_input, self.bias)
            activation = self._activation(neuron_input)
            activation = tf.nn.dropout(activation, keep_prob=self._dropout)
            
            scores = tf.tensordot(activation, self.output_projection, [[input_shape.ndims], [0]])
            return scores
    
    @property
    def output_size(self):
        #return tf.shape(self._embeddings)[0]
        return self._embeddings.shape[0]

    def compute_output_shape(self, *args):
        raise TypeError("that one")


class AttentivePointerLayer(tf.layers.Layer):
    """
    A pointer layer that chooses from the encoding of the inputs, using Luong (multiplicative) Attention
    """
    def __init__(self, enc_hidden_states):
        super().__init__()
        
        self._enc_hidden_states = enc_hidden_states
        self._num_units = enc_hidden_states.shape[-1]

    def call(self, inputs):
        original_shape = common_layers.shape_list(inputs)
        flattened_inputs = common_layers.flatten4d3d(inputs)

        projected_inputs = tf.layers.dense(flattened_inputs, self._num_units,
                                           use_bias=False)
        enc_time = tf.shape(self._enc_hidden_states)[1]

        score = tf.matmul(projected_inputs, self._enc_hidden_states, transpose_b=True)
        score *= tf.rsqrt(tf.to_float(self._num_units))

        return tf.reshape(score, original_shape[:-1] + [enc_time]) # (batch, dec_length, 1, enc_length)

    def compute_output_shape(self, input_shape):
        return input_shape[:-1].concatenate(tf.TensorShape([self._enc_hidden_states.shape[1]]))


class DecayingAttentivePointerLayer(tf.layers.Layer):
    """
    A pointer layer that chooses from the encoding of the inputs, using Luong (multiplicative) Attention
    """
    def __init__(self, enc_hidden_states):
        super().__init__()

        self._enc_hidden_states = enc_hidden_states # (?, ?, 128)
        self.enc_num_units = enc_hidden_states.shape[-1]

    def build(self, input_shape):
        input_shape = tf.TensorShape(input_shape)
        self.dec_num_units = input_shape[-1]
        self.kernel_encode = self.add_variable('kernel_encode', (self.dec_num_units, self.enc_num_units), dtype=self.dtype)
        self.built = True

    def _matmul(self, a, b): # (?, m, n) @ (n, p) -- > (?, m, p)
        return tf.reshape(tf.reshape(a, [-1, tf.shape(a)[-1]]) @ b, [-1, tf.shape(a)[1], tf.shape(b)[-1]])

    def call(self, decode_list):
        inputs = decode_list

        original_shape = common_layers.shape_list(inputs)
        inputs = common_layers.flatten4d3d(inputs) # (?, ?, 1, 128) -- > (?, ?, 128)

        e_ti = tf.matmul(self._matmul(inputs, self.kernel_encode), self._enc_hidden_states, transpose_b=True) # (batch, dec_length, enc_length)

        e_ti_max = tf.reduce_max(e_ti, axis=1, keepdims=True)
        cum_sum_ = tf.cumsum(tf.exp(e_ti - e_ti_max), axis=1)

        w = tf.tile(tf.expand_dims(tf.ones(tf.shape(cum_sum_)[-1]), axis=0), [tf.shape(inputs)[0], 1])
        cum_sum = tf.concat([tf.expand_dims(w, axis=1), cum_sum_[:,:-1,:]], axis=1)

        log_e_ti_prime = e_ti - (e_ti_max + tf.log(cum_sum + 1e-8))
        alpha_ti_encode = tf.nn.softmax(log_e_ti_prime, axis=2)

        enc_time = tf.shape(self._enc_hidden_states)[1]
        return tf.reshape(alpha_ti_encode, original_shape[:-1] + [enc_time]) # (batch, dec_length, 1, enc_length)

    def compute_output_shape(self, input_shape):
        return input_shape[:-1].concatenate(tf.TensorShape([self._enc_hidden_states.shape[1]]))


class DNNPointerLayer(tf.layers.Layer):
    def __init__(self, enc_hidden_states):
        super().__init__()
        
        self._num_units = enc_hidden_states.shape[-1]
        self._max_input_length = enc_hidden_states.shape[1]
        self._enc_hidden_states = enc_hidden_states

        self._layer1 = tf.layers.Dense(self._num_units, activation=tf.tanh, use_bias=True)
        self._layer2 = tf.layers.Dense(1, use_bias=True)

    def build(self, input_shape):

        layer1_input_shape = tf.TensorShape([None, self._max_input_length, input_shape[-1] + self._num_units])
        self._layer1.build(layer1_input_shape)
        intermediate_shape = self._layer1.compute_output_shape(layer1_input_shape)
        self._layer2.build(intermediate_shape)
        self.built = True

    def call(self, inputs):
        # inputs is [batch, depth]
        # tile it to [batch, time, depth]
        input_shape = tf.shape(self._enc_hidden_states)
        batch_size = input_shape[0]
        input_length = input_shape[1]
        tiled_inputs = tf.tile(tf.expand_dims(inputs, axis=1), [1, input_length, 1])

        dnn_inputs = tf.concat((self._enc_hidden_states, tiled_inputs), axis=2)
        dnn_outputs = self._layer2(self._layer1(dnn_inputs))

        # dnn outputs is [batch x time, depth == 1]
        return tf.reshape(dnn_outputs, (batch_size, input_length))

    def compute_output_shape(self, *args):
        return tf.TensorShape([None, self._max_input_length])


def pad_up_to(vector, size):
    rank = vector.get_shape().ndims - 1
    
    length_diff = tf.reshape(size - tf.shape(vector)[1], shape=(1,))
    with tf.control_dependencies([tf.assert_non_negative(length_diff, data=(vector, size, tf.shape(vector)))]):
        padding = tf.reshape(tf.concat([[0, 0, 0], length_diff, [0,0]*(rank-1)], axis=0), shape=((rank+1), 2))
        return tf.pad(vector, padding, mode='constant')


class ParentFeedingCellWrapper(tf.contrib.rnn.RNNCell):
    '''
    A cell wrapper that concatenates a fixed Tensor to the input
    before calling the wrapped cell
    '''
    def __init__(self, wrapped : tf.contrib.rnn.RNNCell, parent_state):
        super().__init__()
        self._wrapped = wrapped
        self._flat_parent_state = tf.concat(nest.flatten(parent_state), axis=1)
        
    def call(self, input, state):
        concat_input = tf.concat((self._flat_parent_state, input), axis=1)
        return self._wrapped.call(concat_input, state)
    
    @property
    def output_size(self):
        return self._wrapped.output_size
    
    @property
    def state_size(self):
        return self._wrapped.state_size


class InputIgnoringCellWrapper(tf.contrib.rnn.RNNCell):
    '''
    A cell wrapper that replaces the cell input with a fixed Tensor
    and ignores whatever input is passed in
    '''
    def __init__(self, wrapped : tf.contrib.rnn.RNNCell, constant_input):
        super().__init__()
        self._wrapped = wrapped
        self._flat_constant_input = tf.concat(nest.flatten(constant_input), axis=1)
        
    def call(self, input, state):
        return self._wrapped.call(self._flat_constant_input, state)
    
    @property
    def output_size(self):
        return self._wrapped.output_size
    
    @property
    def state_size(self):
        return self._wrapped.state_size

def unify_encoder_decoder(cell_dec, enc_hidden_states, enc_final_state):
    encoder_hidden_size = int(enc_hidden_states.get_shape()[-1])
    decoder_hidden_size = int(cell_dec.output_size)

    # if encoder and decoder have different sizes, add a projection layer
    if encoder_hidden_size != decoder_hidden_size:
        assert False, (encoder_hidden_size, decoder_hidden_size)
        with tf.variable_scope('hidden_projection'):
            kernel = tf.get_variable('kernel', (encoder_hidden_size, decoder_hidden_size), dtype=tf.float32)
        
            enc_final_state = nest.map_structure(lambda x: tf.matmul(x, kernel), enc_final_state)
            enc_hidden_states = tf.tensordot(enc_hidden_states, kernel, [[2], [1]])
    else:
        # flatten and repack the state
        enc_final_state = nest.pack_sequence_as(cell_dec.state_size, nest.flatten(enc_final_state))
    
    return enc_hidden_states, enc_final_state


def _enumerated_map_structure_up_to(shallow_structure, map_fn, *args, **kwargs):
    ix = [0]
    def enumerated_fn(*inner_args, **inner_kwargs):
        r = map_fn(ix[0], *inner_args, **inner_kwargs)
        ix[0] += 1
        return r
    return nest.map_structure_up_to(shallow_structure, enumerated_fn, *args, **kwargs)


class NotBrokenDropoutWrapper(tf.contrib.rnn.DropoutWrapper):
    def __init__(self, cell, output_keep_prob):
        self._dropout_state_filter = lambda x: False
        self._state_keep_prob = 1.0
        self._input_keep_prob = 1.0
        self._output_keep_prob = output_keep_prob

        self._cell = cell
        self._variational_recurrent = True
        self._seed = None

        self._recurrent_input_noise = None
        self._recurrent_state_noise = None
        self._recurrent_output_noise = None

        def convert_to_batch_shape(s):
            # Prepend a 1 for the batch dimension; for recurrent
            # variational dropout we use the same dropout mask for all
            # batch elements.
            return tf.concat(([1], tf.TensorShape(s).as_list()), 0)

        def batch_noise(s, inner_seed):
            shape = convert_to_batch_shape(s)
            return tf.random_uniform(shape, seed=inner_seed, dtype=tf.float32)

        self._recurrent_output_noise = _enumerated_map_structure_up_to(
            cell.output_size,
            lambda i, s: batch_noise(s, inner_seed=self._gen_seed("output", i)),
            cell.output_size)


class ActivationWrapper(tf.contrib.rnn.RNNCell):
    def __init__(self, cell, activation=tf.tanh):
        super().__init__()

        self._cell = cell
        self._activation = activation

    @property
    def output_size(self):
        return self._cell.output_size

    @property
    def state_size(self):
        return self._cell.state_size

    def call(self, inputs, state):
        output, next_state = self._cell(inputs, state)
        return nest.map_structure(lambda x: self._activation(x), output), next_state

def apply_attention(cell_dec, enc_hidden_states, enc_final_state, input_length, batch_size, attention_probability_fn,
                    dropout, alignment_history=True):

    if attention_probability_fn == 'softmax':
        probability_fn = tf.nn.softmax
        score_mask_value = float('-inf')
    elif attention_probability_fn == 'hardmax':
        probability_fn = tf.contrib.seq2seq.hardmax
        score_mask_value = float('-inf')
    elif attention_probability_fn == 'sparsemax':
        def sparsemax(attentionscores):
            attentionscores = tf.contrib.sparsemax.sparsemax(attentionscores)
            with tf.control_dependencies([tf.assert_non_negative(attentionscores),
                                          tf.assert_less_equal(attentionscores, 1., summarize=60)]):
                return tf.identity(attentionscores)
        probability_fn = sparsemax
        # sparsemax does not deal with -inf properly, and has significant numerical stability issues
        # with large numbers (positive or negative)
        score_mask_value = -1e+5
    else:
        raise ValueError("Invalid attention_probability_fn " + str(attention_probability_fn))
    
    with tf.variable_scope('attention', initializer=tf.initializers.identity(dtype=tf.float32)):
        attention = LuongAttention(int(cell_dec.output_size), enc_hidden_states,
                                   memory_sequence_length=input_length,
                                   probability_fn=probability_fn,
                                   score_mask_value=score_mask_value)
    cell_dec = AttentionWrapper(cell_dec, attention,
                                cell_input_fn=lambda inputs, _: inputs,
                                attention_layer_size=int(cell_dec.output_size),
                                alignment_history=alignment_history,
                                initial_cell_state=enc_final_state)
    enc_final_state = cell_dec.zero_state(batch_size, dtype=tf.float32)

    cell_dec = ActivationWrapper(cell_dec, activation=tf.tanh)
    cell_dec = NotBrokenDropoutWrapper(cell_dec, output_keep_prob=dropout)

    return cell_dec, enc_final_state


def fast_decode(symbols_to_logits_fn,
                hparams,
                decode_length,
                vocab_size,
                beam_size=1,
                top_beams=1,
                alpha=1.0,
                eos_id=beam_search.EOS_ID,
                batch_size=None,
                force_decode_length=False,
                cache=None):
    """Given encoder output and a symbols to logits function, does fast decoding.

    Implements both greedy and beam search decoding, uses beam search iff
    beam_size > 1, otherwise beam search related arguments are ignored.

    Args:
        encoder_output: Output from encoder.
        encoder_decoder_attention_bias: a bias tensor for use in encoder-decoder
          attention
        symbols_to_logits_fn: Incremental decoding; function mapping triple
          `(ids, step, cache)` to symbol logits.
        hparams: run hyperparameters
        decode_length: an integer.  How many additional timesteps to decode.
        vocab_size: Output vocabulary size.
        beam_size: number of beams.
        top_beams: an integer. How many of the beams to return.
        alpha: Float that controls the length penalty. larger the alpha, stronger
          the preference for longer translations.
        eos_id: End-of-sequence symbol in beam search.
        batch_size: an integer scalar - must be passed if there is no input
        force_decode_length: bool, whether to force the full decode length, or if
          False, stop when all beams hit eos_id.

    Returns:
        A dict of decoding results {
          "outputs": integer `Tensor` of decoded ids of shape
              [batch_size, <= decode_length] if top_beams == 1 or
              [batch_size, top_beams, <= decode_length] otherwise
          "scores": decoding log probs from the beam search,
              None if using greedy decoding (beam_size=1)
        }

    Raises:
      NotImplementedError: If beam size > 1 with partial targets.
    """

    if beam_size > 1:  # Beam Search
        initial_ids = tf.zeros([batch_size], dtype=tf.int32)
        decoded_ids, scores, cache = beam_search.beam_search(
            symbols_to_logits_fn,
            initial_ids,
            beam_size,
            decode_length,
            vocab_size,
            alpha,
            states=cache,
            eos_id=eos_id,
            stop_early=(top_beams == 1))

        if top_beams == 1:
            decoded_ids = decoded_ids[:, 0, 1:]
            scores = scores[:, 0]
        else:
            decoded_ids = decoded_ids[:, :top_beams, 1:]
            scores = scores[:, :top_beams]
            
    else:  # Greedy
        def inner_loop(i, hit_eos, next_id, decoded_ids, cache, log_prob):
            """One step of greedy decoding."""
            logits, cache = symbols_to_logits_fn(next_id, i, cache)
            log_probs = common_layers.log_prob_from_logits(logits)
            temperature = (0.0 if hparams.sampling_method == "argmax" else
                           hparams.sampling_temp)
            next_id = common_layers.sample_with_temperature(logits, temperature)
            hit_eos |= tf.equal(next_id, eos_id)

            log_prob_indices = tf.stack(
                [tf.range(tf.to_int64(batch_size)), next_id], axis=1)
            log_prob += tf.gather_nd(log_probs, log_prob_indices)

            next_id = tf.expand_dims(next_id, axis=1)
            decoded_ids = tf.concat([decoded_ids, next_id], axis=1)
            return i + 1, hit_eos, next_id, decoded_ids, cache, log_prob

        def is_not_finished(i, hit_eos, *_):
            finished = i >= decode_length
            if not force_decode_length:
                finished |= tf.reduce_all(hit_eos)
            return tf.logical_not(finished)

        decoded_ids = tf.zeros([batch_size, 0], dtype=tf.int64)
        hit_eos = tf.fill([batch_size], False)
        next_id = tf.zeros([batch_size, 1], dtype=tf.int64)
        initial_log_prob = tf.zeros([batch_size], dtype=tf.float32)
        _, _, _, decoded_ids, cache, log_prob = tf.while_loop(
            is_not_finished,
            inner_loop, [
                tf.constant(0), hit_eos, next_id, decoded_ids, cache,
                initial_log_prob
            ],
            shape_invariants=[
                tf.TensorShape([]),
                tf.TensorShape([None]),
                tf.TensorShape([None, None]),
                tf.TensorShape([None, None]),
                tf.contrib.framework.nest.map_structure(beam_search.get_state_shape_invariants, cache),
                tf.TensorShape([None]),
            ])
        scores = log_prob

    cache["outputs"] = decoded_ids
    cache["scores"] = scores

    return cache
