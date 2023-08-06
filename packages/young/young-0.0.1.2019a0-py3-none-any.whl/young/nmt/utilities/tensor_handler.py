#!/usr/bin/env python
#-*- coding: utf-8 -*-

import torch

import young_mt.common.globals as global_vars

from young_tools.decorator import InstancesChecker

@InstancesChecker(tensor=torch.Tensor, key=torch.Tensor, dimension=int, descending=bool)
def sort_value_by_key(value, key, dimension, descending=False):
    sorted_key, sorted2unsorted = torch.sort(key, descending=descending)
    sorted_value = torch.index_select(value, dimension, sorted2unsorted)

    _, unsorted2sorted = torch.sort(sorted2unsorted)

    #for sorted_index, unsorted_index in enumerate(sorted2unsorted):
    #    unsorted2sorted[unsorted_index] = sorted_index

    return sorted_value, sorted_key, sorted2unsorted, unsorted2sorted
