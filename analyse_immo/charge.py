#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Provision
    - travaux entretien, rénovation
    - vacance locative
    - charges locative (du locataire)
Charge recuperable/locative
    https://www.service-public.fr/particuliers/vosdroits/F947
    Les charges locatives (ou charges récupérables) sont des dépenses payées initialement par le propriétaire. 
    Le propriétaire se fait rembourser par le locataire.
    - entretien de l'immeuble et des equipements
    - consommations communes
    - consommations personnelles
    - taxe enlevement ordures menageres
    - autres
Charge deductible:
    - frais administration et gestion
    - prime d'assurance (pno, impayé)
    - depenses reparation, entretien, amelioration
    - charges recuperable non recuperees au depart du locataire
    - indeminité d'eviction, frais de relogement
    - taxe fonciere, taxe annexes
    - regimes particuliers, deduction spécifiques
Charge non-deductible:
    - capital d'emprunt (amortissement)
    - autres
Interet d'emprunt (inclu assurance et frais)
Syndic de copropriete:
    - provision pour charges
    - Arrete des comptes
        - saisie rapide du decompte annuel
        - charges recuperable/locative
        - charges deductibles
        - remboursement recu du syndic
        - versement complementaire au syndic
    - avance, provisions et cotisation travaux (non deductible)
    - gros travaux deductibles
'''
from enum import unique, Enum, auto


class Charge:

    @unique
    class gestion_e(Enum):
        provision_travaux = auto()
        vacance_locative = auto()
        agence_immo = auto()
        charge_locative = auto()
        
    @unique
    class deductible_e(Enum):
        copropriete = auto()
        taxe_fonciere = auto()
        prime_assurance = auto()
    
    def __init__(self, lot, defaut=None):
        
        self._lot = lot
        self._default_data = defaut
        self._charges = []
        
    def get_montant(self, charges_list):
        '''
        charges, list of charges
        '''
        value = 0
        for charge_request in charges_list:
            for charge in self._charges:
                if charge_request == charge[0]:
                    value += charge[2]
        return value
        
    def add(self, type_, value):
        taux = 0
        montant = 0
        
        if value == 1 and self._default_data:  # use default
            value = self.__get_default(type_)
        
        if value < 1:
            taux = value
            montant = self._lot.loyer_nu_annuel * taux
        elif value > 1:
            montant = value
            taux = montant / self._lot.loyer_nu_annuel
        
        self._charges.append((type_, taux, montant))
        
    def __get_default(self, type_):
        if type_ == Charge.provision_e.travaux:
            return  self._default_data.provision_travaux_taux
        elif type_ == Charge.provision_e.vacance_locative:
            return self._default_data.vacance_locative_taux
    
