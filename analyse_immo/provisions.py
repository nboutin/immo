#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum, unique, auto


class Provisions:
    
    @unique
    class provision_e(Enum):
        travaux = auto()
        vacance_locative = auto()
    
    def __init__(self, lot, default_data=None):
        
        self._lot = lot
        self._default_data = default_data
        self._provisions = []
        
    def add(self, type_, value):
        taux = 0
        montant = 0
        
        if value == 1 and self._default_data:  # use default
            if type_ == Provisions.provision_e.travaux:
                value = self._default_data.provision_travaux_taux
            elif type_ == Provisions.provision_e.vacance_locative:
                value = self._default_data.vacance_locative_taux
        
        if value < 1:
            taux = value
            montant = self._lot.loyer_nu_annuel * taux
        elif value > 1:
            montant = value
            taux = montant / self._loyer_nu_annuel
        
        self._provisions.append((type_, taux, montant))
