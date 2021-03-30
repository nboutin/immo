
import unittest

from openfisca_france import FranceTaxBenefitSystem
from openfisca_core.simulation_builder import SimulationBuilder

E1 = {
    'individus': {'Nicolas': {'revenu_assimile_salaire': {'2019': 20000}},
                  'Audrey': {'revenu_assimile_salaire': {'2019': 15000}},
                  'Lya': {}},
    'foyers_fiscaux': {'foyer1': {'declarants': ['Nicolas', 'Audrey'],
                                  'personnes_a_charge': ['Lya'],
                                  # 'f4ba': {'year:2020', 10000}
                                  }},
    'menages': {'roles': {'personne_de_reference': 'Nicolas',
                          'conjoint': 'Audrey',
                          'enfants': 'Lya'}},
    'familles': {'roles': {'parents': ['Nicolas', 'Audrey'],
                           'enfants': ['Lya']}},
}

E2 = {
    'individus': {'I1': {}},
    'foyers_fiscaux': {'f1': {'declarants': ['I1']}}
}


class TestRevenuFoncier(unittest.TestCase):

    def setUp(self):
        tax_benefit_system = FranceTaxBenefitSystem()
        simulation_builder = SimulationBuilder()
        self.sim = simulation_builder.build_from_entities(tax_benefit_system, E2)

    def test01(self):
        annee = '2021'
        self.sim.set_input('revenu_assimile_salaire', annee, 30000)
        self.assertEqual(self.sim.calculate('irpp', annee), (30000 * .9 - 10084) * .11)

    def test02(self):
        annee = '2020'
        self.sim.set_input('f4ba', annee, 10000)
        self.assertEqual(self.sim.calculate('revenu_categoriel_foncier', annee), [10000])


if __name__ == '__main__':
    unittest.main()
