#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@date: 2021-04
@author: nboutin
'''
import typing
from .variable import Variable
from . import periods
from .periods import Period


class Holder:
    '''
    Holder keeps track of variable values after set as input or computed by simulation
    '''

    def __init__(self, variable: Variable, population):
        self.variable = variable
        self.population = population
        self.value: typing.Dict[Period] = {}

    def set_input(self, period: str, value):
        period = periods.period(period)

        if period.unit == periods.ETERNITY and self.variable.definition_period != periods.ETERNITY:
            raise Exception(
                "Cannot set value for variable '{}' for ETERNITY. Variable period is {}".format(
                    self.variable.name, self.variable.period))

        self.value[period] = value

    def get_value(self, period: str):

        period = periods.period(period)
        return self.value.get(period, None)

    def get_default(self):
        return self.variable.get_default()
