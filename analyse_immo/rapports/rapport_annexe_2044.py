#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from tabulate import tabulate

from impots.annexe_2044 import L211_loyer_brut, L221_frais_administration, L222_autre_frais_gestion, \
    L223_prime_assurance, L224_travaux, L227_taxe_fonciere, L229_copropriete_provision, L230_copropriete_regularisation, L250_interet_emprunt,\
    L250_assurance_emprunteur, L250_frais_dossier, L250_frais_garantie


def rapport_annexe_2044(annee_start, annexe_2044_list):

    rapport = list()
    separator = ''

    for i, annexe_2044 in enumerate(annexe_2044_list):
        rapport_annee = [
            annee_start + i,
            '{:.0f}'.format(annexe_2044.get_ligne(L211_loyer_brut)),
            '-',
            '-',
            '{:.0f}'.format(annexe_2044.total_recettes),
            separator,
            '{:.0f}'.format(annexe_2044.get_ligne(L221_frais_administration)),
            '{:.0f}'.format(annexe_2044.get_ligne(L222_autre_frais_gestion)),
            '{:.0f}'.format(annexe_2044.get_ligne(L223_prime_assurance)),
            '{:.0f}'.format(annexe_2044.get_ligne(L224_travaux)),
            '{:.0f}'.format(annexe_2044.get_ligne(L227_taxe_fonciere)),
            '{:.0f}'.format(annexe_2044.get_ligne(L229_copropriete_provision)),
            '{:.0f}'.format(annexe_2044.get_ligne(L230_copropriete_regularisation)),
            '{:.0f}'.format(annexe_2044.total_frais_et_charges),
            separator,
            '{:.0f}'.format(annexe_2044.get_ligne(L250_interet_emprunt)),
            '{:.0f}'.format(annexe_2044.get_ligne(L250_assurance_emprunteur)),
            '{:.0f}'.format(annexe_2044.get_ligne(L250_frais_dossier)),
            '{:.0f}'.format(annexe_2044.get_ligne(L250_frais_garantie)),
            '{:.0f}'.format(annexe_2044.total_charges_emprunt),
            separator,
            '{:.0f}'.format(annexe_2044.revenu_foncier_taxable)
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
        'Revenu foncier taxable',
    ])

    rotate = list(zip(*rapport[::-1]))
    logging.info('# Location nu régime réel 2044')
    logging.info(tabulate(rotate, headers="firstrow") + '\n')
