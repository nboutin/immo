#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Lot:
    
    def __init__(self, classification, surface, loyer_mensuel, vacance_locative_taux_annuel=0, PNO=0,
                 gestion_agence_taux=0, copropriete=0):
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
        self._vacance_locative_taux_annuel = vacance_locative_taux_annuel
        self._PNO = PNO
        self._gestion_agence_taux = gestion_agence_taux
        self._copropriete = copropriete
        
    @property
    def surface(self):
        return self._surface

    @property
    def loyer_mensuel(self):
        return self._loyer_mensuel

    @property
    def loyer_annuel(self):
        return self.loyer_mensuel * 12
    
    @property
    def vacance_locative_taux_annuel(self):
        return self._vacance_locative_taux_annuel
    
    @property
    def vacance_locative_montant_annuel(self):
        return self.loyer_annuel * self._vacance_locative_taux_annuel
    
    @property
    def pno_montant_annuel(self):
        return self._PNO

    @property
    def gestion_agence_montant_annuel(self):
        return self.loyer_annuel * self._gestion_agence_taux
    
    @property
    def copropriete(self):
        return self._copropriete


class Bien_Immo:
    '''
    Bien_Immo can contains several lot
    '''
    
    def __init__(self, prix_net_vendeur, frais_agence_immo, frais_notaire,
                 travaux_budget, apport,
                 taxe_fonciere=0, travaux_provision_taux=0):
        '''
        travaux provision: taux appliqué sur le loyer mensuel de chaque lot
        '''
        
        self._prix_net_vendeur = prix_net_vendeur
        self._travaux_budget = travaux_budget
        self._apport = apport
        self._taxe_fonciere = taxe_fonciere
        self._travaux_provision_taux = travaux_provision_taux
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
    def taxe_fonciere(self):
        return self._taxe_fonciere
    
    @property
    def travaux_provision_annuel_total(self):
        return self.loyer_annuel_total * self._travaux_provision_taux
    
    @property
    def vacance_locative_annuel_total(self):
        value = 0
        for lot in self._lots:
            value += lot.vacance_locative_montant_annuel
        return value
    
    @property
    def pno_annuel_total(self):
        value = 0
        for lot in self._lots:
            value += lot.pno_montant_annuel
        return value
    
    @property
    def gestion_agence_annuel_total(self):
        value = 0
        for lot in self._lots:
            value += lot.gestion_agence_montant_annuel
        return value
    
    @property
    def copropriete_annuel_total(self):
        value = 0
        for lot in self._lots:
            value += lot.copropriete
        return value
            
    @property
    def charges_annuel_total(self):
        return self._taxe_fonciere + self.travaux_provision_annuel_total + self.vacance_locative_annuel_total \
            +self.pno_annuel_total + self.gestion_agence_annuel_total + self.copropriete_annuel_total
    
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
    
