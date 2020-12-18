#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
from enum import unique, Enum, auto


class Credit:

    @unique
    class mode_e(Enum):
        m1 = auto()  # mensualite constant, assurance capital initial
        m2 = auto()  # mensualite constant, assurance capital restant
        m3 = auto()  # mensualite degressive, assurance capital restant mensuel
        m4 = auto()  # mensualite degressive, assurance capital restant annuel

    def __init__(self, capital, duree_mois, taux, taux_assurance, mode, frais_dossier, frais_garantie):

        self._capital = capital
        self._duree_mois = duree_mois
        self._taux = taux
        self._mode = mode
        self._taux_assurance = taux_assurance
        self._frais_dossier = frais_dossier
        self._frais_garantie = frais_garantie
        self._tam = []
        self._tam_total = {'amortissement': 0, 'interet': 0,
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

    # Static
    @staticmethod
    def _calcul_mensualite_constante(capital, taux, duree_mois):
        '''
        Calcul de base pour connaitre la mensualite constante de remboursement
        Assurance non-comprise
        mensualite = ( capital_emprunte * taux_interet/12) / 1 - (1 + taux_interet / 12) ^ - duree_mois
        :return: mensualite
        '''
        if capital == 0 or taux == 0 or duree_mois == 0:
            return 0
        return (capital * taux / 12) / (1 - math.pow(1 + taux / 12, -duree_mois))

    @staticmethod
    def _calcul_mensualite_assurance_capital_constant(capital, taux_assurance):
        '''Calcul mensualite d'assurance sur capital constant'''
        return capital * (taux_assurance / 12)

    # Mensualite
    def get_amortissement(self, start=1, stop=None):
        '''
        :param start: first month
        :param stop: last month (included)
        '''
        if not stop:
            stop = start
        return sum(item['amortissement'] for item in self._tam[start - 1:stop])

    def get_interet(self, start=1, stop=None):
        if not stop:
            stop = start
        return sum(item['interet'] for item in self._tam[start - 1:stop])

    def get_mensualite_hors_assurance(self, start=1, stop=None):
        if not stop:
            stop = start
        return sum(item['mensualite_ha'] for item in self._tam[start - 1:stop])

    def get_mensualite_assurance(self, start=1, stop=None):
        '''
        :return montant mensuel de l'assurance
        '''
        if not stop:
            stop = start
        return sum(item['assurance'] for item in self._tam[start - 1:stop])

    def get_mensualite_avec_assurance(self, start=1, stop=None):
        '''
        :return montant mensualite assurance incluse
        '''
        if not stop:
            stop = start
        return sum(item['mensualite_aa'] for item in self._tam[start - 1:stop])

    def get_tableau_amortissement(self, start=1, stop=None):
        if not stop:
            return self._tam[start - 1]
        else:
            return self._tam[start - 1:stop]

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
        '''
        mode calcul possible:
            - mode_1: mensualite constant, assurance capital initial
            - mode_2: mensualite constant, assurance capital restant
            - mode_3: mensualite degressive, assurance capital restant
            - mode_4: mensualite degressive, assurance capital restant annuel
        '''
        capital_restant = self._capital
        mensualite_ha = Credit._calcul_mensualite_constante(self._capital, self._taux, self._duree_mois)
        mensualite_aa = Credit._calcul_mensualite_constante(
            self._capital, self._taux + self._taux_assurance, self._duree_mois)
        assurance = self._calcul_mensualite_assurance_capital_constant(self._capital, self._taux_assurance)

        # Calcul
        for mois in range(self._duree_mois):
            interet = capital_restant * self._taux / 12

            if self._mode == Credit.mode_e.m1:
                amortissement = mensualite_ha - interet
                mensualite_aa = mensualite_ha + assurance

            elif self._mode == Credit.mode_e.m2:
                assurance = capital_restant * self._taux_assurance / 12
                amortissement = mensualite_aa - interet - assurance
                mensualite_ha = mensualite_aa - assurance

            elif self._mode == Credit.mode_e.m3:
                assurance = capital_restant * self._taux_assurance / 12
                amortissement = mensualite_ha - interet
                mensualite_aa = mensualite_ha + assurance

            elif self._mode == Credit.mode_e.m4:
                if mois % 12 == 0:
                    assurance = capital_restant * self._taux_assurance / 12
                amortissement = mensualite_ha - interet
                mensualite_aa = mensualite_ha + assurance

            self._tam.append({'capital': capital_restant,
                              'amortissement': amortissement,
                              'interet': interet,
                              'assurance': assurance,
                              'mensualite_ha': mensualite_ha,
                              'mensualite_aa': mensualite_aa})

            capital_restant -= amortissement

            self._tam_total['amortissement'] += amortissement
            self._tam_total['interet'] += interet
            self._tam_total['assurance'] += assurance
            self._tam_total['mensualite_ha'] += mensualite_ha
            self._tam_total['mensualite_aa'] += mensualite_aa
