#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import sys
import os
sys.path.insert(0, os.path.join('..'))
sys.path.insert(1, os.path.join('..', '..'))

from database import Database
from irpp import IRPP, L1AJ_salaire, L1BJ_salaire, L7UF_dons, L7AE_syndicat
from annexe_2044 import Annexe_2044, L211_loyer_brut


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
        self.assertEqual(ibrut, 0.11)

        ibrut = irpp._impots_brut(tmi, 15000)
        self.assertAlmostEqual(ibrut, 540.76, 2)

        ibrut = irpp._impots_brut(tmi, 20000)
        self.assertAlmostEqual(ibrut, 1090.76, 2)

        ibrut = irpp._impots_brut(tmi, 30000)
        self.assertAlmostEqual(ibrut, 3005.86, 2)

        ibrut = irpp._impots_brut(tmi, 80000)
        self.assertAlmostEqual(ibrut, 18719.10, 2)

    def testImpotBrut(self):
        irpp = IRPP(self.database, 2019, 2.5, 1)
        irpp.add_ligne(L1AJ_salaire, 31407)
        irpp.add_ligne(L1BJ_salaire, 23055)
        self.assertAlmostEqual(irpp.impots_brut, 3340, 0)
        self.assertAlmostEqual(irpp.impots_brut, 3339.81, 2)

    def testImpotNet(self):
        irpp = IRPP(self.database, 2019, 2.5, 1)
        irpp.add_ligne(L1AJ_salaire, 31407)
        irpp.add_ligne(L1BJ_salaire, 23055)
        irpp.add_ligne(L7UF_dons, 200)
        irpp.add_ligne(L7AE_syndicat, 143)

        self.assertAlmostEqual(irpp.impots_net, 3113, 0)
        self.assertAlmostEqual(irpp.impots_net, 3113.43, 2)


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
