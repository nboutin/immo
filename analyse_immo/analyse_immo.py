#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import getopt
import json
import calcul
import credit as cred
from bien_immo import Bien_Immo, Lot
from rendement import Rendement

__NAME = 'Rendement Locatif'
__VERSION = '1.0.0-dev'
__BIEN_IMMO_FILENAME = "bien_immo.json"


def main(argv):

    print('{} {}'.format(__NAME, __VERSION))

    inputfile = parse_args(argv)
    user_input = load_file(inputfile)

    bien_immo = make_bien_immo(user_input['bien_immo'])
#     prepare_inputs(user_input['bien_immo'])
    
    rendement = Rendement(bien_immo)
    credit = make_credit(user_input, bien_immo)
    
#     calcul_cashflow(user_input, credit)
#     calcul_impots_micro_foncier(user_input)
#     calcul_impots_regime_reel(user_input, credit)

    print_report(bien_immo, rendement, credit)


def parse_args(argv):

    inputfile = None

    try:
        opts, args = getopt.getopt(argv, 'i:h', [])
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
        inputfile = __BIEN_IMMO_FILENAME

    with open(inputfile, 'r') as file:
        user_input = json.load(file)

    return user_input


def make_bien_immo(user_input):
    
    bien_immo = Bien_Immo(user_input['prix_net_vendeur'],
                          user_input['frais_agence'],
                          user_input['frais_notaire'],
                          user_input['travaux_budget'],
                          user_input['apport'],
                          taxe_fonciere=user_input['taxe_fonciere'],
                          travaux_provision_taux=user_input['travaux_provision_taux']
                          )
    
    for lot in user_input['lots']:
        bien_immo.add_lot(Lot(lot['type'],
                              lot['surface'],
                              lot['loyer_mensuel'],
                              vacance_locative_taux_annuel=lot['vacance_locative'],
                              PNO=lot['PNO'],
                              gestion_agence_taux=lot['gestion_agence'],
                              copropriete=lot['copropriete']))
    
    return bien_immo


# def prepare_inputs(user_input):
#
#     user_input['loyers_mensuel_total'] = 0
#     user_input['surface_total'] = 0
#     for lot in user_input['lots']:
#         user_input['loyers_mensuel_total'] += lot['loyer_mensuel']
#         user_input['surface_total'] += lot['surface']
# 
#     user_input['loyers_annuel_total'] = user_input['loyers_mensuel_total'] * 12

#     taux = user_input['notaire']['honoraire_taux']
#     montant = user_input['notaire']['honoraire_montant']
#     if taux * user_input['prix_net_vendeur'] != montant:
#         if taux == 0:
#             user_input['notaire']['honoraire_taux'] = montant / user_input['prix_net_vendeur']
#         elif montant == 0:
#             user_input['notaire']['honoraire_montant'] = user_input['prix_net_vendeur'] * taux
#         else:
#             print('Error: notaire')
#             quit()
# 
#     taux = user_input['agence_immo']['honoraire_taux']
#     montant = user_input['agence_immo']['honoraire_montant']
#     if taux * user_input['prix_net_vendeur'] != montant:
#         if taux == 0:
#             user_input['agence_immo']['honoraire_taux'] = montant / user_input['prix_net_vendeur']
#         elif montant == 0:
#             user_input['agence_immo']['honoraire_montant'] = user_input['prix_net_vendeur'] * taux
#         else:
#             print('Error: agence_immo')
#             quit()
# 
#     user_input['invest_initial'] = user_input['prix_net_vendeur'] + user_input['notaire']['honoraire_montant'] \
#         +user_input['agence_immo']['honoraire_montant'] + user_input['travaux_budget'] - user_input['apport']

#     user_input['credit']['capital_emprunt'] = user_input['invest_initial']

#     calcul_charges_annuel(user_input)
#     calcul_surface_prix(user_input)


# def calcul_charges_annuel(user_input):
# 
#     user_input['charges_annuel_total'] = user_input['taxe_fonciere']
#     user_input['travaux_provision_annuel_total'] = 0
#     user_input['vacance_locative_annuel_total'] = 0
#     user_input['assurance_pno_annuel_total'] = 0
#     user_input['gestion_agence_annuel_total'] = 0
#     user_input['copropriete_annuel_total'] = 0
# 
#     for lot in user_input['lots']:
#         loyer = lot['loyer_mensuel']
#         user_input['travaux_provision_annuel_total'] += user_input['travaux_provision'] * loyer * 12
#         user_input['vacance_locative_annuel_total'] += lot['vacance_locative'] * loyer * 12
#         user_input['assurance_pno_annuel_total'] += lot['assurance_pno']
#         user_input['gestion_agence_annuel_total'] += lot['gestion_agence'] * loyer * 12
#         user_input['copropriete_annuel_total'] += lot['copropriete']
# 
#     user_input['charges_annuel_total'] += user_input['travaux_provision_annuel_total']
#     user_input['charges_annuel_total'] += user_input['vacance_locative_annuel_total']
#     user_input['charges_annuel_total'] += user_input['assurance_pno_annuel_total']
#     user_input['charges_annuel_total'] += user_input['gestion_agence_annuel_total']
#     user_input['charges_annuel_total'] += user_input['copropriete_annuel_total']

# def calcul_surface_prix(user_input):
# 
#     user_input['surface_prix'] = 0
# 
#     if user_input['surface_total'] > 0:
#         user_input['surface_prix'] = user_input['prix_net_vendeur'] / user_input['surface_total']

# def calcul_rendement_brut(user_input):
# 
#     user_input['r_brut'] = calcul.rendement_brut(user_input['loyers_annuel_total'], user_input['invest_initial'])

# def calcul_rendement_methode_larcher(user_input):
# 
#     user_input['r_larcher'] = calcul.rendement_methode_larcher(user_input['loyers_mensuel_total'], user_input['invest_initial'])
# 
# 
# def calcul_rendement_net(user_input):
# 
#     user_input['r_net'] = calcul.rendement_net(user_input['loyers_annuel_total'],
#                                               user_input['charges_annuel_total'],
#                                               user_input['invest_initial'])


def make_credit(user_input, bien_immo):
    
    credit = cred.Credit(bien_immo.investissement_initial,
                         user_input['credit']['duree_annee'] * 12,
                         user_input['credit']['taux_interet'],
                         user_input['credit']['taux_assurance'],
                         user_input['credit']['mode'],
                         user_input['credit']['frais_dossier'],
                         user_input['credit']['frais_garantie']
                        )
    return credit


def calcul_cashflow(user_input, credit):

    user_input['cashflow_mensuel'] = \
        calcul.cashflow_mensuel(user_input['loyers_mensuel_total'],
                                credit.get_mensualite_avec_assurance(),
                                user_input['charges_annuel_total'])

    user_input['cashflow_annuel'] = user_input['cashflow_mensuel'] * 12


def calcul_impots_micro_foncier(user_input):

    user_input['impots']['micro_foncier']['base_impossable'] = \
        user_input['loyers_annuel_total'] * (1 - user_input['impots']['micro_foncier']['taux'])

    base = user_input['impots']['micro_foncier']['base_impossable']

    user_input['impots']['micro_foncier']['impots_revenu'] = base * user_input['impots']['tmi']
    user_input['impots']['micro_foncier']['prelevement_sociaux'] = base * user_input['impots']['ps']
    user_input['impots']['micro_foncier']['total'] = \
        user_input['impots']['micro_foncier']['impots_revenu'] + user_input['impots']['micro_foncier']['prelevement_sociaux']


def calcul_impots_regime_reel(user_input, credit):
    '''
    charges deductibles:
        - interet d'emprunt
        - assurance emprunteur
        - assurance PNO
        - taxe fonciere
        - frais bancaire, frais de dossier, fond mutuelle de garantie
        - frais postaux a destination du locataire
        - travaux
    '''
    base = user_input['loyers_annuel_total']
    base -= user_input['taxe_fonciere']
    base -= user_input['assurance_pno_annuel_total']
#     base -= user_input['credit']['cout_interet'] / user_input['credit']['duree_annee']
    # TODO soustraire cout des interets annuels
#     base -= user_input['credit']['mensualite_assurance'] * 12
    # TODO soustraire cout d'assurance emprunteur annuel

    user_input['impots']['regime_reel'] = dict()
    user_input['impots']['regime_reel']['base_impossable'] = base

    user_input['impots']['regime_reel']['impots_revenu'] = base * user_input['impots']['tmi']
    user_input['impots']['regime_reel']['prelevement_sociaux'] = base * user_input['impots']['ps']
    user_input['impots']['regime_reel']['total'] = \
        user_input['impots']['regime_reel']['impots_revenu'] + user_input['impots']['regime_reel']['prelevement_sociaux']

#     interets = calcul.interet_emprunt(user_input['credit']['capital_emprunt'],
#                                       user_input['credit']['duree_annee'] * 12,
#                                       user_input['credit']['taux_interet'],
#                                       user_input['credit']['mensualite_hors_assurance'])
#     interet_annee_1 = 0
#     for i in range(1, 12):
#         interet_annee_1 += interets[i]
#     print(interet_annee_1)


def print_report(bien_immo, rendement, credit):
    from tabulate import tabulate

    achat = [
        ['Prix net\nvendeur', 'Notaire', 'Agence', 'Travaux', 'Apport', 'Invest\ninitial', 'Prix\ne/m²'],
        [bien_immo.prix_net_vendeur,
         '{:.0f}\n({:.2f}%)'.format(bien_immo.notaire_montant, bien_immo.notaire_taux * 100),
         '{:.0f}\n({:.2f}%)'.format(bien_immo.agence_montant, bien_immo.agence_taux * 100),
         bien_immo.travaux_budget,
         bien_immo.apport,
         bien_immo.investissement_initial,
         bien_immo.rapport_surface_prix
        ],
    ]

    location = [
        ['Loyer\nannuel', 'Loyer\nmensuel', 'Charges\nannuel'],
        [bien_immo.loyer_annuel_total,
         bien_immo.loyer_mensuel_total,
         bien_immo.charges_annuel_total, ],
    ]
 
#     charges = [
#         ['Taxe\nFonciere', 'Travaux\nProvision', 'Vacance\nLocative', 'PNO', 'Gestion\nagence', 'Copropriete'],
#         [user_input['taxe_fonciere'],
#          user_input['travaux_provision_annuel_total'],
#          user_input['vacance_locative_annuel_total'],
#          user_input['assurance_pno_annuel_total'],
#          user_input['gestion_agence_annuel_total'],
#          user_input['copropriete_annuel_total'],
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
 
    bilan = [
        ['Rendement\nBrut', 'Rendement\nNet', 'Rendement\nLarcher', 'Cashflow\nMensuel', 'Cashflow\nannuel'],
#         ['{:.2f}%'.format(user_input['r_brut'] * 100),
#         '{:.2f}%'.format(user_input['r_net'] * 100),
#         '{:.2f}%'.format(user_input['r_larcher'] * 100),
#         '{:.2f}'.format(user_input['cashflow_mensuel']),
#         '{:.2f}'.format(user_input['cashflow_annuel'])
#         ]
        ['{:.2f}%'.format(rendement.rendement_brut * 100),
        '{:.2f}%'.format(rendement.rendement_net * 100),
        '{:.2f}%'.format(rendement.rendement_methode_larcher * 100),
        '{:.2f}'.format(rendement.cashflow_mensuel),
        '{:.2f}'.format(rendement.cashflow_annuel)
        ]
    ]
 
#     micro_foncier = [
#         ['Micro\nFoncier', 'Base\nimpossable', 'IR', 'PS', 'Total'],
#         ['-',
#          user_input['impots']['micro_foncier']['base_impossable'],
#          user_input['impots']['micro_foncier']['impots_revenu'],
#          user_input['impots']['micro_foncier']['prelevement_sociaux'],
#          user_input['impots']['micro_foncier']['total'],
#          ]
#     ]
# 
#     regime_reel = [
#         ['Regime\nreel', 'Base\nimpossable', 'IR', 'PS', 'Total'],
#         ['-',
#          user_input['impots']['regime_reel']['base_impossable'],
#          user_input['impots']['regime_reel']['impots_revenu'],
#          user_input['impots']['regime_reel']['prelevement_sociaux'],
#          user_input['impots']['regime_reel']['total'],
#          ]
#     ]

    print(tabulate(achat, headers="firstrow") + '\n')
    print(tabulate(location, headers="firstrow") + '\n')
#     print(tabulate(charges, headers="firstrow") + '\n')
    print(tabulate(credit_in, headers="firstrow") + '\n')
    print(tabulate(credit_out, headers="firstrow") + '\n')
    print(tabulate(bilan, headers="firstrow") + '\n')
#     print(tabulate(micro_foncier, headers="firstrow") + '\n')
#     print(tabulate(regime_reel, headers="firstrow") + '\n')


if __name__ == '__main__':
    main(sys.argv[1:])
