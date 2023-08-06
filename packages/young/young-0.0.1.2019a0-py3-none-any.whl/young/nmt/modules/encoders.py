#!/usr/bin/env python
#-*- coding: utf-8 -*-

import torch

from young_mt.nmt.modules.rnn import GRULayer


class GroundHogEncoder(torch.nn.Module):
    def __init__(self, item_embedding_size, encoder_state_size, encoder_number_of_layers, encoder_dropout_rate):
        super(RNNEncoder, self).__init__()
        self._rnn_layers = torch.nn.GRU(item_embedding_size, encoder_state_size)
        #self._rnn_layers = GRULayer(item_embedding_size, encoder_state_size, encoder_number_of_layers, dropout=encoder_dropout_rate)

    def forward(self, embedded_packed_sentences):
        packed_last_layer_states, last_time_step_states = self._rnn_layers(embedded_packed_sentences)
        return packed_last_layer_states, last_time_step_states
