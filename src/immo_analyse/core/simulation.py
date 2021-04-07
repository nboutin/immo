#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@date: 2021-03
@author: nboutin
'''
from .immo_system_core import ImmoSystemCore
from .population import Population


class Simulation:
    '''
    La Simulation contient une instance d'ImmoSystem et une Population d'Entity comme jeu de donnée
    Simulation can get Variable data according to its Entities of reference
    Simulation can compute Variable data according to its Entities of reference
    '''

    def __init__(self, immo_sys: ImmoSystemCore, populations):
        '''
        :param populations: {entity.key : Population(entity)}
        '''
        self.immo_sys = immo_sys
        self.populations = populations

    def set_input(self, variable_name: str, period: str, value):
        # Check if variable is defined by ImmoSystem

        # Get Variable Holder
        holder = self.get_holder(variable_name)

        # Set input
        holder.set_input(period, value)

    def get_holder(self, variable_name: str):
        # Get Variable Population
        variable = self.immo_sys.get_variable(variable_name)

        # Get Variable Holder from Population
        return self.populations[variable.entity.key].get_holder(variable_name)

    # def get(self, entity: str, period: str, variable: str):
        # e = self._immosys.get_entity(entity)
        #
    # def compute(self, variable: str, period: str):
        # var = self.immosys.get_variable(variable)
        #
        # self._run_formula()
        #
    # def _run_formula(self):
        # pass
