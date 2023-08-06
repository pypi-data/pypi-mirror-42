#!/usr/bin/env python
#-*- coding: utf-8 -*-

import torch

from yount_mt.nmt.modules.rnn import GroundHogGRULayers


class GroundHogDecoder(torch.nn.Module):
    def __init__(self, item_embedding_size, decoder_state_size, decoder_number_of_layers, decoder_dropout_rate):
        super(GroundHogDecoder, self).__init__()
        self._rnn_cell = GroundHogGRUCell(item_embedding_size, decoder_state_size)

    def forward(self, embedded_previously_predicted_items, decoder_previous_time_step_states, current_contexts):
        decoder_current_time_step_states = self._rnn_cell(embedded_previously_predicted_items, decoder_previous_time_step_states, current_contexts)
        return decoder_current_time_step_states
