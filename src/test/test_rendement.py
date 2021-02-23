#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from analyse_immo.bien_immo.bien_immo import Bien_Immo
from analyse_immo.bien_immo.lot import Lot
from analyse_immo.bien_immo.charge import Charge
from analyse_immo.credit import Credit
from analyse_immo.rendement import Rendement


class TestRendement(unittest.TestCase):

    def setUp(self):
        self.credit = Credit(50000, 240, 0.02, Credit.taux_e.periodique, 0, Credit.mode_e.fixe_CI, 0, 0)
        self.irpp_2044_proj = []

    def testRendementBrut(self):
        bi = Bien_Immo(50000, 0, 0, 0, 0)
        bi.add_lot(Lot("T2", 50, 500))
        rdt = Rendement(bi, self.credit, self.irpp_2044_proj)
        self.assertEqual(rdt.rendement_brut, 0.12)

        bi = Bien_Immo(0, 0, 0, 0, 0)
        rdt = Rendement(bi, self.credit, self.irpp_2044_proj)
        self.assertEqual(rdt.rendement_brut, 0)

    def testRendementMethodeLarcher(self):
        bi = Bien_Immo(50000, 0, 0, 0, 0)
        bi.add_lot(Lot("T2", 50, 500))
        rdt = Rendement(bi, self.credit, self.irpp_2044_proj)
        self.assertEqual(rdt.rendement_methode_larcher, 0.09)

        bi = Bien_Immo(0, 0, 0, 0, 0)
        rdt = Rendement(bi, self.credit, self.irpp_2044_proj)
        self.assertEqual(rdt.rendement_methode_larcher, 0)

    def testRendementNet(self):
        bi = Bien_Immo(0, 0, 0, 0, 0)
        rdt = Rendement(bi, self.credit, self.irpp_2044_proj)
        self.assertEqual(rdt.rendement_net(1), 0)

        bi = Bien_Immo(50000, 0, 0, 0, 0)
        bi.add_lot(Lot("T2", 50, 500))
        rdt = Rendement(bi, self.credit, self.irpp_2044_proj)
        self.assertEqual(rdt.rendement_net(1), 0.12)

        lot = Lot("T2", 50, 500)
        charge = Charge(lot, None)
        charge.add(Charge.charge_e.copropriete, 51 * 12)
        charge.add(Charge.charge_e.prime_assurance, 90)
        charge.add(Charge.charge_e.vacance_locative, 1 / 12)
        charge.add(Charge.charge_e.agence_immo, 500 * 12 * 0.05)
        lot.charge = charge
        bi.add_lot(lot)

        self.assertAlmostEqual(bi.charges(1) + bi.provisions(1), 1002, 2)
        self.assertAlmostEqual(rdt.rendement_net(1), 0.21, 2)

    def testCashflow(self):
        bi = Bien_Immo(50000, 0, 0, 0, 0)

        lot1 = Lot("T2", 50, 500)
        bi.add_lot(lot1)
        cr = Credit(50000, 240, 0.02, Credit.taux_e.periodique, 0, Credit.mode_e.fixe_CI, 0, 0)
        rdt = Rendement(bi, cr, self.irpp_2044_proj)
        self.assertAlmostEqual(rdt.cashflow_net_mensuel(1), 247.06, 2)

        lot2 = Lot("T2", 50, 500)
        charge = Charge(lot2, None)
        charge.add(Charge.charge_e.copropriete, 51 * 12)
        charge.add(Charge.charge_e.prime_assurance, 90)
        charge.add(Charge.charge_e.vacance_locative, 1 / 12)
        charge.add(Charge.charge_e.agence_immo, 500 * 12 * 0.05)
        lot2.charge = charge
        bi.add_lot(lot2)

        self.assertAlmostEqual(bi.loyer_nu_brut_annuel(1), 12000, 2)
        self.assertAlmostEqual(bi.charges(1) + bi.provisions(1), 1002, 2)
        self.assertAlmostEqual(cr.get_mensualite_avec_assurance(), 252.94, 2)
        self.assertAlmostEqual(rdt.cashflow_net_mensuel(1), 621.89, 2)
        self.assertAlmostEqual(rdt.cashflow_net_annuel(1), 7462.70, 2)


if __name__ == '__main__':
    unittest.main()
