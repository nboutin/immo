#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from analyse_immo.factory import Factory
from analyse_immo.lot import Lot
from analyse_immo.charge import Charge
from test.testcase_fileloader import TestCaseFileLoader


class TestLot(TestCaseFileLoader):

    def setUp(self):
        super().setUp()
        self.defaut = Factory.make_defaut(self.defaut_data)

    def testInit(self):
        _ = Lot('T1', 30, 350)

    def testLoyerNetMensuel(self):
        lot = Lot('T1', 30, 360)
        self.assertEqual(lot.loyer_nu_net_mensuel, 360)

        charge = Charge(lot, self.defaut)
        charge.add(Charge.charge_e.vacance_locative, 1)
        lot.charge = charge
        self.assertEqual(lot.loyer_nu_net_mensuel, 330.12)


if __name__ == '__main__':
    unittest.main()
