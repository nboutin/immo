#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from analyse_immo.credit import Credit


class TestCredit_Lacentraledefinancement(unittest.TestCase):

    def testExemple2(self):
        '''
        www.lacentraledefinancement.fr
        '''

        credit = Credit(10000, 60, 0.01, Credit.taux_e.periodique, 0.0020, Credit.mode_e.fixe_CRD, 0, 0)

#         self.assertAlmostEqual(credit.get_montant_interet_total(), 308, 0)
#         self.assertAlmostEqual(credit.get_montant_assurance_total(), 100, 0)
        self.assertAlmostEqual(credit.get_cout_total(), 308, 2)

        mois = 1
        self.assertAlmostEqual(credit.get_capital_restant(mois), 9838.20, 2)
        self.assertAlmostEqual(credit.get_amortissement(mois), 161.80, 2)
        self.assertAlmostEqual(credit.get_interet(mois), 8.33, 2)
        self.assertAlmostEqual(credit.get_mensualite_assurance(mois), 1.67, 2)
        self.assertAlmostEqual(credit.get_mensualite_hors_assurance(mois), 170.13, 2)
        self.assertAlmostEqual(credit.get_mensualite_avec_assurance(mois), 171.80, 2)

        mois = 2
        self.assertAlmostEqual(credit.get_capital_restant(mois), 9676.24, 2)
        self.assertAlmostEqual(credit.get_amortissement(mois), 161.96, 2)
        self.assertAlmostEqual(credit.get_interet(mois), 8.20, 2)
        self.assertAlmostEqual(credit.get_mensualite_assurance(mois), 1.64, 2)
        self.assertAlmostEqual(credit.get_mensualite_hors_assurance(mois), 170.16, 2)
        self.assertAlmostEqual(credit.get_mensualite_avec_assurance(mois), 171.80, 2)

        mois = 13
        self.assertAlmostEqual(credit.get_capital_restant(mois), 7883.93, 2)
        self.assertAlmostEqual(credit.get_amortissement(mois), 163.75, 2)
        self.assertAlmostEqual(credit.get_interet(mois), 6.71, 2)
        self.assertAlmostEqual(credit.get_mensualite_assurance(mois), 1.34, 2)
        self.assertAlmostEqual(credit.get_mensualite_hors_assurance(mois), 170.46, 2)
        self.assertAlmostEqual(credit.get_mensualite_avec_assurance(mois), 171.80, 2)

#         mois = 59
#         self.assertAlmostEqual(credit.get_capital_restant(mois), 170.80, 2)
#         self.assertAlmostEqual(credit.get_amortissement(mois), 170.65, 2)
#         self.assertAlmostEqual(credit.get_interet(mois), 0.28, 2)
#         self.assertAlmostEqual(credit.get_mensualite_assurance(mois), 1.67, 2)
#         self.assertAlmostEqual(credit.get_mensualite_avec_assurance(mois), 172.60, 2)

#         mois = 60
#         self.assertAlmostEqual(credit.get_capital_restant(mois), 0, 2)
#         self.assertAlmostEqual(credit.get_amortissement(mois), 170.80, 2)
#         self.assertAlmostEqual(credit.get_interet(mois), 0.14, 2)
#         self.assertAlmostEqual(credit.get_mensualite_assurance(mois), 1.67, 2)
#         self.assertAlmostEqual(credit.get_mensualite_avec_assurance(mois), 172.60, 2)


if __name__ == '__main__':
    unittest.main()
