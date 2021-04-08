#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@date: 2021-03
@author: nboutin
'''
import logging
import os
import sys

from immo_analyse.immo_system import ImmoSystem
from immo_analyse.core.simulation_builder import SimulationBuilder
from immo_analyse.report.report_generator import ReportGenerator

from immo_analyse.input.input_2021_03_im_mir_130 import entities

__NAME = 'Immo Analyse'
__VERSION = '3.0.0-dev'

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
__OUTPUT_FILEPATH = os.path.join(__location__, 'immo_analyse.log')


def main(argv):
    '''
    Demo code, immo_analyse should be use as Python Package
    '''
    immo_sys = ImmoSystem()
    simu_builder = SimulationBuilder()
    simu = simu_builder.build_from_entities(immo_sys, entities)

    rg = ReportGenerator(2021, 25, simu)
    rg.generate_all()


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


if __name__ == '__main__':
    import locale
    locale.setlocale(locale.LC_ALL, '')
    main(sys.argv[1:])
