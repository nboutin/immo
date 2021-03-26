#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@author: nboutin
'''
import math


def taux_periodique(taux_period, n_periode):
    '''
    # Taux proportionnel (credit immo et pro)
    taux_periodique = taux_period / n_periode
    '''
    return taux_period / n_periode


def taux_actuariel(taux_period, n_periode):
    '''
    # Taux actuariel (credit conso)
    taux_periodique = (1 + taux_period)^(1/n_periode)-1
    exemple remboursement mensuel: taux periodique = (1 + taux)^(1/12)-1
    '''
    return math.pow((1 + taux_period), 1 / n_periode) - 1


def capital_compose(capital, taux_periodique, n_periode):
    '''
    @return: capital cumul = capital * (1 + taux_periodique)^(n_periode)
    '''
    return capital * math.pow((1 + taux_periodique), n_periode)
