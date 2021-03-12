#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from analyse_immo.factory import Factory
from analyse_immo.bien_immo.bien_immo import Bien_Immo
from analyse_immo.database import Database


class TestFactory(unittest.TestCase):

    def testMakeAnnexe2044(self):
        bien_immo = Bien_Immo()
        credit = Credit()
        i_annee = 0
        deficit_foncier_anterieur = 0
        Factory.make_annexe_2044(Database(), bien_immo, credit, i_annee, deficit_foncier_anterieur)


if __name__ == '__main__':
    unittest.main()
