#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import calcul


class TestCalcul(unittest.TestCase):

    def testRendementBrut(self):
        rbrut = calcul.rendement_brut(500 * 12, 50000)
        self.assertEqual(rbrut, 0.12)

    def testRendementMethodeLarcher(self):

        rlarcher = calcul.rendement_methode_larcher(500, 50000)
        self.assertEqual(rlarcher, 0.09)


if __name__ == '__main__':
    unittest.main()
