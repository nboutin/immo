#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from analyse_immo.database import Database
from analyse_immo.impots.ligne import Ligne
from analyse_immo.impots.irpp import IRPP, L1AJ_salaire, L1BJ_salaire, L7UF_dons, L7AE_syndicat
from analyse_immo.impots.annexe_2044 import Annexe_2044, L211_loyer_brut


class TestLigne(unittest.TestCase):

    def testEqual(self):
        ligne = Ligne(100, 'nom')
        self.assertEqual(ligne, ligne)


class TestIRPP(unittest.TestCase):

    def setUp(self):
        self.database = Database()

    def testInit(self):
        _ = IRPP(None, 0, 0, 0)

    def testRevenuFiscaleReference(self):

        irpp = IRPP(self.database, 0, 0, 0)
        irpp.add_ligne(L1AJ_salaire, 31407)
        irpp.add_ligne(L1BJ_salaire, 23055)
        self.assertEqual(irpp.revenu_fiscale_reference, 49015.80, 2)

    def testImpotBrutInternal(self):
        irpp = IRPP(self.database, 0, 0, 0)
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

    def testImpotBrut(self):
        irpp = IRPP(self.database, 2019, 2.5, 1)
        irpp.add_ligne(L1AJ_salaire, 31407)
        irpp.add_ligne(L1BJ_salaire, 23055)
        self.assertAlmostEqual(irpp.impots_brut, 3339, 0)
        self.assertAlmostEqual(irpp.impots_brut, 3339.46, 2)

    def testImpotNet(self):
        irpp = IRPP(self.database, 2019, 2.5, 1)
        irpp.add_ligne(L1AJ_salaire, 31407)
        irpp.add_ligne(L1BJ_salaire, 23055)
        irpp.add_ligne(L7UF_dons, 200)
        irpp.add_ligne(L7AE_syndicat, 143)

        self.assertAlmostEqual(irpp.impots_net, 3113, 0)
        self.assertAlmostEqual(irpp.impots_net, 3113.08, 2)

    def testImpotSalaireNetA(self):
        irpp = IRPP(self.database, 2019, 2, 0)
        irpp.add_ligne(L1AJ_salaire, 30000)
        irpp.add_ligne(L1BJ_salaire, 20000)

        self.assertAlmostEqual(irpp.impots_net, 3482, 0)
        self.assertAlmostEqual(irpp.impots_salaires_net, 3482, 0)

        annexe_2044 = Annexe_2044(self.database)
        annexe_2044.add_ligne(L211_loyer_brut, 5000)
        irpp.annexe_2044 = annexe_2044

        self.assertAlmostEqual(annexe_2044.prelevement_sociaux, 5000 * .172, 2)
        self.assertEqual(irpp.revenu_fiscale_reference, 50000 * .9 + 5000)
        self.assertEqual(irpp.quotient_familial, (50000 * .9 + 5000) / 2)
        self.assertAlmostEqual(irpp.impots_net, 4182 + 5000 * .172, 0)
        self.assertAlmostEqual(irpp.impots_salaires_net, 3482, 0)

    def testImpotSalaireNetB(self):
        irpp = IRPP(self.database, 2020, 2.5, 1)
        irpp.add_ligne(L1AJ_salaire, 31500)
        irpp.add_ligne(L1BJ_salaire, 23100)

        self.assertAlmostEqual(irpp.impots_net, 2632, 0)
        self.assertAlmostEqual(irpp.impots_salaires_net, 2632, 0)

        annexe_2044 = Annexe_2044(self.database)
        annexe_2044.add_ligne(L211_loyer_brut, 2212)
        irpp.annexe_2044 = annexe_2044

        self.assertAlmostEqual(annexe_2044.prelevement_sociaux, 2212 * .172, 2)

        self.assertEqual(irpp.revenu_fiscale_reference, 51352)
        self.assertAlmostEqual(irpp.quotient_familial, 20541, 0)
        self.assertAlmostEqual(irpp.impots_net, 2875 + 2212 * .172, 0)
        self.assertAlmostEqual(irpp.impots_salaires_net, 2632, 0)
        self.assertAlmostEqual(irpp.impots_revenu_foncier, 243 + 2212 * .172, 0)

    def testExemple1(self):
        '''
        https://www.service-public.fr/particuliers/actualites/A14556?xtor=EPR-141
        '''
        irpp = IRPP(self.database, 2020, 3, 2)
        irpp.add_ligne(L1AJ_salaire, 55950 / 0.9)

        self.assertEqual(irpp.revenu_net_impossable, 55950)
        self.assertEqual(irpp.quotient_familial, 18650)
        self.assertAlmostEqual(irpp.impots_net, 2826.45, 2)
        self.assertAlmostEqual(irpp.impots_net, 2826, 0)

    def testExemple2(self):
        '''
        https://www.service-public.fr/particuliers/vosdroits/F1419
        '''
        irpp = IRPP(self.database, 2020, 1, 0)
        irpp.add_ligne(L1AJ_salaire, 30000 / 0.9)

        self.assertAlmostEqual(irpp.revenu_net_impossable, 30000, 0)
        self.assertAlmostEqual(irpp.quotient_familial, 30000, 0)
        self.assertAlmostEqual(irpp.impots_net, 3005.45, 2)
        self.assertAlmostEqual(irpp.impots_net, 3005, 0)

    def testExemple3(self):
        '''
        https://www.service-public.fr/particuliers/vosdroits/F1419
        '''
        irpp = IRPP(self.database, 2020, 2, 0)
        irpp.add_ligne(L1AJ_salaire, 60000 / 0.9)

        self.assertAlmostEqual(irpp.revenu_net_impossable, 60000, 0)
        self.assertAlmostEqual(irpp.quotient_familial, 30000, 0)
        self.assertAlmostEqual(irpp.impots_net, 6010.9, 2)

    def testExemple4(self):
        '''
        https://www.service-public.fr/particuliers/vosdroits/F2705
        '''
        # Sans plafonnement
        irpp = IRPP(self.database, 2020, 2, 0)
        irpp.add_ligne(L1AJ_salaire, 63000 / 0.9)

        self.assertAlmostEqual(irpp.revenu_net_impossable, 63000, 0)
        self.assertAlmostEqual(irpp.quotient_familial, 31500, 0)
        self.assertAlmostEqual(irpp.impots_net, 6910.90, 2)

        # Avec plafonnement
        irpp = IRPP(self.database, 2020, 2.5, 1)
        irpp.add_ligne(L1AJ_salaire, 63000 / 0.9)

        self.assertAlmostEqual(irpp.revenu_net_impossable, 63000, 0)
        self.assertAlmostEqual(irpp.quotient_familial, 25200, 0)
        self.assertNotEqual(irpp.impots_net, 4157)  # Dépassement
        self.assertAlmostEqual(irpp.impots_net, 5341, 0)

    def testExemple6(self):
        '''
        http://impotsurlerevenu.org/exemple/124-celibataire-sans-enfant-revenus-eleves.php
        '''
        irpp = IRPP(self.database, 2018, 1, 0)
        irpp.add_ligne(L1AJ_salaire, 37133)

        self.assertAlmostEqual(irpp.revenu_net_impossable, 37133 * .9, 0)
        self.assertAlmostEqual(irpp.quotient_familial, 33420, 0)
        self.assertAlmostEqual(irpp.impots_net, 4227, 0)

    @unittest.skip('')
    def testExemple7(self):
        '''
        http://impotsurlerevenu.org/exemple/125-couple-marie-sans-enfant-revenus-eleves.php
        '''
        irpp = IRPP(self.database, 2018, 2, 0)
        irpp.add_ligne(L1AJ_salaire, 146256)

        self.assertAlmostEqual(irpp.revenu_net_impossable, 146256 * .9, 0)
        self.assertAlmostEqual(irpp.quotient_familial, 66877, 0)
        self.assertAlmostEqual(irpp.impots_net, 28530, 0)

    def testExemple8(self):
        '''
        http://impotsurlerevenu.org/exemple/126-couple-marie-sans-enfant-revenus-modestes.php
        '''
        irpp = IRPP(self.database, 2018, 2, 0)
        irpp.add_ligne(L1AJ_salaire, 44467)

        self.assertAlmostEqual(irpp.revenu_net_impossable, 44467 * .9, 0)
        self.assertAlmostEqual(irpp.quotient_familial, 20010, 0)
        self.assertAlmostEqual(irpp.impots_net, 2813, 0)

    def testExemple10(self):
        '''
        http://impotsurlerevenu.org/exemple/128-couple-marie-avec-enfants-aux-revenus-modestes.php
        '''
        irpp = IRPP(self.database, 2018, 3, 1)
        irpp.add_ligne(L1AJ_salaire, 39519)

        self.assertAlmostEqual(irpp.revenu_net_impossable, 39519 * .9, 0)
        self.assertAlmostEqual(irpp.quotient_familial, 11856, 0)
        self.assertAlmostEqual(irpp.impots_net, 794, 0)

    def testExemple11(self):
        '''
        http://impotsurlerevenu.org/exemple/129-couple-marie-avec-enfants-revenus-eleves.php
        '''
        irpp = IRPP(self.database, 2018, 3, 2)
        irpp.add_ligne(L1AJ_salaire, 123895)

        self.assertAlmostEqual(irpp.revenu_net_impossable, 123895 * .9, 0)
        self.assertAlmostEqual(irpp.quotient_familial, 37169, 0)
        self.assertAlmostEqual(irpp.impots_net, 18753, 0)

    def testExemple12(self):
        '''
        http://impotsurlerevenu.org/exemple/130-couple-marie-avec-1-enfant-aux-revenus-eleves.php
        '''
        irpp = IRPP(self.database, 2018, 2.5, 1)
        irpp.add_ligne(L1AJ_salaire, 85331)

        self.assertAlmostEqual(irpp.revenu_net_impossable, 85331 * .9, 0)
        self.assertAlmostEqual(irpp.quotient_familial, 30719, 0)
        self.assertAlmostEqual(irpp.impots_net, 9891, 0)

    def testExemple20(self):
        '''
        http://impotsurlerevenu.org/nouveautes-impot-2019/1203-bareme-impot-2019.php
        '''
        irpp = IRPP(self.database, 2018, 3, 2)
        irpp.add_ligne(L1AJ_salaire, 60000 / 0.9)

        self.assertAlmostEqual(irpp.revenu_net_impossable, 60000, 0)
        self.assertAlmostEqual(irpp.quotient_familial, 20000, 0)
        self.assertAlmostEqual(irpp.impots_net, 4215, 0)

    def testExemple21(self):
        '''
        http://impotsurlerevenu.org/comprendre-le-calcul-de-l-impot/1194-calcul-de-l-impot-2018.php
        '''
        irpp = IRPP(self.database, 2017, 3, 2)
        irpp.add_ligne(L1AJ_salaire, 89000 / 0.9)

        self.assertAlmostEqual(irpp.revenu_net_impossable, 89000, 0)
        self.assertAlmostEqual(irpp.quotient_familial, 29667, 0)
        self.assertAlmostEqual(irpp.impots_net, 12232, 0)


class TestIRPPAnnexe2044(unittest.TestCase):

    def setUp(self):
        self.database = Database()

    def testAnnexe2044(self):
        irpp = IRPP(self.database, 2019, 2, 0)
        irpp.add_ligne(L1AJ_salaire, 30000)
        irpp.add_ligne(L1BJ_salaire, 20000)
        annexe_2044 = Annexe_2044(self.database)
        annexe_2044.add_ligne(L211_loyer_brut, 6000)
        irpp.annexe_2044 = annexe_2044
        self.assertEqual(irpp.revenu_fiscale_reference, 51000)
        self.assertTrue(isinstance(irpp.annexe_2044, Annexe_2044))


if __name__ == '__main__':
    unittest.main()
