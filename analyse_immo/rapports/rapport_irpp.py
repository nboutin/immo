#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from tabulate import tabulate


def rapport_irpp(annee_start, irpp):

    separator = ''

    rapport = [
        [
            annee_start,
            irpp.salaires,
            '{:.0f}'.format(irpp.revenu_foncier),
            '{:.0f}'.format(irpp.revenu_fiscale_reference),
            separator,
            '{:.0f}'.format(irpp.quotient_familial),
            '{:.0f}'.format(irpp.impots_brut),
            irpp.total_reduction_impot,
            irpp.total_credit_impot,
            '{:.0f}'.format(irpp.impots_net),
            separator,
            '-',
            '-',
        ]
    ]

    rapport.append([
        'Année',
        'Salaires',
        'Revenu foncier',
        'Revenu fiscale reference',
        separator,
        'Quotient familial',
        'Impot brut',
        'Reduction impot',
        'Credit impot',
        'Impot net',
        separator,
        "Impot net (sans foncier)",
        "Delta impot",
    ],)

    rotate = list(zip(*rapport[::-1]))
    logging.info('# IRPP')
    logging.info(tabulate(rotate, headers="firstrow") + '\n')
