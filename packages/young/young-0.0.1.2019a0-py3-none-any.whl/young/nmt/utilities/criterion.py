#!/usr/bin/env python
#-*- coding: utf-8 -*-

import torch

from young_mt.common.constants import NMT, COMMON

class Criterion(torch.nn.Module):
    def __init__(self, label_smoothing_rate):
        self._label_smoothing_rate = label_smoothing_rate
        if self._label_smoothing_rate:
            self._criterion = torch.nn.KLDivLoss(reduction='none')
        else:
            self._criterion = torch.nn.NLLLoss(reduction='none', ignore_index=NMT.PAD_INDEX)

    def forward(self, hypotheses, references, reduction='sum', normalization=1.0):
        batch_size = references.size(0)
        sequence_length = references.size(1)
        vocabulary_size = hypotheses.size(2)

        scores = hypotheses
        ground_truth = references

        if self._label_smoothing_rate:
            ground_truth = torch.full((batch_size, sequence_length, vocabulary_size), (1-self._label_smoothing_rate)/(vocabulary_size-2))
            ground_truth[:, :, NMT.PAD_INDEX] = 0.0
            ground_truth.scatter_(2, references.unsqueeze(2), self._label_smoothing_rate)

        ground_truth.detach_()

        loss = self._criterion(scores, ground_truths)
        loss = loss.div(normalization)
        if reduction == 'sum':
            loss = loss.sum()
        return loss


if __name__ == '__main__':
    pass
