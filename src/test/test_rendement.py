#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from analyse_immo.bien_immo.bien_immo import Bien_Immo
from analyse_immo.bien_immo.lot import Lot
from analyse_immo.bien_immo.charge import Charge
from analyse_immo.credit import Credit
from analyse_immo.rendement import Rendement
from analyse_immo.database import Database
from analyse_immo.impots.irpp import IRPP
from analyse_immo.impots.annexe_2044 import Annexe_2044
from analyse_immo.impots.ligne_definition import *


celibataire = {
    'individus': {'I1': {}},
    'foyers_fiscaux': {'f1': {'declarants': ['I1']}}
}


class TestRendement(unittest.TestCase):

    def setUp(self):
        self.credit = Credit(50000, 240, 0.02, Credit.taux_e.periodique, 0, Credit.mode_e.fixe_CI, 0, 0)
        self.irpp_2044_proj = []
        self.database = Database()

    def test1_RendementBrut(self):
        bi = Bien_Immo(50000)
        bi.add_lot(Lot("T2", 50, 500))
        rdt = Rendement(bi, self.credit, self.irpp_2044_proj)
        self.assertEqual(rdt.rendement_brut, 0.12)

        bi = Bien_Immo()
        rdt = Rendement(bi, self.credit, self.irpp_2044_proj)
        self.assertEqual(rdt.rendement_brut, 0)

    def test2_RendementMethodeLarcher(self):
        bi = Bien_Immo(50000)
        bi.add_lot(Lot("T2", 50, 500))
        rdt = Rendement(bi, self.credit, self.irpp_2044_proj)
        self.assertEqual(rdt.rendement_methode_larcher, 0.09)

        bi = Bien_Immo()
        rdt = Rendement(bi, self.credit, self.irpp_2044_proj)
        self.assertEqual(rdt.rendement_methode_larcher, 0)

    def test3_RendementNet(self):
        bi = Bien_Immo()
        rdt = Rendement(bi, self.credit, self.irpp_2044_proj)
        self.assertEqual(rdt.rendement_net(1), 0)

        bi = Bien_Immo(50000)
        bi.add_lot(Lot("T2", 50, 500))
        rdt = Rendement(bi, self.credit, self.irpp_2044_proj)
        self.assertEqual(rdt.rendement_net(1), 0.12)

        lot = Lot("T2", 50, 500)
        charge = Charge(lot, None)
        charge.add(Charge.charge_e.copropriete, 51 * 12)
        charge.add(Charge.charge_e.prime_assurance, 90)
        charge.add(Charge.charge_e.vacance_locative, 1 / 12)
        charge.add(Charge.charge_e.agence_immo, 500 * 12 * 0.05)
        lot.charge = charge
        bi.add_lot(lot)

        self.assertAlmostEqual(bi.charges(1) + bi.provisions(1), 1002, 2)
        self.assertAlmostEqual(rdt.rendement_net(1), 0.21, 2)

    def test4_Cashflow(self):
        bi = Bien_Immo(50000, 0, 0, 0, 0)

        lot1 = Lot("T2", 50, 500)
        bi.add_lot(lot1)
        cr = Credit(50000, 240, 0.02, Credit.taux_e.periodique, 0, Credit.mode_e.fixe_CI, 0, 0)
        rdt = Rendement(bi, cr, self.irpp_2044_proj)
        self.assertAlmostEqual(rdt.cashflow_net_mensuel(1), 247.06, 2)

        lot2 = Lot("T2", 50, 500)
        charge = Charge(lot2, None)
        charge.add(Charge.charge_e.copropriete, 51 * 12)
        charge.add(Charge.charge_e.prime_assurance, 90)
        charge.add(Charge.charge_e.vacance_locative, 1 / 12)
        charge.add(Charge.charge_e.agence_immo, 500 * 12 * 0.05)
        lot2.charge = charge
        bi.add_lot(lot2)

        self.assertAlmostEqual(bi.loyer_nu_brut_annuel(1), 12000, 2)
        self.assertAlmostEqual(bi.charges(1) + bi.provisions(1), 1002, 2)
        self.assertAlmostEqual(cr.get_mensualite_avec_assurance(), 252.94, 2)
        self.assertAlmostEqual(rdt.cashflow_net_mensuel(1), 621.89, 2)
        self.assertAlmostEqual(rdt.cashflow_net_annuel(1), 7462.70, 2)

    def test5a_cashflow_net_net(self):
        ''' In: Loyer
            Out: credit, charge, provision and impot'''
        bi = Bien_Immo(50000, 0, 0, 0, 0)
        lot1 = Lot("T2", 0, 500)
        bi.add_lot(lot1)

        credit = Credit(0, 0, 0, Credit.taux_e.periodique, 0, Credit.mode_e.fixe_CI, 0, 0)

        annee = '2021'
        irpp = IRPP(celibataire)
        rdt = Rendement(bi, credit, irpp)
        self.assertEqual(rdt.cashflow_net_net_annuel(annee), 12 * 500)

    def test5b_cashflow_net_net(self):
        ''' In: Loyer, credit
            Out: charge, provision and impot'''
        bi = Bien_Immo(50000, 0, 0, 0, 0)
        lot1 = Lot("T2", 0, 500)
        bi.add_lot(lot1)

        credit = Credit(50000, 240, 0.02, Credit.taux_e.periodique, 0, Credit.mode_e.fixe_CI, 0, 0)
        # montant échéance = 252,94 €

        annee = '2021'
        irpp = IRPP(celibataire)
        rdt = Rendement(bi, credit, irpp)

        loyer = 12 * 500
        mensualite = 12 * 252.942
        self.assertAlmostEqual(rdt.cashflow_net_net_annuel(annee)[0], loyer - mensualite, 2)

    def test5c_cashflow_net_net(self):
        ''' In: Loyer, Impot
            Out: credit, charge, provision'''
        bi = Bien_Immo(50000, 0, 0, 0, 0)
        lot1 = Lot("T2", 0, 500)
        bi.add_lot(lot1)

        credit = Credit(0, 0, 0, Credit.taux_e.periodique, 0, Credit.mode_e.fixe_CI, 0, 0)

        irpp = IRPP(self.database, 2021)
        irpp.add_ligne(LN_nombre_de_part, 1)
        irpp.add_ligne(L4_personne_a_charge, 0)
        irpp.add_ligne(L1AJ_salaire, 15000 / 0.9)

        an = Annexe_2044(self.database)
        an.add_ligne(L211_loyer_brut, bi.loyer_nu_net_annuel(1))
        irpp.annexe_2044 = an

        loyer = 12 * 500
        impot = 12 * 500 * (0.11 + 0.172)
        rdt = Rendement(bi, credit, [irpp])
        self.assertEqual(rdt.cashflow_net_net_annuel(1), loyer - impot)

    def test5d_cashflow_net_net(self):
        ''' In: Loyer, credit, Impot
            Out: charge, provision'''
        bi = Bien_Immo(50000, 0, 0, 0, 0)
        lot1 = Lot("T2", 0, 500)
        bi.add_lot(lot1)

        credit = Credit(50000, 240, 0.02, Credit.taux_e.periodique, 0, Credit.mode_e.fixe_CI, 0, 0)
        # montant échéance = 252,94 €

        irpp = IRPP(self.database, 2021)
        irpp.add_ligne(LN_nombre_de_part, 1)
        irpp.add_ligne(L4_personne_a_charge, 0)
        irpp.add_ligne(L1AJ_salaire, 15000 / 0.9)

        an = Annexe_2044(self.database)
        an.add_ligne(L211_loyer_brut, bi.loyer_nu_net_annuel(1))
        irpp.annexe_2044 = an

        loyer = 12 * 500
        mensualite = 12 * 252.942
        impot = 12 * 500 * (0.11 + 0.172)

        rdt = Rendement(bi, credit, [irpp])
        self.assertAlmostEqual(rdt.cashflow_net_net_annuel(1), loyer - mensualite - impot, 2)

    def test5e_cashflow_net_net(self):
        ''' In: Loyer, credit, Impot, Charge
            Out: charge, provision'''
        bi = Bien_Immo(50000, 0, 0, 0, 0)
        lot1 = Lot("T2", 0, 500)
        bi.add_lot(lot1)

        credit = Credit(50000, 240, 0.02, Credit.taux_e.periodique, 0, Credit.mode_e.fixe_CI, 0, 0)
        # montant échéance = 252,94 €

        irpp = IRPP(self.database, 2021)
        irpp.add_ligne(LN_nombre_de_part, 1)
        irpp.add_ligne(L4_personne_a_charge, 0)
        irpp.add_ligne(L1AJ_salaire, 15000 / 0.9)

        an = Annexe_2044(self.database)
        an.add_ligne(L211_loyer_brut, bi.loyer_nu_net_annuel(1))
        i_year = 1
        month_stop = i_year * 12
        month_start = month_stop - 11
        interet = credit.get_interet(month_start, month_stop)  # 981,24 €
        an.add_ligne(L250_interet_emprunt, interet)
        irpp.annexe_2044 = an
        self.assertAlmostEqual(interet, 981.24, 2)

        loyer = 12 * 500
        mensualite = 12 * 252.942
        impot = (loyer - interet) * (0.11 + 0.172)

        rdt = Rendement(bi, credit, [irpp])
        self.assertAlmostEqual(rdt.cashflow_net_net_annuel(1), loyer - mensualite - impot, 2)


if __name__ == '__main__':
    unittest.main()
