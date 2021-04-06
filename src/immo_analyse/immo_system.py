#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@date: 2021-04
@author: nboutin
'''
import os

from immo_analyse.core.immo_system_core import ImmoSystemCore

_location_ = os.path.dirname(os.path.abspath(__file__))


class ImmoSystem(ImmoSystemCore):

    def __init__(self):
        ImmoSystemCore.__init__(self)

        self.add_variables_from_directory(os.path.join(_location_, 'model', 'variable'))
