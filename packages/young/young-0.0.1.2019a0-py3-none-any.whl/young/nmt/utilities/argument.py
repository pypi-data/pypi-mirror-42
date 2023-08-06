#!/usr/bin/env python
#-*- coding: utf-8 -*-

from young_tools.argument import Argument


class NMTArgument(Argument):
    def _add_items(self):
        group = self._argument_parser.add_argument_group('User\'s NMT System Configuration')
        group.add_argument('-t', '--train_or_translate', required=True, choices=['train','translate'])
        group.add_argument('-p', '--working_directory_path', type=str, default='.')
        group.add_argument('-c', '--configuration_file_name', type=str, default=None)


if __name__ == '__main__':
    import argparse
    nmt_parser = argparse.ArgumentParser()
    nmt_argument = NMTArgument(nmt_parser)
    print(nmt_argument.items)
