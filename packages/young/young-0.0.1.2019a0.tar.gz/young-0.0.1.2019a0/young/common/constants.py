#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import numpy

from young.__root__ import project_path

from young_tools.constant import Constant

# Project's Common Constants.
COMMON = Constant()

COMMON.PROJECT_PATH = project_path
COMMON.CFG_PATH = os.path.join(COMMON.PROJECT_PATH, 'young.cfg')
COMMON.SHARD_SIZE = 64 * 1024 * 1024

COMMON.PAD = '<_PAD_>'
COMMON.PAD_INDEX = 0
COMMON.FLOAT_INF = numpy.float32(numpy.finfo('float32').max / 10)

# NMT System's Constants.
NMT = Constant()

NMT.ROOT_PATH = os.path.join(COMMON.PROJECT_PATH, 'nmt')
NMT.CFG_PATH = os.path.join(NMT.ROOT_PATH, 'nmt.cfg')

NMT.PAD = '<_PAD_>'
NMT.BOS = '<_BOS_>'
NMT.EOS = '<_EOS_>'
NMT.UNK = '<_UNK_>'
NMT.RESERVED_ITEMS = [NMT.PAD, NMT.BOS, NMT.EOS, NMT.UNK]
NMT.PAD_INDEX = NMT.RESERVED_ITEMS.index(NMT.PAD)
NMT.BOS_INDEX = NMT.RESERVED_ITEMS.index(NMT.BOS)
NMT.EOS_INDEX = NMT.RESERVED_ITEMS.index(NMT.EOS)
NMT.UNK_INDEX = NMT.RESERVED_ITEMS.index(NMT.UNK)

NMT.MAT= '<_MAT_>'
NMT.DEL= '<_DEL_>'
NMT.INS= '<_INS_>'
NMT.SUB= '<_SUB_>'
NMT.MANIPULATION_ITEMS = [NMT.MAT, NMT.DEL, NMT.INS, NMT.SUB]
NMT.MAT_ID = NMT.MANIPULATION_ITEMS.index(NMT.MAT)
NMT.DEL_ID = NMT.MANIPULATION_ITEMS.index(NMT.DEL)
NMT.INS_ID = NMT.MANIPULATION_ITEMS.index(NMT.INS)
NMT.SUB_ID = NMT.MANIPULATION_ITEMS.index(NMT.SUB)


# SMT System's Constants.
SMT = Constant()


if __name__ == '__main__':
    print(COMMON.__dict__)
    print(NMT.__dict__)
    print(SMT.__dict__)
    print(NMT.PAD)
