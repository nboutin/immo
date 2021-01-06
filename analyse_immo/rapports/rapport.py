#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tabulate import tabulate


def rapport_achat(bien_immo):

    rapport = [
        ['Prix net\nvendeur', 'Notaire', 'Agence', 'Travaux', 'Apport', 'Financement\ntotal', 'Prix\ne/m²'],
        [bien_immo.prix_net_vendeur,
         '{:.0f}\n({:.2f}%)'.format(bien_immo.notaire_montant, bien_immo.notaire_taux * 100),
         '{:.0f}\n({:.2f}%)'.format(bien_immo.agence_montant, bien_immo.agence_taux * 100),
         bien_immo.budget_travaux,
         bien_immo.apport,
         bien_immo.financement_total,
         bien_immo.rapport_surface_prix
         ],
    ]
    print(tabulate(rapport, headers="firstrow") + '\n')


def rapport_location(bien_immo):

    rapport = [
        ['Loyer brut\nmensuel/annuel', 'Loyer net\nmensuel/annuel', 'Charges', 'Provisions'],
        ['{:.0f}/{:.0f}'.format(bien_immo.loyer_nu_brut_mensuel, bien_immo.loyer_nu_brut_annuel),
         '{:.0f}/{:.0f}'.format(bien_immo.loyer_nu_net_mensuel, bien_immo.loyer_nu_net_annuel),
         bien_immo.charges,
         bien_immo.provisions],
    ]
    print(tabulate(rapport, headers="firstrow") + '\n')


def rapport_credit(credit):

    credit_in = [
        ['Capital\nemprunté', 'Durée', 'Taux\ninteret', 'Taux\nassurance', 'Mode'],
        [credit.capital,
         '{}({:.0f})'.format(credit.duree_mois, credit.duree_mois / 12),
         '{:.2f}%'.format(credit.taux * 100),
         '{:.2f}%'.format(credit.taux_assurance * 100),
         credit.mode],
    ]

    credit_out = [
        ['Mensualite\nhors assurance', 'Mensualite\nassurance', 'Mensualite\navec assurance', 'Cout\ninteret',
         'Cout\nassurance', 'Cout\ncredit'],
        ['{:.2f}'.format(credit.get_mensualite_hors_assurance()),
         '{:.2f}'.format(credit.get_mensualite_assurance()),
         '{:.2f}'.format(credit.get_mensualite_avec_assurance()),
         '{:.2f}'.format(credit.get_montant_interet_total()),
         '{:.2f}'.format(credit.get_montant_assurance_total()),
         '{:.2f}'.format(credit.get_cout_total())],
    ]
    print(tabulate(credit_in, headers="firstrow") + '\n')
    print(tabulate(credit_out, headers="firstrow") + '\n')


def rapport_rendement(rendement):
    rdt = [
        ['Rendement\nBrut', 'Rendement\nNet', 'Rendement\nLarcher', 'Cashflow\nMensuel', 'Cashflow\nannuel'],
        ['{:.2f}%'.format(rendement.rendement_brut * 100),
         '{:.2f}%'.format(rendement.rendement_net * 100),
         '{:.2f}%'.format(rendement.rendement_methode_larcher * 100),
         '{:.2f}'.format(rendement.cashflow_mensuel),
         '{:.2f}'.format(rendement.cashflow_annuel)
         ]
    ]
    print(tabulate(rdt, headers="firstrow") + '\n')
