#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import pickle
import codecs

from young_tools.logger import Logger

from young_mt.common.globals import GlobalVariable
from young_mt.common.constants import NMT

#I2I means index2item and item2index
class I2I(object):
    def __init__(self):
        self._index2item = {}
        self._item2index = {}
        self._size = 0

    def add(self, index, item):
        self._index2item[index] = item
        self._item2index[item] = index
        self._size = self.size + 1

    @property
    def size(self):
        return self._size

    def index(self, item):
        if item in self._item2index:
            return self._item2index[item]
        else:
            return self._item2index[NMT.UNK]

    def item(self, index):
        if index in self._index2item:
            return self._index2item[index]
        else:
            return self._index2item[NMT.UNK_INDEX]


class Vocabulary(object):
    def __init__(self, corpora_directory, corpora_name, language, cfg_size, sentence_length_limit):
        data_directory = GlobalVariable.young_mt_configs['NMT_Directory']['Data']
        self._path = os.path.join(data_directory, '{}_{}_{}.vcb'.format(corpora_name, cfg_size, language))
        self._language = language
        self._cfg_size = cfg_size
        self._exact_size = 0
        self._origin_size = 0
        self._i2i = I2I()
        if os.path.isfile(self._path):
            Logger.write('Found the vocabulary file: [{}].\nLoading ...\n'.format(self._path), 'info')
            self._load_from(self._path)
        else:
            Logger.write('Did not find the vocabulary file: [{}] in size of [Configure:{}].\n'.format(self._path, self._cfg_size), 'info')
            corpora_path = os.path.join(corpora_directory, 'Train/{}.{}'.format(corpora_name, language))
            self._extract_vocabulary(corpora_path, sentence_length_limit)
            self._store_to(self._path)

    def _load_from(self, vocabulary_path):
        with open(vocabulary_path, 'rb') as vocabulary_file:
            loaded = pickle.load(vocabulary_file)
        self._path = loaded._path
        self._language = loaded._language
        self._cfg_size = loaded._cfg_size
        self._exact_size = loaded._exact_size
        self._origin_size = loaded._origin_size
        self._i2i = loaded._i2i
        Logger.write('Retrieved the vocabulary in size of [Configure:{}; Origin:{}; Exact:{}].\n'.format(self._cfg_size, self._origin_size, self._exact_size), 'info')

    def _store_to(self, vocabulary_path):
        with open(vocabulary_path, 'wb') as vocabulary_file:
            pickle.dump(self, vocabulary_file)
        Logger.write('Vocabulary stored to {}.\n'.format(vocabulary_path), 'info')

    def _extract_vocabulary(self, corpora_path, sentence_length_limit):
        if os.path.isfile(corpora_path):
            Logger.write('Extracting vocabulary from corpora file: [{}].\n'.format(corpora_path), 'info')
            total_omit = 0
            total_items = 0
            item2frequency = {}
            with codecs.open(corpora_path, 'r', encoding='utf-8') as corpora_file:
                for line in corpora_file:
                    sentence = line.strip()
                    items = sentence.split()
                    if len(items) <= sentence_length_limit:
                        for item in items:
                            total_items = total_items + 1
                            if item in item2frequency:
                                item2frequency[item] = item2frequency[item] + 1
                            else:
                                item2frequency[item] = 1
                                self._origin_size = self._origin_size + 1
                    else:
                        total_omit = total_omit + 1
                        for item in items:
                            total_items = total_items + 1
            Logger.write('Omit {} sentences, because the length of them is larger than limitation of sentence length.\n'.format(total_omit), 'info')

            item2frequency = sorted(item2frequency.items(), key=lambda item:item[1], reverse=True)
            self._exact_size = min(self._origin_size, self._cfg_size)
            for index, item in enumerate(NMT.RESERVED_ITEMS):
                self._i2i.add(index, item)
            for index, item in enumerate(item2frequency[:self._exact_size], start=len(NMT.RESERVED_ITEMS)):
                self._i2i.add(index, item[0])
            Logger.write('Vocabulary extracted.\nThe size of vocabulary is [Configure:{}; Origin:{}; Exact:{}].\nCorpora has total {} items(included omited sentences) and total {} different items.\n'.format(self._cfg_size, self._origin_size, self._exact_size, total_items, self._origin_size), 'info')
        else:
            Logger.write('Did not find the corpora file in language: [{}]!\n'.format(self._language), 'error')

    def write_plain_to(self, plain_name):
        data_directory = GlobalVariable.young_mt_configs['NMT_Directory']['Data']
        plain_path = os.path.join(data_directory, plain_name)
        with codecs.open(plain_path, 'w', encoding='utf-8') as plain_file:
            for index in range(self.i2i.size):
                plain_file.write(self.i2i.item(index)+'\n')

    @property
    def path(self):
        return self._path

    @property
    def language(self):
        return self._language

    @property
    def cfg_size(self):
        return self._cfg_size

    @property
    def exact_size(self):
        return self._exact_size

    @property
    def origin_size(self):
        return self._origin_size

    @property
    def size(self):
        return self.exact_size

    @property
    def i2i(self):
        return self._i2i


if __name__ == '__main__':
    pass
