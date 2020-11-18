#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import rendement


class TestPrepareInput(unittest.TestCase):

    def testLoyerMensuelTotal_A(self):
        
        bien_immo = {'lots' : [{'loyer_mensuel': 100}]}
        rendement.prepare_inputs(bien_immo)
        
        self.assertEqual(bien_immo['loyers_mensuel_total'], 100)
    
    def testLoyerMensuelTotal_B(self):
        
        bien_immo = {'lots' : [{'loyer_mensuel': 100}, {'loyer_mensuel': 250}]}
        rendement.prepare_inputs(bien_immo)
        
        self.assertEqual(bien_immo['loyers_mensuel_total'], 350)
        
    def testLoyerAnnuelTotal(self):

        bien_immo = {'lots' : [{'loyer_mensuel': 100}, {'loyer_mensuel': 250}]}
        rendement.prepare_inputs(bien_immo)
        
        self.assertEqual(bien_immo['loyers_annuel_total'], 350*12)


class TestRendement(unittest.TestCase):

    def testRendementBrut(self):
        
        bien_immo = {'prix_achat' : 100000, 'loyers_annuel_total': 500 * 12}
        
        rendement.calcul_rendement_brut(bien_immo)
        self.assertEqual(bien_immo['r_brut'], 0.06)


if __name__ == '__main__':
    unittest.main()
