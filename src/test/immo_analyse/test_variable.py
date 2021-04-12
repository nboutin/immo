
import unittest
import numpy as np

from immo_analyse.immo_system import ImmoSystem
from immo_analyse.core.simulation_builder import SimulationBuilder


class TestVariable(unittest.TestCase):

    def test01a_Period(self):
        '''
        variable period month
        set month, get month
        '''

        month1 = '2021-01'
        month2 = '2021-02'
        loyer = 500

        immo_sys = ImmoSystem()
        simu_builder = SimulationBuilder()
        simu = simu_builder.build_from_entities(immo_sys, {'lot': {'lot1_name': {'loyer_nu': {month1: loyer}}}})

        self.assertEqual(simu.compute('loyer_nu', month1), loyer)
        self.assertEqual(simu.compute('loyer_nu', month2), 0)

    def test01b_Period(self):
        '''
        variable period month
        set month, get year
        '''
        year1 = '2021'
        month1 = year1 + '-01'
        month2 = year1 + '-02'
        loyer = 500

        immo_sys = ImmoSystem()
        simu_builder = SimulationBuilder()
        simu = simu_builder.build_from_entities(immo_sys, {'lot': {'lot1_name': {'loyer_nu': {month1: loyer,
                                                                                              month2: loyer}}}})

        self.assertEqual(simu.compute('loyer_nu', month1), loyer)
        self.assertEqual(simu.compute('loyer_nu', month2), loyer)
        self.assertEqual(simu.compute('loyer_nu', year1, add=True), loyer * 2)

    def test01c_Period(self):
        '''
        variable period month
        set year, get month
        '''

        year1 = '2021'
        month1 = year1 + '-01'
        month2 = year1 + '-02'
        loyer = 500

        immo_sys = ImmoSystem()
        simu_builder = SimulationBuilder()
        simu = simu_builder.build_from_entities(immo_sys, {'lot': {'lot1_name': {'loyer_nu': {year1: loyer * 12}}}})

        self.assertEqual(simu.compute('loyer_nu', month1), loyer)
        self.assertEqual(simu.compute('loyer_nu', month2), loyer)

    def test02_BienImmoLoyer(self):
        '''
        get loyer bien immo = sommes loyer des lot
        '''
        year = '2021'
        loyer1 = 400
        loyer2 = 500
        entities = {'lot': {'l1': {'loyer_nu': {year: loyer1 * 12}},
                            'l2': {'loyer_nu': {year: loyer2 * 12}}},
                    'bien_immo': {'bi1': {'lot': ['l1', 'l2']}}}

        immo_sys = ImmoSystem()
        simu_builder = SimulationBuilder()
        simu = simu_builder.build_from_entities(immo_sys, entities)

        array = simu.compute('loyer_nu', year, add=True)
        self.assertTrue(np.array_equal(array, [loyer1 * 12, loyer2 * 12]))


if __name__ == "__main__":
    unittest.main()
