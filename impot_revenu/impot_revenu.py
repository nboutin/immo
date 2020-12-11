#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
from tabulate import tabulate
import calcul_impots

__NAME = 'Impots'
__VERSION = '0.1.0-dev'
__IMPOTS_FILENAME = 'res/impots_data.json'


def main(argv):

    inputfile = __IMPOTS_FILENAME
    with open(inputfile, 'r') as file:
        impots = json.load(file)

    calcul_revenu_imposable(impots)
    calcul_quotient_familial(impots)
    calcul_impots_brut(impots)
    calcul_impots_net(impots)

    print_report(impots)


def calcul_revenu_imposable(impots):

    deduction = sum(impots['salaires']) * impots['deduction']
    impots['revenu_imposable'] = sum(impots['salaires']) - deduction


def calcul_quotient_familial(impots):

    impots['quotient_familial_parent'] = impots['revenu_imposable'] / impots['n_parts_fiscales']
    impots['quotient_familial'] = impots['revenu_imposable'] / (impots['n_parts_fiscales'] + impots['n_demi_parts_fiscales'] / 2)


def calcul_impots_brut(impots):

    impots['impots_brut_parent'] = calcul_impots.impots_brut(impots['TMI'][impots['annee']],
                                                             impots['quotient_familial_parent'])
    impots['impots_brut_parent'] *= impots['n_parts_fiscales']

    impots['impots_brut'] = calcul_impots.impots_brut(impots['TMI'][impots['annee']],
                                                      impots['quotient_familial'])
    impots['impots_brut'] *= (impots['n_parts_fiscales'] + impots['n_demi_parts_fiscales'] / 2)


def calcul_impots_net(impots):

    impots['impots_net'] = impots['impots_brut'] 
    impots['impots_net'] -= 0.66 * impots['dons']
    impots['impots_net'] -= 0.66 * impots['syndicat']


def print_report(impots):

    input = [
        ['Salaire 1', 'Salaire 2', 'Revenu\nimposable', 'Impot\nBrut', 'Impot\nnet'],
        [impots['salaires'][0], impots['salaires'][1], impots['revenu_imposable'], impots['impots_brut'], impots['impots_net']]
    ]

    print(tabulate(input, headers="firstrow") + '\n')


if __name__ == '__main__':
    main(sys.argv[1:])

