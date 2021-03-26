#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from tabulate import tabulate

from analyse_immo.rapports.rapport_annexe_2044 import rapport_annexe_2044
# from analyse_immo.rapports.rapport_micro_foncier import rapport_micro_foncier
from analyse_immo.rapports.rapport_irpp import rapport_irpp


def rapport(analyse):
    rapport_achat(analyse.bien_immo)
    rapport_bien_immo(analyse.bien_immo)
    rapport_location(analyse.projection_duree, analyse.bien_immo, analyse.annee_achat)
    rapport_credit(analyse.projection_duree, analyse.credit, analyse.annee_achat)
    rapport_annexe_2044(analyse.annee_achat, analyse.irpp_2044_projection, analyse.bien_immo)
    # rapport_micro_foncier(analyse.annee_achat, analyse.irpp_micro_foncier_projection, analyse.bien_immo)
    rapport_irpp(
        analyse.annee_achat,
        analyse.defaut.salaire_taux,
        analyse.irpp_2044_projection,
        analyse.irpp_micro_foncier_projection)
    rapport_rendement(analyse.annee_achat, analyse.projection_duree, analyse.rendement)
    rapport_overview(
        analyse.annee_achat,
        analyse.projection_duree,
        analyse.bien_immo,
        analyse.credit,
        analyse.irpp_2044_projection,
        analyse.rendement)


def rapport_achat(bien_immo):

    rapport = [['{}'.format(bien_immo.prix_net_vendeur),
                '{:.0f} ({:.2f}%)'.format(bien_immo.notaire_montant,
                                          bien_immo.notaire_taux * 100),
                '{:.0f} ({:.2f}%)'.format(bien_immo.agence_montant,
                                          bien_immo.agence_taux * 100),
                '{:.0f}'.format(bien_immo.travaux_montant),
                '{:.0f}'.format(bien_immo.subvention_montant),
                '{:.0f}'.format(bien_immo.apport),
                '{:.0f}'.format(bien_immo.financement_total),
                '{:.0f}/{:.0f}'.format(bien_immo.rapport_surface_prix_louable,
                                       bien_immo.rapport_surface_prix_final),
                ],
               ['Prix net vendeur',
                'Notaire',
                'Agence',
                'Travaux',
                'Subvention',
                'Apport',
                'Financement total',
                'Prix €/m² (louable/final)',
                ],
               ]
    rotate = list(zip(*rapport[::-1]))
    logging.info('# Achat')
    logging.info(tabulate(rotate) + '\n')


def rapport_bien_immo(bien_immo):

    rapport = list()

    for lot in bien_immo.lots:
        rapport.insert(0,
                       [lot.type,
                        lot.etat,
                        lot.surface,
                        0,
                        lot.loyer_nu_brut_mensuel(),
                        0,
                        0,
                        0
                        ])

    rapport.append([
        'Type',
        'Etat',
        'Surface',
        'Niveau',
        'Loyer hc',
        'charges',
        'evolution',
        'locataire'
    ])
    rotate = list(zip(*rapport[::-1]))
    logging.info('# Bien Immo')
    logging.info(tabulate(rotate) + '\n')


def rapport_location(duree, bien_immo, annee_achat):

    separator = ''
    rapport = list()

    for i in range(duree):
        i_year = i + 1
        i_month = i_year * 12
        rapport_annee = [
            annee_achat + i,
            '{:.0f}'.format(bien_immo.loyer_nu_brut_mensuel(i_month)),
            '{:.0f}'.format(bien_immo.loyer_nu_brut_annuel(i_year)),
            '{:.1f}%'.format(bien_immo.irl_taux_annuel * 100),
            '{:.1f}%'.format(bien_immo.vacance_locative_taux_annuel * 100),
            '{:.0f}'.format(bien_immo.loyer_nu_net_mensuel(i_month)),
            '{:.0f}'.format(bien_immo.loyer_nu_net_annuel(i_year)),
            separator,
            '{:.0f}'.format(bien_immo.charges(i_year)),
            '{:.0f}'.format(bien_immo.provisions(i_year)),
        ]
        rapport.insert(0, rapport_annee)

    rapport.append(['Annee',
                    'Loyer brut mensuel',
                    'Loyer brut annuel',
                    'Taux IRL',
                    'Taux vacance locative',
                    'Loyer net mensuel',
                    'Loyer net annuel',
                    separator,
                    'Charges',
                    'Provisions',
                    ])
    rotate = list(zip(*rapport[::-1]))
    logging.info('# Location')
    logging.info(tabulate(rotate) + '\n')


def rapport_credit(duree, credit, annee_achat):

    # Input
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

    # Cout
    rapport = [
        [
            '{:.2f}'.format(credit.get_montant_interet_total()),
            '{:.2f}'.format(credit.get_montant_assurance_total()),
            '{:.2f}'.format(credit.get_cout_total())
        ],
        [
            'Cout interet',
            'Cout assurance',
            'Cout credit'
        ]
    ]
    rotate = list(zip(*rapport[::-1]))
    logging.info('# Credit cout')
    logging.info(tabulate(rotate) + '\n')

    # Tableau amortissement
    rapport = list()
    for i in range(duree):
        year = i + 1
        b_month = i * 12 + 1
        e_month = year * 12
        rapport_year = [
            '{}'.format(annee_achat + i),
            '{:.2f}'.format(credit.get_amortissement(b_month, e_month)),
            '{:.2f}'.format(credit.get_interet(b_month, e_month)),
            '{:.2f}'.format(credit.get_mensualite_hors_assurance(b_month, e_month)),
            '{:.2f}'.format(credit.get_mensualite_assurance(b_month, e_month)),
            '{:.2f}'.format(credit.get_mensualite_avec_assurance(b_month, e_month)),
            '{:.2f}'.format(credit.get_capital_restant(e_month))
        ]
        rapport.insert(0, rapport_year)

    rapport.append(['Annee',
                    'Amortissement',
                    'Interet',
                    'Mensualite hors assurance',
                    'Mensualite assurance',
                    'Mensualite avec assurance',
                    'Capital restant'
                    ])

    rotate = list(zip(*rapport[::-1]))
    logging.info(tabulate(rotate) + '\n')


def rapport_rendement(annee_achat, projection_duree, rendement):

    rapport = list()

    for i in range(projection_duree):

        i_year = i + 1

        rapport_year = [
            annee_achat + i,
            '{:.2f}'.format(rendement.rendement_brut * 100),
            '{:.2f}'.format(rendement.rendement_net(i_year) * 100),
            '{:.2f}'.format(rendement.rendement_methode_larcher * 100),
            '{:.2f}'.format(rendement.cashflow_net_mensuel(i_year)),
            '{:.2f}'.format(rendement.cashflow_net_annuel(i_year)),
            '{:.2f}'.format(rendement.cashflow_net_net_annuel(i_year)),
        ]
        rapport.insert(0, rapport_year)

    rapport.append([
        'Annee',
        'Rendement Brut (%)',
        'Rendement Net (%)',
        'Rendement Larcher (%)',
        'Différentiel Net mensuel(€)',
        'Différentiel Net annuel(€)',
        'Différentiel Net d"impots annuel(€)'])

    rotate = list(zip(*rapport[::-1]))
    logging.info('# Rendement')
    logging.info(tabulate(rotate) + '\n')


def rapport_overview(annee_achat, projection_duree, bien_immo, credit, irpp, rendement):

    rapport = list()

    for i in range(projection_duree):

        i_year = i + 1

        rapport_year = [
            annee_achat + i,
            '{:.0f}'.format(bien_immo.financement_total),
            '{:.0f}'.format(bien_immo.loyer_nu_brut_annuel(i_year)),
            '{:.0f}/{:.0f}'.format(bien_immo.charges(i_year), bien_immo.provisions(i_year)),
            '{:.0f}ans/{:.2f}%'.format(credit.duree_mois / 12, credit.taux * 100),
            '{:.0f}'.format(irpp[i].impots_revenu_foncier),
            '{:.2f}'.format(rendement.cashflow_net_net_annuel(i_year))
        ]
        rapport.insert(0, rapport_year)

    rapport.append([
        'Annee',
        'Financement Total',
        'Loyer nu brut annuel',
        'Charges/Provision',
        'Credit durée/Taux',
        'Impot foncier',
        'Différentiel net-net annuel'])

    rotate = list(zip(*rapport[::-1]))
    logging.info('# Overview')
    logging.info(tabulate(rotate) + '\n')
