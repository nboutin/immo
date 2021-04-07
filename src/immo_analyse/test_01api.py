
import unittest

from .immo_system import ImmoSystem
from .core.simulation import Simulation
from .core.simulation_builder import SimulationBuilder

entities = {
    'lots': {'lot1': {'lot_type': {'2021-01-01': 'T1'},
                      'surface': {'2021-01-01': 50},
                      'loyer_nu': {'2021': 400 * 12}},
             'lot2': {'lot_type': {'2021-01-01': 'T2'},
                      'surface': {'2021-01-01': 60},
                      'loyer_nu': {'2021': 500 * 12}}},
    'bien_immo': {'bi1': {'lots': [],
                          'prix_achat': {},
                          'frais_notaire': {},
                          'frais_agence': {},
                          'apport': {}}},
    'analyse': {'bien_immo': 'bi1',
                'credit': {},
                'groupe_fiscal': {}},
}


class Test_01API(unittest.TestCase):

    def test01_ImmoSystem(self):
        _ = ImmoSystem()

    def test02a_SimulationBuilder(self):
        _ = ImmoSystem()
        _ = SimulationBuilder()

    def test02b_SimulationBuilder(self):
        immo_sys = ImmoSystem()
        simu_builder = SimulationBuilder()
        _ = simu_builder.build_from_entities(immo_sys, {'lots': {'lot1_name': {'lot_type': {'2021': 'T1'}}}})

    def test03a_SimulationGet(self):
        immo_sys = ImmoSystem()
        simu_builder = SimulationBuilder()
        simu = simu_builder.build_from_entities(immo_sys, {'lots': {'lot1_name': {'lot_type': {'2021': 'T1'}}}})

        self.assertEqual(simu.get('lot_type', '2021'), 'T1')
        # self.assertEqual(simu.get('lot_type', '2020'), '')
        # self.assertEqual(simu.get('lot1', 'lot_type', '2021'), 'T1')
        # self.assertEqual(simu.get('lot1', '2020', 'type'), '')
        # self.assertEqual(simu.get('lot1', '2022', 'type'), 'T1')

    @unittest.skip('')
    def test03a_get_from_entity(self):
        immosys = ImmoSystem()
        simu_builder = SimulationBuilder()
        simu = simu_builder.build_from_entities(immosys, entities)

        self.assertEqual(simu.get('lot1', '2021', 'lot_type'), 'T1')
        self.assertEqual(simu.get('lot1', '2020', 'type'), '')
        self.assertEqual(simu.get('lot1', '2022', 'type'), 'T1')

        self.assertEqual(simu.get('lot2', '2021', 'surface'), 60)
        self.assertEqual(simu.get('lot2', '2020', 'surface'), 0)
        self.assertEqual(simu.get('lot2', '2022', 'surface'), 60)

    @unittest.skip('')
    def test03b_get_from_entity(self):
        immosys = ImmoSystem()
        simu = Simulation(immosys)

        self.assertEqual(simu.compute('2021', 'type'), ['T1', 'T2'])
        self.assertEqual(simu.compute('2020', 'type'), ['', ''])
        self.assertEqual(simu.compute('2022', 'type'), ['T1', 'T2'])

        self.assertEqual(simu.compute('2021', 'surface'), [50, 60])
        self.assertEqual(simu.compute('2020', 'surface'), [0, 0])
        self.assertEqual(simu.compute('2022', 'surface'), [50, 60])


if __name__ == "__main__":
    unittest.main()
