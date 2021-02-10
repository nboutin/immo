#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import getopt
import json
import logging

from analyse_immo.factory import Factory
from analyse_immo.database import Database
from analyse_immo.rendement import Rendement
from analyse_immo.rapports.rapport import generate_rapport

__NAME = 'Analyse Immo'
__VERSION = '2.1.0-dev'

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
__INPUT_FILEPATH = os.path.join(__location__, 'data', 'input_2020.json')
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

    achat_data = input_data['achat']
    defaut_data = input_data['defaut']
    lots_data = input_data['lots']
    credit_data = input_data['credit']
    impot_data = input_data['impot']

    database = Database()
    defaut = Factory.make_defaut(defaut_data)

    bien_immo = Factory.make_bien_immo(achat_data, lots_data, defaut)
    credit = Factory.make_credit(credit_data, bien_immo)
    rendement = Rendement(bien_immo, credit)

    # Impot
    annee_achat = achat_data['annee']
    credit_duree = credit_data['duree_annee']

    # IRPP + 2044
    irpp_2044_list = list()

    for i_annee in range(credit_duree):
        annee_revenu = annee_achat + i_annee
        irpp = Factory.make_irpp(database, impot_data, annee_revenu)

        irpp.annexe_2044 = Factory.make_annexe_2044(database, bien_immo, credit, i_annee + 1)
        irpp_2044_list.append(irpp)

    # IRPP + Micro foncier
    irpp_micro_foncier_list = list()

    for i_annee in range(credit_duree):
        annee_revenu = annee_achat + i_annee
        irpp = Factory.make_irpp(database, impot_data, annee_revenu)

        irpp.micro_foncier = Factory.make_micro_foncier(database, bien_immo)
        irpp_micro_foncier_list.append(irpp)

    # Rapport
    generate_rapport(bien_immo, credit, annee_achat, irpp_2044_list, irpp_micro_foncier_list, rendement)


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

    with open(inputfile, 'r') as file:
        user_input = json.load(file)

    return user_input
