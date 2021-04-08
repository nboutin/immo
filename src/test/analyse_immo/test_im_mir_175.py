#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import os
import json

from analyse_immo.factory import Factory
from analyse_immo.impots.ligne_definition import *
from analyse_immo.impots import irpp


class TestImMir130(unittest.TestCase):

    def setUp(self):

        self.input_pathname = os.path.join('data', 'input_2021_im_mir_175.json')
        with open(self.input_pathname, 'r') as file:
            input_data = json.load(file)
        self.input_data = input_data

    def testAll(self):
        analyse = Factory.make_analyse(self.input_data)

        bien_immo = analyse.bien_immo
        credit = analyse.credit
        rdt = analyse.rendement
        irpp_0 = analyse.irpp_2044_projection[0]
        an2044_0 = irpp_0.annexe_2044

        impot_salaire = (((31500 + 23100) * .9) / 2.5 - 10084) * 2.5 * .11
        impot_salaire -= 143 * .66
        self.assertAlmostEqual(irpp_0.impot_sans_revenu_foncier, impot_salaire, 0)

        loyer = (450 + 350 + 300) * 12
        credit_mensualite = 9050
        cashflow_net = loyer - credit_mensualite - 1000 - 300
        self.assertEqual(bien_immo.loyer_nu_net_annuel(), loyer)
        self.assertAlmostEqual(credit.get_mensualite_avec_assurance(1, 12), credit_mensualite, 0)
        self.assertAlmostEqual(rdt.cashflow_net_annuel(1), cashflow_net, 0)

        self.assertAlmostEqual(an2044_0.sum_ligne(L211_loyer_brut), loyer, 0)
        self.assertAlmostEqual(an2044_0.sum_ligne(L215_total_des_recettes), loyer, 0)

        charges = 1000 + 3 * 100 + 3 * 20
        self.assertAlmostEqual(an2044_0.sum_ligne(L221_frais_administration), 0, 0)
        self.assertAlmostEqual(an2044_0.sum_ligne(L222_autre_frais_gestion), 3 * 20, 0)
        self.assertAlmostEqual(an2044_0.sum_ligne(L223_prime_assurance), 3 * 100, 0)
        self.assertAlmostEqual(an2044_0.sum_ligne(L224_travaux_provision), 0, 0)
        self.assertAlmostEqual(an2044_0.sum_ligne(L224_travaux_renovation), 0, 0)
        self.assertAlmostEqual(an2044_0.sum_ligne(L224_total_travaux), 0, 0)
        self.assertAlmostEqual(an2044_0.sum_ligne(L225_charges_recuperable), 0, 0)
        self.assertAlmostEqual(an2044_0.sum_ligne(L226_indemnites_eviction), 0, 0)
        self.assertAlmostEqual(an2044_0.sum_ligne(L227_taxe_fonciere), 1000, 0)
        self.assertAlmostEqual(an2044_0.sum_ligne(L240_total_frais_et_charges), charges, 0)

        credit_interet = 1713.6
        credit_assurance = 532
        credit_total = credit_interet + credit_assurance + 300
        self.assertAlmostEqual(an2044_0.sum_ligne(L250_interet_emprunt), credit_interet, 0)
        self.assertAlmostEqual(an2044_0.sum_ligne(L250_assurance_emprunteur), credit_assurance, 0)
        self.assertAlmostEqual(an2044_0.sum_ligne(L250_frais_dossier), 300, 0)
        self.assertAlmostEqual(an2044_0.sum_ligne(L250_frais_garantie), 0, 0)
        self.assertAlmostEqual(an2044_0.sum_ligne(L250_total_emprunt), credit_total, 0)

        revenu_foncier = loyer - charges - credit_total
        self.assertAlmostEqual(an2044_0.sum_ligne(L420_resultat_foncier), revenu_foncier, 0)

        revenu = (31500 + 23100) * .9 + revenu_foncier
        self.assertTrue(revenu / 2.5 < 25710)
        # impot_foncier += (min((revenu / 2.5), 25710) - 10084) * 2.5 * .11
        # impot_foncier += (revenu / 2.5 - 25710) * 2.5 * .3
        # impot_foncier = revenu_foncier * .172
        # impot_foncier += (revenu / 2.5 - 10084) * 2.5 * .11 - impot_salaire
        impot_foncier = revenu_foncier * (.11 + .172)

        self.assertAlmostEqual(irpp_0.impot_sans_revenu_foncier, impot_salaire, 0)
        self.assertAlmostEqual(irpp_0.impots_revenu_foncier, impot_foncier, 0)
        # self.assertAlmostEqual(irpp_0.sum_ligne(L9_impot_du), impot_salaire + impot_foncier, 0)

        # # Bien Immo
        # total_travaux = (30 + 60 + 5 + 25 + 5 + 1.9) * 1000
        # self.assertEqual(bien_immo.travaux_montant, total_travaux)
        #
        # # Credit
        # self.assertEqual(credit.frais_dossier, 300)
        # self.assertEqual(credit.frais_garantie, 0)
        #
        # # Impot
        # deficit_foncier_total = 93000
        # self.assertEqual(an2044_0.sum_ligne(L224_travaux_renovation), deficit_foncier_total)
        #
        # self.assertEqual(irpp_0.sum_ligne(L1_1_traitements_salaires_pensions), 54600 * .9)
        # self.assertEqual(irpp_0.sum_ligne(L4_revenus_ou_deficits_nets_fonciers), -10700)
        # self.assertEqual(irpp_0.sum_ligne(L1_5_revenu_brut_global), (54600 * .9) - 10700)
        #
        # revenu_brut = (54600 * .9) - 10700
        # quotient_familial = revenu_brut / 2.5
        # impot = (quotient_familial - 10085) * .11 * 2.5
        # self.assertEqual(irpp_0.sum_ligne(LQ_quotient_familial), quotient_familial)
        # self.assertEqual(irpp_0.sum_ligne(LI_impot), ((((54600 * .9) - 10700) / 2.5) - 10085) * .11 * 2.5)
        # self.assertAlmostEqual(irpp_0.sum_ligne(L7E_impot_avant_reduction_impot), impot, 1)  # 1455.025
        # self.assertEqual(irpp_0.sum_ligne(L9I_total_imputations), 143 * .66)
        # self.assertEqual(irpp_0.sum_ligne(L9PS_prelevement_sociaux), 0)
        # self.assertAlmostEqual(irpp_0.sum_ligne(L9_impot_du), impot - 143 * .66, 0)
        #
        # # Rendement
        # loyer_annuel = (550 + 2 * 476) * 12
        # cashflow_net = loyer_annuel - 15418 - 3 * 100
        # self.assertEqual(rdt.investissement_initial, 115000 * 1.15 + total_travaux + 300)
        # self.assertAlmostEqual(credit.get_mensualite_avec_assurance(1, 12), 15418, 0)
        # self.assertEqual(bien_immo.loyer_nu_net_annuel(), loyer_annuel)
        # self.assertAlmostEqual(rdt.cashflow_net_annuel(1), cashflow_net, 0)  # 2300
        #
        # impot_du_bis = (((54600 * .9) / 2.5) - 10085) * .11 * 2.5 - 143 * .66
        # self.assertEqual(irpp_0.impot_sans_revenu_foncier, impot_du_bis)
        # self.assertAlmostEqual(rdt.cashflow_net_net_annuel(1), cashflow_net - (impot - 143 * .66 - impot_du_bis), 0)
        #
        # # Year 2
        # irpp_1 = analyse.irpp_2044_projection[1]
        # an2044_1 = irpp_1.annexe_2044
        #
        # impot = ((54600 * .9) / 2.5 - 10085) * .11 * 2.5
        # self.assertEqual(an2044_1.sum_ligne(L224_travaux_renovation), 0)
        # self.assertEqual(irpp_1.sum_ligne(L1_1_traitements_salaires_pensions), 54600 * .9)
        # self.assertEqual(irpp_1.sum_ligne(L4_revenus_ou_deficits_nets_fonciers), 0)
        # self.assertEqual(irpp_1.sum_ligne(L1_5_revenu_brut_global), 54600 * .9)
        # self.assertAlmostEqual(irpp_1.sum_ligne(L9_impot_du), impot - 143 * .66, 0)
        #
        # self.assertEqual(an2044_1.sum_ligne(L451_deficit_foncier_anterieur), )


if __name__ == '__main__':
    unittest.main()
