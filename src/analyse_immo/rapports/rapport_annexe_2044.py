#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from tabulate import tabulate

from analyse_immo.bien_immo.charge import Charge
from analyse_immo.impots.ligne_definition import *


def rapport_annexe_2044(annee_achat, irpp_2044_projection, bien_immo):

    rapport = list()
    separator = ''

    for i, irpp in enumerate(irpp_2044_projection):

        i_year = i + 1

        annexe_2044 = irpp.annexe_2044
        if not annexe_2044:
            continue

        rapport_annee = [
            annee_achat + i,
            '{:.0f}'.format(bien_immo.loyer_nu_brut_annuel(i_year)),
            '{:.0f}'.format(bien_immo.get_charge(Charge.charge_e.vacance_locative, i_year)),
            '{:.0f}'.format(annexe_2044.sum_ligne(L211_loyer_brut)),
            '{:.0f}'.format(annexe_2044.sum_ligne(CaseE_total_recettes)),
            separator,
            '{:.0f}'.format(annexe_2044.sum_ligne(L221_frais_administration)),
            '{:.0f}'.format(annexe_2044.sum_ligne(L222_autre_frais_gestion)),
            '{:.0f}'.format(annexe_2044.sum_ligne(L223_prime_assurance)),
            '{:.0f}'.format(annexe_2044.sum_ligne(L224_total_travaux)),
            '{:.0f}'.format(annexe_2044.sum_ligne(L227_taxe_fonciere)),
            '{:.0f}'.format(annexe_2044.sum_ligne(L229_copropriete_provision)),
            '{:.0f}'.format(annexe_2044.sum_ligne(L230_regularisation_des_provisions)),
            '{:.0f}'.format(annexe_2044.sum_ligne(CaseF_total_frais_charges)),
            separator,
            '{:.0f}'.format(annexe_2044.sum_ligne(L250_interet_emprunt)),
            '{:.0f}'.format(annexe_2044.sum_ligne(L250_assurance_emprunteur)),
            '{:.0f}'.format(annexe_2044.sum_ligne(L250_frais_dossier)),
            '{:.0f}'.format(annexe_2044.sum_ligne(L250_frais_garantie)),
            '{:.0f}'.format(annexe_2044.sum_ligne(L250_total_emprunt)),
            separator,
            '{:.1f}'.format(annexe_2044.total_charges_taux * 100),
            '{:.0f}'.format(annexe_2044.sum_ligne(L420_resultat_foncier)),
            '{:.0f}'.format(annexe_2044.prelevement_sociaux),
            '{:.0f}'.format(irpp.impots_revenu_foncier),
        ]

        rapport.insert(0, rapport_annee)

    rapport.append([
        'Année',
        'Loyer nu brut annuel',
        'Vacance locative',
        'Loyer nu net annuel',
        'Total recettes',
        separator,
        'Frais administration',
        'Autres frais gestion',
        'Prime assurance',
        'Travaux',
        'Taxe fonciere',
        'Copropriete provision',
        'Copropriete regularisation',
        'Total frais et charges',
        separator,
        'Interet emprunt',
        'Assurance emprunteur',
        'Frais de dossier',
        'Frais de garantie',
        'Total charge emprunt',
        separator,
        'Total charges (%)',
        'Revenu foncier taxable',
        'Prelevement sociaux',
        'Impot revenu foncier',
    ])

    rotate = list(zip(*rapport[::-1]))
    logging.info('# Location nu régime réel 2044')
    logging.info(tabulate(rotate, headers="firstrow") + '\n')
