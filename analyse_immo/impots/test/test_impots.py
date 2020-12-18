#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import sys
import os
sys.path.insert(0, os.path.join('..'))
sys.path.insert(1, os.path.join('..', '..'))

from database import Database
from impots import Impots


class TestImpots(unittest.TestCase):

    def setUp(self):
        self.database = Database()

    def testInit(self):
        _ = Impots(None, 0, 0, 0)

    def testRevenuFiscaleReference(self):

        impot = Impots(self.database, 0, 0, 0)
        impot.add_revenu(Impots.revenu_e.salaires, 31407)
        impot.add_revenu(Impots.revenu_e.salaires, 23055)
        self.assertEqual(impot.revenu_fiscale_reference, 49015.80, 2)

    def test(self):
        impot = Impots(self.database, 0, 0, 0)
        tmi = [[10084, 0], [25710, 0.11], [73516, 0.30], [158122, 0.41]]

        ibrut = impot._impots_brut(tmi, 5000)
        self.assertEqual(ibrut, 0)

        ibrut = impot._impots_brut(tmi, 10000)
        self.assertEqual(ibrut, 0)

        ibrut = impot._impots_brut(tmi, 10084)
        self.assertEqual(ibrut, 0)

        ibrut = impot._impots_brut(tmi, 10085)
        self.assertEqual(ibrut, 0.11)

        ibrut = impot._impots_brut(tmi, 15000)
        self.assertAlmostEqual(ibrut, 540.76, 2)

        ibrut = impot._impots_brut(tmi, 20000)
        self.assertAlmostEqual(ibrut, 1090.76, 2)

        ibrut = impot._impots_brut(tmi, 30000)
        self.assertAlmostEqual(ibrut, 3005.86, 2)

        ibrut = impot._impots_brut(tmi, 80000)
        self.assertAlmostEqual(ibrut, 18719.10, 2)

    def testImpotBrut(self):
        impot = Impots(self.database, 2019, 2.5, 1)
        impot.add_revenu(Impots.revenu_e.salaires, 31407)
        impot.add_revenu(Impots.revenu_e.salaires, 23055)
        self.assertAlmostEqual(impot.impots_brut, 3340, 0)
        self.assertAlmostEqual(impot.impots_brut, 3339.81, 2)

    def testImpotNet(self):
        impot = Impots(self.database, 2019, 2.5, 1)
        impot.add_revenu(Impots.revenu_e.salaires, 31407)
        impot.add_revenu(Impots.revenu_e.salaires, 23055)
        impot.add_reduction(Impots.reduction_e.dons, 200)
        impot.add_reduction(Impots.reduction_e.cotisations_syndicales, 143)

        self.assertAlmostEqual(impot.impots_net, 3113, 0)
        self.assertAlmostEqual(impot.impots_net, 3113.43, 2)


if __name__ == '__main__':
    unittest.main()
