import unittest

from test.testcase_fileloader import TestCaseFileLoader
from analyse_immo.factory import Factory


class TestDefaut(TestCaseFileLoader):

    def testIrlTauxAnnuel(self):
        defaut = Factory.make_defaut(self.defaut_data)
        self.assertEqual(defaut.irl_taux_annuel, 0.005)

    def testVacanceLocativeTaux(self):
        defaut = Factory.make_defaut(self.defaut_data)
        self.assertEqual(defaut.vacance_locative_taux('T1'), 0.083)
        self.assertEqual(defaut.vacance_locative_taux('T0'), 0)

    def testGestionAgenceTaux(self):
        defaut = Factory.make_defaut(self.defaut_data)
        self.assertEqual(defaut.gestion_agence_taux, 0.08)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
