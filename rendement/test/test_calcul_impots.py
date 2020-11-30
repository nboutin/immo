#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import calcul_impots


class TestCalculImpots(unittest.TestCase):

    def testImpotsBrut(self):

        tmi = [[10084, 0], [25710, 0.11], [73516, 0.30], [158122, 0.41]]
        ibrut = calcul_impots.impots_brut(tmi, 5000)
        self.assertEqual(ibrut, 0)

        ibrut = calcul_impots.impots_brut(tmi, 10000)
        self.assertEqual(ibrut, 0)

        ibrut = calcul_impots.impots_brut(tmi, 10084)
        self.assertEqual(ibrut, 0)

        ibrut = calcul_impots.impots_brut(tmi, 10085)
        self.assertEqual(ibrut, 0.11)

        ibrut = calcul_impots.impots_brut(tmi, 15000)
        self.assertAlmostEqual(ibrut, 540.76, 2)
 
        ibrut = calcul_impots.impots_brut(tmi, 20000)
        self.assertAlmostEqual(ibrut, 1090.76, 2)
 
        ibrut = calcul_impots.impots_brut(tmi, 30000)
        self.assertAlmostEqual(ibrut, 3005.86, 2)
 
        ibrut = calcul_impots.impots_brut(tmi, 80000)
        self.assertAlmostEqual(ibrut, 18719.10, 2)


if __name__ == '__main__':
    unittest.main()
