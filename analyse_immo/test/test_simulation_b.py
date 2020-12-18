#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import sys
import os
sys.path.insert(0, os.path.join('..'))

import json
from factory import Factory
from rendement import Rendement
from impot_regime_reel import Impot_Regime_Reel
from database import Database


class TestSimulationB(unittest.TestCase):
    '''
    Les données sont incompletes ...

    prix de l'annonce: 120K
    montant offre: 95K, 85K(-10%), 76K(-20%)
    % de nego: 20.83%, 28.75%, 36.67%
    notaire: 7600, 6840, 6080
    Travaux: 91780.27, 91780.27, 91780.27
    Total: 194380, 184120, 173860

    Loyer HC mensuel: 1650, .., ..
    Taxe Fonciere: 1700, x, x
    Gestion (annuel): 7%, 1386
    Surface: 170
    prix m2 assurance: 1.50
    Assurance: 255

    Credit taux: 2%
    duree: 20
    mensualite: 981.67, 929.86, 878.04

    Cashflow annuel: 4679, 5301, 5923
    Renta Brut: 10.60, 11.17, 11.80
    Renta Nette (avant impot): 8.47, 8.94, 9.47
    '''

    def setUp(self):
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        __DATA_TEST_PATHNAME = os.path.join(__location__, 'data', 'input_test_simulation_B.json')
        with open(__DATA_TEST_PATHNAME, 'r') as file:
            input_data = json.load(file)

        self.achat_data = input_data['achat']
        self.lots_data = input_data['lots']
        self.credit_data = input_data['credit']

        self.bi = Factory.make_bien_immo(self.achat_data, self.lots_data)
        self.credit = Factory.make_credit(self.credit_data, self.bi)
        self.rdt = Rendement(self.bi, self.credit)
        database = Database()
        self.irr = Impot_Regime_Reel(database, self.bi, self.credit, 0.11)

    def testOffre(self):

        self.assertEqual(self.bi.notaire_montant, 7600)
        self.assertEqual(self.bi.notaire_taux, 0.08)
        self.assertAlmostEqual(self.bi.financement_total, 194380, 0)

    @unittest.skip('fixme')
    def testCredit(self):
        self.assertAlmostEqual(self.credit.get_mensualite_avec_assurance(), 981.67, 2)

    @unittest.skip('fixme')
    def testRendement(self):
        self.assertAlmostEqual(self.rdt.rendement_brut, 0.1060, 4)


if __name__ == '__main__':
    unittest.main()
