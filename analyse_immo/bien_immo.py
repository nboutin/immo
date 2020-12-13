#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from charge import Charge


class Bien_Immo:
    '''
    Bien_Immo can contains several lot
    '''
    
    def __init__(self, prix_net_vendeur, frais_agence, frais_notaire, budget_travaux, apport):
        
        self._prix_net_vendeur = prix_net_vendeur
        self._budget_travaux = budget_travaux
        self._apport = apport
        self._lots = []
        self.__set_notaire_taux_montant(frais_notaire)
        self.__set_agence_taux_montant(frais_agence)
        
    @property
    def prix_net_vendeur(self):
        return self._prix_net_vendeur
        
    @property
    def notaire_taux(self):
        return self._notaire_taux

    @property
    def notaire_montant(self):
        return self._notaire_montant

    @property
    def agence_taux(self):
        return self._agence_taux

    @property
    def agence_montant(self):
        return self._agence_montant
    
    @property
    def budget_travaux(self):
        return self._budget_travaux
    
    @property
    def apport(self):
        return self._apport
    
    @property
    def investissement_initial(self):
        return self._prix_net_vendeur + self._notaire_montant + self._agence_montant + \
            self._budget_travaux - self._apport

    @property
    def loyer_mensuel_total(self):
        value = 0
        for lot in self._lots:
            value += lot.loyer_nu_mensuel
        return value
    
    @property
    def loyer_annuel_total(self):
        return self.loyer_mensuel_total * 12
    
    @property
    def surface_total(self):
        value = 0
        for lot in self._lots:
            value += lot.surface
        return value
    
    @property
    def rapport_surface_prix(self):
        return self._prix_net_vendeur / self.surface_total
    
    @property
    def charge_gestion(self):
        value = 0
        for lot in self._lots:
            value += lot.charge.get_montant(
                [Charge.gestion_e.provision_travaux,
                 Charge.gestion_e.vacance_locative,
                 Charge.gestion_e.agence_immo])
        return value
    
    @property
    def charge_fonciere(self):
        value = 0
        for lot in self._lots:
            value = +lot.charge.get_montant(
                [Charge.deductible_e.copropriete,
                 Charge.deductible_e.taxe_fonciere,
                 Charge.deductible_e.prime_assurance, ])
        return value
    
#     @property
#     def taxe_fonciere(self):
#         return self._taxe_fonciere
#     
#     @property
#     def travaux_provision_annuel_total(self):
#         return self.loyer_annuel_total * self._travaux_provision_taux
#     
#     @property
#     def vacance_locative_annuel_total(self):
#         value = 0
#         for lot in self._lots:
#             value += lot.vacance_locative_montant_annuel
#         return value
#     
#     @property
#     def pno_annuel_total(self):
#         value = 0
#         for lot in self._lots:
#             value += lot.pno_montant_annuel
#         return value
#     
#     @property
#     def gestion_agence_annuel_total(self):
#         value = 0
#         for lot in self._lots:
#             value += lot.gestion_agence_montant_annuel
#         return value
#     
#     @property
#     def copropriete_annuel_total(self):
#         value = 0
#         for lot in self._lots:
#             value += lot.copropriete_annuel
#         return value
#             
#     @property
#     def charges_annuel_total(self):
#         return self._taxe_fonciere + self.travaux_provision_annuel_total + self.vacance_locative_annuel_total \
#             +self.pno_annuel_total + self.gestion_agence_annuel_total + self.copropriete_annuel_total
        
    def add_lot(self, lot):
        self._lots.append(lot)
    
    def __set_notaire_taux_montant(self, value):
        if value < 1:
            self._notaire_taux = value
            self._notaire_montant = self._prix_net_vendeur * self._notaire_taux
        else:
            self._notaire_montant = value
            self._notaire_taux = self._notaire_montant / self._prix_net_vendeur
    
    def __set_agence_taux_montant(self, value):
        if value < 1:
            self._agence_taux = value
            self._agence_montant = self._prix_net_vendeur * self._agence_taux
        else:
            self._agence_montant = value
            self._agence_taux = self._agence_montant / self._prix_net_vendeur
    
