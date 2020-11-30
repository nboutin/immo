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
        
    def testTableauAmortissement_1(self):
        '''
        10K, 2%, 36m, assurance 0%
        '''
        tam, tam_totaux = calcul.tableau_amortissement(10000, 36, 0.02, 0, 'mode_1')
        self.assertAlmostEqual(tam[0]['capital'], 10000, 2)
        self.assertAlmostEqual(tam[0]['amortissement'], 269.76, 2)
        self.assertAlmostEqual(tam[0]['interets'], 16.67, 2)
        self.assertAlmostEqual(tam[0]['assurance'], 0, 2)
        self.assertAlmostEqual(tam[0]['mensualite'], 286.43, 2)

        self.assertAlmostEqual(tam[35]['capital'], 285.95, 2)
        self.assertAlmostEqual(tam[35]['amortissement'], 285.95, 2)
        self.assertAlmostEqual(tam[35]['interets'], 0.48, 2)
        self.assertAlmostEqual(tam[35]['assurance'], 0, 2)
        self.assertAlmostEqual(tam[35]['mensualite'], 286.43, 2)
        
        self.assertAlmostEqual(tam_totaux['amortissement'], 10000, 2)
        self.assertAlmostEqual(tam_totaux['interets'], 311.33, 2)
        self.assertAlmostEqual(tam_totaux['assurance'], 0, 2)
        self.assertAlmostEqual(tam_totaux['mensualite_ha'], 10311.33, 2)
        self.assertAlmostEqual(tam_totaux['mensualite_aa'], 10311.33, 2)
        
    def testTableauAmortissement_2(self):
        '''
        10K, 2%, 36m, assurance 0.30% (capital initial)
        '''
        tam, tam_totaux = calcul.tableau_amortissement(10000, 36, 0.02, 0.0030, 'mode_1')
        self.assertAlmostEqual(tam[0]['capital'], 10000, 2)
        self.assertAlmostEqual(tam[0]['interets'], 16.67, 2)
        self.assertAlmostEqual(tam[0]['assurance'], 2.50, 2)
        self.assertAlmostEqual(tam[0]['amortissement'], 269.76, 2)
        self.assertAlmostEqual(tam[0]['mensualite'], 288.93, 2)

        self.assertAlmostEqual(tam[35]['capital'], 285.95, 2)
        self.assertAlmostEqual(tam[35]['amortissement'], 285.95, 2)
        self.assertAlmostEqual(tam[35]['interets'], 0.48, 2)
        self.assertAlmostEqual(tam[35]['assurance'], 2.5, 2)
        self.assertAlmostEqual(tam[35]['mensualite'], 288.93, 2)
        
        self.assertAlmostEqual(tam_totaux['amortissement'], 10000, 2)
        self.assertAlmostEqual(tam_totaux['interets'], 311.33, 2)
        self.assertAlmostEqual(tam_totaux['assurance'], 90, 2)
        self.assertAlmostEqual(tam_totaux['mensualite_ha'], 10311.33, 2)
        self.assertAlmostEqual(tam_totaux['mensualite_aa'], 10401.33, 2)
        
    def testTableauAmortissement_3(self):
        '''
        10K, 2%, 36m, assurance 0.30% (capital restant), mensualite_aa constant
        '''
        tam, tam_totaux = calcul.tableau_amortissement(10000, 36, 0.02, 0.0030, 'mode_2')
        self.assertAlmostEqual(tam[0]['capital'], 10000, 2)
        self.assertAlmostEqual(tam[0]['interets'], 16.67, 2)
        self.assertAlmostEqual(tam[0]['assurance'], 2.50, 2)
        self.assertAlmostEqual(tam[0]['amortissement'], 268.57, 2)
        self.assertAlmostEqual(tam[0]['mensualite'], 287.74, 2)

        self.assertAlmostEqual(tam[35]['capital'], 287.19, 2)
        self.assertAlmostEqual(tam[35]['interets'], 0.48, 2)
        self.assertAlmostEqual(tam[35]['assurance'], 0.07, 2)
        self.assertAlmostEqual(tam[35]['amortissement'], 287.19, 2)
        self.assertAlmostEqual(tam[35]['mensualite'], 287.74, 2)
        
        self.assertAlmostEqual(tam_totaux['amortissement'], 10000, 2)
        self.assertAlmostEqual(tam_totaux['interets'], 311.78, 2)
        self.assertAlmostEqual(tam_totaux['assurance'], 46.77, 2)
        self.assertAlmostEqual(tam_totaux['mensualite_ha'], 10311.78, 2)
        self.assertAlmostEqual(tam_totaux['mensualite_aa'], 10358.54, 2)
         
    def testTableauAmortissement_4(self):
        '''
        81.6K, 1.15%, 240m, 0.26% (capital restant), mensualite_aa degressive
        '''
         
        tam, tam_totaux = calcul.tableau_amortissement(81600, 240, 0.0115, 0.0026, 'mode_3')
         
        self.assertAlmostEqual(tam_totaux['amortissement'], 81600, 2)
        self.assertAlmostEqual(tam_totaux['interets'], 9782.33, 2)
        self.assertAlmostEqual(tam_totaux['assurance'], 2211.66, 2) #2234.76
        self.assertAlmostEqual(tam_totaux['mensualite_ha'], 91382.33, 2)
        self.assertAlmostEqual(tam_totaux['mensualite_aa'], 93593.98, 2)

        self.assertAlmostEqual(tam[0]['mensualite_ha'], 380.76, 2)
        
    @unittest.skip("not ready")
    def testTableauAmortissement_5(self):
        '''
        81.6K, 1.15%, 240m, 0.26% (capital restant annuel), mensualite_aa degressive
        '''
          
        tam, tam_totaux = calcul.tableau_amortissement(81600, 240, 0.0115, 0.0026, 'mode_4')
        
        self.assertAlmostEqual(tam[0]['assurance'], 11.41, 2)
          
        self.assertAlmostEqual(tam_totaux['amortissement'], 81600, 2)
        self.assertAlmostEqual(tam_totaux['interets'], 9782.33, 2)
        self.assertAlmostEqual(tam_totaux['assurance'], 2234.76, 2)
        self.assertAlmostEqual(tam_totaux['mensualite_ha'], 91382.33, 2)
        self.assertAlmostEqual(tam_totaux['mensualite_aa'], 93617.16, 2)
 
        self.assertAlmostEqual(tam[0]['mensualite_ha'], 380.76, 2)


if __name__ == '__main__':
    unittest.main()
