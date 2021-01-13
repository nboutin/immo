#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json


class Database:

    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    __DATA_FILEPATH = os.path.join(__location__, 'data', 'database.json')

    def __init__(self):

        self._filepath = Database.__DATA_FILEPATH

        with open(self._filepath, 'r') as file:
            data = json.load(file)

        self._impot_data = data['impot']

    @property
    def salaire_abattement(self):
        return self._impot_data['salaire_abattement']

    def irpp_bareme(self, annee):
        if isinstance(annee, int):
            annee = str(annee)
        try:
            return self._impot_data['irpp_bareme'][annee]
        except KeyError:
            return self._impot_data['irpp_bareme']['2021']

    def plafond_quotient_familial(self, annee):
        if isinstance(annee, int):
            annee = str(annee)
        try:
            return self._impot_data['plafond_quotient_familial'][annee]
        except KeyError:
            return self._impot_data['plafond_quotient_familial']['2021']

    @property
    def reduction_dons(self):
        return self._impot_data['reduction']['dons']

    @property
    def reduction_syndicat(self):
        return self._impot_data['reduction']['syndicat']

    @property
    def prelevement_sociaux_taux(self):
        return self._impot_data['prelevement_sociaux_taux']

    @property
    def micro_foncier_taux(self):
        return self._impot_data['micro_foncier']['taux']

    @property
    def micro_foncier_revenu_foncier_plafond(self):
        return self._impot_data['micro_foncier']['revenu_foncier_plafond']

    @property
    def deficit_foncier_plafond_annuel(self):
        return self._impot_data['deficit_foncier_plafond']
