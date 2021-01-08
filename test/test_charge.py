#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import os
import json

from analyse_immo.factory import Factory
from analyse_immo.charge import Charge
from analyse_immo.lot import Lot


class TestCharge(unittest.TestCase):

    def setUp(self):
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        __DATA_TEST_PATHNAME = os.path.join(__location__, 'data', 'input_test.json')
        with open(__DATA_TEST_PATHNAME, 'r') as file:
            input_data = json.load(file)

        defaut_data = input_data['defaut']
        self.defaut = Factory.make_defaut(defaut_data)

    def testInit(self):
        _ = Charge(None)
        _ = Charge(None, None)

    def testAddMontant(self):
        lot = Lot('T2', 45, 450)
        charge = Charge(lot)
        type_ = Charge.charge_e.taxe_fonciere
        charge.add(type_, 500)

        self.assertEqual(charge.get_montant_annuel(type_), 500)

    def testAdd0(self):
        lot = Lot('T2', 45, 450)
        charge = Charge(lot)
        type_ = Charge.charge_e.taxe_fonciere
        charge.add(type_, 0)

        self.assertEqual(charge.get_montant_annuel(type_), 0)

    def testAddVacanceLocative0(self):
        lot = Lot('T2', 45, 450)
        charge = Charge(lot)
        type_ = Charge.charge_e.vacance_locative
        charge.add(type_, 0)

        self.assertEqual(charge.get_montant_annuel(type_), 0)

    def testAddVacanceLocative1A(self):
        '''no default'''
        lot = Lot('T2', 45, 450)
        charge = Charge(lot)
        type_ = Charge.charge_e.vacance_locative
        charge.add(type_, 1)

        self.assertEqual(charge.get_montant_annuel(type_), 0)

    def testAddVacanceLocative1B(self):
        lot = Lot('T2', 45, 450)
        charge = Charge(lot, self.defaut)
        type_ = Charge.charge_e.vacance_locative
        charge.add(type_, 1)

    def testAddTravauxProvision(self):
        '''default'''
        lot = Lot('T2', 45, 500)
        charge = Charge(lot, self.defaut)
        type_ = Charge.charge_e.provision_travaux
        charge.add(type_, 1)

        self.assertEqual(charge.get_taux(type_), 0.01)
        self.assertEqual(charge.get_montant_annuel(type_), 60)

    def testAddMissingDefaut(self):
        lot = Lot('T2', 45, 500)
        charge = Charge(lot, self.defaut)
        type_ = Charge.charge_e.copropriete

        with self.assertRaises(LookupError):
            charge.add(type_, 1)


if __name__ == '__main__':
    unittest.main()
