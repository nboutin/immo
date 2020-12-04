#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import json
import analyse_immo as anim
from rendement import Rendement

# TODO
# - Use setup function to load data_test.json


class TestCashflow(unittest.TestCase):

    __DATA_TEST_PATHNAME = "test/res/data_test.json"

    def testCashflowMensuel(self):
        with open(TestCashflow.__DATA_TEST_PATHNAME, 'r') as file:
            bien_immo = json.load(file)

        bien_immo['prix_net_vendeur'] = 136000
        bien_immo['taxe_fonciere'] = 1500
        bien_immo['travaux_provision'] = 0.05
        bien_immo['lots'][0]['loyer_mensuel'] = 1000
        bien_immo['lots'][0]['assurance_pno'] = 100
        bien_immo['credit']['duree_annee'] = 20
        bien_immo['credit']['taux_interet'] = 0.018
        bien_immo['credit']['taux_assurance'] = 0.0036

        anim.prepare_inputs(bien_immo)
        credit = rendement.calcul_credit(bien_immo)
        rendement.calcul_cashflow(bien_immo, credit)
        self.assertAlmostEqual(bien_immo['cashflow_mensuel'], 100.67, 2)


class TestRendement(unittest.TestCase):

    def setUp(self):
        __DATA_TEST_PATHNAME = "test/res/data_test.json"

        with open(__DATA_TEST_PATHNAME, 'r') as file:
            in_user = json.load(file)
            
        self._bien_immo = in_user['bien_immo']
            
    def testRendementBrut(self):
        self._bien_immo['prix_net_vendeur'] = 100000
        self._bien_immo['lots'][0]['loyer_mensuel'] = 500
        bi = anim.make_bien_immo(self._bien_immo)
        rdt = Rendement(bi)
        self.assertEqual(rdt.rendement_brut, 0.06)
        
        self._bien_immo['frais_agence'] = 0.06
        self._bien_immo['frais_notaire'] = 0.09
        bi = anim.make_bien_immo(self._bien_immo)
        rdt = Rendement(bi)
        self.assertAlmostEqual(rdt.rendement_brut, 0.052, 3)

#     def testRendementBrutB(self):
# 
#         with open(TestRendement.__DATA_TEST_PATHNAME, 'r') as file:
#             bien_immo = json.load(file)
# 
#         bien_immo['prix_net_vendeur'] = 100000
#         bien_immo['lots'][0]['loyer_mensuel'] = 500
#         bien_immo['notaire']['honoraire_taux'] = 0.09
#         bien_immo['agence_immo']['honoraire_taux'] = 0.06
# 
#         rendement.prepare_inputs(bien_immo)
#         rendement.calcul_rendement_brut(bien_immo)
#         self.assertAlmostEqual(bien_immo['r_brut'], 0.052, 3)

    def testRendementMethodeLarcher(self):
        with open(TestRendement.__DATA_TEST_PATHNAME, 'r') as file:
            bien_immo = json.load(file)

        bien_immo['prix_net_vendeur'] = 100000
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
