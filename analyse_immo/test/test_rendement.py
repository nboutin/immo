#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from bien_immo import Bien_Immo, Lot
from rendement import Rendement


class TestRendement(unittest.TestCase):

    def testRendementBrut(self):
        bi = Bien_Immo(50000, 0, 0, 0, 0)
        bi.add_lot(Lot("T2", 50, 500))
        r = Rendement(bi)
        self.assertEqual(r.rendement_brut, 0.12)

    def testRendementMethodeLarcher(self):
        bi = Bien_Immo(50000, 0, 0, 0, 0)
        bi.add_lot(Lot("T2", 50, 500))
        r = Rendement(bi)
        self.assertEqual(r.rendement_methode_larcher, 0.09)

    @unittest.skip('missing charges')
    def testRendementNet(self):
        bi = Bien_Immo(50000, 0, 0, 0, 0)
        bi.add_lot(Lot("T2", 50, 500))
        r = Rendement(bi)
        self.assertEqual(r.rendement_methode_larcher, 0.09)

    @unittest.skip('todo')
    def testCashflowMensuel(self):
        cashflow_mensuel = calcul.cashflow_mensuel(500, 350, 1500)
        self.assertEqual(cashflow_mensuel, 25)


if __name__ == '__main__':
    unittest.main()
