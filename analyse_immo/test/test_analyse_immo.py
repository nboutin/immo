#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import json
import analyse_immo as anim
from rendement import Rendement


class TestRendement(unittest.TestCase):

    def setUp(self):
        __DATA_TEST_PATHNAME = "test/res/input_test.json"
        with open(__DATA_TEST_PATHNAME, 'r') as file:
            input_data = json.load(file)
            
        self.achat_data = input_data['achat']
        self.lots_data = input_data['lots']
            
    def testRendementBrut(self):
        self.achat_data['prix_net_vendeur'] = 100000
        self.lots_data[0]['loyer_nu_mensuel'] = 500
        bi = anim.make_bien_immo(self.achat_data, self.lots_data)
        rdt = Rendement(bi)
        self.assertEqual(rdt.rendement_brut, 0.06)
        
        self.achat_data['frais_agence'] = 0.06
        bi = anim.make_bien_immo(self.achat_data, self.lots_data)
        rdt = Rendement(bi)
        self.assertAlmostEqual(rdt.rendement_brut, 0.057, 3)
        
        self.achat_data['frais_agence'] = 0
        self.achat_data['frais_notaire'] = 0.09
        bi = anim.make_bien_immo(self.achat_data, self.lots_data)
        rdt = Rendement(bi)
        self.assertAlmostEqual(rdt.rendement_brut, 0.055, 3)
        
        self.achat_data['frais_agence'] = 0.06
        self.achat_data['frais_notaire'] = 0.09
        bi = anim.make_bien_immo(self.achat_data, self.lots_data)
        rdt = Rendement(bi)
        self.assertAlmostEqual(rdt.rendement_brut, 0.052, 3)

    def testRendementMethodeLarcher(self):
        self.achat_data['prix_net_vendeur'] = 100000
        self.lots_data[0]['loyer_nu_mensuel'] = 500
        bi = anim.make_bien_immo(self.achat_data, self.lots_data)
        rdt = Rendement(bi)
        self.assertEqual(rdt.rendement_methode_larcher, 0.045)


class TestRendementNet(unittest.TestCase):

    def setUp(self):
        __DATA_TEST_PATHNAME = "test/res/input_test.json"
        with open(__DATA_TEST_PATHNAME, 'r') as file:
            input_data = json.load(file)
            
        self.achat_data = input_data['achat']
        self.lots_data = input_data['lots']
        
    def testSansCharges(self):
        self.achat_data['prix_net_vendeur'] = 115000
        self.lots_data[0]['loyer_nu_mensuel'] = 500
        bi = anim.make_bien_immo(self.achat_data, self.lots_data)
        rdt = Rendement(bi)
        self.assertAlmostEqual(rdt.rendement_net, 0.052, 3)

    def testTaxeFonciere(self):
        self.achat_data['prix_net_vendeur'] = 115000
        self.lots_data[0]['loyer_nu_mensuel'] = 500
        self.achat_data['taxe_fonciere'] = 1000
        bi = anim.make_bien_immo(self.achat_data, self.lots_data)
        rdt = Rendement(bi)
        self.assertAlmostEqual(rdt.rendement_net, 0.0435, 4)

    def testTravauxProvision(self):
        self.achat_data['prix_net_vendeur'] = 115000
        self.lots_data[0]['loyer_nu_mensuel'] = 500
        self.achat_data['travaux_provision_taux'] = 0.01
        bi = anim.make_bien_immo(self.achat_data, self.lots_data)
        rdt = Rendement(bi)
        self.assertAlmostEqual(rdt.rendement_net, 0.0517, 4)

    def testVacanceLocative(self):
        self.achat_data['prix_net_vendeur'] = 115000
        self.lots_data[0]['loyer_nu_mensuel'] = 500
        self.lots_data[0]['vacance_locative'] = 1 / 24
        bi = anim.make_bien_immo(self.achat_data, self.lots_data)
        rdt = Rendement(bi)
        self.assertAlmostEqual(rdt.rendement_net, 0.05, 4)

    def testPNO(self):
        self.achat_data['prix_net_vendeur'] = 115000
        self.lots_data[0]['loyer_nu_mensuel'] = 500
        self.lots_data[0]['PNO'] = 100
        bi = anim.make_bien_immo(self.achat_data, self.lots_data)
        rdt = Rendement(bi)
        self.assertAlmostEqual(rdt.rendement_net, 0.0513, 4)

    def testGestionAgence(self):
        self.achat_data['prix_net_vendeur'] = 115000
        self.lots_data[0]['loyer_nu_mensuel'] = 500
        self.lots_data[0]['gestion_agence'] = 0.075
        bi = anim.make_bien_immo(self.achat_data, self.lots_data)
        rdt = Rendement(bi)
        self.assertAlmostEqual(rdt.rendement_net, 0.0483, 4)

    def testCopropriete(self):
        self.achat_data['prix_net_vendeur'] = 115000
        self.lots_data[0]['loyer_nu_mensuel'] = 500
        self.lots_data[0]['copropriete'] = 1000 / 12
        bi = anim.make_bien_immo(self.achat_data, self.lots_data)
        rdt = Rendement(bi)
        self.assertAlmostEqual(rdt.rendement_net, 0.0435, 4)


@unittest.skip('fixme')
class TestCashflow(unittest.TestCase):
    
    def setUp(self):
        __DATA_TEST_PATHNAME = "test/res/input_test.json"
        with open(__DATA_TEST_PATHNAME, 'r') as file:
            input_data = json.load(file)
            
        self.achat_data = input_data['achat']
        self.lots_data = input_data['lots']
        self.credit_data = input_data['credit']

    def testCashflowMensuel(self):
        self.achat_data['prix_net_vendeur'] = 136000
        self.achat_data['taxe_fonciere'] = 1500
        self.achat_data['travaux_provision'] = 0.05
        self.lots_data[0]['loyer_nu_mensuel'] = 1000
        self.lots_data[0]['assurance_pno'] = 100
        self.credit_data['duree_annee'] = 20
        self.credit_data['taux_interet'] = 0.018
        self.credit_data['taux_assurance'] = 0.0036

        bi = anim.make_bien_immo(self.achat_data, self.lots_data)
        rdt = Rendement(bi)
        cred = anim.make_credit(self._credit_data, bi)

        self.assertAlmostEqual(rdt.cashflow_mensuel(cred), 100.67, 2)
#         anim.prepare_inputs(bien_immo)
#         credit = rendement.calcul_credit(bien_immo)
#         rendement.calcul_cashflow(bien_immo, credit)
#         self.assertAlmostEqual(bien_immo['cashflow_mensuel'], 100.67, 2)


if __name__ == '__main__':
    unittest.main()
