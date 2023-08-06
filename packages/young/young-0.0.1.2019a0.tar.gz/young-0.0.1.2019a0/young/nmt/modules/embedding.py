#!/usr/bin/env/ python
#-*- coding: utf-8 -*-

import torch
from young_mt.common.constants import NMT


class Embedding(torch.nn.Module):
    def __init__(self, number_of_embeddings, embedding_dimension, dropout_rate, padding_index=NMT.PAD_INDEX):
        super(Embedding, self).__init__()

        self._embedding_layer = torch.nn.Embedding(number_of_embeddings, embedding_dimension, padding_idx=padding_index)

        self._init()

        if self._dropout_rate > 0.0:
            self._dropout_layer = torch.nn.Dropout(dropout_rate)

    def _init():
        torch.nn.init.uniform_(self._embedding_layer.weight, -0.1, 0.1)

        with torch.no_grad():
            self._embedding_layer.weight[padding_index].fill_(0.0)

    def forward(self, item):
        item_embedding = self._embedding_layer(item)

        if hasattr(self, '_dropout_layer'):
            item_embedding = self._dropout_layer(item_embedding)

        return item_embedding
