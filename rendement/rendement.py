#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import getopt
import json
import calcul
import credit as cred

__NAME = 'Rendement Locatif'
__VERSION = '1.0.0-dev'
__BIEN_IMMO_FILENAME = "bien_immo.json"


def main(argv):

    print('{} {}'.format(__NAME, __VERSION))

    inputfile = parse_args(argv)
    if not inputfile:
        inputfile = __BIEN_IMMO_FILENAME

    with open(inputfile, 'r') as file:
        bien_immo = json.load(file)

    prepare_inputs(bien_immo)

    calcul_rendement_brut(bien_immo)
    calcul_rendement_methode_larcher(bien_immo)
    calcul_rendement_net(bien_immo)
    credit = calcul_credit(bien_immo)
    calcul_cashflow(bien_immo, credit)

    calcul_impots_micro_foncier(bien_immo)
    calcul_impots_regime_reel(bien_immo, credit)

    print_report(bien_immo, credit)


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


def prepare_inputs(bien_immo):

    bien_immo['loyers_mensuel_total'] = 0
    bien_immo['surface_total'] = 0
    for lot in bien_immo['lots']:
        bien_immo['loyers_mensuel_total'] += lot['loyer_mensuel']
        bien_immo['surface_total'] += lot['surface']

    bien_immo['loyers_annuel_total'] = bien_immo['loyers_mensuel_total'] * 12

    taux = bien_immo['notaire']['honoraire_taux']
    montant = bien_immo['notaire']['honoraire_montant']
    if taux * bien_immo['prix_net_vendeur'] != montant:
        if taux == 0:
            bien_immo['notaire']['honoraire_taux'] = montant / bien_immo['prix_net_vendeur']
        elif montant == 0:
            bien_immo['notaire']['honoraire_montant'] = bien_immo['prix_net_vendeur'] * taux
        else:
            print('Error: notaire')
            quit()

    taux = bien_immo['agence_immo']['honoraire_taux']
    montant = bien_immo['agence_immo']['honoraire_montant']
    if taux * bien_immo['prix_net_vendeur'] != montant:
        if taux == 0:
            bien_immo['agence_immo']['honoraire_taux'] = montant / bien_immo['prix_net_vendeur']
        elif montant == 0:
            bien_immo['agence_immo']['honoraire_montant'] = bien_immo['prix_net_vendeur'] * taux
        else:
            print('Error: agence_immo')
            quit()

    bien_immo['invest_initial'] = bien_immo['prix_net_vendeur'] + bien_immo['notaire']['honoraire_montant'] \
        +bien_immo['agence_immo']['honoraire_montant'] + bien_immo['travaux_budget'] - bien_immo['apport']

    bien_immo['credit']['capital_emprunt'] = bien_immo['invest_initial']

    calcul_charges_annuel(bien_immo)
    calcul_surface_prix(bien_immo)


def calcul_charges_annuel(bien_immo):

    bien_immo['charges_annuel_total'] = bien_immo['taxe_fonciere']
    bien_immo['travaux_provision_annuel_total'] = 0
    bien_immo['vacance_locative_annuel_total'] = 0
    bien_immo['assurance_pno_annuel_total'] = 0
    bien_immo['gestion_agence_annuel_total'] = 0
    bien_immo['copropriete_annuel_total'] = 0

    for lot in bien_immo['lots']:
        loyer = lot['loyer_mensuel']
        bien_immo['travaux_provision_annuel_total'] += bien_immo['travaux_provision'] * loyer * 12
        bien_immo['vacance_locative_annuel_total'] += lot['vacance_locative'] * loyer * 12
        bien_immo['assurance_pno_annuel_total'] += lot['assurance_pno']
        bien_immo['gestion_agence_annuel_total'] += lot['gestion_agence'] * loyer * 12
        bien_immo['copropriete_annuel_total'] += lot['copropriete']

    bien_immo['charges_annuel_total'] += bien_immo['travaux_provision_annuel_total']
    bien_immo['charges_annuel_total'] += bien_immo['vacance_locative_annuel_total']
    bien_immo['charges_annuel_total'] += bien_immo['assurance_pno_annuel_total']
    bien_immo['charges_annuel_total'] += bien_immo['gestion_agence_annuel_total']
    bien_immo['charges_annuel_total'] += bien_immo['copropriete_annuel_total']


def calcul_surface_prix(bien_immo):

    bien_immo['surface_prix'] = 0

    if bien_immo['surface_total'] > 0:
        bien_immo['surface_prix'] = bien_immo['prix_net_vendeur'] / bien_immo['surface_total']


def calcul_rendement_brut(bien_immo):

    bien_immo['r_brut'] = calcul.rendement_brut(bien_immo['loyers_annuel_total'], bien_immo['invest_initial'])


def calcul_rendement_methode_larcher(bien_immo):

    bien_immo['r_larcher'] = calcul.rendement_methode_larcher(bien_immo['loyers_mensuel_total'], bien_immo['invest_initial'])


def calcul_rendement_net(bien_immo):

    bien_immo['r_net'] = calcul.rendement_net(bien_immo['loyers_annuel_total'],
                                              bien_immo['charges_annuel_total'],
                                              bien_immo['invest_initial'])


def calcul_credit(bien_immo):
    
    credit = cred.Credit(bien_immo['credit']['capital_emprunt'],
                         bien_immo['credit']['duree_annee'] * 12,
                         bien_immo['credit']['taux_interet'],
                         bien_immo['credit']['taux_assurance'],
                         bien_immo['credit']['mode'],
                         bien_immo['credit']['frais_dossier'],
                         bien_immo['credit']['frais_garantie']
                        )
    return credit


def calcul_cashflow(bien_immo, credit):

    bien_immo['cashflow_mensuel'] = \
        calcul.cashflow_mensuel(bien_immo['loyers_mensuel_total'],
                                credit.get_mensualite_avec_assurance(),
                                bien_immo['charges_annuel_total'])

    bien_immo['cashflow_annuel'] = bien_immo['cashflow_mensuel'] * 12


def calcul_impots_micro_foncier(bien_immo):

    bien_immo['impots']['micro_foncier']['base_impossable'] = \
        bien_immo['loyers_annuel_total'] * (1 - bien_immo['impots']['micro_foncier']['taux'])

    base = bien_immo['impots']['micro_foncier']['base_impossable']

    bien_immo['impots']['micro_foncier']['impots_revenu'] = base * bien_immo['impots']['tmi']
    bien_immo['impots']['micro_foncier']['prelevement_sociaux'] = base * bien_immo['impots']['ps']
    bien_immo['impots']['micro_foncier']['total'] = \
        bien_immo['impots']['micro_foncier']['impots_revenu'] + bien_immo['impots']['micro_foncier']['prelevement_sociaux']


def calcul_impots_regime_reel(bien_immo, credit):
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
    base = bien_immo['loyers_annuel_total']
    base -= bien_immo['taxe_fonciere']
    base -= bien_immo['assurance_pno_annuel_total']
#     base -= bien_immo['credit']['cout_interet'] / bien_immo['credit']['duree_annee']
    # TODO soustraire cout des interets annuels
#     base -= bien_immo['credit']['mensualite_assurance'] * 12
    # TODO soustraire cout d'assurance emprunteur annuel

    bien_immo['impots']['regime_reel'] = dict()
    bien_immo['impots']['regime_reel']['base_impossable'] = base

    bien_immo['impots']['regime_reel']['impots_revenu'] = base * bien_immo['impots']['tmi']
    bien_immo['impots']['regime_reel']['prelevement_sociaux'] = base * bien_immo['impots']['ps']
    bien_immo['impots']['regime_reel']['total'] = \
        bien_immo['impots']['regime_reel']['impots_revenu'] + bien_immo['impots']['regime_reel']['prelevement_sociaux']

#     interets = calcul.interet_emprunt(bien_immo['credit']['capital_emprunt'],
#                                       bien_immo['credit']['duree_annee'] * 12,
#                                       bien_immo['credit']['taux_interet'],
#                                       bien_immo['credit']['mensualite_hors_assurance'])
#     interet_annee_1 = 0
#     for i in range(1, 12):
#         interet_annee_1 += interets[i]
#     print(interet_annee_1)


def print_report(bien_immo, credit):
    from tabulate import tabulate

    achat = [
        ['Prix net\nvendeur', 'Travaux', 'Apport', 'Notaire', 'Agence', 'Invest\ninitial', 'Prix\ne/m²'],
        [bien_immo['prix_net_vendeur'], bien_immo['travaux_budget'], bien_immo['apport'],
        '{:.0f}\n({:.2f}%)'.format(bien_immo['notaire']['honoraire_montant'], bien_immo['notaire']['honoraire_taux'] * 100),
        '{:.0f}\n({:.2f}%)'.format(bien_immo['agence_immo']['honoraire_montant'], bien_immo['agence_immo']['honoraire_taux'] * 100),
        bien_immo['invest_initial'],
        bien_immo['surface_prix']
        ],
    ]

    location = [
        ['Loyer\nannuel', 'Loyer\nmensuel', 'Charges\nannuel'],
        [bien_immo['loyers_annuel_total'],
         bien_immo['loyers_mensuel_total'],
         bien_immo['charges_annuel_total']],
    ]

    charges = [
        ['Taxe\nFonciere', 'Travaux\nProvision', 'Vacance\nLocative', 'PNO', 'Gestion\nagence', 'Copropriete'],
        [bien_immo['taxe_fonciere'],
         bien_immo['travaux_provision_annuel_total'],
         bien_immo['vacance_locative_annuel_total'],
         bien_immo['assurance_pno_annuel_total'],
         bien_immo['gestion_agence_annuel_total'],
         bien_immo['copropriete_annuel_total'],
         ]
    ]

    credit_in = [
        ['Capital\nemprunté', 'Durée', 'Taux\ninteret', 'Taux\nassurance', 'Mode'],
        [bien_immo['credit']['capital_emprunt'], '{} ans'.format(bien_immo['credit']['duree_annee']),
         '{:.2f}%'.format(bien_immo['credit']['taux_interet'] * 100),
         '{:.2f}%'.format(bien_immo['credit']['taux_assurance'] * 100),
         bien_immo['credit']['mode']],
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
        ['{:.2f}%'.format(bien_immo['r_brut'] * 100),
        '{:.2f}%'.format(bien_immo['r_net'] * 100),
        '{:.2f}%'.format(bien_immo['r_larcher'] * 100),
        '{:.2f}'.format(bien_immo['cashflow_mensuel']),
        '{:.2f}'.format(bien_immo['cashflow_annuel'])
        ]
    ]

    micro_foncier = [
        ['Micro\nFoncier', 'Base\nimpossable', 'IR', 'PS', 'Total'],
        ['-',
         bien_immo['impots']['micro_foncier']['base_impossable'],
         bien_immo['impots']['micro_foncier']['impots_revenu'],
         bien_immo['impots']['micro_foncier']['prelevement_sociaux'],
         bien_immo['impots']['micro_foncier']['total'],
         ]
    ]

    regime_reel = [
        ['Regime\nreel', 'Base\nimpossable', 'IR', 'PS', 'Total'],
        ['-',
         bien_immo['impots']['regime_reel']['base_impossable'],
         bien_immo['impots']['regime_reel']['impots_revenu'],
         bien_immo['impots']['regime_reel']['prelevement_sociaux'],
         bien_immo['impots']['regime_reel']['total'],
         ]
    ]

    print(tabulate(achat, headers="firstrow") + '\n')
    print(tabulate(location, headers="firstrow") + '\n')
    print(tabulate(charges, headers="firstrow") + '\n')
    print(tabulate(credit_in, headers="firstrow") + '\n')
    print(tabulate(credit_out, headers="firstrow") + '\n')
    print(tabulate(bilan, headers="firstrow") + '\n')
    print(tabulate(micro_foncier, headers="firstrow") + '\n')
    print(tabulate(regime_reel, headers="firstrow") + '\n')


if __name__ == '__main__':
    main(sys.argv[1:])
