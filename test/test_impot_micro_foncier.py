#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from analyse_immo.database import Database
from analyse_immo.impots.micro_foncier import Micro_Foncier
from test.testcase_fileloader import TestCaseFileLoader


@unittest.skip('fixme')
class TestImpotMicroFoncier(TestCaseFileLoader):

    def setUp(self):
        self._database = Database()

    def testInit(self):
        _ = Micro_Foncier(self._database, 0, 0)

    def testBasseImpossable(self):
        imf = Micro_Foncier(self._database, 10000, 0)
        self.assertEqual(imf.base_impossable, 7000)

    def testRevenuFoncierImpossable(self):
        imf = Micro_Foncier(self._database, 10000, 0.11)
        self.assertEqual(imf.revenu_foncier_impossable, 770)

    def testPrelevementSociauxMontant(self):
        imf = Micro_Foncier(self._database, 10000, 0.11)
        self.assertEqual(imf.prelevement_sociaux_montant, 1204)

    def testImpotTotal(self):
        imf = Micro_Foncier(self._database, 10000, 0.11)
        self.assertEqual(imf.impot_total, 1974)


if __name__ == '__main__':
    unittest.main()
