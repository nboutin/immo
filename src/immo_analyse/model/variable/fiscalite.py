#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@date: 2021-04
@author: nboutin
'''
# path must be absolute
from immo_analyse.core.variable import Variable
from immo_analyse.core.periods import ETERNITY, YEAR, MONTH
from immo_analyse.model.entities import Fiscalite


class regime(Variable):
    value_type = str
    entity = Fiscalite
    period = MONTH
    label = 'Duree du credit en mois'
    value_accepted = ['location_vide_reel', 'sci_is']
