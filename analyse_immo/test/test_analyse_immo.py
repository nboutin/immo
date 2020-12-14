#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest, sys, os
sys.path.insert(0, os.path.join('..'))

import json
from analyse_immo import make_bien_immo, make_credit
from rendement import Rendement


class TestAnalyseImmoBase(unittest.TestCase):
    
    def setUp(self):
        __DATA_TEST_PATHNAME = "test/res/input_test.json"
        with open(__DATA_TEST_PATHNAME, 'r') as file:
            input_data = json.load(file)

        self.achat_data = input_data['achat']
        self.lots_data = input_data['lots']
        self.credit_data = input_data['credit']


class TestRendement(TestAnalyseImmoBase):
            
    def testRendementBrut(self):
        self.achat_data['prix_net_vendeur'] = 100000
        self.lots_data[0]['loyer_nu_mensuel'] = 500
        bi = make_bien_immo(self.achat_data, self.lots_data)
        rdt = Rendement(bi)
        self.assertEqual(rdt.rendement_brut, 0.06)
        
        self.achat_data['frais_agence'] = 0.06
        bi = make_bien_immo(self.achat_data, self.lots_data)
        rdt = Rendement(bi)
        self.assertAlmostEqual(rdt.rendement_brut, 0.057, 3)
        
        self.achat_data['frais_agence'] = 0
        self.achat_data['frais_notaire'] = 0.09
        bi = make_bien_immo(self.achat_data, self.lots_data)
        rdt = Rendement(bi)
        self.assertAlmostEqual(rdt.rendement_brut, 0.055, 3)
        
        self.achat_data['frais_agence'] = 0.06
        self.achat_data['frais_notaire'] = 0.09
        bi = make_bien_immo(self.achat_data, self.lots_data)
        rdt = Rendement(bi)
        self.assertAlmostEqual(rdt.rendement_brut, 0.052, 3)

    def testRendementMethodeLarcher(self):
        self.achat_data['prix_net_vendeur'] = 100000
        self.lots_data[0]['loyer_nu_mensuel'] = 500
        bi = make_bien_immo(self.achat_data, self.lots_data)
        rdt = Rendement(bi)
        self.assertEqual(rdt.rendement_methode_larcher, 0.045)


class TestRendementNet(TestAnalyseImmoBase):
        
    def testSansCharges(self):
        self.achat_data['prix_net_vendeur'] = 115000
        self.lots_data[0]['loyer_nu_mensuel'] = 500
        bi = make_bien_immo(self.achat_data, self.lots_data)
        rdt = Rendement(bi)
        self.assertAlmostEqual(rdt.rendement_net, 0.052, 3)

    def testTaxeFonciere(self):
        self.achat_data['prix_net_vendeur'] = 115000
        self.lots_data[0]['loyer_nu_mensuel'] = 500
        self.lots_data[0]['charge']['taxe_fonciere'] = 1000
        bi = make_bien_immo(self.achat_data, self.lots_data)
        rdt = Rendement(bi)
        self.assertAlmostEqual(rdt.rendement_net, 0.0435, 4)

    def testTravauxProvision(self):
        self.achat_data['prix_net_vendeur'] = 115000
        self.lots_data[0]['loyer_nu_mensuel'] = 500
        self.lots_data[0]['gestion']['travaux_provision_taux'] = 0.01
        bi = make_bien_immo(self.achat_data, self.lots_data)
        rdt = Rendement(bi)
        self.assertAlmostEqual(rdt.rendement_net, 0.0517, 4)

    def testVacanceLocative(self):
        self.achat_data['prix_net_vendeur'] = 115000
        self.lots_data[0]['loyer_nu_mensuel'] = 500
        self.lots_data[0]['gestion']['vacance_locative_taux'] = 1 / 24
        bi = make_bien_immo(self.achat_data, self.lots_data)
        rdt = Rendement(bi)
        self.assertAlmostEqual(rdt.rendement_net, 0.05, 4)

    def testPNO(self):
        self.achat_data['prix_net_vendeur'] = 115000
        self.lots_data[0]['loyer_nu_mensuel'] = 500
        self.lots_data[0]['charge']['PNO'] = 100
        bi = make_bien_immo(self.achat_data, self.lots_data)
        rdt = Rendement(bi)
        self.assertAlmostEqual(rdt.rendement_net, 0.0513, 4)

    def testGestionAgence(self):
        self.achat_data['prix_net_vendeur'] = 115000
        self.lots_data[0]['loyer_nu_mensuel'] = 500
        self.lots_data[0]['gestion']['agence_immo'] = 0.075
        bi = make_bien_immo(self.achat_data, self.lots_data)
        rdt = Rendement(bi)
        self.assertAlmostEqual(rdt.rendement_net, 0.0483, 4)

    def testCopropriete(self):
        self.achat_data['prix_net_vendeur'] = 115000
        self.lots_data[0]['loyer_nu_mensuel'] = 500
        self.lots_data[0]['charge']['copropriete'] = 1000
        bi = make_bien_immo(self.achat_data, self.lots_data)
        rdt = Rendement(bi)
        self.assertAlmostEqual(rdt.rendement_net, 0.0435, 4)


class TestCashflow(TestAnalyseImmoBase):

    def testCashflowMensuel(self):
        self.achat_data['prix_net_vendeur'] = 136000
        self.lots_data[0]['loyer_nu_mensuel'] = 1000
        self.lots_data[0]['charge']['taxe_fonciere'] = 1500
        self.lots_data[0]['charge']['PNO'] = 100
        self.lots_data[0]['gestion']['travaux_provision_taux'] = 0.05
        self.credit_data['duree_annee'] = 20
        self.credit_data['taux_interet'] = 0.018
        self.credit_data['taux_assurance'] = 0.0036
        self.credit_data['mode'] = 'mode_1'

        bi = make_bien_immo(self.achat_data, self.lots_data)
        rdt = Rendement(bi)
        cred = make_credit(self.credit_data, bi)

        self.assertAlmostEqual(rdt.cashflow_mensuel(cred), 100.67, 2)


if __name__ == '__main__':
    unittest.main()
