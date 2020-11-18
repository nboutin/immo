#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import rendement

class TestRendement(unittest.TestCase):

    def testRendementBrut(self):
        
        data = {'prix_achat' : 100000}
        bien_immo = {'loyers_annuel_total': 500 * 12}
        
        r_brut = rendement.calcul_rendement_brut(data, bien_immo)
        self.assertEqual(r_brut, 0.06)


if __name__ == '__main__':
    unittest.main()
