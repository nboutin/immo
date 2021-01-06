#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import sys
import os
sys.path.insert(0, os.path.join('..'))

from bien_immo import Bien_Immo
from lot import Lot
from charge import Charge
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

        lot = Lot("T2", 50, 500)
        charge = Charge(lot, None)
        charge.add(Charge.charge_e.copropriete, 51 * 12)
        charge.add(Charge.charge_e.prime_assurance, 90)
        charge.add(Charge.charge_e.vacance_locative, 1 / 12)
        charge.add(Charge.charge_e.agence_immo, 0.05)
        lot.charge = charge
        bi.add_lot(lot)

        self.assertAlmostEqual(bi.charges + bi.provisions, 1002, 2)
        self.assertAlmostEqual(rdt.rendement_net, 0.21, 2)

    def testCashflow(self):
        bi = Bien_Immo(50000, 0, 0, 0, 0)

        lot1 = Lot("T2", 50, 500)
        bi.add_lot(lot1)
        cr = Credit(50000, 240, 0.02, 0, Credit.mode_e.m1, 0, 0)
        rdt = Rendement(bi, cr)
        self.assertAlmostEqual(rdt.cashflow_mensuel, 247.06, 2)

        lot2 = Lot("T2", 50, 500)
        charge = Charge(lot2, None)
        charge.add(Charge.charge_e.copropriete, 51 * 12)
        charge.add(Charge.charge_e.prime_assurance, 90)
        charge.add(Charge.charge_e.vacance_locative, 1 / 12)
        charge.add(Charge.charge_e.agence_immo, 0.05)
        lot2.charge = charge
        bi.add_lot(lot2)

        self.assertAlmostEqual(bi.loyer_nu_brut_annuel, 12000, 2)
        self.assertAlmostEqual(bi.charges + bi.provisions, 1002, 2)
        self.assertAlmostEqual(cr.get_mensualite_avec_assurance(), 252.94, 2)
        self.assertAlmostEqual(rdt.cashflow_mensuel, 621.89, 2)
        self.assertAlmostEqual(rdt.cashflow_annuel, 7462.70, 2)


if __name__ == '__main__':
    unittest.main()
