#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@date: 2021-04
@author: nboutin
'''
import typing
import numpy as np
from .variable import Variable
from . import periods
from .periods import Period
from immo_analyse.core.periods import ETERNITY


class Holder:
    '''
    Holder keeps track of variable values after set as input or computed by simulation
    '''

    def __init__(self, variable: Variable, population):
        self.variable = variable
        self.population = population
        self.value: typing.Dict[Period, Variable.value_type] = {}

    def set_input(self, period: str, value):

        # Check value size against population count
        try:
            if value.size != self.population.count:
                raise Exception(
                    "For variable '{}', value size ({}) is not equal to Population count ({})".format(
                        self.variable.name, value.size, self.population.count))
        except (TypeError, AttributeError):
            raise

        period = periods.period(period)

        if period.unit == periods.ETERNITY and self.variable.definition_period != periods.ETERNITY:
            raise Exception(
                "Cannot set value for variable '{}' for ETERNITY. Variable period is {}".format(
                    self.variable.name, self.variable.period))

        if period.unit == self.variable.period:
            self.value[period] = value
        elif period.unit == periods.YEAR and self.variable.period == periods.MONTH and self.variable.year_to_month:
            # Set month variable with year value
            self._set_month_with_year_value(period, value)
        elif self.variable.period == ETERNITY:
            self.value[ETERNITY] = value
        else:
            raise ValueError(
                "Cannot set variable '{}' for period {}. It does not support convertion year_to_month or month_to_year".format(
                    self.variable.name, period))

    def get_value(self, period: str):

        period = periods.period(period)
        return self.value.get(period, None)

    def get_default(self):
        return np.array([self.variable.get_default()] * self.population.count)

    def _set_month_with_year_value(self, period: Period, value):
        sub_period = period.get_subperiods(periods.MONTH)
        value = value / len(sub_period)

        for p in sub_period:
            self.set_input(p, value)
