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
        attr = {name: value for name, value in self.__class__.__dict__.items() if not name.startswith('__')}
        self.value_type = attr['value_type']
        self.entity = attr['entity']
        self.period = attr['period']
        self.label = attr['label']
        self.value_accepted = attr.get('value_accepted', [])
        self.default_value = attr.get('default_value', None)
        self.year_to_month = attr.get('year_to_month', False)
        self.formulas = attr.get('formula', None)

    def get_formula(self, period=None):

        if not self.formulas:
            return None

        return self.formulas

    def get_default(self):
        return self.default_value
