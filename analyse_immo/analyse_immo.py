#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os
import getopt
import json

from database import Database
from defaut import Defaut
from bien_immo import Bien_Immo
from lot import Lot
from charge import Charge
import credit as cred
from rendement import Rendement
from impot_micro_foncier import Impot_Micro_Foncier
from impot_regime_reel import Impot_Regime_Reel

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
    defaut = make_defaut(defaut_data)
    bien_immo = make_bien_immo(achat_data, lots_data, defaut)
    
    credit = make_credit(credit_data, bien_immo)
    rendement = Rendement(bien_immo)
    imf = Impot_Micro_Foncier(database, bien_immo.loyer_nu_annuel, impot_data['2019']['tmi'])
    irr = Impot_Regime_Reel(database, bien_immo, impot_data['2019']['tmi'])
 
    print_report(bien_immo, rendement, credit, imf, irr)


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


def make_defaut(defaut_data):
    
    defaut = Defaut(defaut_data['provision_travaux_taux'],
                    defaut_data['vacance_locative_taux_T1'],
                    defaut_data['vacance_locative_taux_T2'],
                    defaut_data['gestion_agence_taux'],)
    
    return defaut


def make_bien_immo(achat_data, lots_data, defaut=Defaut(0, 0, 0, 0)):
    
    bien_immo = Bien_Immo(achat_data['prix_net_vendeur'],
                          achat_data['frais_agence'],
                          achat_data['frais_notaire'],
                          achat_data['budget_travaux'],
                          achat_data['apport'])
    
    for lot_data in lots_data:
        
        lot = Lot(lot_data['type'],
                  lot_data['surface'],
                  lot_data['loyer_nu_mensuel'])

        charge = Charge(lot, defaut)

        charge_data = lot_data['charge']
        charge.add(charge.gestion_e.charge_locative, charge_data['provision_charge_mensuel'])
        charge.add(charge.deductible_e.copropriete, charge_data['copropriete'])
        charge.add(charge.deductible_e.taxe_fonciere, charge_data['taxe_fonciere'])
        charge.add(charge.deductible_e.prime_assurance, charge_data['PNO'])
        
        gestion_data = lot_data['gestion']
        charge.add(Charge.gestion_e.provision_travaux, gestion_data['travaux_provision_taux'])
        charge.add(Charge.gestion_e.vacance_locative, gestion_data['vacance_locative_taux'])
        charge.add(Charge.gestion_e.agence_immo, gestion_data['agence_immo'])
        lot.charge = charge
        
        bien_immo.add_lot(lot)
    
    return bien_immo


def make_credit(credit_data, bien_immo):
    
    credit = cred.Credit(bien_immo.investissement_initial,
                         credit_data['duree_annee'] * 12,
                         credit_data['taux_interet'],
                         credit_data['taux_assurance'],
                         credit_data['mode'],
                         credit_data['frais_dossier'],
                         credit_data['frais_garantie']
                        )
    return credit


def print_report(bien_immo, rendement, credit, imf, irr):
    from tabulate import tabulate

    achat = [
        ['Prix net\nvendeur', 'Notaire', 'Agence', 'Travaux', 'Apport', 'Invest\ninitial', 'Prix\ne/m²'],
        [bien_immo.prix_net_vendeur,
         '{:.0f}\n({:.2f}%)'.format(bien_immo.notaire_montant, bien_immo.notaire_taux * 100),
         '{:.0f}\n({:.2f}%)'.format(bien_immo.agence_montant, bien_immo.agence_taux * 100),
         bien_immo.budget_travaux,
         bien_immo.apport,
         bien_immo.investissement_initial,
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
 
    micro_foncier = [
        ['Micro\nFoncier', 'Base\nimpossable', 'IR', 'PS', 'Total'],
        ['-',
            imf.base_impossable,
            imf.revenu_foncier_impossable,
            imf.prelevement_sociaux_montant,
            imf.impot_total
         ]
    ]
 
    regime_reel = [
        ['Regime\nreel', 'Base\nimpossable', 'IR', 'PS', 'Total'],
        ['-',
         irr.base_impossable,
         irr.revenu_foncier_impossable,
         irr.prelevement_sociaux_montant,
         irr.impot_total
         ]
    ]
 
    bilan = [
        ['Rendement\nBrut', 'Rendement\nNet', 'Rendement\nLarcher', 'Cashflow\nMensuel', 'Cashflow\nannuel'],
        ['{:.2f}%'.format(rendement.rendement_brut * 100),
        '{:.2f}%'.format(rendement.rendement_net * 100),
        '{:.2f}%'.format(rendement.rendement_methode_larcher * 100),
        '{:.2f}'.format(rendement.cashflow_mensuel(credit)),
        '{:.2f}'.format(rendement.cashflow_annuel(credit))
        ]
    ]

    print(tabulate(achat, headers="firstrow") + '\n')
    print(tabulate(location, headers="firstrow") + '\n')
#     print(tabulate(charges, headers="firstrow") + '\n')
    print(tabulate(credit_in, headers="firstrow") + '\n')
    print(tabulate(credit_out, headers="firstrow") + '\n')
    print(tabulate(micro_foncier, headers="firstrow") + '\n')
    print(tabulate(regime_reel, headers="firstrow") + '\n')
    print(tabulate(bilan, headers="firstrow") + '\n')


if __name__ == '__main__':
    main(sys.argv[1:])
