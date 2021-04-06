#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@date: 2021-03
@author: nboutin
'''
from .immo_system import ImmoSystem
from .simulation import Simulation

entities = {
    'lots': {'lot1': {'type': {'2021-01-01': 'T1'},
                      'surface': {'2021-01-01': 50},
                      'loyer_nu': {'2021': 400 * 12}},
             'lot2': {'type': {'2021-01-01': 'T2'},
                      'surface': {'2021-01-01': 60},
                      'loyer_nu': {'2021': 500 * 12}}},
    'immeubles': {},
    'groupes_fiscal': {}
}

if __name__ == '__main__':
    '''
    Demo code, immo_analyse should be use as Python Package
    '''

    immosys = ImmoSystem(entities)
    simulation = Simulation(immosys)

    simulation.compute()
