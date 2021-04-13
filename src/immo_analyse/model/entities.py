#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@date: 2021-04
@author: nboutin
'''

from immo_analyse.core.entity import Entity


Lot = Entity(key='lot')
BienImmo = Entity(key='bien_immo', sub_entities=[Lot])
Credit = Entity(key='credit')
Fiscalite = Entity(key='fiscalite')
Analyse = Entity(key='analyse')

entities = [Lot, BienImmo, Credit, Fiscalite, Analyse]
