#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from openfisca_france import FranceTaxBenefitSystem
from openfisca_core.simulation_builder import SimulationBuilder

from .ligne_definition import *

_ENTITIES = {
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

    def __init__(self, entities=None):
        self._entities = entities
        if not entities:
            self._entities = _ENTITIES

        self._tax_benefit_system = FranceTaxBenefitSystem()
        self._simulation_builder = SimulationBuilder()
        self._sim = self._simulation_builder.build_from_entities(self._tax_benefit_system, self._entities)

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

    def impot_du(self, annee: str):
        irpp = self._sim.calculate('irpp', annee)
        ps = self._sim.calculate('prelevements_sociaux_revenus_capital', annee)
        return irpp + ps

    def impot_sans_revenu_foncier(self, annee: str):
        salaires = self._sim.calculate_add('salaire_imposable', annee)
        sim = self._simulation_builder.build_from_entities(self._tax_benefit_system, self._entities)
        sim.set_input('salaire_imposable', annee, salaires)
        return sim.calculate('irpp', annee)

    def impot_revenu_foncier(self, annee: str):
        return self.impot_du(annee) - self.impot_sans_revenu_foncier(annee)
