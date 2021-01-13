#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from tabulate import tabulate


def rapport_irpp(annee_achat, irpp_2044_list):

    separator = ''
    rapport = list()

    for i, irpp in enumerate(irpp_2044_list):
        rapport_annee = [
            annee_achat + i,
            irpp.salaires,
            '{:.0f}'.format(irpp.revenu_foncier),
            '{:.0f}'.format(irpp.revenu_fiscale_reference),
            separator,
            '{:.0f}'.format(irpp.quotient_familial),
            '{:.0f}'.format(irpp.impots_brut),
            #             irpp.total_reduction_impot,
            #             irpp.total_credit_impot,
            '{:.0f}'.format(irpp.impots_net),
            separator,
            '{:.0f}'.format(irpp.impots_salaires_net),
            '{:.0f}'.format(irpp.impots_revenu_foncier_total),
        ]
        rapport.insert(0, rapport_annee)

    rapport.append([
        'Année',
        'Salaires',
        'Revenu foncier',
        'Revenu fiscale reference',
        separator,
        'Quotient familial',
        'Impot brut',
        #         'Reduction impot',
        #         'Credit impot',
        'Impot net',
        separator,
        "Impot salaires net",
        "Impot foncier total",
    ],)

    rotate = list(zip(*rapport[::-1]))
    logging.info('# IRPP')
    logging.info(tabulate(rotate, headers="firstrow") + '\n')
