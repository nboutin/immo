#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@date: 2021-03
@author: nboutin
'''


class Variable:
    '''
    :attr name: variable name
    :attr type: variable type (int, float, bool, str, date, Enum)
    :attr entity: entity the variable is defined for (Immeuble, Lot)
    :attr period_definition: period the variable is defined for (MONTH, YEAR, ETERNITY)

    '''

    def __init__(self):
        self.name: str = self.__class__.__name__

    # def formula(self):
    # '''
    # To be defined by derived class if necessary
    # '''
    # pass
