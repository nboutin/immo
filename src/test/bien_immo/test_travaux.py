#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from analyse_immo.bien_immo.travaux import Travaux


class TestTravaux(unittest.TestCase):

    def testInit(self):
        trv = Travaux()

        self.assertEqual(trv.montant_total, 0)
        self.assertEqual(trv.subvention_total, 0)
        self.assertEqual(trv.deficit_foncier_total, 0)

        with self.assertRaises(Exception):
            _ = Travaux(deficit_foncier=[1])


if __name__ == '__main__':
    unittest.main()
