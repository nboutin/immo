#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@date: 2021-04
@author: nboutin
'''
from ..variable import Variable
from ..period import ETERNITY
from .entities import Lot


class lot_type(Variable):
    value_type = str
    entity = Lot
    period = ETERNITY
    label = 'Catégorisation du lot suivant son nombre de pièce à vivre'
