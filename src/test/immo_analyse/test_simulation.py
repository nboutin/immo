
import unittest

from immo_analyse.immo_system import ImmoSystem
from immo_analyse.core.simulation import Simulation
from immo_analyse.core.simulation_builder import SimulationBuilder
from immo_analyse.model.entities import BienImmo


class TestSimulation(unittest.TestCase):

    def test01a_Get(self):
        '''
        Get value from entities
        '''
        immo_sys = ImmoSystem()
        simu_builder = SimulationBuilder()
        simu = simu_builder.build_from_entities(immo_sys, {'lot': {'lot1_name': {'lot_type': {'2021': 'T1'}}}})

        self.assertEqual(simu.get('lot_type', '2021'), 'T1')

    def test01b_Get(self):
        '''
        Get value not set by entities
        '''
        immo_sys = ImmoSystem()
        simu_builder = SimulationBuilder()
        simu = simu_builder.build_from_entities(immo_sys, {'lot': {'lot1_name': {'lot_type': {'2021': 'T1'}}}})

        self.assertEqual(simu.get('lot_type', '2020'), '')


if __name__ == "__main__":
    unittest.main()
