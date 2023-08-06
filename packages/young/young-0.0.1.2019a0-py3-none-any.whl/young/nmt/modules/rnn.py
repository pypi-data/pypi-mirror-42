#!/usr/bin/env python
#-*- coding: utf-8 -*-

import torch

from young_mt.nmt.system.modules.attentions import BahdanauAttention


class GRUCell(torch.nn.Modules):
    def __init__(self, input_vector_size, output_vector_size):
        self._current_input_to_update_gate = torch.nn.Linear(input_vector_size, output_vector_size)
        self._previous_output_to_update_gate = torch.nn.Linear(output_vector_size, output_vector_size)
        self._update_gate = torch.nn.Sigmoid()

        self._current_input_to_reset_gate = torch.nn.Linear(input_vector_size, output_vector_size)
        self._previous_output_to_reset_gate = torch.nn.Linear(output_vector_size, output_vector_size)
        self._reset_gate = torch.nn.Sigmoid()

        self._current_input_to_memory_cell = torch.nn.Linear(input_vector_size, output_vector_size)
        self._previous_output_to_memory_cell = torch.nn.Linear(output_vector_size, output_vector_size)
        self._memory_cell = torch.nn.Tanh()

    def forward(self, current_input_vector, previous_output_vector):

        update_probability = self._update_gate(self._current_input_to_update_gate(current_input_vector) + self._previous_output_to_update_gate(previous_output_vector))

        reset_probability = self._reset_gate(self._current_input_to_reset_gate(current_input_vector) + self._previous_output_to_reset_gate(previous_output_vector))

        new_memory_vector = self._memory_cell(self._current_input_to_memory_cell(current_input_vector) + self._previous_output_to_memory_cell(reset_probability * previous_output_vector))

        current_output_vector = update_probability * previous_output_vector + (1 - update_probability) * new_memory_vecotr


class GroundHogGRUCell(GRUCell):
    def __init__(self, input_vector_size, output_vector_size, context_vector_size):
        super(GroundHogGRUCell, self).__init__()
        self._current_context_to_update_gate = torch.nn.Linear(context_vector_size, output_vector_size)
        self._current_context_to_reset_gate = torch.nn.Linear(context_vector_size, output_vector_size)
        self._current_context_to_memory_cell = torch.nn.Linear(context_vector_size, output_vector_size)

    def forward(self, current_input_vector, previous_output_vector, current_context_vector):

        update_probability = self._update_gate(self._current_input_to_update_gate(current_input_vector) + self._previous_output_to_update_gate(previous_output_vector) + self._current_context_to_update_gate(current_context_vector))

        reset_probability = self._reset_gate(self._current_input_to_reset_gate(current_input_vector) + self._previous_output_to_reset_gate(previous_output_vector) + self._current_context_to_reset_gate(current_context_vector))

        new_memory_vector = self._memory_cell(self._current_input_to_memory_cell(current_input_vector) + self._previous_output_to_memory_cell(reset_probability * previous_output_vector) + self._current_context_to_memory_cell(current_context_vector))

        current_output_vector = update_probability * previous_output_vector + (1 - update_probability) * new_memory_vecotr


class ConditionalGRUCell(torch.nn.Module):
    def __init__(self, item_embedding_size, state_size, context_vector_size, bias=True):
        super(cGRUCell, self).__init__()
        self._gru_cell_1 = torch.nn.GRUCell(item_embedding_size, hidden_state_size)
        self._attention_mechanism = BahdanauAttention(hidden_state_size, context_vector_size)
        self._gru_cell_2 = torch.nn.GRUCell(context_vector_size, hidden_state_size)

    def forward(self, input_item_batchs, previous_hidden_states, context_set):
        intermediate_hidden_states = self._gru_cell_1(input_item_batchs, previous_hidden_states)
        context_vectors = self._attention_mechanism(intermediate_hidden_states, context_set)
        hidden_states = self._gru_cell_2(context_vectors, intermediate_hidden_states)
        return context_vectors, hidden_states


class cGRULayer(torch.nn.Module):
    def __init__(self, input_item_size, hidden_state_size, context_vector_size):
        self._cgru_cell = cGRUCell(item_embedding_size, hidden_state_size, context_vector_size)

    def forward(self, input_sequence_batchs, context_set, initial_hidden_states=None):
        last_layer_context_vectors = []
        last_layer_hidden_states = []
        hidden_states = initial_hidden_states
        for input_item_batchs in torch.split(input_sequence_batchs, 1, 0):
            context_vectors, hidden_states = self._cgru_cell(input_item_batchs, hidden_states, context_set)
            last_layer_context_vectors.append(context_vectors)
            last_layer_hidden_states.append(hidden_states)
        last_layer_context_vectors = torch.stack(last_layer_context_vectors)
        last_layer_hidden_states = torch.stack(last_layer_hidden_states)
        return last_layer_context_vectors, last_layer_hidden_states


class RNNLayers(torch.nn.Module):
    def __init__(self, state_size, input_item_size, number_of_layers, bias, dropout_rate, nonlinearity, rnn_cell_type):
        super(RNNLayers, self).__init__()
        if rnn_cell_type not in {'RNN', 'LSTM', 'GRU'}:
            Logger.write('We do not support such kind of RNN Cell Type:[{}] yet!\nNow using the default type: [RNN]'.format(rnn_cell_type), 'warn')
            rnn_cell_type = 'RNN'
        if rnn_cell_type == 'RNN':
            self._rnn_layers = getattr(torch.nn, rnn_cell_type)(input_size=input_item_size, hidden_size=state_size, num_layers=number_of_layers, bias=bias, dropout=dropout_rate, bidirectional=True, nonlinearity=nonlinearity)
        elif rnn_cell_type == 'LSTM' or rnn_cell_type == 'GRU':
            self._rnn_layers = getattr(torch.nn, rnn_cell_type)(input_size=input_item_size, hidden_size=state_size, num_layers=number_of_layers, bias=bias, dropout=dropout_rate, bidirectional=True)

    def forward(self, input_sequences, initial_states=None):
        output_last_layer_states, output_last_step_states = self._rnn_layers(input_sequences, initial_states)
        return output_last_layer_states, output_last_step_states
