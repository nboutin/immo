#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json


class Database:
    
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    __DATA_FILEPATH = os.path.join(__location__, 'data', 'database.json')
    
    def __init__(self):
        
        self._filepath = Database.__DATA_FILEPATH

        with open(self._filepath, 'r') as file:
            data = json.load(file)

        self._impot_data = data['impot']
        
    @property
    def prelevement_sociaux_taux(self): 
        return self._impot_data['prelevement_sociaux_taux']
        
    @property
    def micro_foncier_taux(self): 
        return self._impot_data['micro_foncier']['taux']
        
    @property
    def micro_foncier_revenu_foncier_plafond(self): 
        return self._impot_data['micro_foncier']['revenu_foncier_plafond']
