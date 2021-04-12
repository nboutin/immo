#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@date: 2021-04
@author: nboutin
'''
from .immo_system_core import ImmoSystemCore
from .simulation import Simulation
import numpy as np


class SimulationBuilder:

    def __init__(self):
        pass

    def build_from_entities(self, immo_sys: ImmoSystemCore, entities_input):

        simulation = Simulation(immo_sys, immo_sys.build_population())

        # Set Simulation for Population
        for population in simulation.populations.values():  # entity_key, population
            population.set_simulation(simulation)

        # Check entities_input against Population from ImmoSystem entities
        # Check entity_key from input

        # Dict[Variable.name, Dict[Period, List[Variable.value_type]]
        buffer = {}

        # Set variable data
        for entity_key, entities_instances in entities_input.items():  # entity_key, entities_instances

            # Set Population count
            simulation.populations[entity_key].count = len(entities_instances)

            for variables in entities_instances.values():  # entity_name, variables
                for variable_name, period_value in variables.items():

                    if variable_name not in buffer:
                        buffer[variable_name] = {}

                    if isinstance(period_value, dict):
                        for period, value in period_value.items():

                            if period not in buffer[variable_name]:
                                buffer[variable_name][period] = []

                            buffer[variable_name][period].append(value)

        for variable_name, periods in buffer.items():
            for period, values in periods.items():
                simulation.set_input(variable_name, period, np.array(values))

        return simulation
