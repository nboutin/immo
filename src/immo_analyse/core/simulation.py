#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@date: 2021-03
@author: nboutin
'''
import typing
import numpy as np
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
        :param populations: Dict[Entity.key, Population]
        '''
        self.immo_sys = immo_sys
        self.populations: typing.Dict[Entity.key, Population] = populations
        self.entities: typing.Dict[Entity.key, Entity] = {}
        self.entities_index: typing.Dict[Entity.key, typing.Dict[str, int]] = {}  # example: [Lot]['Lot1'] = 0

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

    def compute(self, variable_name: str, period: str, add=False, entity_key=None):
        '''
        :param add:bool, if true try to compute on bigger period than variable period definition
            for example: month variable compute for a year
        '''
        if entity_key:
            return self._compute_entity(variable_name, period, add, entity_key)

        if add:
            return self._compute_add(variable_name, period)
        else:
            return self._compute(variable_name, period)

    def _compute(self, variable_name: str, period: str):
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
        if cache is not None:
            return cache

        # Run formula: If Variable does not have formula, so it is input variable, get default value
        value = self._run_formula(variable, population, period)
        if not value:
            value = holder.get_default()

        # Put variable value into holder (cache)
        holder.set_input(period, value)

        return value

    def _compute_entity(self, variable_name, period, add, entity_key):
        '''
        :param entity_key:str,
        '''
        se_values = self.compute(variable_name, period, add)
        variable = self.immo_sys.get_variable(variable_name)
        sub_entity_key = variable.entity.key

        values = []

        for entity_name, variable in self.entities[entity_key].items():

            # sub_entities = [v for k, v in variable.items() if k == sub_entity_key]
            sub_entities = variable[sub_entity_key]

            value = 0
            for se in sub_entities:
                se_index = self.entities_index[sub_entity_key][se]
                value += se_values[se_index]
            values.append(value)

        return np.array(values)

        # for entity_instance in self.entities[variable.entity.key].values():

        # Check that entities instance of entity key has sub-entity key equal to variable.entity.key
        # for entity_name, sub_entities in self.entities[entity_key].items():
        # if sub_entities == entity_key:
        # for sub_entity in sub_entities:
        #
        # for entity_dest in self.entities[variable.entity.key].keys():

    def _compute_add(self, variable_name: str, period: str):
        # Construct period
        if period is not None and not isinstance(period, periods.Period):
            period = periods.period(period)

        variable = self.immo_sys.get_variable(variable_name)

        # Check that the requested period matches definition_period
        if periods.unit_weight(variable.period) > periods.unit_weight(period.unit):
            raise ValueError(
                "Unable to compute variable '{0}' for period {1}: '{0}' can only be computed for {2}-long periods."
                "You can use the DIVIDE option to get an estimate of {0} by dividing the yearly value by 12, "
                "or change the requested period to 'period.this_year'.".format(
                    variable.name, period, variable.period))

        if variable.period not in [periods.DAY, periods.MONTH, periods.YEAR]:
            raise ValueError(
                "Unable to sum constant variable '{}' over period {}: "
                "only variables defined daily, monthly, or yearly can be summed over time.".format(
                    variable.name, period))

        return sum(self.compute(variable_name, sub_period)
                   for sub_period in period.get_subperiods(variable.period))

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
