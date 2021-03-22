#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import os
import json

from analyse_immo.factory import Factory
from analyse_immo.impots.ligne_definition import *


class TestImMir130(unittest.TestCase):

    def setUp(self):

        self.input_pathname = os.path.join('data', 'input_2021_im_mir_130.json')
        with open(self.input_pathname, 'r') as file:
            input_data = json.load(file)
        self.input_data = input_data

    def testAll(self):
        analyse = Factory.make_analyse(self.input_data)

        bien_immo = analyse.bien_immo
        irpp_0 = analyse.irpp_2044_projection[0]
        an2044_0 = irpp_0.annexe_2044

        total_travaux = (30 + 60 + 5 + 25 + 5 + 1.9) * 1000
        self.assertEqual(bien_immo.travaux_montant, total_travaux)
        self.assertEqual(an2044_0.sum_ligne(L224_travaux_renovation), total_travaux)

        self.assertEqual(irpp_0.sum_ligne(L1_1_traitements_salaires_pensions), 54600 * .9)
        self.assertEqual(irpp_0.sum_ligne(L4_revenus_ou_deficits_nets_fonciers), -10700)
        self.assertEqual(irpp_0.sum_ligne(L1_5_revenu_brut_global), (54600 * .9) - 10700)

        revenu_brut = (54600 * .9) - 10700
        quotient_familial = revenu_brut / 2.5
        self.assertEqual(irpp_0.sum_ligne(LQ_quotient_familial), quotient_familial)
        self.assertEqual(irpp_0.sum_ligne(L9_impot_du), (quotient_familial - 10084) * .11 * 2.5)

        # an2044.sum_ligne(L4BA_benefice_foncier)
        # an2044.sum_ligne(L4BB_deficit_foncier_imputable_revenu_foncier)
        # an2044.sum_ligne(L4BC_deficit_foncier_imputable_revenu_global)
        # an2044.sum_ligne(L4BD_deficit_foncier_anterieur)


if __name__ == '__main__':
    unittest.main()
