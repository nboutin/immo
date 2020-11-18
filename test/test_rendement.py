#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import rendement

class TestRendement(unittest.TestCase):

    def testRendementBrut(self):
        
        bien_immo = {'prix_achat' : 100000, 'loyers_annuel_total': 500 * 12}
        
        rendement.calcul_rendement_brut(bien_immo)
        self.assertEqual(bien_immo['r_brut'], 0.06)


if __name__ == '__main__':
    unittest.main()
