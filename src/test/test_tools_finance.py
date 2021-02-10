#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from analyse_immo.tools.finance import interets_compose, taux_periodique, taux_actuariel


class TestTools(unittest.TestCase):

    def testTauxPeriodique(self):
        t_an = 0.10
        self.assertAlmostEqual(taux_periodique(t_an, 1), t_an, 4)
        self.assertAlmostEqual(taux_periodique(t_an, 12), t_an / 12, 4)

    def testtauxActuariel(self):
        t_an = 0.10
        self.assertAlmostEqual(taux_actuariel(t_an, 1), t_an, 2)
        self.assertAlmostEqual(taux_actuariel(t_an, 12), 0.0080, 4)

        self.assertAlmostEqual(taux_actuariel(0.04, 12), 0.00327, 5)
        self.assertAlmostEqual(taux_actuariel(0.0234, 12), 0.00193, 5)

    def testInteretCompose(self):
        t_an = 0.05
        t_men_actu = taux_actuariel(t_an, 12)
        self.assertAlmostEqual(interets_compose(1000, t_an, 4), 1215.51, 2)
        self.assertAlmostEqual(interets_compose(1000, t_men_actu, 4 * 12), 1215.51, 2)


if __name__ == '__main__':
    unittest.main()
