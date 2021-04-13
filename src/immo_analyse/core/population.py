#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@date: 2021-04
@author: nboutin
'''

import typing

from .variable import Variable
from .holder import Holder
from .entity import Entity


class Population:
    '''
    There is one instance of Population by Entity.key
    Population is data for Simulation
    Population is link between Variable and Holder (data of Variable)
    example:
        holders['loyer_nu'] = Holder()
    '''

    def __init__(self, entity: Entity):
        self.entity = entity
        self.count = 0  # number of instance of Entity type
        self.simulation = None
        self._holders: typing.Dict[Variable.name, Holder] = {}

    def set_simulation(self, simulation):
        self.simulation = simulation

    def get_holder(self, variable_name: str):
        '''
        :brief return Holder if exist otherwise create it
        '''
        holder = self._holders.get(variable_name)
        if holder:
            return holder

        variable = self.simulation.immo_sys.get_variable(variable_name)

        self._holders[variable_name] = holder = Holder(variable, self)
        return holder

    def __call__(self, variable_name: str, period, entity_key: str = None):
        return self.simulation.compute(variable_name, period, entity_key=entity_key)
