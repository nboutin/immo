#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from analyse_immo.credit import Credit


class TestCredit01_Construction(unittest.TestCase):

    def testConstructeur(self):
        Credit(0, 0, 0, Credit.taux_e.periodique, 0, Credit.mode_e.fixe_CI, 0, 0)
        Credit(0, 1, 0, Credit.taux_e.periodique, 0, Credit.mode_e.fixe_CRD, 0, 0)

    def testCapital(self):
        credit = Credit(100, 0, 0, Credit.taux_e.periodique, 0, Credit.mode_e.fixe_CI, 0, 0)
        self.assertEqual(credit.capital, 100)

    def testDureeMois(self):
        credit = Credit(0, 15, 0, Credit.taux_e.periodique, 0, Credit.mode_e.fixe_CI, 0, 0)
        self.assertEqual(credit.duree_mois, 15)

    def testTaux(self):
        credit = Credit(0, 0, 1.15, Credit.taux_e.periodique, 0, Credit.mode_e.fixe_CI, 0, 0)
        self.assertEqual(credit.taux, 1.15)

    def testTauxAssurance(self):
        credit = Credit(0, 0, 0, Credit.taux_e.periodique, 0.040, Credit.mode_e.fixe_CI, 0, 0)
        self.assertEqual(credit.taux_assurance, 0.040)

    def testMode(self):
        credit = Credit(0, 0, 0, Credit.taux_e.periodique, 0, Credit.mode_e.fixe_CI, 0, 0)
        self.assertEqual(credit.mode, Credit.mode_e.fixe_CI)

    def testFraisDossier(self):
        credit = Credit(0, 0, 0, Credit.taux_e.periodique, 0, Credit.mode_e.fixe_CI, 500, 0)
        self.assertEqual(credit.frais_dossier, 500)

    def testFraisGarantie(self):
        credit = Credit(0, 0, 0, Credit.taux_e.periodique, 0, Credit.mode_e.fixe_CI, 0, 300)
        self.assertEqual(credit.frais_garantie, 300)


class TestCredit02_Static(unittest.TestCase):

    def test02_MensualitePeriodique(self):
        self.assertAlmostEqual(Credit.mensualite_periodique(100000, 0.005, 240), 716.43, 2)
        self.assertAlmostEqual(Credit.mensualite_periodique(150000, 0.00193, 240), 781.48, 2)

        self.assertAlmostEqual(Credit.mensualite_periodique(100000, 0.015 / 12, 240), 482.55, 2)
        self.assertAlmostEqual(Credit.mensualite_periodique(88000, 0.0099 / 12, 15 * 12), 526.29, 2)
        self.assertAlmostEqual(Credit.mensualite_periodique(136000, 0.018 / 12, 240), 675.19, 2)


class TestCredit03_Mensualite(unittest.TestCase):

    def test01_GetMensualiteHorsAssurance(self):
        cred = Credit(100000, 240, 0.015, Credit.taux_e.periodique, 0, Credit.mode_e.fixe_CI, 0, 0)
        self.assertAlmostEqual(cred.get_mensualite_hors_assurance(), 482.55, 2)
        self.assertAlmostEqual(cred.get_mensualite_hors_assurance(1), 482.55, 2)
        self.assertAlmostEqual(cred.get_mensualite_hors_assurance(10), 482.55, 2)

        cred = Credit(88000, 15 * 12, 0.0099, Credit.taux_e.periodique, 0, Credit.mode_e.fixe_CI, 0, 0)
        self.assertAlmostEqual(cred.get_mensualite_hors_assurance(), 526.29, 2)
        self.assertAlmostEqual(cred.get_mensualite_hors_assurance(150), 526.29, 2)
        self.assertAlmostEqual(cred.get_mensualite_hors_assurance(15 * 12), 526.29, 2)

        cred = Credit(136000, 240, 0.018, Credit.taux_e.periodique, 0, Credit.mode_e.fixe_CI, 0, 0)
        self.assertAlmostEqual(cred.get_mensualite_hors_assurance(), 675.19, 2)

    def test02_GetMensualiteAssurance(self):

        cred = Credit(136000, 12, 0, Credit.taux_e.periodique, 0.0036, Credit.mode_e.fixe_CI, 0, 0)
        self.assertAlmostEqual(cred.get_mensualite_assurance(), 40.80, 2)
        self.assertAlmostEqual(cred.get_mensualite_assurance(1), 40.80, 2)
        self.assertAlmostEqual(cred.get_mensualite_assurance(12), 40.80, 2)

    def test03_GetMensualiteAvecAssurance(self):

        cred = Credit(100000, 1, 0, Credit.taux_e.periodique, 0.0035, Credit.mode_e.fixe_CI, 0, 0)
        self.assertAlmostEqual(cred.get_mensualite_avec_assurance(), 29.17, 2)
        self.assertAlmostEqual(cred.get_mensualite_avec_assurance(1), 29.17, 2)

        cred = Credit(136000, 240, 0.018, Credit.taux_e.periodique, 0.0036, Credit.mode_e.fixe_CI, 0, 0)
        self.assertAlmostEqual(cred.get_mensualite_avec_assurance(), 715.99, 2)
        self.assertAlmostEqual(cred.get_mensualite_avec_assurance(1), 715.99, 2)
        self.assertAlmostEqual(cred.get_mensualite_avec_assurance(24), 715.99, 2)

    def test04_MensualiteAvecAssuranceTotal(self):

        cred = Credit(10000, 36, 0.02, Credit.taux_e.periodique, 0, Credit.mode_e.fixe_CI, 0, 0)
        self.assertAlmostEqual(cred.get_mensualite_avec_assurance_total(), 10311.33, 2)

    def test05_MontantInteretTotal(self):

        cred = Credit(10000, 36, 0.02, Credit.taux_e.periodique, 0, Credit.mode_e.fixe_CI, 0, 0)
        self.assertAlmostEqual(cred.get_montant_interet_total(), 311.33, 2)

        cred = Credit(100000, 240, 0.02, Credit.taux_e.periodique, 0, Credit.mode_e.fixe_CI, 0, 0)
        self.assertAlmostEqual(cred.get_montant_interet_total(), 21412, 2)

        cred = Credit(136000, 240, 0.018, Credit.taux_e.periodique, 0, Credit.mode_e.fixe_CI, 0, 0)
        self.assertAlmostEqual(cred.get_montant_interet_total(), 26046.52, 2)

    def test06_MontantAssuranceTotal(self):

        cred = Credit(10000, 36, 0.02, Credit.taux_e.periodique, 0.0030, Credit.mode_e.fixe_CI, 0, 0)
        self.assertAlmostEqual(cred.get_montant_assurance_total(), 90, 2)

        cred = Credit(136000, 240, 0.02, Credit.taux_e.periodique, 0.0036, Credit.mode_e.fixe_CI, 0, 0)
        self.assertAlmostEqual(cred.get_montant_assurance_total(), 9792, 2)

    def test07_CoutTotal(self):

        cred = Credit(10000, 36, 0.02, Credit.taux_e.periodique, 0.0030, Credit.mode_e.fixe_CI, 100, 200)
        self.assertAlmostEqual(cred.get_cout_total(), 701.33, 2)

        cred = Credit(136000, 240, 0.018, Credit.taux_e.periodique, 0.0036, Credit.mode_e.fixe_CI, 40, 60)
        self.assertAlmostEqual(cred.get_cout_total(), 35938.52, 2)


class TestCredit04_TableauAmortissement(unittest.TestCase):

    def test01_FixeCI1(self):
        cred = Credit(10000, 36, 0.02, Credit.taux_e.periodique, 0, Credit.mode_e.fixe_CI, 0, 0)

        self.assertAlmostEqual(cred.capital, 10000, 2)
        self.assertAlmostEqual(cred.get_amortissement(), 269.76, 2)
        self.assertAlmostEqual(cred.get_interet(), 16.67, 2)
        self.assertAlmostEqual(cred.get_mensualite_assurance(), 0, 2)
        self.assertAlmostEqual(cred.get_mensualite_avec_assurance(), 286.43, 2)

        start = 36
        self.assertAlmostEqual(cred.get_amortissement(start), 285.95, 2)
        self.assertAlmostEqual(cred.get_interet(start), 0.48, 2)
        self.assertAlmostEqual(cred.get_mensualite_assurance(start), 0, 2)
        self.assertAlmostEqual(cred.get_mensualite_avec_assurance(start), 286.43, 2)

    def test02_FixeCI2(self):
        cred = Credit(10000, 36, 0.02, Credit.taux_e.periodique, 0.0030, Credit.mode_e.fixe_CI, 0, 0)

        start = 1
        self.assertAlmostEqual(cred.capital, 10000, 2)
        self.assertAlmostEqual(cred.get_amortissement(start), 269.76, 2)
        self.assertAlmostEqual(cred.get_interet(start), 16.67, 2)
        self.assertAlmostEqual(cred.get_mensualite_assurance(start), 2.5, 2)
        self.assertAlmostEqual(cred.get_mensualite_avec_assurance(start), 288.93, 2)

        start = 36
        self.assertAlmostEqual(cred.get_amortissement(start), 285.95, 2)
        self.assertAlmostEqual(cred.get_interet(start), 0.48, 2)
        self.assertAlmostEqual(cred.get_mensualite_assurance(start), 2.5, 2)
        self.assertAlmostEqual(cred.get_mensualite_avec_assurance(start), 288.93, 2)

    def test03_FixeCRD(self):
        cred = Credit(10000, 36, 0.02, Credit.taux_e.periodique, 0.0030, Credit.mode_e.fixe_CRD, 0, 0)

        start = 1
        self.assertAlmostEqual(cred.get_capital_restant(start), 9731.43, 2)
        self.assertAlmostEqual(cred.get_amortissement(start), 268.57, 2)
        self.assertAlmostEqual(cred.get_interet(start), 16.67, 2)
        self.assertAlmostEqual(cred.get_mensualite_assurance(start), 2.50, 2)
        self.assertAlmostEqual(cred.get_mensualite_hors_assurance(start), 285.24, 2)
        self.assertAlmostEqual(cred.get_mensualite_avec_assurance(start), 287.74, 2)

        start = 2
        self.assertAlmostEqual(cred.get_capital_restant(start), 9462.34, 2)
        self.assertAlmostEqual(cred.get_amortissement(start), 269.09, 2)
        self.assertAlmostEqual(cred.get_interet(start), 16.22, 2)
        self.assertAlmostEqual(cred.get_mensualite_assurance(start), 2.43, 2)
        self.assertAlmostEqual(cred.get_mensualite_hors_assurance(start), 285.30, 2)
        self.assertAlmostEqual(cred.get_mensualite_avec_assurance(start), 287.74, 2)

        start = 36
        self.assertAlmostEqual(cred.get_amortissement(start), 287.19, 2)  # 268.5706
        self.assertAlmostEqual(cred.get_interet(start), 0.48, 2)
        self.assertAlmostEqual(cred.get_mensualite_assurance(start), 0.07, 2)
        self.assertAlmostEqual(cred.get_mensualite_avec_assurance(start), 287.74, 2)

        self.assertAlmostEqual(cred.get_amortissement_total(), 10000, 2)
        self.assertAlmostEqual(cred.get_montant_interet_total(), 311.78, 2)
        self.assertAlmostEqual(cred.get_montant_assurance_total(), 46.77, 2)
        self.assertAlmostEqual(cred.get_mensualite_hors_assurance_total(), 10311.78, 2)
        self.assertAlmostEqual(cred.get_mensualite_avec_assurance_total(), 10358.54, 2)

    def test04_DegressiveCRD(self):
        cred = Credit(81600, 240, 0.0115, Credit.taux_e.periodique,
                      0.0026, Credit.mode_e.degressive_CRD, 0, 0)

        self.assertAlmostEqual(cred.get_mensualite_hors_assurance(), 380.76, 2)

        self.assertAlmostEqual(cred.get_amortissement_total(), 81600, 2)
        self.assertAlmostEqual(cred.get_montant_interet_total(), 9782.33, 2)
        self.assertAlmostEqual(cred.get_montant_assurance_total(), 2211.66, 2)  # 2234.76
        self.assertAlmostEqual(cred.get_mensualite_hors_assurance_total(), 91382.33, 2)
        self.assertAlmostEqual(cred.get_mensualite_avec_assurance_total(), 93593.98, 2)


if __name__ == '__main__':
    unittest.main()
