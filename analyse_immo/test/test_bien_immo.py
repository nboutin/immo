#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest, sys, os
sys.path.insert(0, os.path.join('..'))

from bien_immo import Bien_Immo
from lot import Lot
from charge import Charge


class TestBienImmo(unittest.TestCase):
    
    def testLoyerMensuelTotal(self):
        
        bi = Bien_Immo(0, 0, 0, 0, 0)
        bi.add_lot(Lot("T2", 50, 500))
        self.assertEqual(bi.loyer_nu_mensuel, 500)
        bi.add_lot(Lot("T2", 50, 450))
        self.assertEqual(bi.loyer_nu_mensuel, 950)
    
    def testLoyerAnnuelTotal(self):
        
        bi = Bien_Immo(0, 0, 0, 0, 0)
        bi.add_lot(Lot("T2", 50, 200))
        bi.add_lot(Lot("T2", 50, 300))
        self.assertEqual(bi.loyer_nu_annuel, 500 * 12)
    
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

        bi = Bien_Immo(100000, 0.09 , 0.06, 0, 0)
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
        bi.add_lot(Lot("T2", 50, 500))

        lot = Lot("T2", 50, 500)
        charge = Charge(lot, None)

        charge.add(charge.deductible_e.copropriete, 51 * 12)
        charge.add(charge.deductible_e.prime_assurance, 90)
        charge.add(Charge.gestion_e.vacance_locative, 1 / 12)
        charge.add(Charge.gestion_e.agence_immo, 0.05)
        lot.charge = charge
        bi.add_lot(lot)
        
        self.assertEqual(bi.financement_total, 50000)
        self.assertEqual(bi.loyer_nu_mensuel, 1000)
        self.assertEqual(bi.loyer_nu_annuel, 12000)
        self.assertEqual(bi.charge_gestion + bi.charge_fonciere, 1502)

#         self.assertEqual(bi.taxe_fonciere, 0)
#         self.assertEqual(bi.travaux_provision_annuel_total, 0)
#         self.assertEqual(bi.vacance_locative_annuel_total, 500)
#         self.assertEqual(bi.pno_annuel_total, 90)
#         self.assertEqual(bi.gestion_agence_annuel_total, 25 * 12)
#         self.assertEqual(bi.copropriete_annuel_total, 51 * 12)


if __name__ == '__main__':
    unittest.main()
        
