#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from analyse_immo.database import Database
from analyse_immo.impots.irpp import IRPP, L1AJ_salaire, L1BJ_salaire, L4BD_deficit_foncier_anterieur,\
    L4BA_benefice_foncier, L4BB_deficit_foncier_imputable_revenu_foncier,\
    L4BC_deficit_foncier_imputable_revenu_global,\
    L4_revenus_ou_deficits_nets_fonciers
from analyse_immo.impots.annexe_2044 import Annexe_2044, L211_loyer_brut, L250_interet_emprunt, \
    L227_taxe_fonciere, L223_prime_assurance, L224_travaux, L451_deficit_foncier_anterieur


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
        irpp = list()

        irpp.append(IRPP(self.database, 2020, 2, 0))
        irpp[0].add_ligne(L1AJ_salaire, 15000 / .9)
        irpp[0].add_ligne(L1BJ_salaire, 15000 / .9)

        annexe_2044 = Annexe_2044(self.database)
        annexe_2044.add_ligne(L211_loyer_brut, 12000)
        annexe_2044.add_ligne(L250_interet_emprunt, 2300)
        annexe_2044.add_ligne(L227_taxe_fonciere, 1000)
        annexe_2044.add_ligne(L223_prime_assurance, 600)
        annexe_2044.add_ligne(L224_travaux, 40000)
        irpp[0].annexe_2044 = annexe_2044

        self.assertAlmostEqual(annexe_2044.resultat_foncier, -31900, 0)
        self.assertAlmostEqual(irpp[0].revenu_fiscale_reference, 19300, 2)  # 30K - 10700
        self.assertEqual(annexe_2044.deficit_imputable_revenu_foncier, -21200)
        self.assertEqual(irpp[0].sum_ligne(L4_revenus_ou_deficits_nets_fonciers), -10700)
        self.assertEqual(irpp[0].sum_ligne(L4BA_benefice_foncier), 0)
        self.assertEqual(irpp[0].sum_ligne(L4BB_deficit_foncier_imputable_revenu_foncier), -21200)
        self.assertEqual(irpp[0].sum_ligne(L4BC_deficit_foncier_imputable_revenu_global), -10700)
        self.assertEqual(irpp[0].sum_ligne(L4BD_deficit_foncier_anterieur), 0)

        '''
        Annee 2
        Revenu foncier impossable = 12K - charges - deficit reportable = -13100
        revenu impossable = 30K
        deficit reportable= 13100
        '''
        irpp.append(IRPP(self.database, 2020, 2, 0))
        irpp[1].add_ligne(L1AJ_salaire, 15000 / .9)
        irpp[1].add_ligne(L1BJ_salaire, 15000 / .9)

        annexe_2044 = Annexe_2044(self.database)
        annexe_2044.add_ligne(L211_loyer_brut, 12000)
        annexe_2044.add_ligne(L250_interet_emprunt, 2300)
        annexe_2044.add_ligne(L227_taxe_fonciere, 1000)
        annexe_2044.add_ligne(L223_prime_assurance, 600)
        annexe_2044.add_ligne(L451_deficit_foncier_anterieur,
                              irpp[0].sum_ligne(L4BB_deficit_foncier_imputable_revenu_foncier))
        irpp[1].annexe_2044 = annexe_2044

        self.assertAlmostEqual(annexe_2044.resultat_foncier, 8100, 0)  # 12K - 3900
        self.assertAlmostEqual(irpp[1].revenu_fiscale_reference, 30000, 2)
        self.assertEqual(annexe_2044.deficit_imputable_revenu_foncier, 0)

        self.assertEqual(irpp[1].sum_ligne(L4_revenus_ou_deficits_nets_fonciers), 0)
        self.assertEqual(irpp[1].sum_ligne(L4BA_benefice_foncier), 8100)
        self.assertEqual(irpp[1].sum_ligne(L4BB_deficit_foncier_imputable_revenu_foncier), 0)
        self.assertEqual(irpp[1].sum_ligne(L4BC_deficit_foncier_imputable_revenu_global), 0)
        self.assertEqual(irpp[1].sum_ligne(L4BD_deficit_foncier_anterieur), -21200)


if __name__ == '__main__':
    unittest.main()
