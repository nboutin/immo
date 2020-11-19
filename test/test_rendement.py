#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import json
import rendement

# TODO
# - Use setup function to load data_test.json


class TestCredit(unittest.TestCase):

    __DATA_TEST_PATHNAME = "test/res/data_test.json"

    def testMensualiteHorsAssurance(self):
        with open(TestCredit.__DATA_TEST_PATHNAME, 'r') as file:
            bien_immo = json.load(file)

        bien_immo['credit']['capital_emprunt'] = 136000
        bien_immo['credit']['duree_annee'] = 20
        bien_immo['credit']['taux_interet'] = 0.018

        rendement.calcul_credit(bien_immo)
        self.assertAlmostEqual(bien_immo['credit']['mensualite_hors_assurance'], 675.19, 2)

    def testMensualiteAssurance(self):
        with open(TestCredit.__DATA_TEST_PATHNAME, 'r') as file:
            bien_immo = json.load(file)

        bien_immo['credit']['capital_emprunt'] = 136000
        bien_immo['credit']['taux_assurance'] = 0.0036
        rendement.calcul_credit(bien_immo)
        self.assertAlmostEqual(bien_immo['credit']['mensualite_assurance'], 40.80, 2)

    def testMensualiteTotal(self):
        with open(TestCredit.__DATA_TEST_PATHNAME, 'r') as file:
            bien_immo = json.load(file)

        bien_immo['credit']['capital_emprunt'] = 136000
        bien_immo['credit']['duree_annee'] = 20
        bien_immo['credit']['taux_interet'] = 0.018
        bien_immo['credit']['taux_assurance'] = 0.0036
        rendement.calcul_credit(bien_immo)
        self.assertAlmostEqual(bien_immo['credit']['mensualite_total'], 715.99, 2)

    def testCoutInteret(self):
        with open(TestCredit.__DATA_TEST_PATHNAME, 'r') as file:
            bien_immo = json.load(file)

        bien_immo['credit']['capital_emprunt'] = 136000
        bien_immo['credit']['duree_annee'] = 20
        bien_immo['credit']['taux_interet'] = 0.018
        rendement.calcul_credit(bien_immo)
        self.assertAlmostEqual(bien_immo['credit']['cout_interet'], 26046.52, 2)

    def testCoutAssurance(self):
        with open(TestCredit.__DATA_TEST_PATHNAME, 'r') as file:
            bien_immo = json.load(file)

        bien_immo['credit']['capital_emprunt'] = 136000
        bien_immo['credit']['duree_annee'] = 20
        bien_immo['credit']['taux_assurance'] = 0.0036
        rendement.calcul_credit(bien_immo)
        self.assertAlmostEqual(bien_immo['credit']['cout_assurance'], 9792, 2)

    def testCoutCredit(self):
        with open(TestCredit.__DATA_TEST_PATHNAME, 'r') as file:
            bien_immo = json.load(file)

        bien_immo['credit']['capital_emprunt'] = 136000
        bien_immo['credit']['duree_annee'] = 20
        bien_immo['credit']['taux_interet'] = 0.018
        bien_immo['credit']['taux_assurance'] = 0.0036
        bien_immo['credit']['frais_dossier'] = 40
        bien_immo['credit']['frais_garantie'] = 60
        rendement.calcul_credit(bien_immo)
        self.assertAlmostEqual(bien_immo['credit']['cout_credit'], 35938.52, 2)


class TestPrepareInput(unittest.TestCase):

    __DATA_TEST_PATHNAME = "test/res/data_test.json"

    def testLoyerMensuelTotal_A(self):

        with open(TestPrepareInput.__DATA_TEST_PATHNAME, 'r') as file:
            bien_immo = json.load(file)

        bien_immo['lots'][0]['loyer_mensuel'] = 500
        rendement.prepare_inputs(bien_immo)

        self.assertEqual(bien_immo['loyers_mensuel_total'], 500)

    def testLoyerMensuelTotal_B(self):

        with open(TestPrepareInput.__DATA_TEST_PATHNAME, 'r') as file:
            bien_immo = json.load(file)

        bien_immo['lots'][0]['loyer_mensuel'] = 100
        bien_immo['lots'][1]['loyer_mensuel'] = 250
        rendement.prepare_inputs(bien_immo)
        self.assertEqual(bien_immo['loyers_mensuel_total'], 350)

    def testLoyerAnnuelTotal(self):

        with open(TestPrepareInput.__DATA_TEST_PATHNAME, 'r') as file:
            bien_immo = json.load(file)

        bien_immo['lots'][0]['loyer_mensuel'] = 100
        bien_immo['lots'][1]['loyer_mensuel'] = 250
        rendement.prepare_inputs(bien_immo)
        self.assertEqual(bien_immo['loyers_annuel_total'], 350 * 12)

    def testNotaireA(self):
        with open(TestPrepareInput.__DATA_TEST_PATHNAME, 'r') as file:
            bien_immo = json.load(file)

        bien_immo['prix_achat'] = 100000
        bien_immo['notaire']['honoraire_taux'] = 0.1
        rendement.prepare_inputs(bien_immo)

        self.assertEqual(bien_immo['notaire']['honoraire_montant'], 10000)

    def testNotaireB(self):
        with open(TestPrepareInput.__DATA_TEST_PATHNAME, 'r') as file:
            bien_immo = json.load(file)

        bien_immo['prix_achat'] = 100000
        bien_immo['notaire']['honoraire_montant'] = 5000
        rendement.prepare_inputs(bien_immo)

        self.assertEqual(bien_immo['notaire']['honoraire_taux'], 0.05)

    def testAgenceImmoA(self):
        with open(TestPrepareInput.__DATA_TEST_PATHNAME, 'r') as file:
            bien_immo = json.load(file)

        bien_immo['prix_achat'] = 100000
        bien_immo['agence_immo']['honoraire_taux'] = 0.08
        rendement.prepare_inputs(bien_immo)

        self.assertEqual(bien_immo['agence_immo']['honoraire_montant'], 8000)

    def testAgenceImmoB(self):
        with open(TestPrepareInput.__DATA_TEST_PATHNAME, 'r') as file:
            bien_immo = json.load(file)

        bien_immo['prix_achat'] = 100000
        bien_immo['agence_immo']['honoraire_montant'] = 6500
        rendement.prepare_inputs(bien_immo)

        self.assertEqual(bien_immo['agence_immo']['honoraire_taux'], 0.065)


class TestRendement(unittest.TestCase):

    __DATA_TEST_PATHNAME = "test/res/data_test.json"

    def testRendementBrutA(self):

        with open(TestRendement.__DATA_TEST_PATHNAME, 'r') as file:
            bien_immo = json.load(file)

        bien_immo['prix_achat'] = 100000
        bien_immo['lots'][0]['loyer_mensuel'] = 500
        rendement.prepare_inputs(bien_immo)
        rendement.calcul_rendement_brut(bien_immo)
        self.assertEqual(bien_immo['r_brut'], 0.06)

    def testRendementBrutB(self):

        with open(TestRendement.__DATA_TEST_PATHNAME, 'r') as file:
            bien_immo = json.load(file)

        bien_immo['prix_achat'] = 100000
        bien_immo['lots'][0]['loyer_mensuel'] = 500
        bien_immo['notaire']['honoraire_taux'] = 0.09
        bien_immo['agence_immo']['honoraire_taux'] = 0.06

        rendement.prepare_inputs(bien_immo)
        rendement.calcul_rendement_brut(bien_immo)
        self.assertAlmostEqual(bien_immo['r_brut'], 0.052, 3)

    def testRendementMethodeLarcher(self):
        with open(TestRendement.__DATA_TEST_PATHNAME, 'r') as file:
            bien_immo = json.load(file)

        bien_immo['prix_achat'] = 100000
        bien_immo['lots'][0]['loyer_mensuel'] = 500
        rendement.prepare_inputs(bien_immo)
        rendement.calcul_rendement_methode_larcher(bien_immo)
        self.assertEqual(bien_immo['r_larcher'], 0.045)

    def testRendementNetZeroCharges(self):

        with open(TestRendement.__DATA_TEST_PATHNAME, 'r') as file:
            bien_immo = json.load(file)

        rendement.prepare_inputs(bien_immo)
        bien_immo['invest_initial'] = 115000
        bien_immo['loyers_annuel_total'] = 500 * 12
        rendement.calcul_rendement_net(bien_immo)
        self.assertAlmostEqual(bien_immo['r_net'], 0.052, 3)

    def testRendementNetTaxeFonciere(self):

        with open(TestRendement.__DATA_TEST_PATHNAME, 'r') as file:
            bien_immo = json.load(file)

        bien_immo['taxe_fonciere'] = 1000
        rendement.prepare_inputs(bien_immo)
        bien_immo['invest_initial'] = 115000
        bien_immo['loyers_annuel_total'] = 500 * 12
        rendement.calcul_rendement_net(bien_immo)
        self.assertAlmostEqual(bien_immo['r_net'], 0.0435, 4)

    def testRendementNetTravauxProvision(self):

        with open(TestRendement.__DATA_TEST_PATHNAME, 'r') as file:
            bien_immo = json.load(file)

        bien_immo['lots'][0]['loyer_mensuel'] = 500
        bien_immo['travaux_provision'] = 0.01
        rendement.prepare_inputs(bien_immo)
        bien_immo['invest_initial'] = 115000
        rendement.calcul_rendement_net(bien_immo)
        self.assertAlmostEqual(bien_immo['r_net'], 0.0517, 4)

    def testRendementNetVacanceLocative(self):

        with open(TestRendement.__DATA_TEST_PATHNAME, 'r') as file:
            bien_immo = json.load(file)

        bien_immo['lots'][0]['loyer_mensuel'] = 500
        bien_immo['lots'][0]['vacance_locative'] = 1 / 24
        rendement.prepare_inputs(bien_immo)
        bien_immo['invest_initial'] = 115000
        rendement.calcul_rendement_net(bien_immo)
        self.assertAlmostEqual(bien_immo['r_net'], 0.0500, 4)

    def testRendementNetPNO(self):

        with open(TestRendement.__DATA_TEST_PATHNAME, 'r') as file:
            bien_immo = json.load(file)

        bien_immo['lots'][0]['loyer_mensuel'] = 500
        bien_immo['lots'][0]['assurance_pno'] = 100
        rendement.prepare_inputs(bien_immo)
        bien_immo['invest_initial'] = 115000
        rendement.calcul_rendement_net(bien_immo)
        self.assertAlmostEqual(bien_immo['r_net'], 0.0513, 4)

    def testRendementNetGestionAgence(self):

        with open(TestRendement.__DATA_TEST_PATHNAME, 'r') as file:
            bien_immo = json.load(file)

        bien_immo['lots'][0]['loyer_mensuel'] = 500
        bien_immo['lots'][0]['gestion_agence'] = 0.075
        rendement.prepare_inputs(bien_immo)
        bien_immo['invest_initial'] = 115000
        rendement.calcul_rendement_net(bien_immo)
        self.assertAlmostEqual(bien_immo['r_net'], 0.0483, 4)

    def testRendementNetCopropriete(self):

        with open(TestRendement.__DATA_TEST_PATHNAME, 'r') as file:
            bien_immo = json.load(file)

        bien_immo['lots'][0]['loyer_mensuel'] = 500
        bien_immo['lots'][0]['copropriete'] = 1000
        rendement.prepare_inputs(bien_immo)
        bien_immo['invest_initial'] = 115000
        rendement.calcul_rendement_net(bien_immo)
        self.assertAlmostEqual(bien_immo['r_net'], 0.0435, 4)


if __name__ == '__main__':
    unittest.main()
