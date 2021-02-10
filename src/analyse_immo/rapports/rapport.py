#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from tabulate import tabulate

from .rapport_annexe_2044 import rapport_annexe_2044
from .rapport_micro_foncier import rapport_micro_foncier
from .rapport_irpp import rapport_irpp


def generate_rapport(bien_immo, credit, annee_achat, irpp_2044_list, irpp_micro_foncier_list, rendement):

    annee_achat -= 2000

    rapport_achat(bien_immo)
    rapport_location(bien_immo)
    rapport_credit(credit)
    rapport_annexe_2044(annee_achat, irpp_2044_list, bien_immo)
    rapport_micro_foncier(annee_achat, irpp_micro_foncier_list, bien_immo)
    rapport_irpp(annee_achat, irpp_2044_list, irpp_micro_foncier_list)
    rapport_rendement(rendement)
    rapport_overview(bien_immo, credit, irpp_2044_list[0])


def rapport_overview(bien_immo, credit, irpp):
    rapport = [['{:.0f}'.format(bien_immo.financement_total),
                bien_immo.loyer_nu_brut_annuel,
                '{:.0f}/{:.0f}'.format(bien_immo.charges,
                                       bien_immo.provisions),
                '{:.0f}ans/{:.2f}%'.format(credit.duree_mois / 12, credit.taux * 100),
                '{:.0f}'.format(irpp.impots_revenu_foncier),
                None
                ],
               ['Financement Total',
                'Loyer nu brut annuel',
                'Charges/Provision',
                'Credit durée/Taux',
                'Impot foncier',
                'Différentiel annuel net-net']]
    rotate = list(zip(*rapport[::-1]))
    logging.info('# Overview')
    logging.info(tabulate(rotate) + '\n')


def rapport_achat(bien_immo):

    rapport = [
        [bien_immo.prix_net_vendeur,
         '{:.0f} ({:.2f}%)'.format(bien_immo.notaire_montant, bien_immo.notaire_taux * 100),
         '{:.0f} ({:.2f}%)'.format(bien_immo.agence_montant, bien_immo.agence_taux * 100),
         '{:.0f}'.format(bien_immo.budget_travaux),
         '{:.0f}'.format(bien_immo.apport),
         '{:.0f}'.format(bien_immo.financement_total),
         '{:.0f}'.format(bien_immo.rapport_surface_prix)
         ],
        ['Prix net vendeur', 'Notaire', 'Agence', 'Travaux', 'Apport', 'Financement total', 'Prix €/m²'],
    ]
    rotate = list(zip(*rapport[::-1]))
    logging.info('# Achat')
    logging.info(tabulate(rotate) + '\n')


def rapport_location(bien_immo):

    rapport = [
        ['{:.0f}/{:.0f}'.format(bien_immo.loyer_nu_brut_mensuel, bien_immo.loyer_nu_brut_annuel),
         '{:.0f}/{:.0f}'.format(bien_immo.loyer_nu_net_mensuel, bien_immo.loyer_nu_net_annuel),
         '{:.0f}'.format(bien_immo.charges),
         '{:.0f}'.format(bien_immo.provisions)],
        ['Loyer brut mensuel/annuel', 'Loyer net mensuel/annuel', 'Charges', 'Provisions'],
    ]
    rotate = list(zip(*rapport[::-1]))
    logging.info('# Location')
    logging.info(tabulate(rotate) + '\n')


def rapport_credit(credit):

    rapport = [
        [
            '{:.0f}'.format(credit.capital),
            '{} mois ({:.0f} ans)'.format(credit.duree_mois, credit.duree_mois / 12),
            '{:.2f}%'.format(credit.taux * 100),
            '{:.2f}%'.format(credit.taux_assurance * 100),
            credit.mode],
        ['Capital emprunté', 'Durée', 'Taux interet', 'Taux assurance', 'Mode'],
    ]
    rotate = list(zip(*rapport[::-1]))
    logging.info('# Credit')
    logging.info(tabulate(rotate) + '\n')

    rapport = [
        [
            '{:.2f}'.format(credit.get_mensualite_hors_assurance()),
            '{:.2f}'.format(credit.get_mensualite_assurance()),
            '{:.2f}'.format(credit.get_mensualite_avec_assurance()),
            '{:.2f}'.format(credit.get_montant_interet_total()),
            '{:.2f}'.format(credit.get_montant_assurance_total()),
            '{:.2f}'.format(credit.get_cout_total())],
        ['Mensualite hors assurance', 'Mensualite assurance', 'Mensualite avec assurance', 'Cout interet',
         'Cout assurance', 'Cout credit'],
    ]
    rotate = list(zip(*rapport[::-1]))
    logging.info(tabulate(rotate) + '\n')


def rapport_rendement(rendement):
    rapport = [['{:.2f}'.format(rendement.rendement_brut * 100),
                '{:.2f}'.format(rendement.rendement_net * 100),
                '{:.2f}'.format(rendement.rendement_methode_larcher * 100),
                '{:.2f}'.format(rendement.cashflow_net_mensuel),
                '{:.2f}'.format(rendement.cashflow_net_annuel)],
               ['Rendement Brut (%)',
                'Rendement Net (%)',
                'Rendement Larcher (%)',
                'Différentiel Mensuel Net (€)',
                'Différentiel Annuel Net (€)'],
               ]
    rotate = list(zip(*rapport[::-1]))
    logging.info('# Rendement')
    logging.info(tabulate(rotate) + '\n')
