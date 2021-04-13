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
        # Check sub_entities of entity

        # Dict[Variable.name, Dict[Period, List[Variable.value_type]]
        buffer = {}

        # Set variable data
        for entity_key, entities_instances in entities_input.items():  # entity_key, entities_instances

            # Set Population count
            pop_count = len(entities_instances)
            simulation.populations[entity_key].count = pop_count

            simulation.entities[entity_key] = entities_instances

            for i, (entity_name, variables) in enumerate(entities_instances.items()):  # entity_name, variables
                for variable_name, period_value in variables.items():

                    # Check for sub-entities
                    if variable_name in [e.key for e in immo_sys.entities]:
                        sub_entity_type = variable_name
                        sub_entities_name = period_value
                        simulation.entities[entity_key][entity_name][sub_entity_type] = sub_entities_name
                        continue

                    if variable_name == 'openfisca':
                        continue

                    # Add variable
                    if variable_name not in buffer:
                        buffer[variable_name] = {}

                    for period, value in period_value.items():

                        if period not in buffer[variable_name]:
                            buffer[variable_name][period] = [0] * pop_count

                        # value can be an array of value which must be sum
                        if isinstance(value, list):
                            value = sum(value)
                        buffer[variable_name][period][i] = value

        for variable_name, periods in buffer.items():
            for period, values in periods.items():
                simulation.set_input(variable_name, period, np.array(values))

        # Build entities_index
        for entity_key, entities_instances in entities_input.items():

            if entity_key not in simulation.entities_index:
                simulation.entities_index[entity_key] = {}

            for i, ei_name in enumerate(entities_instances.keys()):
                simulation.entities_index[entity_key][ei_name] = i

        return simulation
