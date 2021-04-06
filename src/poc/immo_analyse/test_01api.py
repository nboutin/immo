
import unittest

from .immo_system import ImmoSystem
from .simulation import Simulation

entities = {
    'lots': {'lot1': {'type': {'2021-01-01': 'T1'},
                      'surface': {'2021-01-01': 50},
                      'loyer_nu': {'2021': 400 * 12}},
             'lot2': {'type': {'2021-01-01': 'T2'},
                      'surface': {'2021-01-01': 60},
                      'loyer_nu': {'2021': 500 * 12}}},
    'immeubles': {},
    'groupes_fiscal': {}
}


class Test_01API(unittest.TestCase):

    def test01a_get_from_entity(self):
        immosys = ImmoSystem(entities)
        simu = Simulation(immosys)

        self.assertEqual(simu.get('lot1', '2021', 'type'), 'T1')
        self.assertEqual(simu.get('lot1', '2020', 'type'), '')
        self.assertEqual(simu.get('lot1', '2022', 'type'), 'T1')

        self.assertEqual(simu.get('lot2', '2021', 'surface'), 60)
        self.assertEqual(simu.get('lot2', '2020', 'surface'), 0)
        self.assertEqual(simu.get('lot2', '2022', 'surface'), 60)

    def test01b_get_from_entity(self):
        immosys = ImmoSystem(entities)
        simu = Simulation(immosys)

        self.assertEqual(simu.compute('2021', 'type'), ['T1', 'T2'])
        self.assertEqual(simu.compute('2020', 'type'), ['', ''])
        self.assertEqual(simu.compute('2022', 'type'), ['T1', 'T2'])

        self.assertEqual(simu.compute('2021', 'surface'), [50, 60])
        self.assertEqual(simu.compute('2020', 'surface'), [0, 0])
        self.assertEqual(simu.compute('2022', 'surface'), [50, 60])


if __name__ == "__main__":
    unittest.main()
