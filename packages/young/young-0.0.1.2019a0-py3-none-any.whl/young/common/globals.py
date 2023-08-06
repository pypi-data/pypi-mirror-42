#!/usr/bin/env python
#-*- coding: utf-8 -*-

class GlobalVariable(object):
    @staticmethod
    def initialize():
        global nmt_logger
        global nmt_train_logger
        global nmt_translate_logger
        global smt_logger

        global young_mt_configs
        global nmt_configs
        global smt_configs

        nmt_logger = None
        nmt_train_logger = None
        nmt_translate_logger = None
        smt_logger = None

        young_mt_configs = None
        nmt_configs = None
        smt_configs = None
