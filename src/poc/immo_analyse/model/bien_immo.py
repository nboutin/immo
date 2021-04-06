#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@date: 2021-04
@author: nboutin
'''
from ..variable import Variable
from .entities import Lot
from ..period import ETERNITY


class type_logement(Variable):
    type = str
    entity = Lot
    period = ETERNITY
