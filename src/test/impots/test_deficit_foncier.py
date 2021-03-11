#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from analyse_immo.database import Database
from analyse_immo.impots.irpp import IRPP, L1AJ_salaire, L1BJ_salaire
from analyse_immo.impots.annexe_2044 import Annexe_2044, L211_loyer_brut, L250_interet_emprunt, \
    L227_taxe_fonciere, L223_prime_assurance, L224_travaux


class TestIRPPDeficitFoncier(unittest.TestCase):

    def setUp(self):
        self.database = Database()

    def testExample1(self):
        '''
        Salaire 30K/an
        Revenuf foncier: 12K/an
        Interet emprunt: 2300/an
        Taxe Fonciere: 1000
        Assurance: 600
        Travaux: 40000

        Annee 1
        Charges = 2300 + 1000 + 600
        Revenu foncier impossable = 12K - charges - travaux = -31900
        revenu impossable= 30K - 10700 = 19300
        deficit reportable= 31900-10700 = 21200
        '''
        irpp = IRPP(self.database, 2020, 2, 0)
        irpp.add_ligne(L1AJ_salaire, 15000 / .9)
        irpp.add_ligne(L1BJ_salaire, 15000 / .9)

        annexe_2044 = Annexe_2044(self.database)
        annexe_2044.add_ligne(L211_loyer_brut, 12000)
        annexe_2044.add_ligne(L250_interet_emprunt, 2300)
        annexe_2044.add_ligne(L227_taxe_fonciere, 1000)
        annexe_2044.add_ligne(L223_prime_assurance, 600)
        annexe_2044.add_ligne(L224_travaux, 40000)

        irpp.annexe_2044 = annexe_2044

        self.assertAlmostEqual(annexe_2044.resultat_foncier, -31900, 0)
        self.assertAlmostEqual(irpp.revenu_fiscale_reference, 19300, 2) # 30K - 10700
        self.assertEqual(annexe_2044.deficit_imputable_revenu_foncier, -21200)

        '''
        Annee 2
        Revenu foncier impossable = 12K - charges - deficit reportable = -13100
        revenu impossable = 30K
        deficit reportable= 13100
        '''


if __name__ == '__main__':
    unittest.main()
