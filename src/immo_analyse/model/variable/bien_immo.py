#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@date: 2021-04
@author: nboutin
'''
# path must be absolute
from immo_analyse.core.variable import Variable
from immo_analyse.core.periods import ETERNITY
from immo_analyse.model.entities import Lot, BienImmo


class lot_type(Variable):
    value_type = str
    entity = Lot
    period = ETERNITY
    label = 'Catégorisation du lot suivant son nombre de pièce à vivre'
    value_accepted = ['T1', 'T2', 'T3', 'Commercial', 'Commun']


class surface_carrez(Variable):
    value_type = float
    entity = [Lot, BienImmo]
    period = ETERNITY
    label = 'surface habitable suivant la loi carrez'
