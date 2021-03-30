
import unittest

from openfisca_france import FranceTaxBenefitSystem
from openfisca_core.simulation_builder import SimulationBuilder

annee = '2021'
E1 = {
    'individus': {'I1': {'salaire_imposable': {annee: 20000}},
                  'I2': {'salaire_imposable': {annee: 15000}},
                  'I3': {}},
    'foyers_fiscaux': {'f1': {'declarants': ['I1', 'I2'],
                              'personnes_a_charge': ['I3']}},
    'menages': {'roles': {'personne_de_reference': 'I1',
                          'conjoint': 'I2',
                          'enfants': 'I3'}},
    'familles': {'roles': {'parents': ['I1', 'I2'],
                           'enfants': ['I3']}},
}

E2 = {
    'individus': {'I1': {}},
    'foyers_fiscaux': {'f1': {'declarants': ['I1']}}
}

# self.sim.trace = True
# self.sim.tracer.print_computation_log()


class TestRevenuFoncier(unittest.TestCase):

    def setUp(self):
        tax_benefit_system = FranceTaxBenefitSystem()
        simulation_builder = SimulationBuilder()
        self.sim = simulation_builder.build_from_entities(tax_benefit_system, E2)

    def test01(self):
        salaire = 25000
        impot = (salaire * .9 - 10084) * .11
        decote = 779 - impot * .4525

        self.sim.set_input('salaire_imposable', annee, salaire)

        self.assertAlmostEqual(self.sim.calculate('ir_ss_qf', annee)[0], impot, 1)
        self.assertAlmostEqual(self.sim.calculate('decote', annee)[0], decote, 0)

        self.assertAlmostEqual(self.sim.calculate('irpp', annee)[0], -round(impot) + decote, 1)

    def test02(self):
        self.sim.set_input('f4ba', annee, 10000)
        self.assertEqual(self.sim.calculate('revenu_categoriel_foncier', annee), [10000])


if __name__ == '__main__':
    unittest.main()
