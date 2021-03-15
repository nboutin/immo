#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import getopt
import json
import logging

from analyse_immo.factory import Factory
from analyse_immo.rapports.rapport import rapport

__NAME = 'Analyse Immo'
__VERSION = '2.1.0-dev'

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
__INPUT_FILEPATH = os.path.join(__location__, 'data', 'input_2021_im_mir_130.json')
__OUTPUT_FILEPATH = os.path.join(__location__, 'analyse_immo.log')


def main(argv):
    configure_logger()

    logging.info('{} {}\n'.format(__NAME, __VERSION))

    inputfile = parse_args(argv)
    # If path to input file is provided, create output log file in the same folder
    if inputfile:
        location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(inputfile)))
        filepath = os.path.join(location, 'analyse_immo.log')
        add_logger_file_handler(filepath)

    input_data = load_file(inputfile)
    analyse = Factory.make_analyse(input_data)
    rapport(analyse)


def parse_args(argv):

    inputfile = None

    try:
        opts, _ = getopt.getopt(argv, 'i:h', [])
    except getopt.GetoptError:
        print_help()
        quit()

    for opt, arg in opts:
        if opt == '-h':
            print_help()
            quit()
        elif opt in ('-i'):
            inputfile = arg

    return inputfile


def print_help():
    print('-i input file')
    print('-h help')


def configure_logger():
    '''
    write to console, simple message with log level info
    write to file, formatted message with log level debug
    '''
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.INFO)
    consoleFormatter = logging.Formatter('%(message)s')
    consoleHandler.setFormatter(consoleFormatter)
    logger.addHandler(consoleHandler)

    fileHandler = logging.FileHandler(__OUTPUT_FILEPATH, mode='w')
    fileHandler.setLevel(logging.DEBUG)
    fileFormatter = logging.Formatter('%(message)s')
    fileHandler.setFormatter(fileFormatter)
    logger.addHandler(fileHandler)


def add_logger_file_handler(filepath):
    import logging.handlers
    logger = logging.getLogger()

    fileHandler = logging.handlers.TimedRotatingFileHandler(filepath, when='S')
    fileHandler.setLevel(logging.DEBUG)
    fileFormatter = logging.Formatter('%(message)s')
    fileHandler.setFormatter(fileFormatter)
    logger.addHandler(fileHandler)


def load_file(inputfile):
    if not inputfile:
        inputfile = __INPUT_FILEPATH

    logging.info('Load file:{}'.format(inputfile))
    with open(inputfile, 'r') as file:
        user_input = json.load(file)

    return user_input


if __name__ == '__main__':
    import locale
    locale.setlocale(locale.LC_ALL, '')
    main(sys.argv[1:])
