#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import sys
import os
sys.path.insert(0, os.path.join('..'))

from credit import Credit


class TestCredit(unittest.TestCase):

    def testConstructeur(self):
        Credit(0, 0, 0, 0, Credit.mode_e.m1, 0, 0)
        Credit(0, 1, 0, 0, Credit.mode_e.m2, 0, 0)

    def testGetMensualiteConstante(self):

        self.assertAlmostEqual(Credit._calcul_mensualite_constante(100000, 0.015, 240), 482.55, 2)
        self.assertAlmostEqual(
            Credit._calcul_mensualite_constante(88000, 0.0099, 15 * 12), 526.29, 2)
        self.assertAlmostEqual(Credit._calcul_mensualite_constante(136000, 0.018, 240), 675.19, 2)

    def testGetMensualiteHorsAssurance(self):

        cred = Credit(100000, 240, 0.015, 0, Credit.mode_e.m1, 0, 0)
        self.assertAlmostEqual(cred.get_mensualite_hors_assurance(), 482.55, 2)

        cred = Credit(88000, 15 * 12, 0.0099, 0, Credit.mode_e.m1, 0, 0)
        self.assertAlmostEqual(cred.get_mensualite_hors_assurance(), 526.29, 2)

        cred = Credit(136000, 240, 0.018, 0, Credit.mode_e.m1, 0, 0)
        self.assertAlmostEqual(cred.get_mensualite_hors_assurance(), 675.19, 2)

    @unittest.skip('fixme')
    def testGetMensualiteAssurance(self):

        cred = Credit(136000, 0, 0, 0.0036, Credit.mode_e.m1, 0, 0)
        self.assertAlmostEqual(cred.get_mensualite_assurance(), 40.80, 2)

    def testGetMensualiteAvecAssurance(self):

        cred = Credit(100000, 1, 0, 0.0035, Credit.mode_e.m1, 0, 0)
        self.assertAlmostEqual(cred.get_mensualite_avec_assurance(), 29.17, 2)

        cred = Credit(136000, 240, 0.018, 0.0036, Credit.mode_e.m1, 0, 0)
        self.assertAlmostEqual(cred.get_mensualite_avec_assurance(), 715.99, 2)

    def testMensualiteTotal(self):

        cred = Credit(10000, 36, 0.02, 0, Credit.mode_e.m1, 0, 0)
        self.assertAlmostEqual(cred.get_mensualite_total(), 10311.33, 2)

    def testMontantInteretTotal(self):

        cred = Credit(10000, 36, 0.02, 0, Credit.mode_e.m1, 0, 0)
        self.assertAlmostEqual(cred.get_montant_interet_total(), 311.33, 2)

        cred = Credit(100000, 240, 0.02, 0, Credit.mode_e.m1, 0, 0)
        self.assertAlmostEqual(cred.get_montant_interet_total(), 21412, 2)

        cred = Credit(136000, 240, 0.018, 0, Credit.mode_e.m1, 0, 0)
        self.assertAlmostEqual(cred.get_montant_interet_total(), 26046.52, 2)

    def testMontantAssuranceTotal(self):

        cred = Credit(10000, 36, 0.02, 0.0030, Credit.mode_e.m1, 0, 0)
        self.assertAlmostEqual(cred.get_montant_assurance_total(), 90, 2)

        cred = Credit(136000, 240, 0.02, 0.0036, Credit.mode_e.m1, 0, 0)
        self.assertAlmostEqual(cred.get_montant_assurance_total(), 9792, 2)

    def testCoutTotal(self):

        cred = Credit(10000, 36, 0.02, 0.0030, Credit.mode_e.m1, 100, 200)
        self.assertAlmostEqual(cred.get_cout_total(), 701.33, 2)

        cred = Credit(136000, 240, 0.018, 0.0036, Credit.mode_e.m1, 40, 60)
        self.assertAlmostEqual(cred.get_cout_total(), 35938.52, 2)

    def testAmortissementMode1A(self):
        cred = Credit(10000, 36, 0.02, 0, Credit.mode_e.m1, 0, 0)

        tam = cred.get_amortissement(1)
        self.assertAlmostEqual(tam['capital'], 10000, 2)
        self.assertAlmostEqual(tam['amortissement'], 269.76, 2)
        self.assertAlmostEqual(tam['interet'], 16.67, 2)
        self.assertAlmostEqual(tam['assurance'], 0, 2)
        self.assertAlmostEqual(tam['mensualite_aa'], 286.43, 2)

        tam = cred.get_amortissement(36)
        self.assertAlmostEqual(tam['capital'], 285.95, 2)
        self.assertAlmostEqual(tam['amortissement'], 285.95, 2)
        self.assertAlmostEqual(tam['interet'], 0.48, 2)
        self.assertAlmostEqual(tam['assurance'], 0, 2)
        self.assertAlmostEqual(tam['mensualite_aa'], 286.43, 2)

    def testAmortissementMode1B(self):
        cred = Credit(10000, 36, 0.02, 0.0030, Credit.mode_e.m1, 0, 0)

        tam = cred.get_amortissement(1)
        self.assertAlmostEqual(tam['capital'], 10000, 2)
        self.assertAlmostEqual(tam['interet'], 16.67, 2)
        self.assertAlmostEqual(tam['assurance'], 2.50, 2)
        self.assertAlmostEqual(tam['amortissement'], 269.76, 2)
        self.assertAlmostEqual(tam['mensualite_aa'], 288.93, 2)

        tam = cred.get_amortissement(36)
        self.assertAlmostEqual(tam['capital'], 285.95, 2)
        self.assertAlmostEqual(tam['amortissement'], 285.95, 2)
        self.assertAlmostEqual(tam['interet'], 0.48, 2)
        self.assertAlmostEqual(tam['assurance'], 2.5, 2)
        self.assertAlmostEqual(tam['mensualite_aa'], 288.93, 2)

    def testAmortissementMode2(self):
        cred = Credit(10000, 36, 0.02, 0.0030, Credit.mode_e.m2, 0, 0)

        tam = cred.get_amortissement(1)
        self.assertAlmostEqual(tam['capital'], 10000, 2)
        self.assertAlmostEqual(tam['interet'], 16.67, 2)
        self.assertAlmostEqual(tam['assurance'], 2.50, 2)
        self.assertAlmostEqual(tam['amortissement'], 268.57, 2)
        self.assertAlmostEqual(tam['mensualite_aa'], 287.74, 2)

        tam = cred.get_amortissement(36)
        self.assertAlmostEqual(tam['capital'], 287.19, 2)
        self.assertAlmostEqual(tam['interet'], 0.48, 2)
        self.assertAlmostEqual(tam['assurance'], 0.07, 2)
        self.assertAlmostEqual(tam['amortissement'], 287.19, 2)
        self.assertAlmostEqual(tam['mensualite_aa'], 287.74, 2)

        self.assertAlmostEqual(cred.get_amortissement_total(), 10000, 2)
        self.assertAlmostEqual(cred.get_montant_interet_total(), 311.78, 2)
        self.assertAlmostEqual(cred.get_montant_assurance_total(), 46.77, 2)
        self.assertAlmostEqual(cred.get_mensualite_hors_assurance_total(), 10311.78, 2)
        self.assertAlmostEqual(cred.get_mensualite_avec_assurance_total(), 10358.54, 2)

    def testAmortissementMode3(self):
        cred = Credit(81600, 240, 0.0115, 0.0026, Credit.mode_e.m3, 0, 0)

        tam = cred.get_amortissement(1)
        self.assertAlmostEqual(tam['mensualite_ha'], 380.76, 2)

        self.assertAlmostEqual(cred.get_amortissement_total(), 81600, 2)
        self.assertAlmostEqual(cred.get_montant_interet_total(), 9782.33, 2)
        self.assertAlmostEqual(cred.get_montant_assurance_total(), 2211.66, 2)  # 2234.76
        self.assertAlmostEqual(cred.get_mensualite_hors_assurance_total(), 91382.33, 2)
        self.assertAlmostEqual(cred.get_mensualite_avec_assurance_total(), 93593.98, 2)

    @unittest.skip("not ready")
    def testAmortissementMode4(self):
        pass
#         '''
#         81.6K, 1.15%, 240m, 0.26% (capital restant annuel), mensualite_aa degressive
#         '''
#
#         tam, tam_totaux = calcul.tableau_amortissement(81600, 240, 0.0115, 0.0026, 'mode_4')
#
#         self.assertAlmostEqual(tam[0]['assurance'], 11.41, 2)
#
#         self.assertAlmostEqual(tam_totaux['amortissement'], 81600, 2)
#         self.assertAlmostEqual(tam_totaux['interets'], 9782.33, 2)
#         self.assertAlmostEqual(tam_totaux['assurance'], 2234.76, 2)
#         self.assertAlmostEqual(tam_totaux['mensualite_ha'], 91382.33, 2)
#         self.assertAlmostEqual(tam_totaux['mensualite_aa'], 93617.16, 2)
#
#         self.assertAlmostEqual(tam[0]['mensualite_ha'], 380.76, 2)


if __name__ == '__main__':
    unittest.main()
