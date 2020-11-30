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

    def testCashflowMensuel(self):

        cashflow_mensuel = calcul.cashflow_mensuel(500, 350, 1500)
        self.assertEqual(cashflow_mensuel, 25)

    def testInteretEmprunt(self):

        interets = calcul.interet_emprunt(15000, 15 * 12, 0.04, 111)
        self.assertEqual(interets[0], 0)
        self.assertEqual(interets[1], 50)
        self.assertAlmostEqual(interets[12], 47.73, 2)
        self.assertAlmostEqual(interets[24], 45.15, 2)
        self.assertAlmostEqual(interets[36], 42.46, 2)


if __name__ == '__main__':
    unittest.main()
