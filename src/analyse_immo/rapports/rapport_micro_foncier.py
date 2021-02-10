#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from tabulate import tabulate

from analyse_immo.bien_immo.charge import Charge
from analyse_immo.impots.micro_foncier import L4EB_recettes_brutes


def rapport_micro_foncier(annee_achat, irpp_micro_foncier_list, bien_immo):

    rapport = list()
    separator = ''

    for i, irpp in enumerate(irpp_micro_foncier_list):
        micro_foncier = irpp.micro_foncier

        if not micro_foncier:
            continue

        rapport_annee = [
            annee_achat + i,
            '{:.0f}'.format(bien_immo.loyer_nu_brut_annuel),
            '{:.0f}'.format(bien_immo.get_charge(Charge.charge_e.vacance_locative)),
            '{:.0f}'.format(micro_foncier.get_ligne(L4EB_recettes_brutes)),
            separator,
            '{:.0f}'.format(micro_foncier.revenu_foncier_taxable),
            '{:.0f}'.format(micro_foncier.prelevement_sociaux),
            '{:.0f}'.format(irpp.impots_revenu_foncier),
        ]

        rapport.insert(0, rapport_annee)

    rapport.append([
        'Année',
        'Loyer nu brut annuel',
        'Vacance locative',
        'Total recettes',
        separator,
        'Revenu foncier taxable',
        'Prelevement sociaux',
        'Impot revenu foncier',
    ])

    rotate = list(zip(*rapport[::-1]))
    logging.info('# Micro Foncier')
    logging.info(tabulate(rotate, headers="firstrow") + '\n')
