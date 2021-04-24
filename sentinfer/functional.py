# -*- coding: utf-8 -*-
# file: functional.py
# time: 2021/4/22 0022
# author: yangheng <yangheng@m.scnu.edu.cn>
# github: https://github.com/yangheng95
# Copyright (C) 2021. All Rights Reserved.

import os
from argparse import Namespace

from sentinfer.batch_inferring.inferring import INFER_MODEL
from sentinfer.main.train import train_by_single_config
from sentinfer.main.training_configs import *


def init_training_config(config_dict):
    config = Namespace()
    if 'SRD' in config_dict:
        config.SRD = config_dict['SRD']
    else:
        config.SRD = SRD

    if 'batch_size' in config_dict:
        config.batch_size = config_dict['batch_size']
    else:
        config.batch_size = batch_size

    if 'distance_aware_window' in config_dict:
        config.distance_aware_window = config_dict['distance_aware_window']
    else:
        config.distance_aware_window = distance_aware_window

    if 'dropout' in config_dict:
        config.dropout = config_dict['dropout']
    else:
        config.dropout = dropout

    if 'l2reg' in config_dict:
        config.l2reg = config_dict['l2reg']
    else:
        config.l2reg = l2reg

    if 'lcf' in config_dict:
        config.lcf = config_dict['lcf']
    else:
        config.lcf = lcf

    if 'initializer' in config_dict:
        config.initializer = config_dict['initializer']
    else:
        config.initializer = 'xavier_uniform_'

    if 'learning_rate' in config_dict:
        config.learning_rate = config_dict['learning_rate']
    else:
        config.learning_rate = learning_rate

    if 'max_seq_len' in config_dict:
        config.max_seq_len = config_dict['max_seq_len']
    else:
        config.max_seq_len = max_seq_len

    if 'model_name' in config_dict:
        config.model_name = config_dict['model_name']
    else:
        config.model_name = model_name

    if 'num_epoch' in config_dict:
        config.num_epoch = config_dict['num_epoch']
    else:
        config.num_epoch = num_epoch

    if 'optimizer' in config_dict:
        config.optimizer = config_dict['optimizer']
    else:
        config.optimizer = optimizer

    if 'pretrained_bert_name' in config_dict:
        config.pretrained_bert_name = config_dict['pretrained_bert_name']
    else:
        config.pretrained_bert_name = pretrained_bert_name

    if 'use_bert_spc' in config_dict:
        config.use_bert_spc = config_dict['use_bert_spc']
    else:
        config.use_bert_spc = use_bert_spc

    if 'use_dual_bert' in config_dict:
        config.use_dual_bert = config_dict['use_dual_bert']
    else:
        config.use_dual_bert = use_dual_bert

    if 'window' in config_dict:
        config.window = config_dict['window']
    else:
        config.window = window

    if 'seed' in config_dict:
        config.seed = config_dict['seed']
    else:
        config.seed = 996
    if 'device' in config_dict:
        config.device = config_dict['device']
    else:
        try:
            from sentinfer.utils.Pytorch_GPUManager import GPUManager
            choice = GPUManager().auto_choice()
            config.device = 'cuda:' + str(choice)
        except:
            config.device = 'cpu'
    if 'distance_aware_windows' in config_dict:
        config.distance_aware_windows = config_dict['distance_aware_windows']
    else:
        config.distance_aware_windows = True
    config.embed_dim = 768
    config.hidden_dim = 768
    config.polarities_dim = 3
    return config


def train(parameter_dict=None, train_dataset_path=None, model_path_to_save=None):
    if not train_dataset_path:
        train_dataset_path = os.getcwd()
        print('Try to load dataset in current path.')
    # load training set
    try:
        if os.path.isdir(train_dataset_path):
            train_dataset_path += '/' + [p for p in os.listdir(train_dataset_path) if 'train' in p.lower()][0]
    except:
        raise RuntimeError('Can not find path of train dataset!')
    config = init_training_config(parameter_dict)
    config.train_dataset_path = train_dataset_path
    config.model_path_to_save = model_path_to_save + '/' + config.model_name
    return INFER_MODEL(trainer=train_by_single_config(config))


def load_trained_model(parameter_dict=None, trained_model_path=None):
    print('Be sure this path has only one saved state dict.')

    if not trained_model_path:
        trained_model_path = os.getcwd()
        print('Try to load dataset in current path.')
    try:
        if os.path.isdir(trained_model_path):
            # load training set
            trained_model_path += '/' + [p for p in os.listdir(trained_model_path) if '.state_dict' in p.lower()][0]
    except:
        raise RuntimeError('Can not find path of trained model!')
    config = init_training_config(parameter_dict)
    InferModel = INFER_MODEL(config, trained_model_path)
    return InferModel


def print_usages():
    usages = '1. Use your data to train the model, please build a custom data set according ' \
             'to the format of the data set provided by the reference\n' \
             '利用你的数据训练模型，请根据参考提供的数据集的格式构建自定义数据集\n' \
             'infer_model = train(param_dict, train_set_path, model_path_to_save)\n' \
                \
             '2. Load the trained model\n' \
             '加载已训练并保存的模型\n' \
             'infermodel = load_trained_model(param_dict, model_path_to_save)\n' \
                \
             '3. Batch reasoning about emotional polarity based on files\n' \
             '根据文件批量推理情感极性\n' \
             'result = infermodel.batch_infer(test_set_path)\n' \
                \
             '4. Input a single text to infer sentiment\n' \
             '输入单条文本推理情感\n' \
             'infermodel.infer(text)\n' \
                \
             '5. Convert the provided dataset into a dataset for inference\n' \
             '将提供的数据集转换为推理用的数据集\n' \
             'convert_dataset_for_inferring(dataset_path)\n'

    print(usages)
