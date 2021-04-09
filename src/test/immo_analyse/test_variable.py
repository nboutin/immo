
import unittest

from immo_analyse.immo_system import ImmoSystem
from immo_analyse.core.simulation_builder import SimulationBuilder


class TestVariable(unittest.TestCase):

    def test01_ComputeMonthForMonth(self):

        month1 = '2021-01'
        month2 = '2021-02'
        loyer = 500

        immo_sys = ImmoSystem()
        simu_builder = SimulationBuilder()
        simu = simu_builder.build_from_entities(immo_sys, {'lots': {'lot1_name': {'loyer_nu': {month1: loyer}}}})

        self.assertEqual(simu.compute('loyer_nu', month1), loyer)
        self.assertEqual(simu.compute('loyer_nu', month2), 0)

    def test01_ComputeYearForMonth(self):

        year1 = '2021'
        month1 = year1 + '-01'
        month2 = year1 + '-02'
        loyer = 500

        immo_sys = ImmoSystem()
        simu_builder = SimulationBuilder()
        simu = simu_builder.build_from_entities(immo_sys, {'lots': {'lot1_name': {'loyer_nu': {month1: loyer},
                                                                                  'loyer_nu': {month2: loyer}}}})

        self.assertEqual(simu.compute('loyer_nu', year1), loyer * 2)


if __name__ == "__main__":
    unittest.main()
