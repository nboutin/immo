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
    '''
    Store and handle charges and provisions
    '''

    @unique
    class charge_e(Enum):
        # Provisions
        provision_travaux = auto()
        vacance_locative = auto()
        # Charges proprietaire
        copropriete = auto()
        taxe_fonciere = auto()
        prime_assurance = auto()
        agence_immo = auto()
        # Charges locataire
        charge_locative = auto()

    def __init__(self, default, lot_type='T1'):

        self._default = default
        self._lot_type = lot_type
        self._charges = []

    def get_montant_annuel(self, charge_type_list):
        '''
        :param charge_type_list: list of charge type
        '''
        # Convert to list
        if not isinstance(charge_type_list, list) and not isinstance(charge_type_list, tuple):
            charge_type_list = [charge_type_list]

        try:
            return sum(charge['value'] for charge in self._charges if charge['charge'] in charge_type_list)
        except TypeError:
            raise Exception('Charge {} does not support value'.format(charge_type_list))

    def get_taux(self, charge_type):
        '''
        @param charge_type: charge type
        '''
        return sum(charge['taux'] for charge in self._charges if charge['charge'] == charge_type)

    def add(self, charge, value):
        taux = None
        montant = None

        # use default
        if value == 1:
            value = self.__get_default(charge)

        if value > 0 and value < 1:
            taux = value
        elif value > 1:
            montant = value
        else:
            taux = 0
            montant = 0

        self._charges.append({'charge': charge, 'taux': taux, 'value': montant})

    def __get_default(self, type_):
        if type_ == Charge.charge_e.provision_travaux:
            return self._default.provision_travaux_taux
        elif type_ == Charge.charge_e.vacance_locative:
            return self._default.vacance_locative_taux(self._lot_type)
        else:
            raise LookupError
