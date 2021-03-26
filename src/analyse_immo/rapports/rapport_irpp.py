#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from tabulate import tabulate

from analyse_immo.impots.ligne_definition import *


def rapport_irpp(annee_achat, salaire_taux_annuel, irpp_2044_projection, irpp_mf_projection):

    separator = ''
    rapport = list()

    for i, irpp_2044 in enumerate(irpp_2044_projection):
        rapport_annee = [
            annee_achat + i,
            '{:.0f}'.format(irpp_2044.sum_ligne(L1_1_traitements_salaires_pensions)),
            '{:.2f}%'.format(salaire_taux_annuel * 100),
            '{:.0f}'.format(irpp_2044.sum_ligne(L4_revenus_ou_deficits_nets_fonciers)),
            '{:.0f}'.format(irpp_2044.sum_ligne(L1_5_revenu_brut_global)),
            '{:.0f}'.format(irpp_2044.sum_ligne(LQ_quotient_familial)),
            '{:.0f}'.format(irpp_2044.sum_ligne(L9_impot_du)),
            separator,
            '{:.0f}'.format(irpp_2044.impot_sans_revenu_foncier),
            '{:.0f}'.format(irpp_2044.impots_revenu_foncier),
            '{:.0f}'.format(irpp_2044.sum_ligne(L9PS_prelevement_sociaux)),
        ]
        rapport.insert(0, rapport_annee)

    rapport.append([
        'Année',
        'Salaires',
        'Salaire taux annuel',
        'Revenu foncier',
        'Revenu brut global',
        'Quotient familial',
        'Impot du',
        separator,
        "Impot salaires",
        "Impot foncier 2044",
        "Prelevement sociaux",
    ],)

    rotate = list(zip(*rapport[::-1]))
    logging.info('# IRPP')
    logging.info(tabulate(rotate, headers="firstrow") + '\n')
