#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from analyse_immo.factory import Factory
from analyse_immo.bien_immo.bien_immo import Bien_Immo
from analyse_immo.bien_immo.charge import Charge
from analyse_immo.database import Database

from test.testcase_fileloader import TestCaseFileLoader

class TestFactory(TestCaseFileLoader):
    
    def setUp(self):
        super().setUp()
        self.defaut = Factory.make_defaut(self.defaut_data)
        
        self.travaux_data = {'montant': [1000, 2000, 3000],
                             'subvention':[1500, 200], 
                             'deficit_foncier':[]}
        self.commun_data = {'travaux': {'montant': [5000], 
                                        'subvention':[1500], 
                                        'deficit_foncier':[2000]}}
        self.charges_data = {'provision_charge_mensuel': 10, 
                             'copropriete': 20, 
                             'taxe_fonciere':30, 
                             'PNO':40, 
                             'agence_immo':50, 
                             'travaux_provision_taux':0.1, 
                             'vacance_locative_taux':0.2}
    
    def testMakeTravaux(self):
        trv = Factory.make_travaux(self.travaux_data)
        self.assertEqual(trv.montant_total, 6000)
        self.assertEqual(trv.subvention_total, 1700)
        self.assertEqual(trv.deficit_foncier_total, 0)
        
    def testMakeCommun(self):
        com = Factory.make_commun(self.commun_data)
        self.assertEqual(com.travaux.montant_total, 5000)
        
    def testMakeCharges(self):
        chg = Factory.make_charges(self.charges_data, self.defaut, "T1")
        self.assertEqual(chg.get_montant_annuel(
            [Charge.charge_e.charge_locative,
             Charge.charge_e.copropriete, 
             Charge.charge_e.taxe_fonciere, 
             Charge.charge_e.prime_assurance, 
             Charge.charge_e.agence_immo]), 150)

    # def testMakeAnnexe2044(self):
        # bien_immo = Bien_Immo()
        # credit = Credit()
        # i_annee = 0
        # deficit_foncier_anterieur = 0
        # Factory.make_annexe_2044(Database(), bien_immo, credit, i_annee, deficit_foncier_anterieur)


if __name__ == '__main__':
    unittest.main()
