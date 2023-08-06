#!/usr/bin/env/ python
#-*- coding: utf-8 -*-

import os
import pickle
import codecs

from young_mt.common.globals import GlobalVariable
from young_mt.common.constants import NMT, COMMON
from young_mt.common.vocabulary import Vocabulary

from young_tools.logger import Logger
from young_tools.decorator import InstancesChecker


#Instance: (X, Y) where 'X' is a set of 'Features' or 'Attributes' and 'Y' is the 'Label' of the 'Instance', (X, Y) is also called as 'Example' or 'Sample'.
#In Machine Translation Task, 'Attributes' can be a list of words within a single sentence, 'labels' can be a set of references sentences(there may be multiple reference sentences in Development Dataset for Multi-BLEU testing script.)
class Instance(object):
    @InstancesChecker(attributes=list, labels=list)
    def __init__(self, attributes, labels):
        self._attributes = attributes
        self._labels = labels

    def __len__(self):
        return len(self._attributes) + len(self._labels)

    def __str__(self):
        attributes_string = 'Attributes:\n'
        for attribute in self._attributes:
            attributes_string += str(attribute) + '\n'

        labels_string = 'Labels:\n'
        for label in self._labels:
            labels_string += str(label) + '\n'

        print_string = attributes_string + labels_string

        return print_string

    @property
    def attributes(self):
        return self._attributes

    @property
    def labels(self):
        return self._labels


#Data Set contains a set of 'Instances'.
class DataSet(object):
    @InstancesChecker(dataset_base_path=str)
    def __init__(self, dataset_base_path):
        self._dataset_base_path = dataset_base_path
        self._instance_length = 0
        self._attributes_length = 0
        self._labels_length = 0
        self._on_the_way = False

        self._number_of_shards = 0
        self._number_of_instances = 0

        self._buffer = []
        self._buffer_dump_size = pickle.dumps(self._buffer).__sizeof__()
        self._current_buffer_index = 0
        self._current_shard_index = 0
        self._current_instance_index = 0

        self.open()
        self.close()


    def _shard_path(self, index):
        return self._dataset_base_path+'-'+str(index)

    @property
    def size(self):
        return self._number_of_instances

    @property
    def instance_length(self):
        return self._instance_length

    @property
    def attributes_length(self):
        return self._attributes_length

    @property
    def labels_length(self):
        return self._labels_length

    @property
    def _buffer_full(self):
        if self._buffer_dump_size >= COMMON.SHARD_SIZE:
            return True
        if self._buffer_dump_size < COMMON.SHARD_SIZE:
            return False

    def open(self):
        if self._on_the_way:
            Logger.write('Data Set is opened previously. Ignoring this operation.\n', 'warn')
            return
        else:
            self._on_the_way = True

        index = 0
        while os.path.isfile(self._shard_path(index)):
            with open(self._shard_path(index), 'rb') as shard_file:
                self._buffer = pickle.load(shard_file)
            index = index + 1
            self._number_of_instances += len(self._buffer)
            self._buffer_dump_size = pickle.dumps(self._buffer).__sizeof__()
            if self._buffer_full:
                self._number_of_shards += 1

    def close(self):
        if not self._on_the_way:
            Logger.write('Data Set is not opened previously. Ignoring this operation.\n', 'warn')
            return
        else:
            self._on_the_way = False

        if len(self._buffer):
            with open(self._shard_path(self._number_of_shards), 'wb') as shard_file:
                pickle.dump(self._buffer, shard_file)
            self._number_of_shards += 1
            self._buffer.clear()
            self._buffer_dump_size = pickle.dumps(self._buffer).__sizeof__()

    @InstancesChecker(instance=Instance)
    def add(self, instance):
        if not self._on_the_way:
            Logger.write('Data Set is not opened.\n', 'error')

        if len(instance) != self._instance_length or len(instance.attributes) != self._attributes_length or len(instance.labels) != self._labels_length:
            Logger.write('The instance you add to this Data Set is not match the settings.\n', 'error')

        if self._buffer_full:
            with open(self._shard_path(self._number_of_shards), 'wb') as shard_file:
                pickle.dump(self._buffer, shard_file)
            self._number_of_shards += 1
            self._buffer.clear()
            self._buffer_dump_size = pickle.dumps(self._buffer).__sizeof__()

        self._buffer.append(instance)
        self._buffer_dump_size += pickle.dumps(instance).__sizeof__()
        self._number_of_instances += 1

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()
        if exc_type:
            return False
        return True

    def __iter__(self):
        if not self._on_the_way:
            Logger.write('Data Set is not opened.\n', 'error')

        self._current_instance_index = 0
        self._current_shard_index = 0
        self._current_buffer_index = 0
        return self

    def __next__(self):
        if not self._on_the_way:
            Logger.write('Data Set is not opened.\n', 'error')

        if self._current_instance_index < self._number_of_instances:
            if self._current_buffer_index == len(self._buffer):
                with open(self._shard_path(self._current_shard_index), 'rb') as shard_file:
                    self._buffer = pickle.load(shard_file)
                self._current_shard_index += 1
                self._current_buffer_index = 0

            instance = self._buffer[self._current_buffer_index]
            self._current_instance_index += 1
            self._current_buffer_index += 1
            return instance
        else:
            raise StopIteration


class BatchData(object):
    @InstancesChecker(dataset=DataSet, batch_size=int, bucket_size=int)
    def __init__(self, dataset, batch_size=1, bucket_size=1, sort_by_id=0):
        if batch_size <= 0:
            Logger.write('Batch Size should not less than 1!\n', 'error')
        if bucket_size <= 0:
            Logger.write('Bucket Size should not less than 1!\n', 'error')

        self._dataset = dataset
        self._batch_size = batch_size
        self._bucket_size = bucket_size

    def _pad_sequences(self, sequences):
        sequence_lengths = [len(sequence) for sequence in sequences]
        max_sequence_length = max(sequence_lengths)
        padded_sequences = []
        for sequence in sequences:
            padded_sequence = [COMMON.PAD_INDEX for index in range(max_sequence_length)]
            padded_seuqence[:len(sequence)] = sequence
            padded_sequences.append(padded_seuqence)

        return padded_sequences, sequence_lengths

    def _package_batch(self, instances):
        batch_size = len(instances)

        # Deal with attributes
        attributes = []
        for attribute_index in range(self._dataset.attributes_length):
            ith_attributes = [instance.attributes[attribute_index] for instance in instances]

            ith_padded_attributes, ith_attribute_lengths = self._pad_sequences(ith_attributes)

            attributes.append((ith_padded_attributes, ith_attribute_lengths))

        # Deal with labels
        labels = []
        for label_index in range(self._dataset.labels_length):
            ith_labels = [instance.labels[label_index] for instance in instances]

            ith_padded_labels, ith_label_lengths = self._pad_sequences(ith_labels)

            labels.append((ith_padded_labels, ith_label_lengths))

        batch = (attributes, labels)
        return batch

    def __iter__(self):
        instance_buffer = []
        instance_number = 0
        for instance in self._dataset:
            instance_buffer.append(instance)
            instance_number += 1
            if len(instance_buffer) == self._batch_size*self._bucket_size or instance_number == self._dataset.size:
                instance_buffer = sorted(instance_buffer, key=lambda instance : len(instance.attributes[0])+random.uniform(-1.0, 1.0))
                for batch_index in range(self._bucket_size):
                    left_boundary = batch_index * self._batch_size
                    right_boundary = left_boundary + self._batch_size

                    batch = self._package_batch(instance_buffer[left_boundary:right_boundary])
                    yield batch
                instance_buffer.clear()


class MultilingualDataSet(DataSet):
    @InstancesChecker(dataset_base_path=str, vocabularies=list, languages=list, corpora_directory=str, corpora_name=str, source_language_number=int, sentence_length_limit=int)
    def __init__(self, dataset_base_path, vocabularies, languages, corpora_directory, corpora_name, source_language_number=1, sentence_length_limit=10000):
        if len(vocabularies) != len(languages):
            GlobalVariable.nmt_logger.write_log('Arguments vocabularies and languages contain different number of elements!\n', 'error')

        for vocabulary in vocabularies:
            if not isinstance(vocabulary, Vocabulary):
                GlobalVariable.nmt_logger.write_log('Invalid Vocabulary argument type!', 'error')

        for language in languages:
            if not isinstance(language, str):
                GlobalVariable.nmt_logger.write_log('Invalid Language argument type!', 'error')

        if source_language_number < 1:
            GlobalVariable.nmt_logger.write_log('The number of source side language you set is less than [1]!', 'error')
        if source_language_number > len(languages):
            GlobalVariable.nmt_logger.write_log('The number of source side language you set is larger than the languages list\'s length you provided!', 'error')

        dataset_base_path = os.path.join(dataset_base_path, '{}'.format(corpora_name)) + '.packaged'
        super(MultilingualDataSet, self).__init__(dataset_base_path)

        self._instance_length = len(languages)
        self._attributes_length = source_language_number
        self._labels_length = self._instance_length - self._attributes_length
        self._languages = languages
        self._vocabularies = vocabularies

        self._language_paths = []
        for language in self._languages:
            language_path = os.path.join(corpora_directory, '{}.{}'.format(corpora_name, language))
            if not os.path.isfile(language_path):
                GlobalVariable.nmt_logger.write_log('Part of corpora in language: [{}] at path: [{}] do not exists.\nNMT system shut down!\n'.format(language, language_path), 'error')
            self._language_paths.append(language_path)

        if not self.size:
            GlobalVariable.nmt_logger.write_log('Data Set is not exists.\nNow packaging data from corpora [{}] at [{}]... ...\n'.format(corpora_name, self._dataset_base_path), 'info')
            self._package_data(sentence_length_limit)
            GlobalVariable.nmt_logger.write_log('Packaged Data Set!\n', 'info')
            GlobalVariable.nmt_logger.write_log(self.__str__(), 'info')
        else:
            GlobalVariable.nmt_logger.write_log(self.__str__(), 'info')
            GlobalVariable.nmt_logger.write_log('Data Set exists, if you want to rebuild, please back up your origin Data Set files and delete the files(files in [Data] directroy and their extension is .packaged-*).\n', 'warn')
            system_continue = input('Continue Runing The System, press any key and \'Enter\' to continue or \'n\' to halt the system. [Y/n]:')
            if system_continue == 'n':
                Logger.write('Halt the system.\n', 'exit')
            else:
                Logger.write('Continue running ... ...\n', 'info')

    def __str__(self):
        information = 'The Data Set saved into: [{}];\nLanguages: {};\nAttributes: {};\nLabels: {}.\n'.format(self._dataset_base_path, self._languages, self._languages[:self._attributes_length], self._languages[self._attributes_length:])
        return information

    def _package_data(self, sentence_length_limit):
        self.open()
        total_sentence_line_tuple = 0
        total_valid = 0
        total_limit_omit = 0
        language_files = []
        for language_path in self._language_paths:
            language_files.append(codecs.open(language_path, 'r', encoding='utf-8'))

        for sentence_line_tuple in zip(*language_files):
            total_sentence_line_tuple += 1
            indices_list = []
            for language_index in range(len(sentence_line_tuple)):
                sentence_line = sentence_line_tuple[language_index]
                sentence_line = sentence_line.strip()
                sentence_line = NMT.BOS + ' ' + sentence_line + ' ' + NMT.EOS
                indices = [self._vocabularies[language_index].i2i.index(item) for item in sentence_line.split()]
                indices_list.append(indices)
            if max([len(indices) for indices in indices_list]) > sentence_length_limit:
                total_limit_omit = total_limit_omit + 1
                continue
            total_valid = total_valid + 1

            attributes = indices_list[:self._attributes_length]
            labels = indices_list[self._attributes_length:]
            instance = Instance(attributes, labels)
            self.add(instance)
        GlobalVariable.nmt_logger.write('Corpora has total {} Instances. Data Set contains {} valid Instances(extracted from corpora), omit {} Instances because of the length limit.\n'.format(total_sentence_line_tuple, total_valid, total_limit_omit), 'info')
        self.close()


if __name__ == '__main__':
    pass
