#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import sys
import os
sys.path.insert(0, os.path.join('..'))

from bien_immo import Bien_Immo
from lot import Lot
from charge import Charge


class TestBienImmo(unittest.TestCase):

    def testLoyerBrutMensuelTotal(self):

        bi = Bien_Immo(0, 0, 0, 0, 0)
        bi.add_lot(Lot("T2", 50, 500))
        self.assertEqual(bi.loyer_nu_brut_mensuel, 500)
        bi.add_lot(Lot("T2", 50, 450))
        self.assertEqual(bi.loyer_nu_brut_mensuel, 950)

    def testLoyerBrutAnnuelTotal(self):

        bi = Bien_Immo(0, 0, 0, 0, 0)
        bi.add_lot(Lot("T2", 50, 200))
        bi.add_lot(Lot("T2", 50, 300))
        self.assertEqual(bi.loyer_nu_brut_annuel, 500 * 12)

    def testNotaire(self):

        bi = Bien_Immo(100000, 0, 0.1, 0, 0)
        self.assertEqual(bi.notaire_taux, 0.1)
        self.assertEqual(bi.notaire_montant, 10000)

        bi = Bien_Immo(100000, 0, 5000, 0, 0)
        self.assertEqual(bi.notaire_taux, 0.05)
        self.assertEqual(bi.notaire_montant, 5000)

    def testAgentImmo(self):

        bi = Bien_Immo(100000, 0.08, 0, 0, 0)
        self.assertEqual(bi.agence_taux, 0.08)
        self.assertEqual(bi.agence_montant, 8000)

        bi = Bien_Immo(100000, 6500, 0, 0, 0)
        self.assertEqual(bi.agence_taux, 0.065)
        self.assertEqual(bi.agence_montant, 6500)

    def testInvestissementInitial(self):

        bi = Bien_Immo(130000, 9000, 6000, 15000, 10000)
        self.assertEqual(bi.financement_total, 150000)

        bi = Bien_Immo(100000, 0.09, 0.06, 0, 0)
        self.assertEqual(bi.financement_total, 115000)

    def testSurfaceTotal(self):

        bi = Bien_Immo(0, 0, 0, 0, 0)
        bi.add_lot(Lot("T2", 65, 0))
        bi.add_lot(Lot("T2", 51, 0))
        self.assertEqual(bi.surface_total, 116)

    def testSurfacePrix(self):

        bi = Bien_Immo(130000, 0, 0, 0, 0)
        bi.add_lot(Lot("T2", 65, 0))
        self.assertEqual(bi.rapport_surface_prix, 2000)

    def testCharges(self):

        bi = Bien_Immo(50000, 0, 0, 0, 0)
        lot1 = Lot("T2", 50, 500)
        bi.add_lot(lot1)

        lot2 = Lot("T2", 50, 500)
        charge = Charge(lot2, None)

        charge.add(Charge.charge_e.copropriete, 51 * 12)
        charge.add(Charge.charge_e.prime_assurance, 90)
        charge.add(Charge.charge_e.vacance_locative, 1 / 12)
        charge.add(Charge.charge_e.agence_immo, 0.05)
        lot2.charge = charge
        bi.add_lot(lot2)

        self.assertEqual(bi.financement_total, 50000)
        self.assertEqual(bi.loyer_nu_brut_mensuel, 1000)
        self.assertEqual(bi.loyer_nu_brut_annuel, 12000)
        self.assertEqual(bi.loyer_nu_net_annuel, 11500)
        self.assertAlmostEqual(bi.loyer_nu_net_mensuel, 958.33, 2)
        self.assertEqual(bi.charges + bi.provisions, 1002)

        self.assertEqual(bi.get_charge(Charge.charge_e.taxe_fonciere), 0)
        self.assertEqual(bi.get_charge(Charge.charge_e.provision_travaux), 0)
        self.assertEqual(bi.get_charge(Charge.charge_e.vacance_locative), 500)
        self.assertEqual(bi.get_charge(Charge.charge_e.prime_assurance), 90)
        self.assertEqual(bi.get_charge(Charge.charge_e.agence_immo), 25 * 12)
        self.assertEqual(bi.get_charge(Charge.charge_e.copropriete), 51 * 12)


if __name__ == '__main__':
    unittest.main()
