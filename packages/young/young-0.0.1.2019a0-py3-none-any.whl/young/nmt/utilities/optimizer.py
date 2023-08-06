#!/usr/bin/env python
#-*- coding: utf-8 -*-

import torch

import young_mt.common.globals as global_vars

class Optimizer(object):
    def __init__(self, name, model, initial_learning_rate, weight_decay=0.0, gradient_clipping=0.0):
        if name not in {'Adadelta', 'Adagrad', 'Adam', 'Adamax', 'ASGD', 'RMSprop', 'SGD'}:
            global_vars.nmt_train_logger.error('The Optimizer\'s name you provided is not support now.\n'.format(name))
        self._name = name
        self._model = model
        self._initial_learning_rate = initial_learning_rate
        self._weight_decay = weight_decay
        self._gradient_clipping = gradient_clipping

        self._parameters_value = (parameter_value for (parameter_name, parameter_value) in self._parameters_require_gradient(self._model))

        self._weight_parameters_value_group = (parameter_value for (parameter_name, parameter_value) in self._parameters_require_gradient(self._model) if 'weight' in parameter_name)
        self._bias_parameters_value_group = (parameter_value for (parameter_name, parameter_value) in self._parameters_require_gradient(self._model) if 'bias' in parameter_name)

        self._parameters_value_group = [
                {
                    'params': self._weight_parameters_value_group,
                    'weight_decay': self._weight_decay,
                    },
                {
                    'params': self._bias_parameters_value_group,
                    },
                ]
        self._optimizer = getattr(torch.optim, name)(self._parameters_value_group, lr=self._initial_learning_rate)

    def _parameters_require_gradient(self, model):
        for (parameter_name, parameter_value) in model.named_parameters():
            if parameter_value.requires_grad:
                yield (parameter_name, parameter_value)

    def zero_grad(self):
        self.optimizer.zero_grad()

    def step(self, closure=None):
        if self._gradient_clipping_value:
            torch.nn.utils.clip_grad_norm_(self._parameters_value, self._gradient_clipping)
        self.optimizer.step(closure)

    def load_state_dict(self, state_dict):
        self.optimizer.load_state_dict(state_dict)

    def state_dict(self):
        return self.optimizer.state_dict()


if __name__ == '__main__':
    pass
 
