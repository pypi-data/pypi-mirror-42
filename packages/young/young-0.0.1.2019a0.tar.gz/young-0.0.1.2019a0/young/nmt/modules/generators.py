#!/usr/bin/env python
#-*- coding: utf-8 -*-

import torch

from young_mt.common.constants import NMT

class RNNSearchGenerator(torch.nn.Module):
    @InstancesChecker(generator_maxout=bool)
    def __init__(self, encoder_state_size, decoder_state_size, target_vocabulary_size, target_item_embedding_size, generator_state_size, generator_maxout=False)generator_state_size, input_state_size, embedded_item_size, context_vector_size, generator_maxout):
        self._generator_maxout = generator_maxout
        if self._generator_maxout:
            self._generator_state_size = generator_state_size//2
        else:
            self._generator_state_size = generator_state_size
            self._activate = torch.nn.Tanh()

        self._weight_decoder_state = torch.nn.Linear(decoder_state_size, 2*generator_state_size)
        self._weight_embedded_item = torch.nn.Linear(target_item_embedding_size, 2*generator_state_size)
        self._weight_context = torch.nn.Linear(encoder_state_size, 2*generator_state_size)

        self._dropout_layer = torch.nn.Dropout(dropout_rate)
        self._projection_layer = torch.nn.Linear(generator_state_size, target_vocabulary_size)
        self._normalize = torch.nn.LogSoftmax(1)

    def forward(self, decoder_states, embedded_items, contexts):
        weighted_decoder_states = self._weight_decoder_state(decoder_states)
        weighted_embedded_items = self._weight_embedded_item(embedded_items)
        weighted_contexts = self._weight_context(contexts)
        generator_states = weighted_input_state + weighted_embedded_item + weighted_context
        if self._generator_maxout:
            generator_states = generator_states.view(generator_states.size(0), generator_states.size(1)//2, 2).max(-1)[0]
        else:
            generator_states = self._activate(generator_states)

        generator_states = self._dropout_layer(generator_states)
        logits = self._projection_layer(generator_states)
        probabilities = self._normalize(logits)

        return probabilities
