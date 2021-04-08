#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@date: 2021-03
@author: nboutin
'''
from .immo_system_core import ImmoSystemCore
from . import periods
from .periods import Period
from .entity import Entity
from .variable import Variable
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

    def get(self, variable_name: str, period: str, entity: Entity=None):
        '''
        :brief Get value of variable_name if set as input or previously computed
                Otherwise return None and does not cache value
        :param entity: Entity, Entity type use when Variable support multiple Entity type
                None for Variable which support only one type, if not an error is raised
        '''
        holder = self.get_holder(variable_name)
        return holder.get_value(period)

    def compute(self, variable_name: str, period: str):
        # Construct period
        if period is not None and not isinstance(period, periods.Period):
            period = periods.period(period)

        population = self.get_variable_population(variable_name)
        holder = population.get_holder(variable_name)
        variable = self.immo_sys.get_variable(variable_name)

        # Check period consistency
        self._check_period(period, variable)

        # Lookup in cache
        cache = holder.get_value(period)
        if cache:
            return cache

        # Run formula: If Variable does not have formula, so it is input variable, get default value
        value = self._run_formula(variable, population, period)
        if not value:
            value = holder.get_default()

        # Put variable value into holder (cache)
        holder.set_input(period, value)

        return value

    def _check_period(self, period: Period, variable: Variable):
        '''
        :brief Check that period matches variable.period definition
        '''

        # For variable constant in time, all periods are accepted
        if variable.period == periods.ETERNITY:
            return

        if variable.period == periods.MONTH and period.unit != periods.MONTH:
            raise ValueError(
                "Cannot compute variable '{}' for period {}: Must be computed for a month. Use ADD to get it on a year".format(
                    variable.name, period))

        if variable.period == periods.YEAR and period.unit != periods.YEAR:
            raise ValueError(
                "Cannot compute variable '{}' for period {}: Must be computed for a year. Use DIVIDE to get it on a month".format(
                    variable.name, period))

        if period.size != 1:
            raise ValueError(
                "Cannot compute variable '{}' for period {}. Variable period is {}".format(
                    variable.name, period, variable.period))

    def _run_formula(self, variable: Variable, population: Population, period: Period):
        '''
        :brief Find the variable formula for the given period and apply it to population
                Also provide ImmoSystem Parameter to formula
        :return result from variable formula
        '''
        formula = variable.get_formula(period)
        if not formula:
            return None

        return formula(population, period, None)

    # --- Getter/Setter

    def get_variable_population(self, variable_name: str):
        '''
        :return Population: Population containing variable
        '''
        # Get Variable Population
        variable = self.immo_sys.get_variable(variable_name, check_existence=True)
        return self.populations[variable.entity.key]

    def get_holder(self, variable_name: str):
        '''
        Get Variable Holder from Population
        '''
        population = self.get_variable_population(variable_name)
        return population.get_holder(variable_name)
