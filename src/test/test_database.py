#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from analyse_immo.database import Database


class TestDatabase(unittest.TestCase):

    def testIRPPBareme(self):
        database = Database()
        self.assertTrue(set(database.irpp_bareme(2020)[0]) & set([10064, 0]))
        self.assertTrue(set(database.irpp_bareme('2020')[0]) & set([10064, 0]))

    def testPlafondQuotientFamilial(self):
        database = Database()
        self.assertEqual(database.plafond_quotient_familial(2021), 1570)
        self.assertEqual(database.plafond_quotient_familial('2021'), 1570)

    def testPrelevementSociaux(self):
        database = Database()
        self.assertEqual(database.prelevement_sociaux_taux, 0.172)

    def testMicroFoncierTaux(self):
        database = Database()
        self.assertEqual(database.micro_foncier_taux, 0.3)

    def testRevenuFoncierPlafond(self):
        database = Database()
        self.assertEqual(database.micro_foncier_revenu_foncier_plafond, 15000)


if __name__ == '__main__':
    unittest.main()
