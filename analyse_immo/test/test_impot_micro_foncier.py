#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest, sys, os
sys.path.insert(0, os.path.join('..'))

from database import Database
from impot_micro_foncier import Impot_Micro_Foncier


class TestImpotMicroFoncier(unittest.TestCase):
    
    def setUp(self):
#         __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
#         self._database = Database(os.path.join(__location__, 'data', 'database_test.json'))
        self._database = Database()
                                  
    def testInit(self):
        _ = Impot_Micro_Foncier(self._database, 0, 0)

    def testBasseImpossable(self):
        imf = Impot_Micro_Foncier(self._database, 10000, 0)
        self.assertEqual(imf.base_impossable, 7000)

    def testRevenuFoncierImpossable(self):
        imf = Impot_Micro_Foncier(self._database, 10000, 0.11)
        self.assertEqual(imf.revenu_foncier_impossable, 770)

    def testPrelevementSociauxMontant(self):
        imf = Impot_Micro_Foncier(self._database, 10000, 0.11)
        self.assertEqual(imf.prelevement_sociaux_montant, 1204)

    def testImpotTotal(self):
        imf = Impot_Micro_Foncier(self._database, 10000, 0.11)
        self.assertEqual(imf.impot_total, 1974)


if __name__ == '__main__':
    unittest.main()
