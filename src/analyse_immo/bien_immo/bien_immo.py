#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .charge import Charge


class Bien_Immo:
    '''
    Bien_Immo can contains several lot
    Augmentation annuel du loyer 0.1%
    Augmentation annuel des charges 2%
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
    def financement_total(self):
        return self._prix_net_vendeur + self._notaire_montant + self._agence_montant + \
            self._budget_travaux - self._apport

    def loyer_nu_brut_mensuel(self, i_month=1):
        '''
        Loyer nu (hors charges) brut (sans provision)
        @param i_month: month index
        @see: loyer_nu_net_mensuel
        '''
        return sum(lot.loyer_nu_brut_mensuel(i_month) for lot in self._lots)

    def loyer_nu_brut_annuel(self, i_year=1):
        '''
        @param i_year: year index
        '''
        return self.loyer_nu_brut_mensuel(i_year * 12) * 12

    def loyer_nu_net_mensuel(self, i_month=1):
        '''
        @param i_month: month index
        Provision sur loyer nu brut de :
            - vacance locative
        '''
        return sum(lot.loyer_nu_net_mensuel(i_month) for lot in self._lots)

    def loyer_nu_net_annuel(self, i_year=1):
        '''
        @param i_year: year index
        '''
        return self.loyer_nu_net_mensuel(i_year * 12) * 12

    @property
    def surface_total(self):
        return sum(lot.surface for lot in self._lots)

    @property
    def rapport_surface_prix(self):
        try:
            return self._prix_net_vendeur / self.surface_total
        except ZeroDivisionError:
            return 0

    def get_charge(self, charges_list):
        #         return sum(lot.charge.get_montant_annuel(charges_list) for lot in self._lots)
        sum = 0
        for charge in charges_list:
            for lot in self._lots:
                value = lot.charge.get_montant_annuel(charge)
                # If taux
                if value < 1:
                    value = value * lot.loyer_nu_net_annuel()
                sum += value
        return sum

    @property
    def charges(self):
        return self.get_charge(
            [Charge.charge_e.copropriete,
             Charge.charge_e.taxe_fonciere,
             Charge.charge_e.prime_assurance,
             Charge.charge_e.agence_immo])

    @property
    def provisions(self):
        '''
        Charge.charge_e.vacance_locative is not used here but for loyer_nu_net
        '''
        return self.get_charge([Charge.charge_e.provision_travaux])

    def add_lot(self, lot):
        self._lots.append(lot)

    @property
    def lot_count(self):
        return len(self._lots)

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
