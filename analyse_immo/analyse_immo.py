#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import getopt
import json

from factory import Factory
from database import Database
from rendement import Rendement
# from impots.micro_foncier import Micro_Foncier
# from impot_regime_reel import Annexe_2044

__NAME = 'Analyse Immo'
__VERSION = '1.0.0-dev'

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
__INPUT_FILEPATH = os.path.join(__location__, 'data', 'input.json')


def main(argv):

    print('{} {}'.format(__NAME, __VERSION))

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

    tmi = impot_data['2019']['tmi']
#     imf = Micro_Foncier(database, bien_immo.loyer_nu_annuel, tmi)
#     irr = Annexe_2044(database, bien_immo, credit, tmi)

#     print_report(bien_immo, rendement, credit, imf, irr)
    print_report(bien_immo, rendement, credit, None, None)


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


def load_file(inputfile):
    if not inputfile:
        inputfile = __INPUT_FILEPATH

    with open(inputfile, 'r') as file:
        user_input = json.load(file)

    return user_input


def print_report(bien_immo, rendement, credit, imf, irr):
    from tabulate import tabulate

    achat = [
        ['Prix net\nvendeur', 'Notaire', 'Agence', 'Travaux', 'Apport', 'Financement\ntotal', 'Prix\ne/m²'],
        [bien_immo.prix_net_vendeur,
         '{:.0f}\n({:.2f}%)'.format(bien_immo.notaire_montant, bien_immo.notaire_taux * 100),
         '{:.0f}\n({:.2f}%)'.format(bien_immo.agence_montant, bien_immo.agence_taux * 100),
         bien_immo.budget_travaux,
         bien_immo.apport,
         bien_immo.financement_total,
         bien_immo.rapport_surface_prix
         ],
    ]

    location = [
        ['Loyer\nannuel', 'Loyer\nmensuel', 'Charges\nfonciere', 'Charges\ngestion'],
        [bien_immo.loyer_nu_annuel,
         bien_immo.loyer_nu_mensuel,
         bien_immo.charge_fonciere,
         bien_immo.charge_gestion],
    ]

#     charges = [
#         ['Taxe\nFonciere', 'Travaux\nProvision', 'Vacance\nLocative', 'PNO', 'Gestion\nagence', 'Copropriete'],
#         [bien_immo.taxe_fonciere,
#          bien_immo.travaux_provision_annuel_total,
#          bien_immo.vacance_locative_annuel_total,
#          bien_immo.pno_annuel_total,
#          bien_immo.gestion_agence_annuel_total,
#          bien_immo.copropriete_annuel_total,
#          ]
#     ]

    credit_in = [
        ['Capital\nemprunté', 'Durée', 'Taux\ninteret', 'Taux\nassurance', 'Mode'],
        [credit.capital,
         '{}({:.0f})'.format(credit.duree_mois, credit.duree_mois / 12),
         '{:.2f}%'.format(credit.taux * 100),
         '{:.2f}%'.format(credit.taux_assurance * 100),
         credit.mode],
    ]

    credit_out = [
        ['Mensualite\nhors assurance', 'Mensualite\nassurance', 'Mensualite\navec assurance', 'Cout\ninteret',
         'Cout\nassurance', 'Cout\ncredit'],
        ['{:.2f}'.format(credit.get_mensualite_hors_assurance()),
         '{:.2f}'.format(credit.get_mensualite_assurance()),
         '{:.2f}'.format(credit.get_mensualite_avec_assurance()),
         '{:.2f}'.format(credit.get_montant_interet_total()),
         '{:.2f}'.format(credit.get_montant_assurance_total()),
         '{:.2f}'.format(credit.get_cout_total())],
    ]

#     micro_foncier = [
#         ['Micro\nFoncier', 'Base\nimpossable', 'IR', 'PS', 'Total'],
#         ['-',
#             imf.base_impossable,
#             imf.revenu_foncier_impossable,
#             imf.prelevement_sociaux_montant,
#             imf.impot_total
#          ]
#     ]
#
#     regime_reel = [
#         ['Regime\nreel', 'Base\nimpossable', 'IR', 'PS', 'Total'],
#         ['-',
#          irr.base_impossable,
#          irr.revenu_foncier_impossable,
#          irr.prelevement_sociaux_montant,
#          irr.impot_total
#          ]
#     ]

    bilan = [
        ['Rendement\nBrut', 'Rendement\nNet', 'Rendement\nLarcher', 'Cashflow\nMensuel', 'Cashflow\nannuel'],
        ['{:.2f}%'.format(rendement.rendement_brut * 100),
         '{:.2f}%'.format(rendement.rendement_net * 100),
         '{:.2f}%'.format(rendement.rendement_methode_larcher * 100),
         '{:.2f}'.format(rendement.cashflow_mensuel),
         '{:.2f}'.format(rendement.cashflow_annuel)
         ]
    ]

    print(tabulate(achat, headers="firstrow") + '\n')
    print(tabulate(location, headers="firstrow") + '\n')
#     print(tabulate(charges, headers="firstrow") + '\n')
    print(tabulate(credit_in, headers="firstrow") + '\n')
    print(tabulate(credit_out, headers="firstrow") + '\n')
#     print(tabulate(micro_foncier, headers="firstrow") + '\n')
#     print(tabulate(regime_reel, headers="firstrow") + '\n')
    print(tabulate(bilan, headers="firstrow") + '\n')


if __name__ == '__main__':
    main(sys.argv[1:])
