#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from openfisca_france import FranceTaxBenefitSystem
from openfisca_core.simulation_builder import SimulationBuilder

from .ligne_definition import *

entities = {
    'individus': {'Nicolas': {},
                  'Audrey': {},
                  'Lya': {}},
    'foyers_fiscaux': {'foyer1': {'declarants': ['Nicolas', 'Audrey'],
                                  'personnes_a_charge': ['Lya']}},
    'menages': {'roles': {'personne_de_reference': 'Nicolas',
                          'conjoint': 'Audrey',
                          'enfants': 'Lya'}},
    'familles': {'roles': {'parents': ['Nicolas', 'Audrey'],
                           'enfants': ['Lya']}},
}


class IRPP:

    def __init__(self):
        self._tax_benefit_system = FranceTaxBenefitSystem()
        self._simulation_builder = SimulationBuilder()
        self._sim = self._simulation_builder.build_from_entities(self._tax_benefit_system, entities)

        self._annexe = dict()  # Key is str(year)

    def set_input(self, variable: str, annee: str, values):
        self._sim.set_input(variable, annee, values)

    def calculate(self, variable: str, annee: str):
        return self._sim.calculate(variable, annee)

    def set_annexe(self, annee: str, annexe):
        self._annexe[annee] = annexe

        L4BA = annexe.sum_ligne(L4BA_benefice_foncier)
        L4BB = annexe.sum_ligne(L4BB_deficit_foncier_imputable_revenu_foncier)
        L4BC = annexe.sum_ligne(L4BC_deficit_foncier_imputable_revenu_global)
        L4BD = annexe.sum_ligne(L4BD_deficit_foncier_anterieur)

        self._sim.set_input('f4ba', annee, L4BA)
        self._sim.set_input('f4bb', annee, L4BB)
        self._sim.set_input('f4bc', annee, L4BC)
        self._sim.set_input('f4bd', annee, L4BD)

    @property
    def annexe(self):
        return self._annexe

    def impots_sans_revenu_foncier(self, annee: str):
        salaires = self._sim.calculate_add('salaire_imposable', annee)
        sim = self._simulation_builder.build_from_entities(self._tax_benefit_system, entities)
        sim.set_input('salaire_imposable', annee, salaires)
        return abs(sim.calculate('irpp', annee)[0])

    def impots_revenu_foncier(self, annee: str):
        irpp_rf = self._sim.calculate('irpp', annee)
        return abs(irpp_rf[0]) - self.impots_sans_revenu_foncier(annee)
