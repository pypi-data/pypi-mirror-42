#!/usr/bin/env python
#-*- coding: utf-8 -*-

import torch

class NMTModel(torch.nn.Module):
    def __init__(self):
        super(NMTModel, self).__init__()

    def forward(self, source_sentences, target_sentences):
        raise NotImplementedError
