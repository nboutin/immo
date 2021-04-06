#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@date: 2021-03
@author: nboutin
'''


class ImmoSystem:
    '''
    Parameter
    '''

    def __init__(self, entities):
        self._lots = entities['lots']

    def get_entity(self, entity: str):
        if entity in self._lots:
            return self._lots['entity']
        else:
            return None
