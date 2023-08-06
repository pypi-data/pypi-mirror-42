#!/usr/bin/env python
#-*- coding: utf-8 -*-

import torch

from young_tools.logger import Logger


class RNNSearchAttention(torch.nn.Module):
    def __init__(self, attention_type, encoder_state_size, decoder_state_size, attention_state_size=None):
        self._attention_type = attention_type.lower()

        if hasattr(self, '_initialize_'+self._attention_type):
            if self._attention_type in {'dot'}:
                if encoder_state_size != decoder_state_size:
                    Logger.write('\'[{}]\' Attention require the same size of encoder state and decoder state'.format(self._attention_type), 'error')
                getattr(self, '_initialize_'+self._attention_type)(encoder_state_size, decoder_state_size)

            if self._attention_type in {'general', 'concat'}:
                if not attention_state_size:
                    Logger.write('\'[{}]\' Attention require the size of attention state'.format(self._attention_type), 'error')
                getattr(self, '_initialize_'+self._attention_type)(encoder_state_size, decoder_state_size, attention_state_size)
        else:
            Logger.write('Do not support this kind of \'Attention Type\'\n', 'error')

    def _initialize_dot(self, encoder_state_size, decoder_state_size):
        pass

    def _initialize_general(self, encoder_state_size, decoder_state_size, attention_state_size):
        pass

    def _initialize_concat(self, encoder_state_size, decoder_state_size, attention_state_size):
        self._weight_eplls = torch.nn.Linear(encoder_state_size, attention_state_size)
        self._weight_dptss = torch.nn.Linear(decoder_state_size, attention_state_size)
        self._activate = torch.nn.Tanh()
        self._score = torch.nn.Linear(attention_state_size, 1)
        self._normalize = torch.nn.Softmax(0)

    def forward(self, encoder_padded_last_layer_states, decoder_previous_time_step_state):
        if hasattr(self, '_'+self._attention_type):
            return getattr(self, '_'+self._attention_type)(encoder_padded_last_layer_states, decoder_previous_time_step_state)
        else:
            Logger.write('Do not support this kind of \'Attention Type\'\n', 'error')

    def _dot(self, encoder_padded_last_layer_states, decoder_previous_time_step_state):
        pass

    def _general(self, encoder_padded_last_layer_states, decoder_previous_time_step_state):
        pass

    def _concat(self, encoder_padded_last_layer_states, decoder_previous_time_step_state):
        # [Input]encoder_padded_last_layer_states: sequences length * batch size * encoder state size
        weighted_eplls = self._weight_eplls(encoder_padded_last_layer_states)
        # [Output]weighted_eppls: sequences length * batch size * attention state size

        # [Input]decoder_previous_time_step_state: batch size * decoder state size
        weighted_dltss = self._weight_dptss(decoder_previous_time_step_state)
        # [Output]weighted_dltss: batch size * attention state size

        weighted_dltss = weighted_dltss.expand(weighted_eplls.size())
        # [Output]weighted_dltss: sequences length * batch size * attention state size

        scores = self._score(self._activate(weighted_eplls+weighted_dltss))
        # [Output]scores: sequences length * batch size * 1

        alignment_weights = self._normalize(scores)
        # [Output]alignment_weights: sequences length * batch size * 1

        alignment_weights = alignment_weights.transpose(0, 1).transpose(1,2)
        # [Output]alignment_weights: batch size * 1 * sequences length
        eplls = encoder_padded_last_layer_states.transpose(0, 1)
        # [Output]weighted_eplls: batch size * sequences length * encoder state size

        contexts = torch.bmm(alignment_weights, eplls)
        # [Output]contexts: batch size * 1 * encoder state size
        contexts = contexts.squeeze()
        # [Output]contexts: batch size * encoder state size

        return contexts

