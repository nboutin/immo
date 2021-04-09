
import unittest

from openfisca_france import FranceTaxBenefitSystem
from openfisca_core.simulation_builder import SimulationBuilder

E1 = {
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


class TestIRPP(unittest.TestCase):

    def setUp(self):
        tax_benefit_system = FranceTaxBenefitSystem()
        simulation_builder = SimulationBuilder()
        self.sim = simulation_builder.build_from_entities(tax_benefit_system, E1)

    def test00a(self):
        '''
        variable period month
        set annee, get month
        '''
        annee = '2019'
        self.sim.set_input('salaire_de_base', annee, [12000, 0, 0])
        self.assertEqual(self.sim.calculate('salaire_de_base', '2019-01')[0], [1000])

    def test00b(self):
        '''
        variable period month
        set month, get year
        '''
        self.sim.set_input('salaire_de_base', '2019-01', [1000, 0, 0])
        self.sim.set_input('salaire_de_base', '2019-02', [2000, 0, 0])
        self.assertEqual(self.sim.calculate('salaire_de_base', '2019')[0], [3000])

    def test01(self):
        annee = '2019'
        self.sim.set_input('salaire_imposable', annee, [31407, 23055, 0])

        self.assertTrue(self.sim.calculate('maries_ou_pacses', annee))
        impot = round((((31407 + 23055) * .9 / 2.5) - 10064) * 2.5 * .14)
        self.assertEqual(self.sim.calculate('irpp', annee), [-impot])

    def test02(self):
        annee = '2019'
        self.sim.set_input('salaire_imposable', annee, [31407, 23055, 0])
        self.sim.set_input('f7ac', annee, [0, 143, 0])

        impot = round((((31407 + 23055) * .9 / 2.5) - 10064) * 2.5 * .14)
        impot = round(impot - 143 * .66)
        self.assertEqual(self.sim.calculate('credit_cotisations_syndicales', annee), 143 * .66)
        self.assertEqual(self.sim.calculate('irpp', annee), [-impot])

    def test03(self):
        annee = '2019'
        self.sim.set_input('salaire_imposable', annee, [31407, 23055, 0])
        self.sim.set_input('f7uf', annee, 200)
        impot = round((((31407 + 23055) * .9 / 2.5) - 10064) * 2.5 * .14)
        impot -= 200 * .66
        self.assertEqual(self.sim.calculate('irpp', annee), [-impot])

    def test04(self):
        annee = '2019'
        self.sim.set_input('salaire_imposable', annee, [31407, 23055, 0])
        self.sim.set_input('f7ac', annee, [0, 143, 0])
        self.sim.set_input('f7uf', annee, 200)
        impot = round((((31407 + 23055) * .9 / 2.5) - 10064) * 2.5 * .14)
        impot = round(impot - 200 * .66 - 143 * .66)
        self.assertEqual(self.sim.calculate('irpp', annee), [-impot])


if __name__ == '__main__':
    unittest.main()
