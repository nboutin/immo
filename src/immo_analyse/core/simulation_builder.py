#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@date: 2021-04
@author: nboutin
'''
from .immo_system_core import ImmoSystemCore
from .simulation import Simulation


class SimulationBuilder:

    def __init__(self):
        pass

    def build_from_entities(self, immo_sys: ImmoSystemCore, entities):

        simulation = Simulation(immo_sys, immo_sys.build_population(entities))
