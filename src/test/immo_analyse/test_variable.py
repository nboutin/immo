
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

    def test02_Credit(self):
        '''
        '''
        m_start = '2021-01'
        entities = {
            'bien_immo': {'bi1': {
                'lot': [],
                'date_achat': {m_start: m_start},
                'prix_achat': {m_start: 115000},
                'taux_notaire': {m_start: 0.08}, }},
            'credit': {'c1': {'bien_immo': ['bi1'],
                              'credit_duree': {m_start: 20 * 12},
                              'taux_interet': {m_start: 0.0115}, },
                       }}

        immo_sys = ImmoSystem()
        simu_builder = SimulationBuilder()
        simu = simu_builder.build_from_entities(immo_sys, entities)

        self.assertEqual(simu.compute('capital_emprunte', m_start), 0)


if __name__ == "__main__":
    unittest.main()
