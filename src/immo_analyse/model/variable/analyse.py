#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@date: 2021-04
@author: nboutin
'''
# path must be absolute
from immo_analyse.core.variable import Variable
from immo_analyse.core.periods import ETERNITY, MONTH, YEAR
from immo_analyse.model.entities import Analyse


class rdt_brut(Variable):
    value_type = float
    entity = Analyse
    period = MONTH
    label = ''

    def formula(population, period, parameter):
        '''
        r_brut = loyer_nu_brut_annuel / financement total
        '''
        loyer = population('loyer_nu', period, entity_key='bien_immo')
        financement = population('financement', period)
        return loyer / financement
