#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import os
import json

from analyse_immo.factory import Factory
from analyse_immo.lot import Lot
from analyse_immo.charge import Charge


class TestLot(unittest.TestCase):

    def setUp(self):
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        __DATA_TEST_PATHNAME = os.path.join(__location__, 'data', 'input_test.json')
        with open(__DATA_TEST_PATHNAME, 'r') as file:
            input_data = json.load(file)

        defaut_data = input_data['defaut']
        self.defaut = Factory.make_defaut(defaut_data)

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
