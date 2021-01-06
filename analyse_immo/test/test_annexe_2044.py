#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import sys
import os
sys.path.insert(0, os.path.join('..'))
sys.path.insert(1, os.path.join('..', '..'))

from impots.annexe_2044 import Annexe_2044, L211_loyer_brut, L221_frais_administration, L222_autre_frais_gestion, \
    L223_prime_assurance, L224_travaux, L227_taxe_fonciere, L250_interet_emprunt,\
    L250_assurance_emprunteur, L250_frais_dossier, L250_frais_garantie


class TestAnnexe2044(unittest.TestCase):

    def testInit(self):
        _ = Annexe_2044()

    def testTotalRecettes(self):
        an = Annexe_2044()
        an.add_ligne(L211_loyer_brut, 6000)

        self.assertEqual(an.total_recettes, 6000)

    def testTotalFraisCharges(self):
        an = Annexe_2044()
        an.add_ligne(L211_loyer_brut, 6000)
        an.add_ligne(L221_frais_administration, 0)
        an.add_ligne(L222_autre_frais_gestion, 20)
        an.add_ligne(L223_prime_assurance, 100)
        an.add_ligne(L224_travaux, 500)
        an.add_ligne(L227_taxe_fonciere, 650)

        self.assertEqual(an.total_frais_et_charges, 1270)

    def testTotalChargesEmprunt(self):
        an = Annexe_2044()
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
        an = Annexe_2044()
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


if __name__ == '__main__':
    unittest.main()
