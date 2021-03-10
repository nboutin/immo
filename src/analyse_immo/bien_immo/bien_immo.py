#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import statistics
from .lot import Lot
from .charge import Charge


class Bien_Immo:
    '''
    Bien_Immo can contains several lot
    Augmentation annuel du loyer 0.1%
    Augmentation annuel des charges 2%
    '''

    def __init__(self, prix_net_vendeur, frais_agence, frais_notaire, apport):

        self._commun = None
        self._lots = []
        self._prix_net_vendeur = prix_net_vendeur
        self._apport = apport
        self.__set_notaire_taux_montant(frais_notaire)
        self.__set_agence_taux_montant(frais_agence)

    @property
    def commun(self):
        return self._commun

    @commun.setter
    def commun(self, commun):
        self._commun = commun

    def add_lot(self, lot):
        self._lots.append(lot)

    @property
    def lot_count(self):
        return len(self._lots)

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
    def travaux_montant(self):
        return self._commun.travaux.montant_total + sum([lot.travaux.montant_total for lot in self._lots])

    @property
    def subvention_montant(self):
        return self._commun.travaux.subvention_total + \
            sum([lot.travaux.subvention_total for lot in self._lots])

    @property
    def apport(self):
        return self._apport

    @property
    def financement_total(self):
        return self._prix_net_vendeur + self._notaire_montant + self._agence_montant + \
            self.travaux_montant - self._apport

    @property
    def surface_total_louable(self):
        return sum(lot.surface for lot in self._lots if lot.etat == Lot.etat_e.louable)

    @property
    def surface_total_amenageable(self):
        return sum(lot.surface for lot in self._lots if lot.etat == Lot.etat_e.amenageable)

    @property
    def surface_total_final(self):
        return sum(lot.surface for lot in self._lots)

    @property
    def rapport_surface_prix_louable(self):
        try:
            return self._prix_net_vendeur / self.surface_total_louable
        except ZeroDivisionError:
            return 0

    @property
    def rapport_surface_prix_final(self):
        try:
            return self._prix_net_vendeur / self.surface_total_final
        except ZeroDivisionError:
            return 0

    @property
    def irl_taux_annuel(self):
        data = [lot.irl_taux_annuel for lot in self._lots]
        return statistics.mean(data)

    @property
    def vacance_locative_taux_annuel(self):
        data = [lot.charge.get_taux(Charge.charge_e.vacance_locative) for lot in self._lots]
        return statistics.mean(data)

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

    def get_charge(self, charge_type_list, i_year=1):
        '''
        Here it assumes that provision_travaux and vacance_locative are taux
        '''
        # Convert to list
        if not isinstance(charge_type_list, list) and not isinstance(charge_type_list, tuple):
            charge_type_list = [charge_type_list]

        sum_ = 0
        for charge in charge_type_list:
            for lot in self._lots:
                if charge == Charge.charge_e.provision_travaux:
                    value = lot.charge.get_taux(charge)
                    value = value * lot.loyer_nu_net_annuel(i_year)
                elif charge == Charge.charge_e.vacance_locative:
                    value = lot.charge.get_taux(charge)
                    value = value * lot.loyer_nu_brut_annuel(i_year)
                else:
                    value = lot.charge.get_montant_annuel(charge)
                sum_ += value
        return sum_

    def charges(self, i_year=1):
        return self.get_charge(
            [Charge.charge_e.copropriete,
             Charge.charge_e.taxe_fonciere,
             Charge.charge_e.prime_assurance,
             Charge.charge_e.agence_immo], i_year)

    def provisions(self, i_year=1):
        '''
        Charge.charge_e.vacance_locative is not used here but for loyer_nu_net
        '''
        return self.get_charge([Charge.charge_e.provision_travaux], i_year)

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
