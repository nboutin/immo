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
        lot = Lot('T1', 30, 350)
        self.assertEqual(lot.etat, Lot.etat_e.louable)
        self.assertTrue(lot.travaux is not None)

    def testSurface(self):
        lot = Lot('T1', 45, 123)
        self.assertEqual(lot.surface, 45)

    def testIRLTauxAnnuel(self):
        lot = Lot('T1', 45, 123)
        self.assertEqual(lot.irl_taux_annuel, 0)

        lot = Lot('T1', 45, 123, 10)
        self.assertEqual(lot.irl_taux_annuel, 10)

        lot = Lot('T1', 45, 123, 0.01)
        self.assertEqual(lot.irl_taux_annuel, 0.01)

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

    def testLoyerNetMensuelA(self):
        '''get loyer_nu_net_mensuel without vacance locative'''
        lot = Lot('T1', 30, 360)
        self.assertEqual(lot.loyer_nu_net_mensuel(), 360)

    def testLoyerNetMensuelB(self):
        '''get loyer_nu_net_mensuel with vacance locative default value'''
        lot = Lot('T1', 30, 360)
        charge = Charge(self.defaut, lot.type)
        charge.add(Charge.charge_e.vacance_locative, 1)
        lot.charge = charge
        self.assertEqual(lot.loyer_nu_net_mensuel(), 330.12)

    def testLoyerNuNetMensuel(self):
        '''With irl_taux_annuel and vacance locative'''
        lot = Lot('T2', 45, 400, irl_taux_annuel=0.01)
        charge = Charge(self.defaut, lot.type)
        charge.add(Charge.charge_e.vacance_locative, 1 / 24)
        lot.charge = charge

        self.assertAlmostEqual(lot.loyer_nu_net_mensuel(1), 400 * (1 - 1 / 24), 2)
        self.assertAlmostEqual(lot.loyer_nu_net_mensuel(13), 400 * 1.01 * (1 - 1 / 24), 2)

    def testLoyerNuNetAnnuel(self):
        '''With irl_taux_annuel and vacance locative'''
        lot = Lot('T2', 45, 500, irl_taux_annuel=0.02)
        charge = Charge(self.defaut, lot.type)
        charge.add(Charge.charge_e.vacance_locative, 0.04)
        lot.charge = charge

        self.assertAlmostEqual(lot.loyer_nu_net_annuel(1), 500 * 12 * (1 - 0.04), 2)
        self.assertAlmostEqual(lot.loyer_nu_net_annuel(2), 500 * 12 * 1.02 * (1 - 0.04), 2)
        self.assertAlmostEqual(lot.loyer_nu_net_annuel(10), 500 * 12 * math.pow(1.02, 9) * (1 - 0.04), 2)


if __name__ == '__main__':
    unittest.main()
