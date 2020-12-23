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
    def financement_total(self):
        return self._prix_net_vendeur + self._notaire_montant + self._agence_montant + \
            self._budget_travaux - self._apport

    @property
    def loyer_nu_mensuel(self):
        return sum(lot.loyer_nu_mensuel for lot in self._lots)

    @property
    def loyer_nu_annuel(self):
        return self.loyer_nu_mensuel * 12

    @property
    def surface_total(self):
        return sum(lot.surface for lot in self._lots)

    @property
    def rapport_surface_prix(self):
        return self._prix_net_vendeur / self.surface_total

    def get_charge(self, charges_list):
        return sum(lot.charge.get_montant(charges_list) for lot in self._lots)

    @property
    def charge_gestion(self):
        return self.get_charge(
            [Charge.gestion_e.provision_travaux,
                Charge.gestion_e.vacance_locative,
                Charge.gestion_e.agence_immo])

    @property
    def charge_fonciere(self):
        return self.get_charge(
            [Charge.deductible_e.copropriete,
             Charge.deductible_e.taxe_fonciere,
             Charge.deductible_e.prime_assurance])

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
