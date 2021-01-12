#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from analyse_immo.credit import Credit


class TestCreditMode2(unittest.TestCase):

    def setUp(self):

        self.credit = Credit(50000, 240, 0.0115, 0.0026, Credit.mode_e.m2, 0, 0)

    def testTotal(self):
        self.assertAlmostEqual(self.credit.get_montant_interet_total(), 6043.69, 2)
        self.assertAlmostEqual(self.credit.get_montant_assurance_total(), 1366.40, 2)
        self.assertAlmostEqual(self.credit.get_amortissement_total(), 50000, 2)
        self.assertAlmostEqual(self.credit.get_mensualite_hors_assurance_total(), 56043.69, 2)
        self.assertAlmostEqual(self.credit.get_mensualite_avec_assurance_total(), 57410.09, 2)
        self.assertAlmostEqual(self.credit.get_cout_total(), 7410.09, 2)

    def testRangeNone(self):
        self.assertAlmostEqual(self.credit.get_amortissement(), 180.46, 2)
        self.assertAlmostEqual(self.credit.get_interet(), 47.92, 2)
        self.assertAlmostEqual(self.credit.get_mensualite_assurance(), 10.83, 2)
        self.assertAlmostEqual(self.credit.get_mensualite_hors_assurance(), 228.38, 2)
        self.assertAlmostEqual(self.credit.get_mensualite_avec_assurance(), 239.21, 2)

    def testRange1(self):
        self.assertAlmostEqual(self.credit.get_amortissement(1), 180.46, 2)
        self.assertAlmostEqual(self.credit.get_interet(1), 47.92, 2)
        self.assertAlmostEqual(self.credit.get_mensualite_assurance(1), 10.83, 2)
        self.assertAlmostEqual(self.credit.get_mensualite_hors_assurance(1), 228.38, 2)
        self.assertAlmostEqual(self.credit.get_mensualite_avec_assurance(1), 239.21, 2)

    def testRange2(self):
        start = 2
        self.assertAlmostEqual(self.credit.get_amortissement(start), 180.67, 2)
        self.assertAlmostEqual(self.credit.get_interet(start), 47.74, 2)
        self.assertAlmostEqual(self.credit.get_mensualite_assurance(start), 10.79, 2)
        self.assertAlmostEqual(self.credit.get_mensualite_hors_assurance(start), 228.41, 2)
        self.assertAlmostEqual(self.credit.get_mensualite_avec_assurance(start), 239.21, 2)

    def testRange12(self):
        start = 12
        self.assertAlmostEqual(self.credit.get_amortissement(start), 182.80, 2)
        self.assertAlmostEqual(self.credit.get_interet(start), 46, 2)
        self.assertAlmostEqual(self.credit.get_mensualite_assurance(start), 10.40, 2)
        self.assertAlmostEqual(self.credit.get_mensualite_hors_assurance(start), 228.81, 2)
        self.assertAlmostEqual(self.credit.get_mensualite_avec_assurance(start), 239.21, 2)

    def testRange228(self):
        start = 228
        self.assertAlmostEqual(self.credit.get_amortissement(start), 235.58, 2)
        self.assertAlmostEqual(self.credit.get_interet(start), 2.96, 2)
        self.assertAlmostEqual(self.credit.get_mensualite_assurance(start), 0.67, 2)
        self.assertAlmostEqual(self.credit.get_mensualite_hors_assurance(start), 238.54, 2)
        self.assertAlmostEqual(self.credit.get_mensualite_avec_assurance(start), 239.21, 2)

    def testRange240(self):
        start = 240
        self.assertAlmostEqual(self.credit.get_amortissement(start), 238.93, 2)
        self.assertAlmostEqual(self.credit.get_interet(start), 0.23, 2)
        self.assertAlmostEqual(self.credit.get_mensualite_assurance(start), 0.05, 2)
        self.assertAlmostEqual(self.credit.get_mensualite_hors_assurance(start), 239.16, 2)
        self.assertAlmostEqual(self.credit.get_mensualite_avec_assurance(start), 239.21, 2)

    def testRange1_2(self):
        start = 1
        stop = 2
        self.assertAlmostEqual(self.credit.get_amortissement(start, stop), 180.46 + 180.67, 2)
        self.assertAlmostEqual(self.credit.get_interet(start, stop), 47.92 + 47.74, 2)
        self.assertAlmostEqual(self.credit.get_mensualite_assurance(start, stop), 10.83 + 10.80, 2)
        self.assertAlmostEqual(self.credit.get_mensualite_hors_assurance(start, stop), 228.38 + 228.41, 2)
        self.assertAlmostEqual(self.credit.get_mensualite_avec_assurance(start, stop), 239.21 + 239.21, 2)

    def testRange1_240(self):
        start = 1
        stop = 240
        self.assertAlmostEqual(self.credit.get_amortissement(start, stop), 50000, 2)
        self.assertAlmostEqual(self.credit.get_interet(start, stop), 6043.69, 2)
        self.assertAlmostEqual(self.credit.get_mensualite_assurance(start, stop), 1366.40, 2)
        self.assertAlmostEqual(self.credit.get_mensualite_hors_assurance(start, stop), 56043.69, 2)
        self.assertAlmostEqual(self.credit.get_mensualite_avec_assurance(start, stop), 57410.09, 2)


if __name__ == '__main__':
    unittest.main()
