#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@date: 2021-03
@author: nboutin
'''
from .immo_system_core import ImmoSystemCore
from .entity import Entity
from .variable import Variable
from . import periods


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

    def get(self, variable_name: str, period: str, entity: Entity=None):
        '''
        :param entity: Entity, Entity type use when Variable support multiple Entity type
                None for Variable which support only one type, if not an error is raised
        '''
        return self.get_holder(variable_name).get_value(period)

    def compute(self, variable_name: str, period: str):
        # Construct period
        if period is not None and not isinstance(period, periods.Period):
            period = periods.period(period)

        population = self.get_variable_population(variable_name)
        holder = population.get_holder(variable_name)

        # Lookup in cache
        cache = holder.get_value(period)
        if cache:
            return cache

        # Run formula
        # If Variable does not have formula, so it is input variable, get default value
        # Put variable value into holder (cache)
        pass

    def _run_formula(self, variable: Variable, population: Population, period: Period):
        '''
        :brief Find the variable formula for the given period and apply it to population
                Also provide ImmoSystem Parameter to formula
        :return result from variable formula
        '''

        pass

    # --- Getter/Setter

    def get_variable_population(self, variable_name: str):
        '''
        :return Population: Population containing variable
        '''
        # Get Variable Population
        variable = self.immo_sys.get_variable(variable_name)
        return self.populations[variable.entity.key]

    def get_holder(self, variable_name: str):
        # Get Variable Holder from Population
        return self.get_variable_population(variable_name).get_holder(variable_name)
