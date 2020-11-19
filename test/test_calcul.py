#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import calcul


class TestCalcul(unittest.TestCase):

    def testRendementBrut(self):
        rbrut = calcul.rendement_brut(500 * 12, 50000)
        self.assertEqual(rbrut, 0.12)

    def testRendementMethodeLarcher(self):

        rlarcher = calcul.rendement_methode_larcher(500, 50000)
        self.assertEqual(rlarcher, 0.09)

    def testRendementNet(self):

        r_net = calcul.rendement_net(500 * 12, 1500, 50000)
        self.assertEqual(r_net, 0.09)

    def testCreditRemboursementConstantA(self):

        mensualite = calcul.credit_remboursement_constant(100000, 20, 0.015)
        self.assertAlmostEqual(mensualite, 482.55, 2)

    def testCreditRemboursementConstantB(self):

        mensualite = calcul.credit_remboursement_constant(88000, 15, 0.0099)
        self.assertAlmostEqual(mensualite, 526.29, 2)

    def testMensualiteAssurance(self):

        mensualite_assurance = calcul.mensualite_assurance(100000, 0.0035)
        self.assertAlmostEqual(mensualite_assurance, 29.17, 2)

    def testCoutInteret(self):

        cout_interet = calcul.cout_interet(100000, 20, 450)
        self.assertEqual(cout_interet, 8000)

    def testCoutAssurance(self):
        
        cout_assurance = calcul.cout_assurance(30, 20)
        self.assertEqual(cout_assurance, 7200)

if __name__ == '__main__':
    unittest.main()
