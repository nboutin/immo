#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Lot:
    
    def __init__(self, classification, surface, loyer_mensuel):
        '''    
            "type": "T1",
            "surface": 65,
            "loyer_mensuel": 450,
            "charges_locataire": 50,
            "__comment": "1/12=0.083, 1/24=0.042",
            "vacance_locative": 0.042,
            "copropriete": 40,
            "assurance_pno": 100,
            "gestion_agence": 0
        '''
        self._type = classification
        self._surface = surface
        self._loyer_mensuel = loyer_mensuel
        
    @property
    def surface(self):
        return self._surface

    @property
    def loyer_mensuel(self):
        return self._loyer_mensuel


class Bien_Immo:
    '''
    Bien_Immo can contains several lot
    '''
    
    def __init__(self, prix_net_vendeur, frais_agence_immo, frais_notaire, travaux_budget, apport):
        
        self._prix_net_vendeur = prix_net_vendeur
        self._travaux_budget = travaux_budget
        self._apport = apport
        self._lots = []
        
        self.__set_notaire_taux_montant(frais_notaire)
        self.__set_agence_taux_montant(frais_agence_immo)
        
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
    def travaux_budget(self):
        return self._travaux_budget
    
    @property
    def apport(self):
        return self._apport
    
    @property
    def investissement_initial(self):
        return self._prix_net_vendeur + self._notaire_montant + self._agence_montant + \
            self._travaux_budget - self._apport

    @property
    def loyer_mensuel_total(self):
        value = 0
        for lot in self._lots:
            value += lot.loyer_mensuel
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
    def charges_annuel_total(self):
        return 0
    
    @property
    def rapport_surface_prix(self):
        return self._prix_net_vendeur / self.surface_total
        
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
    
