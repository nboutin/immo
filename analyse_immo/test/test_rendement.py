#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from bien_immo import Bien_Immo, Lot
from rendement import Rendement
# from analyse_immo.bien_immo import Bien_Immo


class TestRendement(unittest.TestCase):

    def testRendementBrut(self):
#         rbrut = calcul.rendement_brut(500 * 12, 50000)
#         self.assertEqual(rbrut, 0.12)

        bi = Bien_Immo(50000, 0, 0, 0, 0)
        bi.add(Lot("T2", 50, 500))
        r = Rendement(bi)
        self.assertEqual(r.rendement_brut, 0.12)

    def testRendementMethodeLarcher(self):
#         rlarcher = calcul.rendement_methode_larcher(500, 50000)
#         self.assertEqual(rlarcher, 0.09)
        bi = Bien_Immo(50000, 0, 0, 0, 0)
        bi.add(Lot("T2", 50, 500))
        r = Rendement(bi)
        self.assertEqual(r.rendement_methode_larcher, 0.09)

    @unittest.skip('missing charges')
    def testRendementNet(self):
#         r_net = calcul.rendement_net(500 * 12, 1500, 50000)
#         self.assertEqual(r_net, 0.09)

        bi = Bien_Immo(50000, 0, 0, 0, 0)
        bi.add(Lot("T2", 50, 500))
        r = Rendement(bi)
        self.assertEqual(r.rendement_methode_larcher, 0.09)

    @unittest.skip('todo')
    def testCashflowMensuel(self):
        cashflow_mensuel = calcul.cashflow_mensuel(500, 350, 1500)
        self.assertEqual(cashflow_mensuel, 25)


if __name__ == '__main__':
    unittest.main()
