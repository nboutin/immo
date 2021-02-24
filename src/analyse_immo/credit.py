#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import logging
from enum import unique, Enum, auto
from analyse_immo.tools import finance


class Credit:
    '''
    # TAEG :
    = taux debiteur + frais de dossier + cout assurance
    Utilise le taux actuariel

    # TAEA : Taux Annuel Effectif d'Assurance

    Assurance CI: Capital Initial
    Assurance CRD: Capital Restant Du
    Mensualité: Lisser ou Degressive

    # Source
    https://www.inc-conso.fr/content/comment-sont-calculees-les-mensualites-de-votre-emprunt
    https://www.moneyvox.fr/credit/principe.php

    # Simulateur
    https://www.moneyvox.fr/calculatrice/credit/emprunt.php
    https://www.moneyvox.fr/credit/tableau-amortissement.php
    https://www.calcamo.org/calcul-de-credit/
    https://www.lacentraledefinancement.fr/pret-credit-immobilier/les-simulateurs-de-prets-et-de-credit-immobilier/simulateur-tableau-amortissement-de-pret-immobilier/
    (Pas fiable) https://www.jechange.fr/credit/simulateur
    '''

    @unique
    class mode_e(Enum):
        fixe_CI = auto()
        fixe_CRD = auto()
        degressive_CRD = auto()

    @unique
    class taux_e(Enum):
        periodique = auto()
        actuariel = auto()

    def __init__(
            self,
            capital,
            duree_mois,
            taux_debiteur_fixe,
            taux_mode,
            taux_assurance,
            mode,
            frais_dossier,
            frais_garantie):

        self._capital = capital
        self._duree_mois = duree_mois
        self._taux = taux_debiteur_fixe
        self._taux_mode = taux_mode
        self._taux_assurance = taux_assurance
        self._mode = mode
        self._frais_dossier = frais_dossier
        self._frais_garantie = frais_garantie

        self._tam = []
        self._tam_total = {'capital': 0, 'amortissement': 0, 'interet': 0,
                           'assurance': 0, 'mensualite_ha': 0, 'mensualite_aa': 0}

        self._calcul_tableau_amortissement()

    # Attibut
    @property
    def capital(self):
        return self._capital

    @property
    def duree_mois(self):
        return self._duree_mois

    @property
    def taux(self):
        return self._taux

    @property
    def taux_assurance(self):
        return self._taux_assurance

    @property
    def mode(self):
        return self._mode

    @property
    def frais_dossier(self):
        return self._frais_dossier

    @property
    def frais_garantie(self):
        return self._frais_garantie

    @staticmethod
    def mensualite_periodique(capital, taux_periodique, duree_mois):
        '''
        echeance = (C * T) / (1 - (1 + T)^(-N))
        '''
        try:
            return (capital * taux_periodique) / (1 - math.pow(1 + taux_periodique, -duree_mois))
        except ZeroDivisionError:
            return 0

    # Mensualite
    def get_capital_restant(self, month=1):
        try:
            return self._tam[month - 1]['capital']
        except IndexError:
            return 0

    def get_amortissement(self, b_month=1, e_month=None):
        '''
        :param b_month: first month
        :param e_month: last month (included)
        '''
        if not e_month:
            e_month = b_month
        return sum(item['amortissement'] for item in self._tam[b_month - 1:e_month])

    def get_interet(self, b_month=1, e_month=None):
        if not e_month:
            e_month = b_month
        return sum(item['interet'] for item in self._tam[b_month - 1:e_month])

    def get_mensualite_hors_assurance(self, b_month=1, e_month=None):
        if not e_month:
            e_month = b_month
        return sum(item['mensualite_ha'] for item in self._tam[b_month - 1:e_month])

    def get_mensualite_assurance(self, b_month=1, e_month=None):
        '''
        :return montant mensuel de l'assurance
        '''
        if not e_month:
            e_month = b_month
        return sum(item['assurance'] for item in self._tam[b_month - 1:e_month])

    def get_mensualite_avec_assurance(self, b_month=1, e_month=None):
        '''
        :return montant mensualite assurance incluse
        '''
        if not e_month:
            e_month = b_month
        return sum(item['mensualite_aa'] for item in self._tam[b_month - 1:e_month])

    # Total
    def get_montant_interet_total(self):
        return self._tam_total['interet']

    def get_montant_assurance_total(self):
        return self._tam_total['assurance']

    def get_cout_total(self):
        return self.get_montant_interet_total() + self.get_montant_assurance_total() + \
            self._frais_dossier + self._frais_garantie

    def get_amortissement_total(self):
        return self._tam_total['amortissement']

    def get_mensualite_hors_assurance_total(self):
        return self._tam_total['mensualite_ha']

    def get_mensualite_avec_assurance_total(self):
        return self._tam_total['mensualite_aa']

    # Private
    def _calcul_tableau_amortissement(self):

        capital_restant = self._capital

        # Taux
        if self._taux_mode == Credit.taux_e.periodique:
            taux_periodique = finance.taux_periodique(self._taux, 12)
            taux_assurance_periodique = finance.taux_periodique(self._taux_assurance, 12)
        elif self._taux_mode == Credit.taux_e.actuariel:
            taux_periodique = Credit.taux_actuariel(self._taux, 12)
            taux_assurance_periodique = Credit.taux_actuariel(self._taux_assurance, 12)

        # Mode
        if self._mode == Credit.mode_e.fixe_CI:
            mensualite_ha = Credit.mensualite_periodique(self._capital, taux_periodique, self._duree_mois)
            assurance = self._capital * taux_assurance_periodique

        elif self._mode == Credit.mode_e.fixe_CRD:
            taux = taux_periodique + taux_assurance_periodique
            mensualite_aa = Credit.mensualite_periodique(self._capital, taux, self._duree_mois)

        elif self._mode == Credit.mode_e.degressive_CRD:
            mensualite_ha = Credit.mensualite_periodique(self._capital, taux_periodique, self._duree_mois)

        # Calcul
        for _ in range(self._duree_mois):

            if self._mode == Credit.mode_e.fixe_CI:
                interet = capital_restant * taux_periodique
                amortissement = mensualite_ha - interet
                mensualite_aa = mensualite_ha + assurance
                capital_restant -= amortissement

            elif self._mode == Credit.mode_e.fixe_CRD:
                interet = capital_restant * taux_periodique
                assurance = capital_restant * taux_assurance_periodique
                amortissement = mensualite_aa - interet - assurance
                mensualite_ha = mensualite_aa - assurance
                capital_restant -= amortissement

            elif self._mode == Credit.mode_e.degressive_CRD:
                interet = capital_restant * taux_periodique
                assurance = capital_restant * taux_assurance_periodique
                amortissement = mensualite_ha - interet
                mensualite_aa = mensualite_ha + assurance
                capital_restant -= amortissement

            else:
                break

            self._tam.append({'capital': capital_restant,
                              'amortissement': amortissement,
                              'interet': interet,
                              'assurance': assurance,
                              'mensualite_ha': mensualite_ha,
                              'mensualite_aa': mensualite_aa})

            self._tam_total['amortissement'] += amortissement
            self._tam_total['interet'] += interet
            self._tam_total['assurance'] += assurance
            self._tam_total['mensualite_ha'] += mensualite_ha
            self._tam_total['mensualite_aa'] += mensualite_aa
