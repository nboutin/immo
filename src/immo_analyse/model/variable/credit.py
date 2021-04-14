#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@date: 2021-04
@author: nboutin
'''
# path must be absolute
from immo_analyse.core.variable import Variable
from immo_analyse.core.periods import ETERNITY, YEAR, MONTH
from immo_analyse.model.entities import Credit


class duree(Variable):
    value_type = int
    entity = Credit
    period = MONTH
    label = 'Duree du credit en mois'
    # value_accepted = ['T1', 'T2', 'T3', 'Commercial', 'Commun']


class taux_interet(Variable):
    value_type = float
    entity = Credit
    period = MONTH
    label = "Taux d'interet"


class taux_assurance(Variable):
    value_type = float
    entity = Credit
    period = MONTH
    label = "Taux d'assurance"


class frais_dossier(Variable):
    value_type = int
    entity = Credit
    period = MONTH
    label = "Frais de dossier pour le credit"


class frais_garantie(Variable):
    value_type = int
    entity = Credit
    period = MONTH
    label = "Frais de garantie pour le credit"


class amortissement(Variable):
    value_type = float
    entity = Credit
    period = MONTH
    label = ""


class interet(Variable):
    value_type = float
    entity = Credit
    period = MONTH
    label = ""


class mensualite_ha(Variable):
    value_type = float
    entity = Credit
    period = MONTH
    label = "Mensualite hors assurance"


class mensualite_assurance(Variable):
    value_type = float
    entity = Credit
    period = MONTH
    label = "mensualite assurance seul"


class mensualite_aa(Variable):
    value_type = float
    entity = Credit
    period = MONTH
    label = "Mensualite avec assurance"


class capital_restant(Variable):
    value_type = float
    entity = Credit
    period = MONTH
    label = "Capital restant a rembourser"
