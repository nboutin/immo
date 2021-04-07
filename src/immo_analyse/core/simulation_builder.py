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

    def build_from_entities(self, immo_sys: ImmoSystemCore, entities_input):

        simulation = Simulation(immo_sys, immo_sys.build_population())

        # Set Simulation for Population
        for entity_key, population in simulation.populations.items():
            population.set_simulation(simulation)

        # Check entities_input against Population from ImmoSystem entities

        # Set variable data
        for entity_type, entity_instance in entities_input.items():
            for entity_name, variables in entity_instance.items():
                for variable_name, period_value in variables.items():
                    for period, value in period_value.items():
                        simulation.set_input(variable_name, period, value)

        return simulation
