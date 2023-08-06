#!/usr/bin/env python
#-*- coding: utf-8 -*-

import torch

from young_mt.nmt.modules.embedding import Embedding
from young_mt.nmt.modules.encoders import GroundHogEncoder
from young_mt.nmt.modules.decoders import GroundHogDecoder
from young_mt.nmt.modules.attentions import RNNSearchAttention
from young_mt.nmt.modules.generators import RNNSearchGenerator

from young_mt.common.constants import NMT
from young_mt.nmt.utilities.tensor_handler import sort_value_by_key

class GroundHog(torch.nn.Module):
    def __init__(self,
            generator_maxout, generator_state_size,
            attention_type, attention_state_size,
            source_vocabulary_size, target_vocabulary_size,
            source_item_embedding_size, target_item_embedding_size,
            source_embedding_dropout_rate, target_embedding_dropout_rate,
            encoder_state_size, decoder_state_size,
            encoder_number_of_layers, decoder_number_of_layers,
            encoder_dropout_rate, decoder_dropout_rate):

        super(GroundHog, self).__init__()
        self._source_embedding = Embedding(source_vocabulary_size, source_item_embedding_size, source_embedding_dropout_rate)
        self._target_embedding = Embedding(target_vocabulary_size, target_item_embedding_size, target_embedding_dropout_rate)

        self._encoder = GroundHogEncoder(source_item_embedding_size, encoder_state_size, encoder_number_of_layers, encoder_dropout_rate)
        self._decoder = GroundHogDecoder(target_item_embedding_size, decoder_state_size, decoder_number_of_layers, decoder_dropout_rate)

        self._attention = RNNSearchAttention(attention_type, encoder_state_size, decoder_state_size, attention_state_size)
        self._generator = RNNSearchGenerator(encoder_state_size, decoder_state_size, target_vocabulary_size, target_item_embedding_size, generator_state_size, generator_maxout)

        self._trans_size_enc2dec = torch.nn.Linear(encoder_state_size, decoder_state_size)

    def _initialize_codes(self, encoder_padded_last_layer_states, encoder_last_time_step_states):
        return torch.nn.functional.tanh(self._trans_size_enc2dec(encoder_last_time_step_states))

    def encode(self, sequences):
        (padded_sequences, sequences_length) = sequences
        padded_sequences = torch.tensor(padded_sequences, dtype=torch.int64)
        sequences_length = torch.tensor(sequences_length, dtype=torch.int64)

        # Sort
        # [Begin]
        padded_sequences, sequences_length, sorted2unsorted_index_map, unsorted2sorted_index_map = sort_value_by_key(padded_sequences, sequences_length, dimension=1, descending=True)
        # [End]

        # Embedding
        # [Begin]
        embedded_padded_sequences = self._source_embedding(padded_sequences)
        # [End]

        # Encoder
        # [Begin]
        embedded_packed_sequences = torch.nn.utils.rnn.pack_padded_sequence(embedded_padded_sequences, sequences_length) # padded -> packed
        packed_last_layer_states, last_time_step_states = self._encoder(embedded_packed_sequences) # packed
        padded_last_layer_states, last_layer_states_length = torch.nn.utils.rnn.pad_packed_sequence(packed_last_layer_states) # packed -> padded
        # [End]

        # DeSort
        # [Begin]
        padded_last_layer_states = torch.index_select(padded_last_layer_states, 1, unsorted2sorted_index_map)
        last_time_step_states = torch.index_select(last_time_step_states, 1, unsorted2sorted_index_map)
        last_layer_states_length = torch.index_select(last_layer_states_length, 0, unsorted2sorted_index_map)
        # last_layer_states_length is reversed for the future using.
        # [End]

        annotations = padded_last_layer_states
        codes = self._initialize_codes(padded_last_layer_states, last_time_step_states)

        return annotations, codes

    def decode(self, annotations, previous_items, decoder_previous_time_step_states):
        embedded_previous_items = self._target_embedding(previous_items)
        current_context = self._attention(annotations, decoder_previous_time_step_states)
        decoder_current_time_step_states = self._decoder(embedded_previous_items, decoder_previous_time_step_states, current_contexts)
        current_probabilities = self._generator(decoder_previous_time_step_states, embedded_previous_items, current_contexts)
        return current_probabilities, current_contexts, decoder_current_time_step_states

    def forward(self, source_sequences, target_sequences, teacher_forcing_rate=0.0):
        annotations, codes = self.encode(source_sequences)

        (padded_target_sequences, target_sequences_length) = target_sequences
        padded_target_sequences = torch.tensor(padded_target_sequences, dtype=torch.int64)
        target_sequences_length = torch.tensor(target_sequences_length, dtype=torch.int64)

        previous_items = torch.full((padded_target_sequences.size(0),1), NMT.BOS_INDEX, dtype=torch.int64)
        decoder_previous_time_step_states = codes
        probabilities_list = []
        for time_step in range(1, padded_target_sequences.size(1)):
            if random.random() < teacher_forcing_rate:
                previous_items = padded_target_sequences[:, time_step-1]
            current_probabilities, current_contexts, decoder_current_time_step_states = self.decode(annotations, previous_items, decoder_previous_time_step_states)
            previous_items = torch.topk(current_probabilities, 1, 1)[1]
            decoder_previous_time_step_states = decoder_current_time_step_states

            probabilities_list.append(current_probabilities)

        return torch.stack(probabilities_list, dim=1) # batch size * sequences length * target vocabulary size

class DL4MT(torch.nn.Module):
    def __init__(self,
            ):
        super(DL4MT, self).__init__()

    def forward(self):
        pass
