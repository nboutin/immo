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

    def testRendementNet(self):

        r_net = calcul.rendement_net(500 * 12, 1500, 50000)
        self.assertEqual(r_net, 0.09)

    def testCashflowMensuel(self):

        cashflow_mensuel = calcul.cashflow_mensuel(500, 350, 1500)
        self.assertEqual(cashflow_mensuel, 25)


if __name__ == '__main__':
    unittest.main()
