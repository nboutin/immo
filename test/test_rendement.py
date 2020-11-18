#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import json
import rendement


class TestPrepareInput(unittest.TestCase):

    __DATA_A_PATHNAME = "test/res/dataA.json"
    __DATA_B_PATHNAME = "test/res/dataB.json"

    def testLoyerMensuelTotal_A(self):

        with open(TestPrepareInput.__DATA_A_PATHNAME, 'r') as file:
            bien_immo = json.load(file)
        rendement.prepare_inputs(bien_immo)

        self.assertEqual(bien_immo['loyers_mensuel_total'], 500)

    def testLoyerMensuelTotal_B(self):

        with open(TestPrepareInput.__DATA_B_PATHNAME, 'r') as file:
            bien_immo = json.load(file)
        rendement.prepare_inputs(bien_immo)

        self.assertEqual(bien_immo['loyers_mensuel_total'], 350)

    def testLoyerAnnuelTotal(self):

        with open(TestPrepareInput.__DATA_B_PATHNAME, 'r') as file:
            bien_immo = json.load(file)
        rendement.prepare_inputs(bien_immo)

        self.assertEqual(bien_immo['loyers_annuel_total'], 350 * 12)

    def testNotaireA(self):
        with open(TestPrepareInput.__DATA_A_PATHNAME, 'r') as file:
            bien_immo = json.load(file)

        bien_immo['notaire']['honoraire_taux'] = 0.1
        rendement.prepare_inputs(bien_immo)

        self.assertEqual(bien_immo['notaire']['honoraire_montant'], 10000)

    def testNotaireB(self):
        with open(TestPrepareInput.__DATA_A_PATHNAME, 'r') as file:
            bien_immo = json.load(file)

        bien_immo['notaire']['honoraire_montant'] = 5000
        rendement.prepare_inputs(bien_immo)

        self.assertEqual(bien_immo['notaire']['honoraire_taux'], 0.05)

    def testAgenceImmoA(self):
        with open(TestPrepareInput.__DATA_A_PATHNAME, 'r') as file:
            bien_immo = json.load(file)

        bien_immo['agence_immo']['honoraire_taux'] = 0.08
        rendement.prepare_inputs(bien_immo)

        self.assertEqual(bien_immo['agence_immo']['honoraire_montant'], 8000)

    def testAgenceImmoB(self):
        with open(TestPrepareInput.__DATA_A_PATHNAME, 'r') as file:
            bien_immo = json.load(file)

        bien_immo['agence_immo']['honoraire_montant'] = 6500
        rendement.prepare_inputs(bien_immo)

        self.assertEqual(bien_immo['agence_immo']['honoraire_taux'], 0.065)


class TestRendement(unittest.TestCase):

    __DATA_A_PATHNAME = "test/res/dataA.json"
    __DATA_B_PATHNAME = "test/res/dataB.json"

    def testRendementBrutA(self):

        with open(TestRendement.__DATA_A_PATHNAME, 'r') as file:
            bien_immo = json.load(file)

        rendement.prepare_inputs(bien_immo)
        rendement.calcul_rendement_brut(bien_immo)
        self.assertEqual(bien_immo['r_brut'], 0.06)

    def testRendementBrutB(self):

        with open(TestRendement.__DATA_A_PATHNAME, 'r') as file:
            bien_immo = json.load(file)

        bien_immo['notaire']['honoraire_taux'] = 0.09
        bien_immo['agence_immo']['honoraire_taux'] = 0.06

        rendement.prepare_inputs(bien_immo)
        rendement.calcul_rendement_brut(bien_immo)
        self.assertAlmostEqual(bien_immo['r_brut'], 0.052, 3)

    def testRendementMethodeLarcher(self):
        with open(TestRendement.__DATA_A_PATHNAME, 'r') as file:
            bien_immo = json.load(file)

        rendement.prepare_inputs(bien_immo)
        rendement.calcul_rendement_methode_larcher(bien_immo)
        self.assertEqual(bien_immo['r_larcher'], 0.045)


if __name__ == '__main__':
    unittest.main()
