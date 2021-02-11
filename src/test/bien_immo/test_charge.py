#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from analyse_immo.factory import Factory
from analyse_immo.bien_immo.charge import Charge
from test.testcase_fileloader import TestCaseFileLoader


class TestCharge(TestCaseFileLoader):

    def setUp(self):
        super().setUp()
        self.defaut = Factory.make_defaut(self.defaut_data)

    def testInit(self):
        _ = Charge(None)
        _ = Charge(None, None)

        with self.assertRaises(TypeError):
            _ = Charge()

    def testAddMontant(self):
        charge = Charge(self.defaut)
        type_ = Charge.charge_e.taxe_fonciere
        charge.add(type_, 500)
        self.assertEqual(charge.get_montant_annuel(type_), 500)

    def testAdd0(self):
        charge = Charge(self.defaut)
        type_ = Charge.charge_e.taxe_fonciere
        charge.add(type_, 0)
        self.assertEqual(charge.get_montant_annuel(type_), 0)

    def testAddVacanceLocative0(self):
        charge = Charge(self.defaut)
        type_ = Charge.charge_e.vacance_locative
        charge.add(type_, 0)

        self.assertEqual(charge.get_montant_annuel(type_), 0)

    def testAddVacanceLocative1A(self):
        '''looking for default value but lot_type is not defined'''
        charge = Charge(self.defaut)
        type_ = Charge.charge_e.vacance_locative
        charge.add(type_, 1)
        self.assertEqual(charge.get_taux(type_), 0.083)

    def testAddVacanceLocative1B(self):
        '''looking for default value'''
        charge = Charge(self.defaut, 'T1')
        type_ = Charge.charge_e.vacance_locative
        charge.add(type_, 1)

    def testAddVacanceLocative1C(self):
        '''Add a taux and ask for a montant'''
        charge = Charge(self.defaut, 'T1')
        type_ = Charge.charge_e.vacance_locative
        charge.add(type_, 0.5)
        with self.assertRaises(Exception):
            charge.get_montant_annuel(type_)

    def testAddVacanceLocative1D(self):
        charge = Charge(self.defaut, 'T2')
        type_ = Charge.charge_e.vacance_locative
        charge.add(type_, 0.5)
        self.assertEqual(charge.get_taux(type_), 0.5)

    def testAddTravauxProvision(self):
        '''default'''
        charge = Charge(self.defaut)
        type_ = Charge.charge_e.provision_travaux
        charge.add(type_, 1)

        self.assertEqual(charge.get_taux(type_), 0.01)
        with self.assertRaises(Exception):
            charge.get_montant_annuel(type_)

    def testAddMissingDefaut(self):
        charge = Charge(self.defaut)
        type_ = Charge.charge_e.copropriete

        with self.assertRaises(LookupError):
            charge.add(type_, 1)

    def testGetMontantAnnuel(self):
        '''get_montant_annuel with tuple, list'''
        charge = Charge(self.defaut)
        charge.add(Charge.charge_e.copropriete, 10)
        charge.add(Charge.charge_e.taxe_fonciere, 20)
        self.assertEqual(
            charge.get_montant_annuel(
                (Charge.charge_e.copropriete,
                 Charge.charge_e.taxe_fonciere)), 30)
        self.assertEqual(
            charge.get_montant_annuel(
                [Charge.charge_e.copropriete,
                 Charge.charge_e.taxe_fonciere]), 30)


if __name__ == '__main__':
    unittest.main()
