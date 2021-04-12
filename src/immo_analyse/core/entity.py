#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@date: 2021-04
@author: nboutin
'''
import typing


class Entity:

    def __init__(self, key, sub_entities=None):
        self.key: str = key
        self.sub_entities: typing.List[Entity.key] = sub_entities
