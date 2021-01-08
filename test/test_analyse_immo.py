#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from analyse_immo.factory import Factory
from analyse_immo.rendement import Rendement
from test.testcase_fileloader import TestCaseFileLoader


class TestRendement(TestCaseFileLoader):

    def testRendementBrut(self):
        self.achat_data['prix_net_vendeur'] = 100000
        self.lots_data[0]['loyer_nu_mensuel'] = 500
        bi = Factory.make_bien_immo(self.achat_data, self.lots_data)
        rdt = Rendement(bi)
        self.assertEqual(rdt.rendement_brut, 0.06)

        self.achat_data['frais_agence'] = 0.06
        bi = Factory.make_bien_immo(self.achat_data, self.lots_data)
        rdt = Rendement(bi)
        self.assertAlmostEqual(rdt.rendement_brut, 0.057, 3)

        self.achat_data['frais_agence'] = 0
        self.achat_data['frais_notaire'] = 0.09
        bi = Factory.make_bien_immo(self.achat_data, self.lots_data)
        rdt = Rendement(bi)
        self.assertAlmostEqual(rdt.rendement_brut, 0.055, 3)

        self.achat_data['frais_agence'] = 0.06
        self.achat_data['frais_notaire'] = 0.09
        bi = Factory.make_bien_immo(self.achat_data, self.lots_data)
        rdt = Rendement(bi)
        self.assertAlmostEqual(rdt.rendement_brut, 0.052, 3)

    def testRendementMethodeLarcher(self):
        self.achat_data['prix_net_vendeur'] = 100000
        self.lots_data[0]['loyer_nu_mensuel'] = 500
        bi = Factory.make_bien_immo(self.achat_data, self.lots_data)
        rdt = Rendement(bi)
        self.assertEqual(rdt.rendement_methode_larcher, 0.045)


class TestRendementNet(TestCaseFileLoader):

    def testSansCharges(self):
        self.achat_data['prix_net_vendeur'] = 115000
        self.lots_data[0]['loyer_nu_mensuel'] = 500
        bi = Factory.make_bien_immo(self.achat_data, self.lots_data)
        rdt = Rendement(bi)
        self.assertAlmostEqual(rdt.rendement_net, 0.052, 3)

    def testTaxeFonciere(self):
        self.achat_data['prix_net_vendeur'] = 115000
        self.lots_data[0]['loyer_nu_mensuel'] = 500
        self.lots_data[0]['charges']['taxe_fonciere'] = 1000
        bi = Factory.make_bien_immo(self.achat_data, self.lots_data)
        rdt = Rendement(bi)
        self.assertAlmostEqual(rdt.rendement_net, 0.0435, 4)

    def testTravauxProvision(self):
        self.achat_data['prix_net_vendeur'] = 115000
        self.lots_data[0]['loyer_nu_mensuel'] = 500
        self.lots_data[0]['charges']['travaux_provision_taux'] = 0.01
        bi = Factory.make_bien_immo(self.achat_data, self.lots_data)
        rdt = Rendement(bi)
        self.assertAlmostEqual(rdt.rendement_net, 0.0517, 4)

    def testVacanceLocative(self):
        self.achat_data['prix_net_vendeur'] = 115000
        self.lots_data[0]['loyer_nu_mensuel'] = 500
        self.lots_data[0]['charges']['vacance_locative_taux'] = 1 / 24
        bi = Factory.make_bien_immo(self.achat_data, self.lots_data)
        rdt = Rendement(bi)
        self.assertAlmostEqual(rdt.rendement_net, 0.05, 4)

    def testPNO(self):
        self.achat_data['prix_net_vendeur'] = 115000
        self.lots_data[0]['loyer_nu_mensuel'] = 500
        self.lots_data[0]['charges']['PNO'] = 100
        bi = Factory.make_bien_immo(self.achat_data, self.lots_data)
        rdt = Rendement(bi)
        self.assertAlmostEqual(rdt.rendement_net, 0.0513, 4)

    def testGestionAgence(self):
        self.achat_data['prix_net_vendeur'] = 115000
        self.lots_data[0]['loyer_nu_mensuel'] = 500
        self.lots_data[0]['charges']['agence_immo'] = 0.075
        bi = Factory.make_bien_immo(self.achat_data, self.lots_data)
        rdt = Rendement(bi)
        self.assertAlmostEqual(rdt.rendement_net, 0.0483, 4)

    def testCopropriete(self):
        self.achat_data['prix_net_vendeur'] = 115000
        self.lots_data[0]['loyer_nu_mensuel'] = 500
        self.lots_data[0]['charges']['copropriete'] = 1000
        bi = Factory.make_bien_immo(self.achat_data, self.lots_data)
        rdt = Rendement(bi)
        self.assertAlmostEqual(rdt.rendement_net, 0.0435, 4)


class TestCashflow(TestCaseFileLoader):

    def testCashflowMensuel(self):
        self.achat_data['prix_net_vendeur'] = 136000
        self.lots_data[0]['loyer_nu_mensuel'] = 1000
        self.lots_data[0]['charges']['taxe_fonciere'] = 1500
        self.lots_data[0]['charges']['PNO'] = 100
        self.lots_data[0]['charges']['travaux_provision_taux'] = 0.05
        self.credit_data['duree_annee'] = 20
        self.credit_data['taux_interet'] = 0.018
        self.credit_data['taux_assurance'] = 0.0036
        self.credit_data['mode'] = 'mode_1'

        bi = Factory.make_bien_immo(self.achat_data, self.lots_data)
        cred = Factory.make_credit(self.credit_data, bi)
        rdt = Rendement(bi, cred)

        self.assertAlmostEqual(rdt.cashflow_mensuel, 100.67, 2)


if __name__ == '__main__':
    unittest.main()
