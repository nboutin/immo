#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import getopt
import json
import logging

# from analyse_immo import analyse_immo
from analyse_immo.factory import Factory
# from analyse_immo.database import Database
# from analyse_immo.rendement import Rendement
from analyse_immo.rapports.rapport import rapport_achat, rapport_location, rapport_credit, rapport_rendement, rapport_overview
from analyse_immo.rapports.rapport_annexe_2044 import rapport_annexe_2044
from analyse_immo.rapports.rapport_micro_foncier import rapport_micro_foncier
from analyse_immo.rapports.rapport_irpp import rapport_irpp
# from analyse_immo.impots import irpp

__NAME = 'Analyse Immo'
__VERSION = '2.1.0-dev'

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
__INPUT_FILEPATH = os.path.join(__location__, 'data', 'input_2021.json')
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

    # achat_data = input_data['achat']
    # defaut_data = input_data['defaut']
    # commun_data = input_data['commun']
    # lots_data = input_data['lots']
    # credit_data = input_data['credit']
    # impot_data = input_data['impot']
    #
    # database = Database()
    # defaut = Factory.make_defaut(defaut_data)
    #
    # bien_immo = Factory.make_bien_immo(achat_data, commun_data, lots_data, defaut)
    # credit = Factory.make_credit(credit_data, bien_immo)
    #
    # # Impot
    # annee_achat = achat_data['annee']
    # credit_duree = credit_data['duree_annee']
    # projection_duree = credit_duree + 5
    # salaire_taux = defaut_data['salaire_taux_annuel']
    #
    # # IRPP + 2044
    # irpp_2044_projection = Factory.make_irpp_projection(
    # projection_duree, annee_achat, database, impot_data, salaire_taux, bien_immo, credit)
    #
    # # IRPP + Micro foncier
    # irpp_micro_foncier_projection = list()
    #
    # for i_annee in range(projection_duree):
    # annee_revenu = annee_achat + i_annee
    # irpp = Factory.make_irpp(database, impot_data, annee_revenu, i_annee, salaire_taux)
    #
    # irpp.micro_foncier = Factory.make_micro_foncier(database, bien_immo, i_annee + 1)
    # irpp_micro_foncier_projection.append(irpp)

    # # Rendement
    # rendement = Rendement(bien_immo, credit, irpp_2044_projection)

    # Rapport
    rapport_achat(analyse.bien_immo)
    rapport_location(analyse.projection_duree, analyse.bien_immo, analyse.annee_achat)
    rapport_credit(analyse.projection_duree, analyse.credit, analyse.annee_achat)
    rapport_annexe_2044(analyse.annee_achat, analyse.irpp_2044_projection, analyse.bien_immo)
    rapport_micro_foncier(analyse.annee_achat, analyse.irpp_micro_foncier_projection, analyse.bien_immo)
    rapport_irpp(
        analyse.annee_achat,
        analyse.defaut.salaire_taux,
        analyse.irpp_2044_projection,
        analyse.irpp_micro_foncier_projection)
    rapport_rendement(analyse.annee_achat, analyse.projection_duree, analyse.rendement)
    rapport_overview(
        analyse.annee_achat,
        analyse.projection_duree,
        analyse.bien_immo,
        analyse.credit,
        analyse.irpp_2044_projection,
        analyse.rendement)


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
