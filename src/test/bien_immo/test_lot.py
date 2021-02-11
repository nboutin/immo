#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import math

from analyse_immo.factory import Factory
from analyse_immo.bien_immo.lot import Lot
from analyse_immo.bien_immo.charge import Charge
from test.testcase_fileloader import TestCaseFileLoader


class TestLot(TestCaseFileLoader):

    def setUp(self):
        super().setUp()
        self.defaut = Factory.make_defaut(self.defaut_data)

    def testInit(self):
        _ = Lot('T1', 30, 350)

    def testSurface(self):
        lot = Lot('T1', 45, 123)
        self.assertEqual(lot.surface, 45)

    def testLoyerNuBrutMensuel(self):
        lot = Lot('T1', 30, 350)
        self.assertEqual(lot.loyer_nu_brut_mensuel(), 350)
        self.assertEqual(lot.loyer_nu_brut_mensuel(1), 350)
        self.assertEqual(lot.loyer_nu_brut_mensuel(2), 350)
        self.assertEqual(lot.loyer_nu_brut_mensuel(3), 350)
        self.assertEqual(lot.loyer_nu_brut_mensuel(12), 350)
        self.assertEqual(lot.loyer_nu_brut_mensuel(13), 350)

        lot = Lot('T1', 30, 350, 0.01)
        self.assertEqual(lot.loyer_nu_brut_mensuel(), 350)
        self.assertEqual(lot.loyer_nu_brut_mensuel(1), 350)
        self.assertEqual(lot.loyer_nu_brut_mensuel(2), 350)
        self.assertEqual(lot.loyer_nu_brut_mensuel(3), 350)
        self.assertEqual(lot.loyer_nu_brut_mensuel(12), 350)
        self.assertEqual(lot.loyer_nu_brut_mensuel(12 + 1), 350 * 1.01)
        self.assertEqual(lot.loyer_nu_brut_mensuel(14), 350 * 1.01)
        self.assertEqual(lot.loyer_nu_brut_mensuel(24 + 1), 350 * 1.01 * 1.01)

    def testLoyerNuBrutAnnuel(self):
        lot = Lot('T1', 30, 350)
        self.assertEqual(lot.loyer_nu_brut_annuel(), 350 * 12)
        self.assertEqual(lot.loyer_nu_brut_annuel(1), 350 * 12)
        self.assertEqual(lot.loyer_nu_brut_annuel(2), 350 * 12)
        self.assertEqual(lot.loyer_nu_brut_annuel(3), 350 * 12)
        self.assertEqual(lot.loyer_nu_brut_annuel(10), 350 * 12)

        lot = Lot('T1', 30, 350, 0.01)
        self.assertEqual(lot.loyer_nu_brut_annuel(), 350 * 12)
        self.assertEqual(lot.loyer_nu_brut_annuel(1), 350 * 12)
        self.assertEqual(lot.loyer_nu_brut_annuel(2), 350 * 12 * 1.01)
        self.assertEqual(lot.loyer_nu_brut_annuel(3), 350 * 12 * 1.01 * 1.01)
        self.assertEqual(lot.loyer_nu_brut_annuel(10), 350 * 12 * math.pow(1.01, 9))

    def testLoyerNetMensuel(self):
        lot = Lot('T1', 30, 360)
        self.assertEqual(lot.loyer_nu_net_mensuel(), 360)

        charge = Charge(lot, self.defaut)
        charge.add(Charge.charge_e.vacance_locative, 1)
        lot.charge = charge
        self.assertEqual(lot.loyer_nu_net_mensuel(), 330.12)


if __name__ == '__main__':
    unittest.main()
