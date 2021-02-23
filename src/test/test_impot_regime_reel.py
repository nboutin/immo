#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from analyse_immo.database import Database
from analyse_immo.bien_immo.bien_immo import Bien_Immo
from analyse_immo.bien_immo.lot import Lot
from analyse_immo.bien_immo.charge import Charge
from analyse_immo.credit import Credit
from analyse_immo.impots.annexe_2044 import Annexe_2044


@unittest.skip('fixme')
class TestImpotRegimeReel(unittest.TestCase):

    def setUp(self):
        self._database = Database()
        self.credit = Credit(0, 0, 0, 0, None, 0, 0)

    def testInit(self):
        _ = Annexe_2044(self._database, None, None, 0)

    def testBaseImpossable(self):

        bien_immo = Bien_Immo(0, 0, 0, 0, 0)
        lot = Lot("", 0, 500)
        bien_immo.add_lot(lot)

        irr = Annexe_2044(self._database, bien_immo, self.credit, 0)

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
        charge.add(Charge.charge_e.provision_travaux, 0.01)
        charge.add(Charge.charge_e.vacance_locative, 1 / 12)
        self.assertAlmostEqual(irr.base_impossable, 4100)

        # Gestion agence locative
        charge.add(Charge.charge_e.agence_immo, 0.05)
        self.assertAlmostEqual(irr.base_impossable, 3800)

    def testRevenuFoncierImpossableA(self):
        bien_immo = Bien_Immo(0, 0, 0, 0, 0)
        lot = Lot("", 0, 500)
        bien_immo.add_lot(lot)
        charge = Charge(lot)
        lot.charge = charge

        irr = Annexe_2044(self._database, bien_immo, self.credit, 0)
        self.assertAlmostEqual(irr.revenu_foncier_impossable, 0)

        irr = Annexe_2044(self._database, bien_immo, self.credit, 0.11)
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

        irr = Annexe_2044(self._database, bien_immo, self.credit, 0.11)
        self.assertAlmostEqual(irr.prelevement_sociaux_montant, 1032)

        charge.add(charge.deductible_e.copropriete, 1000)
        self.assertAlmostEqual(irr.prelevement_sociaux_montant, 860)

    def testImpotTotal(self):
        bien_immo = Bien_Immo(0, 0, 0, 0, 0)
        lot = Lot("", 0, 500)
        bien_immo.add_lot(lot)
        charge = Charge(lot)
        lot.charge = charge

        irr = Annexe_2044(self._database, bien_immo, self.credit, 0.11)
        self.assertAlmostEqual(irr.impot_total, 1032 + 660)

        charge.add(charge.deductible_e.copropriete, 1000)
        self.assertAlmostEqual(irr.impot_total, 860 + 550)


if __name__ == '__main__':
    unittest.main()
