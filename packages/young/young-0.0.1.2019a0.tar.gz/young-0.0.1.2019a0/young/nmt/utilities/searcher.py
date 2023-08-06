#!/usr/bin/env python
#-*- coding: utf-8 -*-

import torch

from young_mt.common.constants import COMMON, NMT

def beam_search(model, attributes, vocabulary_size, beam_size, time_step_limit, length_penalty):
    batch_size = attributes[0].size(0)
    annotations, codes = model.encode(attributes[0])
    inf_scores = torch.full((1, vocabulary_size), COMMON.FLOAT_INF)
    inf_scores[0, NMT.EOS_INDEX] = 0.0
    beam_scores = torch.full((batch_size, beam_size), 0, dtype=torch.float)
    mask = torch.full((batch_size, beam_size), 1, dtype=torch.float)
    length = torch.full((batch_size, beam_size), 0, dtype=torch.float)
    result = torch.full((batch_size, beam_size, 1), NMT.BOS_INDEX, dtype=torch.int64)

    decoder_previous_time_step_states = codes.unsqueeze(1).expand(-1, beam_size, -1)

    probabilities_list = []
    for time_step in range(time_step_limit):
        current_probabilities, current_contexts, decoder_current_time_step_states = self.decode(annotations, result[:, :, -1].view(batch_size*beam_size, -1), decoder_previous_time_step_states.view(batch_size*beam_size, -1))
        current_scores = - current_probabilities.view(batch_size, beam_size, -1)
        current_scores = mask.unsqueeze(2) * current_scores + (1 - mask).unsqueeze(2) * inf_scores
        beam_scores = beam_scores.unsqueeze(2) + current_scores

        beam_scores = beam_scores.view(batch_size, beam_size*vocabulary_size)
        indices = torch.topk(beam_scores, beam_size, dim=1, largest=False, sorted=False)[1]
        beam_id = indices / beam_size
        item_id = indices % vocabulary_size
        beam_scores = torch.gather(beam_scores, 1, indices)

        gather_indices = beam_id + (torch.arange(0, batch_size) * beam_size).view(batch_size, 1) # batch size * beam size & batch size * 1
        mask = torch.index_select(mask.view(-1), 0, gather_indices.view(-1)).view(batch_size, beam_size)
        length = torch.index_select(length.view(-1), 0, gather_indices.view(-1)).view(batch_size, beam_size)
        result = torch.index_select(result.view(batch_size, beam_size, -1), 0, gather_indices.view(-1)).view(batch_size, beam_size, 1)
        decoder_previous_time_step_states = torch.index_select(decoder_previous_time_step_states.view(batch_size, beam_size, -1), 0, gather_indices.view(-1)).view(batch_size, beam_size, 1)

        eos_mask = (1 - item_id.eq(NMT.EOS_INDEX)).float()
        item_id.masked_fill_((mask + eos_mask).eq(0.0), NMT.PDA_INDEX)
        mask = mask * eos_mask
        length = length + mask
        result = torch.cat((result, item_id.view(batch_size, beam_size, 1)), dim=2)
        if mask.eq(0.0).all():
            break
