#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from test.testcase_fileloader import TestCaseFileLoader
from analyse_immo.factory import Factory
from analyse_immo.impots.annexe_2044 import Annexe_2044, L211_loyer_brut, L221_frais_administration, L222_autre_frais_gestion, \
    L223_prime_assurance, L224_travaux, L227_taxe_fonciere, L250_interet_emprunt,\
    L250_assurance_emprunteur, L250_frais_dossier, L250_frais_garantie


class TestAnnexe2044(TestCaseFileLoader):

    def setUp(self):
        super().setUp()
        self.defaut = Factory.make_defaut(self.defaut_data)

    def testInit(self):
        _ = Annexe_2044(self.defaut)

    def testTotalRecettes(self):
        an = Annexe_2044(self.defaut)
        an.add_ligne(L211_loyer_brut, 6000)

        self.assertEqual(an.total_recettes, 6000)

    def testTotalFraisCharges(self):
        an = Annexe_2044(self.defaut)
        an.add_ligne(L211_loyer_brut, 6000)
        an.add_ligne(L221_frais_administration, 0)
        an.add_ligne(L222_autre_frais_gestion, 20)
        an.add_ligne(L223_prime_assurance, 100)
        an.add_ligne(L224_travaux, 500)
        an.add_ligne(L227_taxe_fonciere, 650)

        self.assertEqual(an.total_frais_et_charges, 1270)

    def testTotalChargesEmprunt(self):
        an = Annexe_2044(self.defaut)
        an.add_ligne(L211_loyer_brut, 6000)
        an.add_ligne(L221_frais_administration, 0)
        an.add_ligne(L222_autre_frais_gestion, 20)
        an.add_ligne(L223_prime_assurance, 100)
        an.add_ligne(L224_travaux, 500)
        an.add_ligne(L227_taxe_fonciere, 650)
        an.add_ligne(L250_interet_emprunt, 2000)
        an.add_ligne(L250_assurance_emprunteur, 300)
        an.add_ligne(L250_frais_dossier, 150)
        an.add_ligne(L250_frais_garantie, 1000)

        self.assertEqual(an.total_charges_emprunt, 3450)

    def testRevenuFoncierTaxable(self):
        an = Annexe_2044(self.defaut)
        an.add_ligne(L211_loyer_brut, 6000)
        an.add_ligne(L221_frais_administration, 0)
        an.add_ligne(L222_autre_frais_gestion, 20)
        an.add_ligne(L223_prime_assurance, 100)
        an.add_ligne(L224_travaux, 500)
        an.add_ligne(L227_taxe_fonciere, 650)
        an.add_ligne(L250_interet_emprunt, 2000)
        an.add_ligne(L250_assurance_emprunteur, 300)
        an.add_ligne(L250_frais_dossier, 150)
        an.add_ligne(L250_frais_garantie, 1000)

        self.assertEqual(an.revenu_foncier_taxable, 1280)

    def testTotalChargesTaux(self):
        '''
        def total_charges_taux(self):
            return 1 - (self.revenu_foncier_taxable / self.total_recettes)
        '''
        an = Annexe_2044(self.defaut)
        an.add_ligne(L211_loyer_brut, 6000)
        self.assertAlmostEqual(an.total_charges_taux, 0, 2)

        an.add_ligne(L223_prime_assurance, 1000)
        self.assertAlmostEqual(an.total_charges_taux, 1 - (5 / 6), 2)

        anB = Annexe_2044(self.defaut)
        anB.add_ligne(L211_loyer_brut, 6000)
        anB.add_ligne(L221_frais_administration, 0)
        anB.add_ligne(L222_autre_frais_gestion, 20)
        anB.add_ligne(L223_prime_assurance, 100)
        anB.add_ligne(L224_travaux, 500)
        anB.add_ligne(L227_taxe_fonciere, 650)
        anB.add_ligne(L250_interet_emprunt, 2000)
        anB.add_ligne(L250_assurance_emprunteur, 300)
        anB.add_ligne(L250_frais_dossier, 150)
        anB.add_ligne(L250_frais_garantie, 1000)
        self.assertEqual(anB.revenu_foncier_taxable, 1280)
        self.assertAlmostEqual(anB.total_charges_taux, 1 - (1280 / 6000), 2)


if __name__ == '__main__':
    unittest.main()
