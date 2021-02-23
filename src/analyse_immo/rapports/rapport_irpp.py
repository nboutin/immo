#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from tabulate import tabulate


def rapport_irpp(annee_achat, salaire_taux_annuel, irpp_2044_projection, irpp_mf_projection):

    separator = ''
    rapport = list()

    for i, irpp_2044 in enumerate(irpp_2044_projection):
        rapport_annee = [
            annee_achat + i,
            '{:.0f}'.format(irpp_2044.salaires),
            '{:.2f}%'.format(salaire_taux_annuel * 100),
            '{:.0f}'.format(irpp_2044.revenu_foncier),
            '{:.0f}'.format(irpp_2044.revenu_fiscale_reference),
            separator,
            '{:.0f}'.format(irpp_2044.quotient_familial),
            '{:.0f}'.format(irpp_2044.impots_brut),
            #             irpp_2044.total_reduction_impot,
            #             irpp_2044.total_credit_impot,
            '{:.0f}'.format(irpp_2044.impots_net),
            separator,
            '{:.0f}'.format(irpp_2044.impots_salaires_net),
            '{:.0f}'.format(irpp_2044.impots_revenu_foncier),
            '{:.0f}'.format(irpp_mf_projection[i].impots_revenu_foncier),
        ]
        rapport.insert(0, rapport_annee)

    rapport.append([
        'Année',
        'Salaires',
        'Salaire taux annuel',
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
        "Impot foncier 2044",
        "Impot micro foncier",
    ],)

    rotate = list(zip(*rapport[::-1]))
    logging.info('# IRPP')
    logging.info(tabulate(rotate, headers="firstrow") + '\n')
