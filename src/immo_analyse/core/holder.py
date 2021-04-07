#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@date: 2021-04
@author: nboutin
'''
import typing
from .variable import Variable
from .period import Period


class Holder:
    '''
    Holder keeps track of variable values after set as input or computed by simulation
    '''

    def __init__(self, variable: Variable, population):
        self.variable = variable
        self.population = population
        self.value: typing.Dict[Period] = {}

    def set_input(self, period: str, value):
        period = Period(period)
        self.value[period] = value
