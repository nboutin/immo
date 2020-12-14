#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest, sys, os
sys.path.insert(0, os.path.join('..'))

from impot_micro_foncier import Impot_Micro_Foncier


class TestImpotMicroFoncier(unittest.TestCase):
    
    def testInit(self):
        imf = Impot_Micro_Foncier(0, 0)

    def testBasseImpossable(self):
        imf = Impot_Micro_Foncier(10000, 0)
        self.assertEqual(imf.base_impossable, 7000)

    def testRevenuFoncierImpossable(self):
        imf = Impot_Micro_Foncier(10000, 0.11)
        self.assertEqual(imf.revenu_foncier_impossable, 770)

    def testPrelevementSociauxMontant(self):
        imf = Impot_Micro_Foncier(10000, 0.11)
        self.assertEqual(imf.prelevement_sociaux_montant, 1204)

    def testImpotTotal(self):
        imf = Impot_Micro_Foncier(10000, 0.11)
        self.assertEqual(imf.impot_total, 1974)
        
