#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@date: 2021-03
@author: nboutin
'''
from .immo_system import ImmoSystem


class Simulation:

    def __init__(self, immosys: ImmoSystem):
        self._immosys = immosys

    def get(self, entity: str, period: str, variable: str):
        e = self._immosys.get_entity(entity)

    def compute(self, variable: str, period: str):
        var = self.immosys.get_variable(variable)
        
        self._run_formula()
        
    def _run_formula(self):
        