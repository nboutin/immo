#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import os
import json

from analyse_immo.factory import Factory
from analyse_immo.impots.annexe_2044 import L224_travaux


class TestImMir130(unittest.TestCase):

    def setUp(self):

        self.input_pathname = os.path.join('..', 'analyse_immo', 'data', 'input_2021_im_mir_130.json')
        with open(self.input_pathname, 'r') as file:
            input_data = json.load(file)
        self.input_data = input_data

    def testAll(self):
        analyse = Factory.make_analyse(self.input_data)

        bien_immo = analyse.bien_immo
        irpp_0 = analyse.irpp_2044_projection[0]
        an2044_0 = irpp_0.annexe_2044

        self.assertNotEqual(bien_immo.travaux_montant, 0)
        self.assertNotEqual(an2044_0.sum_ligne(L224_travaux), 0)
        self.assertNotEqual(irpp_0.revenu_foncier, 0)
        self.assertEqual(irpp_0.revenu_foncier, -10700)

        # an2044.sum_ligne(L4BA_benefice_foncier)
        # an2044.sum_ligne(L4BB_deficit_foncier_imputable_revenu_foncier)
        # an2044.sum_ligne(L4BC_deficit_foncier_imputable_revenu_global)
        # an2044.sum_ligne(L4BD_deficit_foncier_anterieur)


if __name__ == '__main__':
    unittest.main()
