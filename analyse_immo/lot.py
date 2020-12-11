#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from provisions import Provisions


class Lot:
    
    def __init__(self, classification, surface, loyer_nu_mensuel, provision_charge_mensuel):
#                  vacance_locative_taux_annuel=0, PNO=0,
#                  gestion_agence_taux=0, copropriete_mensuel=0):

        self._type = classification
        self._surface = surface
        self._loyer_nu_mensuel = loyer_nu_mensuel
        self._provision_charge_mensuel = provision_charge_mensuel
        
#         self._vacance_locative_taux_annuel = vacance_locative_taux_annuel
#         self._PNO = PNO
#         self._gestion_agence_taux = gestion_agence_taux
#         self._copropriete_mensuel = copropriete_mensuel
        
    @property
    def surface(self):
        return self._surface

    @property
    def loyer_nu_mensuel(self):
        return self._loyer_nu_mensuel

    @property
    def loyer_nu_annuel(self):
        return self.loyer_nu_mensuel * 12
    
    def set_provisions(self, provisions):
        self._provisions = provisions
    
#     @property
#     def vacance_locative_taux_annuel(self):
#         return self._vacance_locative_taux_annuel
#     
#     @property
#     def vacance_locative_montant_annuel(self):
#         return self.loyer_nu_annuel * self._vacance_locative_taux_annuel
    
    @property
    def pno_montant_annuel(self):
        return self._PNO

    @property
    def gestion_agence_montant_annuel(self):
        return self.loyer_nu_annuel * self._gestion_agence_taux
    
    @property
    def copropriete_mensuel(self):
        return self._copropriete_mensuel
    
    @property
    def copropriete_annuel(self):
        return self.copropriete_mensuel * 12
