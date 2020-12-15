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
        if type_ == Charge.gestion_e.provision_travaux:
            return  self._default_data.provision_travaux_taux
        elif type_ == Charge.gestion_e.vacance_locative:
            return self._default_data.vacance_locative_taux(self._lot.type)
        
'''
/* emptying table `typologie` */
truncate table `typologie` ;
/* dumping data for table `typologie` */
insert into `typologie` (`id`,`type`,`foncier`,`comptable`,`tresorerie`) values ('11','Charge récupérable/locative : Entretien de l’immeuble et des équipements','0','1','1');
insert into `typologie` (`id`,`type`,`foncier`,`comptable`,`tresorerie`) values ('12','Charge récupérable/locative : Consommations communes','0','1','1');
insert into `typologie` (`id`,`type`,`foncier`,`comptable`,`tresorerie`) values ('13','Charge récupérable/locative : Consommations personnelles','0','1','1');
insert into `typologie` (`id`,`type`,`foncier`,`comptable`,`tresorerie`) values ('14','Charge récupérable/locative : Taxe d’enlèvement des ordures ménagères','0','1','1');
insert into `typologie` (`id`,`type`,`foncier`,`comptable`,`tresorerie`) values ('19','Charge récupérable/locative : Autres','0','1','1');
insert into `typologie` (`id`,`type`,`foncier`,`comptable`,`tresorerie`) values ('21','Charge déductible : Frais d’administration et de gestion','1','1','1');
insert into `typologie` (`id`,`type`,`foncier`,`comptable`,`tresorerie`) values ('22','Charge déductible : Primes d’assurance','1','1','1');
insert into `typologie` (`id`,`type`,`foncier`,`comptable`,`tresorerie`) values ('23','Charge déductible : Dépenses de réparation, d’entretien et d’amélioration','1','1','1');
insert into `typologie` (`id`,`type`,`foncier`,`comptable`,`tresorerie`) values ('24','Charge déductible : Charges récupérables non récupérées au départ du locataire','1','0','0');
insert into `typologie` (`id`,`type`,`foncier`,`comptable`,`tresorerie`) values ('25','Charge déductible : Indemnités d’éviction, frais de relogement','1','1','1');
insert into `typologie` (`id`,`type`,`foncier`,`comptable`,`tresorerie`) values ('26','Charge déductible : Taxes foncières (hors TEOM), taxes annexes','1','1','1');
insert into `typologie` (`id`,`type`,`foncier`,`comptable`,`tresorerie`) values ('29','Charge déductible : Régimes particuliers, déductions spécifiques','1','0','0');
insert into `typologie` (`id`,`type`,`foncier`,`comptable`,`tresorerie`) values ('30','Charge non déductible : Capital d\'emprunt (amortissement)','0','0','1');
insert into `typologie` (`id`,`type`,`foncier`,`comptable`,`tresorerie`) values ('31','Charge non déductible : Autres','0','1','1');
insert into `typologie` (`id`,`type`,`foncier`,`comptable`,`tresorerie`) values ('41','Intérêts d’emprunt (inc. assurances et frais)','1','1','1');
insert into `typologie` (`id`,`type`,`foncier`,`comptable`,`tresorerie`) values ('91','Syndic de copropriété : Provisions pour charges','1','1','1');
insert into `typologie` (`id`,`type`,`foncier`,`comptable`,`tresorerie`) values ('92','Syndic de copropriété : Arrêté des comptes : Charges récupérables/locatives','0','0','0');
insert into `typologie` (`id`,`type`,`foncier`,`comptable`,`tresorerie`) values ('93','Syndic de copropriété : Arrêté des comptes : Charges déductibles','0','0','0');
insert into `typologie` (`id`,`type`,`foncier`,`comptable`,`tresorerie`) values ('94','Syndic de copropriété : Arrêté des comptes : Charges non déductibles','0','0','0');
insert into `typologie` (`id`,`type`,`foncier`,`comptable`,`tresorerie`) values ('95','Syndic de copropriété : Arrêté des comptes : Remboursement reçu du syndic','-1','1','1');
insert into `typologie` (`id`,`type`,`foncier`,`comptable`,`tresorerie`) values ('96','Syndic de copropriété : Arrêté des comptes : Versement complémentaire au syndic','1','1','1');
insert into `typologie` (`id`,`type`,`foncier`,`comptable`,`tresorerie`) values ('97','Syndic de copropriété : Avances, provisions et cotisations travaux (non déductible)','0','1','1');
insert into `typologie` (`id`,`type`,`foncier`,`comptable`,`tresorerie`) values ('98','Syndic de copropriété : Gros travaux déductibles','1','0','0');
'''
    
