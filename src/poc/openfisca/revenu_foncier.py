
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

    def test04_A(self):
        annee = '2021'
        salaire = 25000
        base = (salaire * .9 - 10084) * .11
        decote = round(779 - base * .4525)
        impot = round(base - decote)
        self.sim.set_input('salaire_imposable', annee, salaire)
        self.assertEqual(self.sim.calculate('decote', annee), decote)
        self.assertEqual(self.sim.calculate('irpp', annee), [-impot])

    def test04_B(self):
        annee = '2021'
        salaire = 25000
        revenu_foncier = 500 * 12 * .60

        revenu = salaire * .9 + revenu_foncier
        t1 = (min(revenu, 25710) - 10084) * .11
        t2 = (min(revenu, 73516) - 25710) * .3
        base = t1 + t2
        decote = max(0, round(779 - base * .4525))
        impot = round(base - decote)

        self.sim.set_input('salaire_imposable', annee, salaire)
        self.sim.set_input('f4ba', annee, revenu_foncier)

        self.assertEqual(self.sim.calculate('decote', annee), decote)
        self.assertEqual(self.sim.calculate('irpp', annee), [-impot])

    def test05_A(self):

        E = {
            'individus': {'I1': {}, 'I2': {}, 'I3': {}},
            'foyers_fiscaux': {'f1': {'declarants': ['I1', 'I2'],
                                      'personnes_a_charge': ['I3']}}
        }

        tax_benefit_system = FranceTaxBenefitSystem()
        simulation_builder = SimulationBuilder()
        sim = simulation_builder.build_from_entities(tax_benefit_system, E)
        sim.trace = True

        import math
        annee = '2021'

        rbg = math.floor((31407 + 23055) * .9 + 5000)
        revenu = (31407 + 23055) * .9 + 5000
        t1 = (min(revenu, 25710) / 2.5 - 10084) * 2.5 * .11
        t2 = (min(revenu, 73516) / 2.5 - 25710) * 2.5 * .3
        impot = t1 + t2
        print('impot', impot)

        sim.set_input('salaire_imposable', annee, [31407, 23055, 0])
        sim.set_input('f4ba', annee, 5000)

        self.assertEqual(sim.calculate('revenu_categoriel_foncier', annee), 5000)
        self.assertEqual(sim.calculate('rbg', annee), [rbg])
        # PS 17,2 (CSG 9,2 CRDS 0,5 prelet solida 7,5)

        # 5000 * 17.2% = 860
        # 5000 * 9.2% = 460
        # 5000 * 0.5% = 25
        # 5000 * 7.5% = 375

        # csg [-495.    0.    0.]
        # prelevements_sociaux_revenus_capital_hors_csg_crds [-340.00003]
        # crds_revenus_capital [-25.]
        # total = 495+340+25 = 860

        # prelevements_sociaux.contributions.csg.capital.glob = 0.099

        print('csg_revenus_capital', sim.calculate('csg_revenus_capital', annee))
        print('csg', sim.calculate('csg', annee))
        print('prelevements_sociaux_revenus_capital_hors_csg_crds', sim.calculate(
            'prelevements_sociaux_revenus_capital_hors_csg_crds', annee))
        print('crds_revenus_capital', sim.calculate('crds_revenus_capital', annee))
        print('crds', sim.calculate('crds', annee))

        print('prelevements_sociaux_revenus_capital', sim.calculate('prelevements_sociaux_revenus_capital', annee))
        print('prelevement_forfaitaire_liberatoire', sim.calculate('prelevement_forfaitaire_liberatoire', annee))

        print('bouclier_imp_gen', sim.calculate('bouclier_imp_gen', annee))
        print('bouclier_sumimp', sim.calculate('bouclier_sumimp', annee))

        print('revenus_nets_du_capital', sim.calculate('revenus_nets_du_capital', annee))

        # print('total_impots_plafonnement_isf_ifi', sim.calculate('total_impots_plafonnement_isf_ifi', annee))
        # print('isf_ifi_avant_plaf', sim.calculate('isf_ifi_avant_plaf', annee))
        # print('isf_ifi_apres_plaf', sim.calculate('isf_ifi_apres_plaf', annee))
        # print('bouclier_imp_gen', sim.calculate('bouclier_imp_gen', annee))
        #
        # print('acomptes_ir', sim.calculate('acomptes_ir', annee))
        # print('irpp', sim.calculate('irpp', annee))
        # print('irpp_economique', sim.calculate('irpp_economique', annee))

        self.assertEqual(sim.calculate('crds', annee)[0], -5000 * 0.005)
        # self.assertEqual(sim.calculate('csg', annee)[0], -5000 * 0.092)

        self.assertEqual(sim.calculate('prelevements_sociaux_revenus_capital', annee)[0], round(-5000 * 0.172))
        # self.assertEqual(sim.calculate('prelevements_sociaux_revenus_capital_hors_csg_crds', annee), [-5000 * 0.075])
        # self.assertEqual(sim.calculate('crds_revenus_capital', annee), [-5000 * 0.005])
        # self.assertEqual(sim.calculate('crds', annee)[0], -5000 * 0.005)
        #
        # sim.tracer.print_computation_log()
        # irpp_impot = sim.calculate('irpp', annee)
        # self.assertEqual(irpp_impot, impot)

    def test05_B(self):

        E = {
            'individus': {'I1': {}, 'I2': {}, 'I3': {}},
            'foyers_fiscaux': {'f1': {'declarants': ['I1', 'I2'],
                                      'personnes_a_charge': ['I3']}}
        }

        tax_benefit_system = FranceTaxBenefitSystem()
        simulation_builder = SimulationBuilder()
        sim = simulation_builder.build_from_entities(tax_benefit_system, E)
        sim.trace = True

        annee = '2021'

        revenu = (31407 + 23055) * .9 + 5000  # 54015 / 2.5 = 21606
        impot = round((revenu / 2.5 - 10084) * 2.5 * .11)
        ps = round(5000 * 0.172)

        sim.set_input('salaire_imposable', annee, [31407, 23055, 0])
        sim.set_input('f4ba', annee, 5000)

        self.assertEqual(impot, 3169)
        self.assertEqual(ps, 860)

        self.assertEqual(sim.calculate('prelevements_sociaux_revenus_capital', annee)[0], round(-ps))
        self.assertEqual(sim.calculate('irpp', annee)[0], round(-impot))


if __name__ == '__main__':
    unittest.main()
