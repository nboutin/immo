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
        for population in simulation.populations.values():  # entity_key, population
            population.set_simulation(simulation)

        # Check entities_input against Population from ImmoSystem entities

        # Set variable data
        for entity_instance in entities_input.values():  # entity_type, entity_instance
            for variables in entity_instance.values():  # entity_name, variables
                for variable_name, period_value in variables.items():
                    if isinstance(period_value, dict):
                        for period, value in period_value.items():
                            simulation.set_input(variable_name, period, value)

        return simulation
