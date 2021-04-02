#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from analyse_immo.database import Database
from analyse_immo.impots.irpp import IRPP
from analyse_immo.impots.annexe_2044 import Annexe_2044
from analyse_immo.impots.ligne_definition import *


class TestIRPP(unittest.TestCase):

    def setUp(self):
        self.database = Database()

    def test0_Init(self):
        _ = IRPP()

    def test1_RevenuFiscaleReference(self):
        annee = '2020'
        irpp = IRPP()
        irpp.set_input('salaire_imposable', annee, [31407, 23055, 0])
        self.assertEqual(irpp.calculate('rbg', annee), [49015])

    @unittest.skip('deprecated')
    def test2_ImpotBrutInternal(self):
        irpp = IRPP(self.database, 0)
        tmi = [[10084, 0], [25710, 0.11], [73516, 0.30], [158122, 0.41]]

        ibrut = irpp._impots_brut(tmi, 5000)
        self.assertEqual(ibrut, 0)

        ibrut = irpp._impots_brut(tmi, 10000)
        self.assertEqual(ibrut, 0)

        ibrut = irpp._impots_brut(tmi, 10084)
        self.assertEqual(ibrut, 0)

        ibrut = irpp._impots_brut(tmi, 10085)
        self.assertEqual(ibrut, 0)

        ibrut = irpp._impots_brut(tmi, 10086)
        self.assertEqual(ibrut, 0.11)

        ibrut = irpp._impots_brut(tmi, 15000)
        self.assertAlmostEqual(ibrut, 540.65, 2)

        ibrut = irpp._impots_brut(tmi, 20000)
        self.assertAlmostEqual(ibrut, 1090.65, 2)

        ibrut = irpp._impots_brut(tmi, 30000)
        self.assertAlmostEqual(ibrut, 3005.45, 2)

        ibrut = irpp._impots_brut(tmi, 80000)
        self.assertAlmostEqual(ibrut, 18718.28, 2)

    def test3_ImpotBrut(self):
        annee = '2019'
        irpp = IRPP()
        irpp.set_input('salaire_imposable', annee, [31407, 23055, 0])
        self.assertEqual(irpp.calculate('irpp', annee), [-3340])

    def test4_ImpotNet(self):
        annee = '2019'
        irpp = IRPP()
        irpp.set_input('salaire_imposable', annee, [31407, 23055, 0])
        irpp.set_input('f7ac', annee, [0, 143, 0])
        irpp.set_input('f7uf', annee, 200)
        self.assertEqual(irpp.calculate('irpp', annee), [-3114])

    def test5_ImpotSansRevenuFoncierA1(self):
        annee = '2019'
        irpp = IRPP()
        irpp.set_input('salaire_imposable', annee, [31407, 23055, 0])
        impot = abs(irpp.calculate('irpp', annee)[0])
        self.assertEqual(irpp.impot_revenu_foncier(annee), 0)
        self.assertEqual(irpp.impot_sans_revenu_foncier(annee), [-impot])

    def test5_ImpotSansRevenuFoncierA2(self):
        annee = '2021'
        irpp = IRPP()
        irpp.set_input('salaire_imposable', annee, [31407, 23055, 0])

        impot = round(((31407 + 23055) * .9 / 2.5 - 10084) * 2.5 * .11)
        decote = round(1289 - (impot * .4525))
        impot -= decote

        self.assertEqual(decote, irpp.calculate('decote', annee))
        self.assertEqual([-impot], irpp.calculate('irpp', annee))

        self.assertEqual(irpp.impot_revenu_foncier(annee), 0)
        self.assertEqual(irpp.impot_sans_revenu_foncier(annee), [-impot])

    def test5_ImpotSansRevenuFoncierB(self):
        import math
        annee = '2021'

        loyer = 5000
        revenu = (31407 + 23055) * .9 + loyer
        impot_salaire = round(((31407 + 23055) * .9 / 2.5 - 10084) * 2.5 * .11)
        impot_salaire -= round(1289 - (impot_salaire * .4525))
        impot = round((revenu / 2.5 - 10084) * 2.5 * .11)
        ps = round(loyer * .172)

        irpp = IRPP()
        irpp.set_input('salaire_imposable', annee, [31407, 23055, 0])
        an_2044 = Annexe_2044(self.database)
        an_2044.add_ligne(L211_loyer_brut, loyer)
        irpp.set_annexe(annee, an_2044)

        self.assertEqual(impot, 3169)
        self.assertEqual(impot_salaire, 2515)
        self.assertEqual(ps, 860)

        self.assertEqual(irpp.calculate('revenu_categoriel_foncier', annee), loyer)
        self.assertEqual(irpp.calculate('rbg', annee), [math.floor(revenu)])

        self.assertEqual(irpp.calculate('irpp', annee)[0], -impot)
        self.assertEqual(irpp.calculate('prelevements_sociaux_revenus_capital', annee), [-ps])
        self.assertEqual(irpp.impot_du(annee), [-(impot + ps)])
        self.assertEqual(irpp.impot_sans_revenu_foncier(annee), [-impot_salaire])
        self.assertEqual(irpp.impot_revenu_foncier(annee), [-(impot + ps - impot_salaire)])

    @unittest.skip('deprecated')
    def test5_ImpotSansRevenuFoncierC(self):
        irpp = IRPP(self.database, 2020)
        irpp.add_ligne(LN_nombre_de_part, 2.5)
        irpp.add_ligne(L4_personne_a_charge, 1)
        irpp.add_ligne(L1AJ_salaire, 31500)
        irpp.add_ligne(L1BJ_salaire, 23100)

        self.assertAlmostEqual(irpp.sum_ligne(L9_impot_du), 2632, 0)
        self.assertAlmostEqual(irpp.impot_sans_revenu_foncier, 2632, 0)

        annexe_2044 = Annexe_2044(self.database)
        annexe_2044.add_ligne(L211_loyer_brut, 2212)
        irpp.annexe_2044 = annexe_2044

        self.assertAlmostEqual(irpp.sum_ligne(L4_revenus_ou_deficits_nets_fonciers), 2212, 2)
        self.assertAlmostEqual(irpp.sum_ligne(L9PS_prelevement_sociaux), 2212 * .172, 2)
        self.assertEqual(irpp.sum_ligne(L1_5_revenu_brut_global), 51352)
        self.assertAlmostEqual(irpp.sum_ligne(LQ_quotient_familial), 20541, 0)
        self.assertAlmostEqual(irpp.sum_ligne(L9_impot_du), 2875 + 2212 * .172, 0)
        self.assertAlmostEqual(irpp.impot_sans_revenu_foncier, 2632, 0)
        self.assertAlmostEqual(irpp.impots_revenu_foncier, 243 + 2212 * .172, 0)

    @unittest.skip('deprecated')
    def test6_Exemple01(self):
        '''
        https://www.service-public.fr/particuliers/actualites/A14556?xtor=EPR-141
        '''
        irpp = IRPP(self.database, 2020)
        irpp.add_ligne(LN_nombre_de_part, 3)
        irpp.add_ligne(L4_personne_a_charge, 2)
        irpp.add_ligne(L1AJ_salaire, 55950 / 0.9)

        self.assertEqual(irpp.sum_ligne(L1_5_revenu_brut_global), 55950)
        self.assertEqual(irpp.sum_ligne(LQ_quotient_familial), 18650)
        self.assertAlmostEqual(irpp.sum_ligne(LI_impot), 2826.45, 2)
        self.assertAlmostEqual(irpp.sum_ligne(L9_impot_du), 2826.45, 2)

    @unittest.skip('deprecated')
    def test6_Exemple02(self):
        '''
        https://www.service-public.fr/particuliers/vosdroits/F1419
        '''
        irpp = IRPP(self.database, 2020)
        irpp.add_ligne(LN_nombre_de_part, 1)
        irpp.add_ligne(L4_personne_a_charge, 0)
        irpp.add_ligne(L1AJ_salaire, 30000 / 0.9)

        self.assertAlmostEqual(irpp.sum_ligne(L1_5_revenu_brut_global), 30000, 0)
        self.assertAlmostEqual(irpp.sum_ligne(LQ_quotient_familial), 30000, 0)
        self.assertAlmostEqual(irpp.sum_ligne(L9_impot_du), 3005.45, 2)

    @unittest.skip('deprecated')
    def test6_Exemple03(self):
        '''
        https://www.service-public.fr/particuliers/vosdroits/F1419
        '''
        irpp = IRPP(self.database, 2020)
        irpp.add_ligne(LN_nombre_de_part, 2)
        irpp.add_ligne(L4_personne_a_charge, 0)
        irpp.add_ligne(L1AJ_salaire, 60000 / 0.9)

        self.assertAlmostEqual(irpp.sum_ligne(L1_5_revenu_brut_global), 60000, 0)
        self.assertAlmostEqual(irpp.sum_ligne(LQ_quotient_familial), 30000, 0)
        self.assertAlmostEqual(irpp.sum_ligne(L9_impot_du), 6010.9, 2)

    @unittest.skip('deprecated')
    def test6_Exemple04(self):
        '''
        https://www.service-public.fr/particuliers/vosdroits/F2705
        '''
        # Sans plafonnement
        irppA = IRPP(self.database, 2020)
        irppA.add_ligne(LN_nombre_de_part, 2)
        irppA.add_ligne(L4_personne_a_charge, 0)
        irppA.add_ligne(L1AJ_salaire, 63000 / 0.9)

        self.assertAlmostEqual(irppA.sum_ligne(L1_5_revenu_brut_global), 63000, 0)
        self.assertAlmostEqual(irppA.sum_ligne(LQ_quotient_familial), 31500, 0)
        self.assertAlmostEqual(irppA.sum_ligne(L9_impot_du), 6910.90, 2)

        # Avec plafonnement
        irpp = IRPP(self.database, 2020)
        irpp.add_ligne(LN_nombre_de_part, 2.5)
        irpp.add_ligne(L4_personne_a_charge, 1)
        irpp.add_ligne(L1AJ_salaire, 63000 / 0.9)

        self.assertAlmostEqual(irpp.sum_ligne(L1_5_revenu_brut_global), 63000, 0)
        self.assertAlmostEqual(irpp.sum_ligne(LQ_quotient_familial), 25200, 0)
        self.assertAlmostEqual(irpp.sum_ligne(L6A_plafonnement_quotient_familial), irppA.sum_ligne(L9_impot_du), 0)
        self.assertAlmostEqual(irpp.sum_ligne(L6B_plafonnement_quotient_familial), 1570, 0)
        self.assertAlmostEqual(irpp.sum_ligne(L6C_plafonnement_quotient_familial), 5341, 0)
        self.assertAlmostEqual(irpp.sum_ligne(L9_impot_du), 5341, 0)

    @unittest.skip('deprecated')
    def test6_Exemple06(self):
        '''
        http://impotsurlerevenu.org/exemple/124-celibataire-sans-enfant-revenus-eleves.php
        '''
        irpp = IRPP(self.database, 2018)
        irpp.add_ligne(LN_nombre_de_part, 1)
        irpp.add_ligne(L4_personne_a_charge, 0)
        irpp.add_ligne(L1AJ_salaire, 37133)

        self.assertAlmostEqual(irpp.sum_ligne(L1_5_revenu_brut_global), 37133 * .9, 0)
        self.assertAlmostEqual(irpp.sum_ligne(LQ_quotient_familial), 33420, 0)
        self.assertAlmostEqual(irpp.sum_ligne(L9_impot_du), 4227, 0)

    @unittest.skip('deprecated')
    def test6_Exemple07(self):
        '''
        http://impotsurlerevenu.org/exemple/125-couple-marie-sans-enfant-revenus-eleves.php
        '''
        irpp = IRPP(self.database, 2018)
        irpp.add_ligne(LN_nombre_de_part, 2)
        irpp.add_ligne(L4_personne_a_charge, 0)
        irpp.add_ligne(L1AJ_salaire, 119564)

        self.assertAlmostEqual(irpp.sum_ligne(L1_5_revenu_brut_global), 119564 * .9, 0)
        self.assertAlmostEqual(irpp.sum_ligne(LQ_quotient_familial), 53804, 0)
        self.assertAlmostEqual(irpp.sum_ligne(L9_impot_du), 20685.4, 1)

    @unittest.skip('deprecated')
    def test6_Exemple08(self):
        '''
        http://impotsurlerevenu.org/exemple/126-couple-marie-sans-enfant-revenus-modestes.php
        '''
        irpp = IRPP(self.database, 2018)
        irpp.add_ligne(LN_nombre_de_part, 2)
        irpp.add_ligne(L4_personne_a_charge, 0)
        irpp.add_ligne(L1AJ_salaire, 44467)

        self.assertAlmostEqual(irpp.sum_ligne(L1_5_revenu_brut_global), 44467 * .9, 0)
        self.assertAlmostEqual(irpp.sum_ligne(LQ_quotient_familial), 20010, 0)
        self.assertAlmostEqual(irpp.sum_ligne(L9_impot_du), 2813, 0)

    @unittest.skip('deprecated')
    def test6_Exemple10(self):
        '''
        http://impotsurlerevenu.org/exemple/128-couple-marie-avec-enfants-aux-revenus-modestes.php
        '''
        irpp = IRPP(self.database, 2018)
        irpp.add_ligne(LN_nombre_de_part, 3)
        irpp.add_ligne(L4_personne_a_charge, 1)
        irpp.add_ligne(L1AJ_salaire, 39519)

        self.assertAlmostEqual(irpp.sum_ligne(L1_5_revenu_brut_global), 39519 * .9, 0)
        self.assertAlmostEqual(irpp.sum_ligne(LQ_quotient_familial), 11856, 0)
        self.assertAlmostEqual(irpp.sum_ligne(L9_impot_du), 794, 0)

    @unittest.skip('deprecated')
    def test6_Exemple11(self):
        '''
        http://impotsurlerevenu.org/exemple/129-couple-marie-avec-enfants-revenus-eleves.php
        '''
        irpp = IRPP(self.database, 2018)
        irpp.add_ligne(LN_nombre_de_part, 3)
        irpp.add_ligne(L4_personne_a_charge, 2)
        irpp.add_ligne(L1AJ_salaire, 123895)

        self.assertAlmostEqual(irpp.sum_ligne(L1_5_revenu_brut_global), 123895 * .9, 0)
        self.assertAlmostEqual(irpp.sum_ligne(LQ_quotient_familial), 37169, 0)
        self.assertAlmostEqual(irpp.sum_ligne(L9_impot_du), 18753, 0)

    @unittest.skip('deprecated')
    def test6_Exemple12(self):
        '''
        http://impotsurlerevenu.org/exemple/130-couple-marie-avec-1-enfant-aux-revenus-eleves.php
        '''
        irpp = IRPP(self.database, 2018)
        irpp.add_ligne(LN_nombre_de_part, 2.5)
        irpp.add_ligne(L4_personne_a_charge, 1)
        irpp.add_ligne(L1AJ_salaire, 85331)

        self.assertAlmostEqual(irpp.sum_ligne(L1_5_revenu_brut_global), 85331 * .9, 0)
        self.assertAlmostEqual(irpp.sum_ligne(LQ_quotient_familial), 30719, 0)
        self.assertAlmostEqual(irpp.sum_ligne(L9_impot_du), 9891, 0)

    @unittest.skip('deprecated')
    def test6_Exemple20(self):
        '''
        http://impotsurlerevenu.org/nouveautes-impot-2019/1203-bareme-impot-2019.php
        '''
        irpp = IRPP(self.database, 2018)
        irpp.add_ligne(LN_nombre_de_part, 3)
        irpp.add_ligne(L4_personne_a_charge, 2)
        irpp.add_ligne(L1AJ_salaire, 60000 / 0.9)

        self.assertAlmostEqual(irpp.sum_ligne(L1_5_revenu_brut_global), 60000, 0)
        self.assertAlmostEqual(irpp.sum_ligne(LQ_quotient_familial), 20000, 0)
        self.assertAlmostEqual(irpp.sum_ligne(L9_impot_du), 4215, 0)

    @unittest.skip('deprecated')
    def test6_Exemple21(self):
        '''
        http://impotsurlerevenu.org/comprendre-le-calcul-de-l-impot/1194-calcul-de-l-impot-2018.php
        '''
        irpp = IRPP(self.database, 2017)
        irpp.add_ligne(LN_nombre_de_part, 3)
        irpp.add_ligne(L4_personne_a_charge, 2)
        irpp.add_ligne(L1AJ_salaire, 89000 / 0.9)

        self.assertAlmostEqual(irpp.sum_ligne(L1_5_revenu_brut_global), 89000, 0)
        self.assertAlmostEqual(irpp.sum_ligne(LQ_quotient_familial), 29667, 0)
        self.assertAlmostEqual(irpp.sum_ligne(L9_impot_du), 12232, 0)


class TestIRPPAnnexe2044(unittest.TestCase):

    def setUp(self):
        self.database = Database()

    def testAnnexe2044(self):
        annee = '2021'
        irpp = IRPP()
        irpp.set_input('salaire_imposable', annee, [30000, 20000, 0])
        annexe_2044 = Annexe_2044(self.database)
        annexe_2044.add_ligne(L211_loyer_brut, 6000)
        irpp.set_annexe(annee, annexe_2044)

        self.assertEqual(irpp.calculate('rni', annee), 50000 * .9 + 6000)
        self.assertTrue(isinstance(irpp.annexe[annee], Annexe_2044))


if __name__ == '__main__':
    unittest.main()
