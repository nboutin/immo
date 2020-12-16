#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest, sys, os
sys.path.insert(0, os.path.join('..'))

from database import Database
from bien_immo import Bien_Immo
from lot import Lot
from charge import Charge
from impot_regime_reel import Impot_Regime_Reel


class TestImpotRegimeReel(unittest.TestCase):
        
    def setUp(self):
        self._database = Database()
        
    def testInit(self):
        _ = Impot_Regime_Reel(self._database, None, 0)

    def testBaseImpossable(self):
        
        bien_immo = Bien_Immo(0, 0, 0, 0, 0)
        lot = Lot("", 0, 500)
        bien_immo.add_lot(lot)
        
        irr = Impot_Regime_Reel(self._database, bien_immo, 0)
        
        # Pas de charges
        self.assertAlmostEqual(irr.base_impossable, 6000)

        charge = Charge(lot)
        lot.charge = charge
        
        # Copropriete        
        charge.add(charge.deductible_e.copropriete, 1000)
        self.assertAlmostEqual(irr.base_impossable, 5000)
        
        # Taxe fonciere
        charge.add(charge.deductible_e.copropriete, 800)
        self.assertAlmostEqual(irr.base_impossable, 4200)
        
        # PNO
        charge.add(charge.deductible_e.prime_assurance, 100)
        self.assertAlmostEqual(irr.base_impossable, 4100)
        
        # Autres
        charge.add(Charge.gestion_e.provision_travaux, 0.01)
        charge.add(Charge.gestion_e.vacance_locative, 1 / 12)
        self.assertAlmostEqual(irr.base_impossable, 4100)
        
        # Gestion agence locative
        charge.add(Charge.gestion_e.agence_immo, 0.05)
        self.assertAlmostEqual(irr.base_impossable, 3800)

    def testRevenuFoncierImpossableA(self):
        bien_immo = Bien_Immo(0, 0, 0, 0, 0)
        lot = Lot("", 0, 500)
        bien_immo.add_lot(lot)
        charge = Charge(lot)
        lot.charge = charge
        
        irr = Impot_Regime_Reel(self._database, bien_immo, 0)
        self.assertAlmostEqual(irr.revenu_foncier_impossable, 0)
        
        irr = Impot_Regime_Reel(self._database, bien_immo, 0.11)
        self.assertAlmostEqual(irr.revenu_foncier_impossable, 660)
        
        charge.add(charge.deductible_e.copropriete, 1000)
        self.assertAlmostEqual(irr.revenu_foncier_impossable, 550)
        
    @unittest.skip('todo')
    def testRevenuFoncierImpossableB(self):
        '''
        Take into account credit
        '''
        pass
        
        

    def testPrelevementSociaux(self):
        bien_immo = Bien_Immo(0, 0, 0, 0, 0)
        lot = Lot("", 0, 500)
        bien_immo.add_lot(lot)
        charge = Charge(lot)
        lot.charge = charge
        
        irr = Impot_Regime_Reel(self._database, bien_immo, 0.11)
        self.assertAlmostEqual(irr.prelevement_sociaux_montant, 1032)
        
        charge.add(charge.deductible_e.copropriete, 1000)
        self.assertAlmostEqual(irr.prelevement_sociaux_montant, 860)

    def testImpotTotal(self):
        bien_immo = Bien_Immo(0, 0, 0, 0, 0)
        lot = Lot("", 0, 500)
        bien_immo.add_lot(lot)
        charge = Charge(lot)
        lot.charge = charge
        
        irr = Impot_Regime_Reel(self._database, bien_immo, 0.11)
        self.assertAlmostEqual(irr.impot_total, 1032 + 660)
        
        charge.add(charge.deductible_e.copropriete, 1000)
        self.assertAlmostEqual(irr.impot_total, 860 + 550)


if __name__ == '__main__':
    unittest.main()
