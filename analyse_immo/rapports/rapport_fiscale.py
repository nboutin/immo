#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from tabulate import tabulate


def print_rapport_fiscale(annee_start, annexe_2044):
    '''
    annee
    loyer (appliquer vacance locative)
    travaux
    interet
    Autre deduction
    Revenu foncier impossable
    Impot sur le revenu
    Prelevement Sociaux
    Fiscalite totale
    '''
    rapport = [['1',
                annexe_2044.total_recettes,
                0,
                '{:.0f}'.format(annexe_2044.total_charges_emprunt),
                '{:.0f}'.format(annexe_2044.total_frais_et_charges),
                '{:.0f}'.format(annexe_2044.revenu_foncier_taxable)],
               ['Année',
                'Loyer nu',
                'Travaux',
                'Emprunt deductible',
                'Charges deductible',
                'Revenu foncier'],
               ]

    rotate = list(zip(*rapport[::-1]))
    logging.info(tabulate(rotate, headers="firstrow") + '\n')
