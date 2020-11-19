#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import calcul

__DATA_FILENAME = "data.json"


def main():

    with open(__DATA_FILENAME, 'r') as file:
        bien_immo = json.load(file)

    prepare_inputs(bien_immo)

    calcul_rendement_brut(bien_immo)
    calcul_rendement_methode_larcher(bien_immo)
    calcul_rendement_net(bien_immo)
    calcul_credit(bien_immo)
    calcul_cashflow(bien_immo)

    print_repport(bien_immo)


def prepare_inputs(bien_immo):

    bien_immo['loyers_mensuel_total'] = 0
    for lot in bien_immo['lots']:
        bien_immo['loyers_mensuel_total'] += lot['loyer_mensuel']

    bien_immo['loyers_annuel_total'] = bien_immo['loyers_mensuel_total'] * 12

    taux = bien_immo['notaire']['honoraire_taux']
    montant = bien_immo['notaire']['honoraire_montant']
    if taux * bien_immo['prix_achat'] != montant:
        if taux == 0:
            bien_immo['notaire']['honoraire_taux'] = montant / bien_immo['prix_achat']
        elif montant == 0:
            bien_immo['notaire']['honoraire_montant'] = bien_immo['prix_achat'] * taux
        else:
            print('Error: notaire')
            quit()

    taux = bien_immo['agence_immo']['honoraire_taux']
    montant = bien_immo['agence_immo']['honoraire_montant']
    if taux * bien_immo['prix_achat'] != montant:
        if taux == 0:
            bien_immo['agence_immo']['honoraire_taux'] = montant / bien_immo['prix_achat']
        elif montant == 0:
            bien_immo['agence_immo']['honoraire_montant'] = bien_immo['prix_achat'] * taux
        else:
            print('Error: agence_immo')
            quit()

    bien_immo['invest_initial'] = bien_immo['prix_achat'] + bien_immo['notaire']['honoraire_montant'] + bien_immo['agence_immo']['honoraire_montant']

    calcul_charges_annuel(bien_immo)


def calcul_charges_annuel(bien_immo):

    bien_immo['charges_annuel_total'] = bien_immo['taxe_fonciere']

    for lot in bien_immo['lots']:
        loyer = lot['loyer_mensuel']
        bien_immo['charges_annuel_total'] += bien_immo['travaux_provision'] * loyer * 12
        bien_immo['charges_annuel_total'] += lot['vacance_locative'] * loyer * 12
        bien_immo['charges_annuel_total'] += lot['assurance_pno']
        bien_immo['charges_annuel_total'] += lot['gestion_agence'] * loyer * 12
        bien_immo['charges_annuel_total'] += lot['copropriete']


def calcul_rendement_brut(bien_immo):

    bien_immo['r_brut'] = calcul.rendement_brut(bien_immo['loyers_annuel_total'], bien_immo['invest_initial'])


def calcul_rendement_methode_larcher(bien_immo):

    bien_immo['r_larcher'] = calcul.rendement_methode_larcher(bien_immo['loyers_mensuel_total'], bien_immo['invest_initial'])


def calcul_rendement_net(bien_immo):

    bien_immo['r_net'] = calcul.rendement_net(bien_immo['loyers_annuel_total'],
                                              bien_immo['charges_annuel_total'],
                                              bien_immo['invest_initial'])


def calcul_credit(bien_immo):

    bien_immo['credit']['mensualite_hors_assurance'] = \
        calcul.credit_remboursement_constant(bien_immo['credit']['capital_emprunt'],
                                             bien_immo['credit']['duree_annee'],
                                             bien_immo['credit']['taux_interet'])

    bien_immo['credit']['mensualite_assurance'] = \
        calcul.mensualite_assurance(bien_immo['credit']['capital_emprunt'],
                                    bien_immo['credit']['taux_assurance'])

    bien_immo['credit']['mensualite_total'] = \
        bien_immo['credit']['mensualite_hors_assurance'] + bien_immo['credit']['mensualite_assurance']

    bien_immo['credit']['cout_interet'] = \
        calcul.cout_interet(bien_immo['credit']['capital_emprunt'],
                            bien_immo['credit']['duree_annee'],
                            bien_immo['credit']['mensualite_hors_assurance'])

    bien_immo['credit']['cout_assurance'] = \
        calcul.cout_assurance(bien_immo['credit']['mensualite_assurance'],
                              bien_immo['credit']['duree_annee'])

    bien_immo['credit']['cout_credit'] = \
        bien_immo['credit']['cout_interet'] + bien_immo['credit']['cout_assurance'] \
        +bien_immo['credit']['frais_dossier'] + bien_immo['credit']['frais_garantie']


def calcul_cashflow(bien_immo):

    bien_immo['cashflow_mensuel'] = \
        calcul.cashflow_mensuel(bien_immo['loyers_mensuel_total'],
                                bien_immo['credit']['mensualite_total'],
                                bien_immo['charges_annuel_total'])


def print_repport(bien_immo):

    print(bien_immo)


if __name__ == '__main__':
  main()
