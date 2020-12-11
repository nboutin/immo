#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json


class Impot_Micro_Foncier:
    '''
    https://www.corrigetonimpot.fr/impot-location-vide-appartement-proprietaire-calcul/
    '''

    __IMPOT_DATA = 'res/impot_data.json'
    
    def __init__(self, revenu_foncier, tmi):
        
        with open(Impot_Micro_Foncier.__IMPOT_DATA, 'r') as file:
            data = json.load(file)

        self._prelevement_sociaux_taux = data['prelevement_sociaux_taux']
        self._taux = data['micro_foncier']['taux']
        self._revenu_foncier_plafond = data['micro_foncier']['revenu_foncier_plafond']
        
        if revenu_foncier > self._revenu_foncier_plafond:
            raise Exception("Revenu Foncier supérieur au plafond")
        
        self._revenu_foncier = revenu_foncier
        self._tmi = tmi
    
    @property
    def base_impossable(self):
        return self._revenu_foncier * (1 - self._taux)
    
    @property
    def revenu_foncier_impossable(self):
        return self.base_impossable * self._tmi
    
    @property
    def prelevement_sociaux_montant(self):
        return self.base_impossable * self._prelevement_sociaux_taux
    
    @property
    def impot_total(self):
        return self.revenu_foncier_impossable + self.prelevement_sociaux_montant
