#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math


def rendement_brut(loyers_annuel_total, invest_initial):

    return loyers_annuel_total / invest_initial


def rendement_methode_larcher(loyers_mensuel_total, invest_initial):
    '''
    La méthode larcher de calcul du rendement permet une approximation rapide 
    du rendement net.
    Les charges sont évaluées à 25% soit 3 mois de loyer
    '''

    return (loyers_mensuel_total * 9) / invest_initial


def rendement_net(loyer_annuel_total, charges_annuel_total, invest_initial):

    return (loyer_annuel_total - charges_annuel_total) / invest_initial


def credit_remboursement_constant(capital_emprunt, duree_annee, taux_interet):
    '''
    mensualite_hors_assurance 
        = ( capital_emprunte * taux_interet/12) /
        1 - (1 + taux_interet / 12) ^ - duree_mois
        
    @return: mensualite hors assurance  
    '''

    if capital_emprunt == 0 or taux_interet == 0:
        return 0

    return (capital_emprunt * taux_interet / 12) / (1 - math.pow(1 + taux_interet / 12, -duree_annee * 12))


def mensualite_assurance(capital_emprunt, taux_assurance):

    return capital_emprunt * taux_assurance / 12


def cout_interet(capital_emprunt, duree_annee, mensualite_hors_assurance):

    return 12 * duree_annee * mensualite_hors_assurance - capital_emprunt


def cout_assurance(mensualite_assurance, duree_annee):

    return mensualite_assurance * duree_annee * 12


def cashflow_mensuel(loyer_mensuel_total, credit_mensualite_total, charges_annuel_total):

    return loyer_mensuel_total - credit_mensualite_total - charges_annuel_total / 12


def interet_emprunt(capital, duree_mois, taux_annuel, mensualite_credit):
    '''
    Un emprunt de 15 000 €, 48 mois, taux de 6% l'an, avec des mensualités de 352,28 €. 
    Intérêts du 1er mois = 15 000 € x (6%/12) = 75 € ; 
    Intérêts du 2e mois = [15 000 € - (352,28 € - 75 €)] x (6%/12) = 73,61 €
    '''

    capital_restant = capital

    interets = []
    interets.append(0)
    interets.append(capital_restant * (taux_annuel / 12))

    capital_restant -= mensualite_credit - interets[1]

    for i in range(2, duree_mois + 1):
         interets.append(capital_restant * (taux_annuel / 12))
         capital_restant -= mensualite_credit - interets[i]

    return interets
