#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@date: 2021-03-10
@author: nboutin
'''

from .travaux import Travaux


class Commun:

    def __init__(self, travaux=Travaux()):
        self._travaux = travaux

    @property
    def travaux(self):
        return self._travaux
