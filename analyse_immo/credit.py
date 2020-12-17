#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
from enum import unique, Enum, auto


class Credit:

    @unique
    class mensualite_e(Enum):
        constante = auto()
        degressive = auto()

    @unique
    class assurance_e(Enum):
        capital_initial = auto()
        capital_restant = auto()

    def __init__(self, capital, duree_mois, taux, mensualite_mode,
                 taux_assurance, assurance_mode, frais_dossier, frais_garantie):
        '''
        - mode_1: mensualite constant, assurance capital initial
        - mode_2: mensualite constant, assurance capital restant
        - mode_3: mensualite degressive, assurance capital restant mensuel
        - mode_4: mensualite degressive, assurance capital restant annuel
        '''
        self._capital = capital
        self._duree_mois = duree_mois
        self._taux = taux
        self._mensualite_mode = mensualite_mode
        self._taux_assurance = taux_assurance
        self._assurance_mode = assurance_mode
        self._frais_dossier = frais_dossier
        self._frais_garantie = frais_garantie
        self._tam = []
        self._tam_total = {'amortissement': 0, 'interet': 0,
                           'assurance': 0, 'mensualite_ha': 0, 'mensualite_aa': 0}

        self._calcul_tableau_amortissement()

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

#     @property
#     def mode(self):
#         return self._mode

    @staticmethod
    def _calcul_mensualite_constante(capital, taux, duree_mois):
        '''
        Calcul de base pour connaitre la mensualite constante de remboursement
        Assurance non-comprise
        mensualite = ( capital_emprunte * taux_interet/12) / 1 - (1 + taux_interet / 12) ^ - duree_mois
        @return: mensualite
        '''
        return (capital * taux / 12) / (1 - math.pow(1 + taux / 12, -duree_mois))

    @staticmethod
    def _calcul_mensualite_assurance_capital_constant(capital, taux_assurance):
        '''Calcul mensualite d'assurance sur capital constant'''
        return capital * (taux_assurance / 12)

    def get_mensualite_hors_assurance(self):
        if self._capital == 0 or self._taux == 0:
            return 0

        return Credit._calcul_mensualite_constante(self._capital, self._taux, self._duree_mois)

    def get_mensualite_assurance(self, mois=None):
        '''
        @todo Use parameter mois
        '''
        if not mois:
            mois = 1

        if self._mode == 'mode_1':
            return Credit._calcul_mensualite_assurance_capital_constant(
                self._capital, self._taux_assurance)
        else:
            return self._tam[mois - 1]['assurance']

    def get_mensualite_avec_assurance(self, mois=None):
        '''
        @todo Use parameter mois
        mode_1: return mensualite constante
        mode_2/3/4: return mensualite variable
        '''
        if self._mode == 'mode_1':
            return self._tam[0]['mensualite_aa']
        elif self._mode == 'mode2' or self._mode == 'mode_3':
            return self._tam[0]['mensualite_aa']
        else:
            return 0

    def get_mensualite_total(self):
        return self._tam_total['mensualite_aa']

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

    def get_amortissement(self, mois):
        '''
        1er mois = 1
        '''
        return self._tam[mois - 1]

    def _calcul_tableau_amortissement(self):
        '''
        mode calcul possible:
            - mode_1: mensualite constant, assurance capital initial
            - mode_2: mensualite constant, assurance capital restant
            - mode_3: mensualite degressive, assurance capital restant
            - mode_4: mensualite degressive, assurance capital restant annuel
        '''
        capital_restant = self._capital

        # Mensualite
        if self._mensualite_mode == Credit.mensualite_e.constante:
            mensualite_ha = Credit._calcul_mensualite_constante(self._capital, self._taux, self._duree_mois)

        elif self._mensualite_mode == Credit.mensualite_e.degressive:
            pass

        else:
            return

        # Assurance
        if self._assurance_mode == Credit.assurance_e.capital_initial:
            assurance = self._calcul_mensualite_assurance_capital_constant(
                self._capital, self._taux_assurance)

        elif self._assurance_mode == Credit.assurance_e.capital_restant:
            mensualite_aa = Credit._calcul_mensualite_constante(
                self._capital, self._taux + self._taux_assurance, self._duree_mois)

        else:
            return

#         if self._mode == 'mode_1':
#             mensualite_ha = self.get_mensualite_hors_assurance()
#             assurance = self.get_mensualite_assurance()
#
#         elif self._mode == 'mode_2':
#             mensualite_aa = self.get_mensualite_hors_assurance(
#                 self._taux + self._taux_assurance)
#
#         elif self._mode == 'mode_3' or self._mode == 'mode_4':
#             mensualite_ha = self.get_mensualite_hors_assurance()
#
#         else:
#             return

        for mois in range(self._duree_mois):
            interet = capital_restant * self._taux / 12

            if self._mode == 'mode_1':
                amortissement = mensualite_ha - interet
                mensualite_aa = mensualite_ha + assurance

            elif self._mode == 'mode_2':
                assurance = capital_restant * self._taux_assurance / 12
                amortissement = mensualite_aa - interet - assurance
                mensualite_ha = mensualite_aa - assurance

            elif self._mode == 'mode_3':
                assurance = capital_restant * self._taux_assurance / 12
                amortissement = mensualite_ha - interet
                mensualite_aa = mensualite_ha + assurance

            elif self._mode == 'mode_4':
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
