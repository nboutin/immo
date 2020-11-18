#!/usr/bin/env python3
# -*- coding: utf-8 -*-


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
