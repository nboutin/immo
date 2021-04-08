#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@date: 2021-04
@author: nboutin
'''

from immo_analyse.core.entity import Entity


Lot = Entity(key='lot')
BienImmo = Entity(key='bien_immo')
Credit = Entity(key='credit')

entities = [Lot, BienImmo, Credit]
