#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from analyse_immo.bien_immo.bien_immo import Bien_Immo
from analyse_immo.bien_immo.lot import Lot
from analyse_immo.bien_immo.charge import Charge
from analyse_immo.bien_immo.travaux import Travaux
from analyse_immo.bien_immo.commun import Commun


class TestBienImmo(unittest.TestCase):

    def test01_PrixNetVendeur(self):
        bi = Bien_Immo('2020', 0)
        self.assertEqual(bi.prix_net_vendeur, 0)
        bi = Bien_Immo('2020', 123456)
        self.assertEqual(bi.prix_net_vendeur, 123456)

    def test01_Apport(self):
        bi = Bien_Immo('2020', apport=456)
        self.assertEqual(bi.apport, 456)

    def test03_LoyerBrutMensuelTotal(self):

        bi = Bien_Immo('2020')
        bi.add_lot(Lot("T2", 50, 500))
        self.assertEqual(bi.loyer_nu_brut_mensuel(), 500)
        bi.add_lot(Lot("T2", 50, 450))
        self.assertEqual(bi.loyer_nu_brut_mensuel(), 950)

    def test03b_LoyerBrutAnnuelTotal(self):

        bi = Bien_Immo('2020')
        bi.add_lot(Lot("T2", 50, 200))
        bi.add_lot(Lot("T2", 50, 300))
        self.assertEqual(bi.loyer_nu_brut_annuel(), 500 * 12)

    def test04_Notaire(self):

        bi = Bien_Immo('2020', 100000, frais_notaire=0.1)
        self.assertEqual(bi.notaire_taux, 0.1)
        self.assertEqual(bi.notaire_montant, 10000)

        bi = Bien_Immo('2020', 100000, frais_notaire=5000)
        self.assertEqual(bi.notaire_taux, 0.05)
        self.assertEqual(bi.notaire_montant, 5000)

    def test05_AgentImmo(self):

        bi = Bien_Immo('2020', 100000, frais_agence=0.08)
        self.assertEqual(bi.agence_taux, 0.08)
        self.assertEqual(bi.agence_montant, 8000)

        bi = Bien_Immo('2020', 100000, frais_agence=6500)
        self.assertEqual(bi.agence_taux, 0.065)
        self.assertEqual(bi.agence_montant, 6500)

    def test06_InvestissementInitial(self):

        bi = Bien_Immo('2020', 130000, frais_agence=9000, frais_notaire=6000, apport=10000)
        bi.add_lot(Lot("", 0, 0, travaux=Travaux(montant=[15000])))
        self.assertEqual(bi.financement_total, 150000)

        bi = Bien_Immo('2020', 100000, frais_agence=0.09, frais_notaire=0.06)
        self.assertEqual(bi.financement_total, 115000)

    def test07a_SurfaceTotal(self):

        bi = Bien_Immo('2020')
        bi.add_lot(Lot("T2", 65, 0))
        bi.add_lot(Lot("T2", 51, 0))
        self.assertEqual(bi.surface_total_final, 116)

    def test07b_SurfaceLouable(self):

        bi = Bien_Immo('2020')
        bi.add_lot(Lot("T2", 65, 0))
        bi.add_lot(Lot("T2", 51, 0))
        self.assertEqual(bi.surface_total_louable, 116)

    def test07c_SurfaceAmenageable(self):

        bi = Bien_Immo('2020')
        bi.add_lot(Lot("T2", 65, 0))
        bi.add_lot(Lot("T2", 51, 0, etat=Lot.etat_e.amenageable))
        self.assertEqual(bi.surface_total_louable, 65)
        self.assertEqual(bi.surface_total_amenageable, 51)

    def test08_SurfacePrix(self):
        bi = Bien_Immo('2020', 130000)
        bi.add_lot(Lot("T2", 65, 0))
        self.assertEqual(bi.rapport_surface_prix_final, 2000)

        bi = Bien_Immo('2020', 130000)
        bi.add_lot(Lot("T2", 0, 0))
        self.assertEqual(bi.rapport_surface_prix_final, 0)

    def test08b_SurfacePrixLouable(self):
        bi = Bien_Immo('2020', 130000)
        bi.add_lot(Lot("T2", 10, 0))
        bi.add_lot(Lot("T2", 20, 0, etat=Lot.etat_e.amenageable))
        bi.add_lot(Lot("T2", 30, 0))
        bi.add_lot(Lot("T2", 40, 0, etat=Lot.etat_e.amenageable))
        self.assertEqual(bi.rapport_surface_prix_louable, 130000 / (10 + 30))

        bi = Bien_Immo(50000)
        self.assertEqual(bi.rapport_surface_prix_louable, 0)

    def test09_IrlTauxAnnuel(self):
        bi = Bien_Immo('2020', 130000)
        bi.add_lot(Lot("T2", 65, 0))
        bi.add_lot(Lot("T1", 45, 0))
        self.assertEqual(bi.irl_taux_annuel, 0)

        bi = Bien_Immo('2020', 130000)
        bi.add_lot(Lot("T2", 65, 0, 0.01))
        bi.add_lot(Lot("T1", 45, 0, 0))
        self.assertEqual(bi.irl_taux_annuel, 0.005)

        bi = Bien_Immo('2020', 130000)
        bi.add_lot(Lot("T2", 65, 0, 0.01))
        self.assertEqual(bi.irl_taux_annuel, 0.01)

    def test10_VacanceLocativeTauxAnnuel(self):
        bi = Bien_Immo('2020', 130000)
        lot = Lot("T2", 65, 0)
        charge = Charge(lot, None)
        charge.add(Charge.charge_e.vacance_locative, 1 / 12)
        lot.charge = charge
        bi.add_lot(lot)
        self.assertEqual(bi.vacance_locative_taux_annuel, 1 / 12)

        lotB = Lot("T2", 65, 0)
        chargeB = Charge(lot, None)
        chargeB.add(Charge.charge_e.vacance_locative, 1 / 24)
        lotB.charge = chargeB
        bi.add_lot(lotB)
        self.assertEqual(bi.vacance_locative_taux_annuel, (1 / 12 + 1 / 24) / 2)

    def test11_LotCount(self):
        bi = Bien_Immo('2020', 130000)
        bi.add_lot(Lot("T2", 65, 0))
        self.assertEqual(bi.lot_count, 1)

        bi.add_lot(Lot("T1", 30, 0))
        bi.add_lot(Lot("T2", 50, 0))
        self.assertEqual(bi.lot_count, 3)

    def test12_Lot(self):
        bi = Bien_Immo('2020', 50000)
        bi.add_lot(Lot("T2", 50, 0))
        bi.add_lot(Lot("T2", 50, 0))
        bi.add_lot(Lot("T2", 50, 0))

        self.assertEqual(len(bi.lots), 3)

    def test13_Charges(self):

        bi = Bien_Immo('2020', 50000)
        lot1 = Lot("T2", 50, 500)
        bi.add_lot(lot1)

        lot2 = Lot("T2", 50, 500)
        charge = Charge(lot2, None)

        charge.add(Charge.charge_e.copropriete, 51 * 12)
        charge.add(Charge.charge_e.prime_assurance, 90)
        charge.add(Charge.charge_e.vacance_locative, 1 / 12)
        charge.add(Charge.charge_e.agence_immo, 500 * 12 * 0.05)
        charge.add(Charge.charge_e.provision_travaux, 0.01)
        lot2.charge = charge
        bi.add_lot(lot2)

        self.assertEqual(bi.financement_total, 50000)
        self.assertEqual(bi.loyer_nu_brut_mensuel(), 1000)
        self.assertEqual(bi.loyer_nu_brut_annuel(), 12000)
        self.assertEqual(bi.loyer_nu_net_annuel(), 11500)
        self.assertAlmostEqual(bi.loyer_nu_net_mensuel(), 500 + 500 * (1 - 1 / 12), 2)

        self.assertEqual(bi.get_charge(Charge.charge_e.taxe_fonciere), 0)
        self.assertEqual(bi.get_charge(Charge.charge_e.provision_travaux), 500 * (1 - 1 / 12) * 12 * 0.01)
        self.assertEqual(bi.get_charge(Charge.charge_e.vacance_locative), 500)
        self.assertEqual(bi.get_charge(Charge.charge_e.prime_assurance), 90)
        self.assertEqual(bi.get_charge(Charge.charge_e.agence_immo), 25 * 12)
        self.assertEqual(bi.get_charge(Charge.charge_e.copropriete), 51 * 12)
        self.assertEqual(bi.charges() + bi.provisions(), 1002 + 500 * (1 - 1 / 12) * 12 * 0.01)

    def test14_SubventionMontant(self):

        bi = Bien_Immo('2020', commun=Commun(Travaux(montant=[5000], subvention=[100, 200])))
        bi.add_lot(Lot("", 0, 0, travaux=Travaux(montant=[5000], subvention=[300, 400])))

        self.assertEqual(bi.subvention_montant, 1000)


if __name__ == '__main__':
    unittest.main()
