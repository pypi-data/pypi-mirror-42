#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import torch
import argparse

from young_tools.logger import Logger
from young_tools.cfgparser import ConfigParser

from young_mt.common.globals import GlobalVariable
from young_mt.common.dataset import BatchData, MultilingualDataSet
from young_mt.common.constants import NMT, COMMON
from young_mt.common.vocabulary import Vocabulary

from young_mt.nmt.utilities.searcher import beam_search
from young_mt.nmt.utilities.argument import NMTArgument
from young_mt.nmt.utilities.optimizer import Optimizer
from young_mt.nmt.utilities.criterion import Criterion
from young_mt.nmt.utilities.scheduler import Scheduler


def load_configuration(configuration_file_name):
    GlobalVariable.young_mt_configs = ConfigParser()
    GlobalVariable.young_mt_configs.read(COMMON.CFG_PATH)

    GlobalVariable.nmt_configs = ConfigParser()
    GlobalVariable.nmt_configs.read(NMT.CFG_PATH)

    if configuration_file_name:
        tmp_configs = ConfigParser()
        tmp_configs.read(configuration_file_name)
        for section in tmp_configs.sections():
            if section in GlobalVariable.nmt_configs.sections():
                for key in tmp_configs[section]:
                    if key in GlobalVariable.nmt_configs[section]:
                        GlobalVariable.nmt_configs[section][key] = tmp_configs[section][key]
                    else:
                        GlobalVariable.nmt_logger.write_log('User defined Key \'{}\' in Section [{}] is not defined in the System configuration file.\nPlease check the documentation of YoungMT - NMT part.\n'.format(key, section), 'info')
            else:
                GlobalVariable.nmt_logger.write_log('User defined Section [{}] is not defined in the System configuration file.\nPlease check the documentation of YoungMT - NMT part.\n'.format(section), 'info')


def set_essential_directory(directory_path):
    if os.path.isdir(directory_path):
        Logger.write('... Directory: {} exists ... ... PASS\n'.format(directory_path), 'info')
    else:
        Logger.write('... Directory: {} is not exists ...\n'.format(directory_path), 'info')
        os.mkdir(directory_path)
        Logger.write('... Created directory: {} ...\n'.format(directory_path), 'info')


def set_workplace(working_directory_path):
    if not os.path.isdir(working_directory_path):
        os.makedirs(working_directory_path)
    os.chdir(working_directory_path)
    Logger.write('The YoungMT - NMT system running under the directory: {}\n'.format(working_directory_path), 'info')

    set_essential_directory(GlobalVariable.young_mt_configs['NMT_Directory']['Log'])
    set_essential_directory(GlobalVariable.young_mt_configs['NMT_Directory']['Model'])
    data_dir = GlobalVariable.young_mt_configs['NMT_Directory']['Data']
    set_essential_directory(data_dir)
    set_essential_directory(os.path.join(data_dir, 'Train'))
    set_essential_directory(os.path.join(data_dir, 'Dev'))
    set_essential_directory(os.path.join(data_dir, 'Test'))


def set_loggers(train_or_translate):
    log_dir = GlobalVariable.young_mt_configs['NMT_Directory']['Log']

    nmt_log_file_path = os.path.join(log_dir, 'nmt.log')
    GlobalVariable.nmt_logger = Logger(nmt_log_file_path)
    GlobalVariable.nmt_logger.write_log('NMT log will be saved into the file: {}.\n'.format(nmt_log_file_path), 'info')

    if train_or_translate == 'train':
        nmt_train_log_file_path = os.path.join(log_dir, 'nmt_train.log')
        GlobalVariable.nmt_train_logger = Logger(nmt_train_log_file_path)
        GlobalVariable.nmt_train_logger.write_log('NMT Training log will be saved into the file: {}.\n'.format(nmt_train_log_file_path), 'info')

    if train_or_translate == 'translate':
        nmt_translate_log_file_path = os.path.join(log_dir, 'nmt_translate.log')
        GlobalVariable.nmt_translate_logger = Logger(nmt_translate_log_file_path)
        GlobalVariable.nmt_translate_logger.write_log('NMT Translating log will be saved into the file: {}.\n'.format(nmt_translate_log_file_path), 'info')


def check_device():
    #Check if CUDA is available
    if torch.cuda.is_available():
        GlobalVariable.nmt_logger.write_log('CUDA is available, system could be run on GPU.\n', 'info')
    else:
        GlobalVariable.nmt_logger.write_log('Your Machine has no CUDA or GPU. YoungMT - NMT does not support CPU.\n', 'error')

    #Check if the GPU number is right
    try:
        gpu_id_list = ConfigParser.get_list(GlobalVariable.nmt_configs['Train']['GPUs'], 'int')
    except:
        GlobalVariable.nmt_logger.write_log('Invalid GPU ID! Using System\'s GPU ID configuration: GPUs ID = 0.\n', 'info')
        gpu_id_list = [0,]

    gpu_id_list = sorted(gpu_id_list)

    if len(gpu_id_list) <= torch.cuda.device_count():
        if 0 <= min(gpu_id_list) and max(gpu_id_list) < torch.cuda.device_count():
            GlobalVariable.nmt_logger.write_log('You set GPU ID: {}.\n'.format(gpu_id_list), 'info')
        else:
            GlobalVariable.nmt_logger.write_log('The GPU ID you set is illegal(ID may be larger than the number of GPU or smaller than Zero).\nPlease check the format of your GPU ID.\n', 'error')
    else:
        GlobalVariable.nmt_logger.write_log('You set {} GPU, but you only have {} GPU, check the number of your GPU.\n'.format(len(gpu_id_list), torch.cuda.device_count()), 'error')

def get_vocabulary():
    corpora_directory = GlobalVariable.nmt_configs['Corpora']['Directory']
    corpora_name = GlobalVariable.nmt_configs['Corpora']['Name']
    source_language = GlobalVariable.nmt_configs['Corpora']['Source_Language']
    target_language = GlobalVariable.nmt_configs['Corpora']['Target_Language']
    sentence_length_limit = ConfigParser.get_expression_result(GlobalVariable.nmt_configs['Common']['Sentence_Length_Limit'])

    source_vocabulary_size = ConfigParser.get_expression_result(GlobalVariable.nmt_configs['Vocabulary']['Source_Size'])
    target_vocabulary_size = ConfigParser.get_expression_result(GlobalVariable.nmt_configs['Vocabulary']['Target_Size'])

    vocabulary = {}

    GlobalVariable.nmt_logger.write_log('Preparing source side language vocabulary ...\n', 'info')
    vocabulary['source'] = Vocabulary(corpora_directory, corpora_name, source_language, source_vocabulary_size, sentence_length_limit)
    GlobalVariable.nmt_logger.write_log('Finished.\n', 'info')

    GlobalVariable.nmt_logger.write_log('Preparing target side language vocabulary ...\n', 'info')
    vocabulary['target'] = Vocabulary(corpora_directory, corpora_name, target_language, target_vocabulary_size, sentence_length_limit)
    GlobalVariable.nmt_logger.write_log('Finished.\n', 'info')

    return vocabulary


def get_dataset(source_vocabulary, target_vocabulary):
    corpora_directory = GlobalVariable.nmt_configs['Corpora']['Directory']
    corpora_name = GlobalVariable.nmt_configs['Corpora']['Name']
    source_language = GlobalVariable.nmt_configs['Corpora']['Source_Language']
    target_language = GlobalVariable.nmt_configs['Corpora']['Target_Language']
    sentence_length_limit = ConfigParser.get_expression_result(GlobalVariable.nmt_configs['Common']['Sentence_Length_Limit'])

    data_directory = GlobalVariable.young_mt_configs['NMT_Directory']['Data']

    dataset = {}

    GlobalVariable.nmt_logger.write_log('Preparing training data ...\n', 'info')
    dataset['training'] = MultilingualDataSet(os.path.join(data_directory, 'Train'), [source_vocabulary, target_vocabulary], [source_language, target_language], os.path.join(corpora_directory, 'Train'), corpora_name, sentence_length_limit=sentence_length_limit)

    GlobalVariable.nmt_logger.write_log('Preparing development data ...\n', 'info')
    dataset['development'] = MultilingualDataSet(os.path.join(data_directory, 'Dev'), [source_vocabulary, target_vocabulary], [source_language, target_language], os.path.join(corpora_directory, 'Dev'), corpora_name)

    GlobalVariable.nmt_logger.write_log('Preparing testing data ...\n', 'info')
    dataset['testing'] = MultilingualDataSet(os.path.join(data_directory, 'Test'), [source_vocabulary, ], [source_language, ], os.path.join(corpora_directory, 'Test'), corpora_name)

    return dataset


def get_model(source_vocabulary_size, target_vocabulary_size):
    user_defined = GlobalVariable.nmt_configs['Model']['User_Defined']
    model_name = GlobalVariable.nmt_configs['Model']['Name']
    if user_defined:
        try:
            from user_defined import model_name
        except:
            GlobalVariable.nmt_train_logger.write_log('Failed to import Model:[{}] from User_Defined:[{}]. Please check if the name of User_Defined and Model you provided is correct.\n'.format(model_name, user_defined), 'error')
    else:
        try:
            from young_mt.nmt.models import model_name
        except:
            GlobalVariable.nmt_train_logger.write_log('Failed to import Model:[{}]. Please check if the Name of the Model you provided is correct.\n'.format(model_name), 'error')

    try:
        model = eval(model_name)(source_vocabulary_size, target_vocabulary_size)
    except:
        GlobalVariable.nmt_train_logger.write_log('Failed to Build the object of the Model:[{}]. Please check if the type or the number of arguments you provided is correct.\n'.format(model_name), 'error')

    GlobalVariable.nmt_train_logger.write_log('Successfully built Model:[{}]\n'.format(model_name), 'info')

    return model


def compute_loss(mode, model, criterion, attributes, labels, teacher_forcing_rate=0.0, reduction='sum', normalization=1.0):
    if mode == 'train':
        gradient_mode = 'enable_grad'
    if mode == 'eval':
        gradient_mode = 'no_grad'

    if mode not in {'train', 'eval'}:
        GlobalVariable.nmt_train_logger.write_log('No such Mode:[{}]\n'.format(mode), 'error')

    sources = attributes[0]
    targets = labels[0]

    getattr(model, mode)()
    getattr(criterion, mode)()
    with getattr(torch, gradient_mode)():
        hypotheses = model(sources, targets, teacher_forcing_rate)
        loss = criterion(hypotheses, targets, reduction, normalization)

    if mode == 'train':
        loss.backword()

    return loss


def train(vocabulary, dataset):
    GlobalVariable.nmt_train_logger.write_log('Training process start ... ...\n', 'info')

    source_vocabulary_size = vocabulary['source'].size
    target_vocabulary_size = vocabulary['target'].size

    model = get_model(source_vocabulary_size, target_vocabulary_size)
    model.cuda()
    label_smoothing_rate = GlobalVariable.nmt_configs['Criterion']['Label_Smoothing_Rate']
    criterion = Criterion(label_smoothing_rate)
    criterion.cuda()

    optimizer_name = GlobalVariable.nmt_configs['Optimizer']['Name']
    initial_learning_rate = ConfigParser.get_expression_result(GlobalVariable.nmt_configs['Optimizer']['Initial_Learning_Rate'])
    weight_decay = ConfigParser.get_expression_result(GlobalVariable.nmt_configs['Optimizer']['Weight_Decay'])
    gradient_clipping = ConfigParser.get_expression_result(GlobalVariable.nmt_configs['Optimizer']['Gradient_Clipping'])
    optimizer = Optimizer(optimizer_name, model, initial_learning_rate, weight_decay, gradient_clipping)

    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer)#Scheduler(optimizer)

    load_last_checkpoint(model, optimizer, scheduler)


    number_of_epoch = ConfigParser.get_expression_result(GlobalVariable.nmt_configs['Train']['Number_of_Epoch'])
    batch_size = ConfigParser.get_expression_result(GlobalVariable.nmt_configs['Train']['Batch_Size'])
    teacher_forcing_rate = ConfigParser.get_expression_result(GlobalVariable.nmt_configs['Train']['Teacher_Forcing_Rate'])

    for epoch_index in range(number_of_epoch):
        GlobalVariable.nmt_train_logger.write_log('Now is the {}th epoch ... ...\n'.format(epoch_index+1), 'info')

        scheduler.step()
        optimizer.zero_grad()
        # Training
        # [Begin]
        for batch in BatchData(dataset['training'], batch_size):
            (attributes, labels) = batch
            training_loss = compute_loss('train', model, criterion, attributes, labels, teacher_forcing_rate, reduction='none')
        optimizer.step()
        # [End]

        # Loss Evaluation
        # [Begin]
        number_of_sentences = 0
        sum_of_evaluation_loss = 0.0
        for batch in BatchData(dataset['development'], batch_size):
            (attributes, labels) = batch
            evaluation_loss = compute_loss('eval', model, criterion, attributes, labels, teacher_forcing_rate, reduction='sum')
            if torch.isnan(evaluation_loss):
                GlobalVariable.nmt_train_logger.write_log('NaN Detected!\n', 'warn')
            number_of_sentences += len(attributes[0][0])
            sum_of_evaluation_loss += evaluation_loss
        evaluation_loss = sum_of_evaluation_loss / number_of_sentences
        # [End]

        # BLUE Evaluation
        # [Begin]
        bleu_score = compute_bleu(dataset['development'].batches(batch_size), model, )
        # [End]

    GlobalVariable.nmt_train_logger.write_log('Training process finish!\n', 'info')


def translate(vocabulary, dataset):
    source_vocabulary_size = vocabulary['source'].size
    target_vocabulary_size = vocabulary['target'].size
    model = get_model(source_vocabulary_size, target_vocabulary_size)
    model.eval()
    model.load()
    model.cuda()

    translation = []
    for instance in BatchData(dataset['testing'], 1):
        (attributes, labels) = instance
        with torch.no_grad():
            hypotheses = beam_search(model, attributes, target_vocabulary_size, beam_size, step_limit, alpha)


def main():
    user_nmt_argument_parser = argparse.ArgumentParser(prog='YoungMT - NMT', description='NMT System Framework.')
    user_nmt_argument = NMTArgument(user_nmt_argument_parser)
    user_nmt_args = user_nmt_argument.items

    GlobalVariable.initialize()

    load_configuration(user_nmt_args.configuration_file_name)

    set_workplace(user_nmt_args.working_directory_path)

    set_loggers(user_nmt_args.train_or_translate)

    check_device()

    vocabulary = get_vocabulary()
    vocabulary['source'].write_plain_to('src-vcb')
    vocabulary['target'].write_plain_to('tgt-vcb')

    dataset = get_dataset(vocabulary['source'], vocabulary['target'])

    if user_nmt_args.train_or_translate == 'train':
        train(vocabulary, dataset)

    if user_nmt_args.train_or_translate == 'translate':
        translate(vocabulary, dataset)


if __name__ == '__main__':
    main()
