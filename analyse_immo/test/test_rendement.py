#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from bien_immo import Bien_Immo
from lot import Lot
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
                       copropriete_mensuel=51))
        
        self.assertAlmostEqual(bi.charges_annuel_total, 1502, 2)
        self.assertAlmostEqual(rdt.rendement_net, 0.21, 2)

    def testCashflow(self):
        bi = Bien_Immo(50000, 0, 0, 0, 0)
        bi.add_lot(Lot("T2", 50, 500))
        cr = Credit(50000, 240, 0.02, 0, 'mode_1', 0, 0)
        rdt = Rendement(bi)
        self.assertAlmostEqual(rdt.cashflow_mensuel(cr), 247.06, 2)
        
        bi.add_lot(Lot("T2", 50, 500,
                       vacance_locative_taux_annuel=1 / 12,
                       PNO=90,
                       gestion_agence_taux=0.05,
                       copropriete_mensuel=51))
        
        self.assertAlmostEqual(bi.loyer_annuel_total, 12000, 2)
        self.assertAlmostEqual(bi.charges_annuel_total, 1502, 2)
        self.assertAlmostEqual(cr.get_mensualite_avec_assurance(), 252.94, 2)
        self.assertAlmostEqual(rdt.cashflow_mensuel(cr), 621.89, 2)
        self.assertAlmostEqual(rdt.cashflow_annuel(cr), 7462.70, 2)


if __name__ == '__main__':
    unittest.main()
