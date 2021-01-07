#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import getopt
import json
import logging

from factory import Factory
from database import Database
from rendement import Rendement
from impots.irpp import IRPP
from rapports.rapport import generate_rapport

__NAME = 'Analyse Immo'
__VERSION = '1.0.0-dev'

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
__INPUT_FILEPATH = os.path.join(__location__, 'data', 'input.json')
__OUTPUT_FILEPATH = os.path.join(__location__, 'output', 'analyse_immo.log')


def main(argv):
    configure_logger()

    logging.info('{} {}\n'.format(__NAME, __VERSION))

    inputfile = parse_args(argv)
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
    annexe_2044_list = list()
    for annee_index in range(credit_data['duree_annee']):
        annexe_2044_list.append(Factory.make_annexe_2044(bien_immo, credit, annee_index + 1))

    annee_courante = achat_data['annee']
    irpp = Factory.make_irpp(database, achat_data, impot_data, annee_courante)
    irpp.add_annexe(annexe_2044_list[0])

    # Rapport
    generate_rapport(bien_immo, credit, annee_courante, annexe_2044_list, irpp, rendement)


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
    print('help')


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


def load_file(inputfile):
    if not inputfile:
        inputfile = __INPUT_FILEPATH

    with open(inputfile, 'r') as file:
        user_input = json.load(file)

    return user_input


if __name__ == '__main__':
    main(sys.argv[1:])
