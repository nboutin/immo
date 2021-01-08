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

    def test(self):
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
        irpp = IRPP(self.database, 2018, 2.5, 1)
        irpp.add_ligne(L1AJ_salaire, 31407)
        irpp.add_ligne(L1BJ_salaire, 23055)
        self.assertAlmostEqual(irpp.impots_brut, 3339, 0)
        self.assertAlmostEqual(irpp.impots_brut, 3339.46, 2)

    def testImpotNet(self):
        irpp = IRPP(self.database, 2018, 2.5, 1)
        irpp.add_ligne(L1AJ_salaire, 31407)
        irpp.add_ligne(L1BJ_salaire, 23055)
        irpp.add_ligne(L7UF_dons, 200)
        irpp.add_ligne(L7AE_syndicat, 143)

        self.assertAlmostEqual(irpp.impots_net, 3113, 0)
        self.assertAlmostEqual(irpp.impots_net, 3113.08, 2)

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

    @unittest.skip('')
    def testExemple5(self):
        '''
        http://impotsurlerevenu.org/exemple/123-celibataire-sans-enfant-revenus-modestes.php
        '''
        irpp = IRPP(self.database, 2019, 1, 0)
        irpp.add_ligne(L1AJ_salaire, 17372)

        self.assertAlmostEqual(irpp.revenu_net_impossable, 17372 * .9, 0)
        self.assertAlmostEqual(irpp.quotient_familial, 15635, 0)
        self.assertAlmostEqual(irpp.impots_net, 794, 0)

    @unittest.skip('')
    def testExemple6(self):
        '''
        http://impotsurlerevenu.org/exemple/124-celibataire-sans-enfant-revenus-eleves.php
        '''
        irpp = IRPP(self.database, 2019, 1, 0)
        irpp.add_ligne(L1AJ_salaire, 51039)

        self.assertAlmostEqual(irpp.revenu_net_impossable, 51039 * .9, 0)
        self.assertAlmostEqual(irpp.quotient_familial, 45935, 0)
        self.assertAlmostEqual(irpp.impots_net, 7983, 0)

    @unittest.skip('')
    def testExemple7(self):
        '''
        http://impotsurlerevenu.org/exemple/125-couple-marie-sans-enfant-revenus-eleves.php
        '''
        irpp = IRPP(self.database, 2018, 2, 0)
        irpp.add_ligne(L1AJ_salaire, 139099)

        self.assertAlmostEqual(irpp.revenu_net_impossable, 139099 * .9, 0)
        self.assertAlmostEqual(irpp.quotient_familial, 63299, 0)
        self.assertAlmostEqual(irpp.impots_net, 26383, 0)


class TestIRPPAnnexe2044(unittest.TestCase):

    def setUp(self):
        self.database = Database()

    def testAnnexe2044(self):
        irpp = IRPP(self.database, 2019, 2, 0)
        irpp.add_ligne(L1AJ_salaire, 30000)
        irpp.add_ligne(L1BJ_salaire, 20000)
        an = Annexe_2044()
        an.add_ligne(L211_loyer_brut, 6000)
        irpp.add_annexe(an)
        self.assertEqual(irpp.revenu_fiscale_reference, 51000)


if __name__ == '__main__':
    unittest.main()
