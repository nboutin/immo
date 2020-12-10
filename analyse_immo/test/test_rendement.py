#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from bien_immo import Bien_Immo, Lot
from credit import Credit
from rendement import Rendement


class TestRendement(unittest.TestCase):

    def testRendementBrut(self):
        bi = Bien_Immo(50000, 0, 0, 0, 0)
        bi.add_lot(Lot("T2", 50, 500))
        rdt = Rendement(bi)
        self.assertEqual(rdt.rendement_brut, 0.12)

    def testRendementMethodeLarcher(self):
        bi = Bien_Immo(50000, 0, 0, 0, 0)
        bi.add_lot(Lot("T2", 50, 500))
        rdt = Rendement(bi)
        self.assertEqual(rdt.rendement_methode_larcher, 0.09)

    def testRendementNet(self):
        bi = Bien_Immo(50000, 0, 0, 0, 0)
        bi.add_lot(Lot("T2", 50, 500))
        rdt = Rendement(bi)
        self.assertEqual(rdt.rendement_net, 0.12)
        
        bi.add_lot(Lot("T2", 50, 500,
                       vacance_locative_taux_annuel=1 / 12,
                       PNO=90,
                       gestion_agence_taux=0.05,
                       copropriete=51))
        self.assertAlmostEqual(rdt.rendement_net, 0.22, 2)

    @unittest.skip('todo')
    def testCashflowMensuel(self):
        cashflow_mensuel = calcul.cashflow_mensuel(500, 350, 1500)
        self.assertEqual(cashflow_mensuel, 25)


if __name__ == '__main__':
    unittest.main()
