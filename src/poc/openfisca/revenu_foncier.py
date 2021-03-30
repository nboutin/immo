
import unittest

from openfisca_france import FranceTaxBenefitSystem
from openfisca_core.simulation_builder import SimulationBuilder

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
        annee = '2021'
        salaire = 25000
        impot = (salaire * .9 - 10084) * .11
        decote = 779 - impot * .4525

        self.sim.set_input('salaire_imposable', annee, salaire)

        self.assertAlmostEqual(self.sim.calculate('ir_ss_qf', annee)[0], impot, 1)
        self.assertAlmostEqual(self.sim.calculate('decote', annee)[0], decote, 0)

        self.assertAlmostEqual(self.sim.calculate('irpp', annee)[0], -round(impot) + decote, 1)

    def test02(self):
        annee = '2021'
        self.sim.set_input('f4ba', annee, 10000)
        self.assertEqual(self.sim.calculate('revenu_categoriel_foncier', annee), [10000])

    def test03_A(self):
        annee = '2021'
        salaire = 30000
        impot_revenu = 2106
        self.sim.set_input('salaire_imposable', annee, salaire)
        self.assertEqual(self.sim.calculate('irpp', annee), [-impot_revenu])

    def test03_B(self):
        '''
        Salaire 30K/an
        Revenuf foncier: 12K/an
        Interet emprunt: 2300/an
        Taxe Fonciere: 1000
        Assurance: 600
        Travaux: 40000

        Annee 1
        Charges = 2300 + 1000 + 600
        Revenu foncier impossable = 12K - charges - travaux = -31900
        revenu impossable= 30K - 10700 = 19300
        deficit reportable= 31900-10700 = 21200
        '''
        annee = '2021'
        salaire = 30000
        rfi = -31900  # revenu foncier impossable
        plafond = 10700
        decote = 470
        impot = round((((salaire * .9) - plafond) - 10084) * .11 - decote)

        self.sim.set_input('salaire_imposable', annee, salaire)

        self.sim.set_input('f4ba', annee, 0)
        self.sim.set_input('f4bb', annee, abs(rfi - plafond))
        self.sim.set_input('f4bc', annee, abs(plafond))
        self.sim.set_input('f4bd', annee, 0)

        self.assertEqual(self.sim.calculate('revenu_categoriel_foncier', annee), [-plafond])
        self.assertEqual(self.sim.calculate('decote', annee), decote)
        self.assertEqual(self.sim.calculate('irpp', annee), [-impot])

    def test03_C(self):
        '''
        Revenu foncier impossable = 12K - charges - deficit reportable = -13100
        revenu impossable = 30K
        deficit reportable= 13100
        '''
        annee = '2022'
        salaire = 30000
        rfi = -31900  # revenu foncier impossable
        plafond = 10700
        decote = 0
        impot = 2106

        self.sim.set_input('salaire_imposable', annee, salaire)

        self.sim.set_input('f4ba', annee, 8100)
        self.sim.set_input('f4bb', annee, 0)
        self.sim.set_input('f4bc', annee, 0)
        self.sim.set_input('f4bd', annee, abs(rfi - plafond))

        self.assertEqual(self.sim.calculate('revenu_categoriel_foncier', annee), 0)
        self.assertEqual(self.sim.calculate('decote', annee), decote)
        self.assertEqual(self.sim.calculate('irpp', annee), [-impot])


if __name__ == '__main__':
    unittest.main()
