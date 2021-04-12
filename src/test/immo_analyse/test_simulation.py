
import unittest
import numpy as np
from immo_analyse.immo_system import ImmoSystem
from immo_analyse.core.simulation import Simulation
from immo_analyse.core.simulation_builder import SimulationBuilder
from immo_analyse.model.entities import BienImmo


class TestSimulation(unittest.TestCase):

    @unittest.skip('')
    def test01a_Get(self):
        '''
        Get value from entities
        '''
        immo_sys = ImmoSystem()
        simu_builder = SimulationBuilder()
        simu = simu_builder.build_from_entities(immo_sys, {'lot': {'lot1_name': {'lot_type': {'2021': 'T1'}}}})

        self.assertEqual(simu.get('lot_type', '2021'), 'T1')

    @unittest.skip('')
    def test01b_Get(self):
        '''
        Get value not set by entities
        '''
        immo_sys = ImmoSystem()
        simu_builder = SimulationBuilder()
        simu = simu_builder.build_from_entities(immo_sys, {'lot': {'lot1_name': {'lot_type': {'2021': 'T1'}}}})

        self.assertEqual(simu.get('lot_type', '2020'), '')

    def test02_EntitiesIndex(self):

        entities = {'lot': {'l1': {},
                            'l2': {}},
                    'bien_immo': {'bi1': {},
                                  'bi2': {}}}

        immo_sys = ImmoSystem()
        simu_builder = SimulationBuilder()
        simu = simu_builder.build_from_entities(immo_sys, entities)

        self.assertEqual(simu.entities_index['lot']['l1'], 0)
        self.assertEqual(simu.entities_index['lot']['l2'], 1)
        self.assertEqual(simu.entities_index['bien_immo']['bi1'], 0)
        self.assertEqual(simu.entities_index['bien_immo']['bi2'], 1)

    def test02a_ComputeEntity(self):
        '''
        1 Entity with 2 sub-entity
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

        array = simu.compute('loyer_nu', year, add=True, entity_key='bien_immo')
        self.assertTrue(np.array_equal(array, [loyer1 * 12 + loyer2 * 12]))

    def test02b_ComputeEntity(self):
        '''
        2 Entity 2 sub-entity each
        '''
        year = '2021'
        loyer1 = 100
        loyer2 = 200
        loyer3 = 300
        loyer4 = 400
        entities = {'lot': {'l1': {'loyer_nu': {year: loyer1 * 12}},
                            'l2': {'loyer_nu': {year: loyer2 * 12}},
                            'l3': {'loyer_nu': {year: loyer3 * 12}},
                            'l4': {'loyer_nu': {year: loyer4 * 12}}, },
                    'bien_immo': {'bi1': {'lot': ['l1', 'l2']},
                                  'bi2': {'lot': ['l3', 'l4']}}}

        immo_sys = ImmoSystem()
        simu_builder = SimulationBuilder()
        simu = simu_builder.build_from_entities(immo_sys, entities)

        array = simu.compute('loyer_nu', year, add=True)
        self.assertTrue(np.array_equal(array, [loyer1 * 12, loyer2 * 12, loyer3 * 12, loyer4 * 12]))

        array = simu.compute('loyer_nu', year, add=True, entity_key='bien_immo')
        self.assertTrue(np.array_equal(array, [loyer1 * 12 + loyer2 * 12, loyer3 * 12 + loyer4 * 12]))


if __name__ == "__main__":
    unittest.main()
