#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from analyse_immo.impots.ligne import Ligne


class TestLigne(unittest.TestCase):

    def testInit(self):
        _ = Ligne('0', 'name')
        _ = Ligne('0', 'name', 0)

    def testGetter(self):

        ligne = Ligne('abc123', 'name_abc123')
        self.assertEqual(ligne.numero, 'abc123')
        self.assertEqual(ligne.value, 0)

    def testSetter(self):
        ligne = Ligne('abc123', 'name_abc123', 123)
        self.assertEqual(ligne.value, 123)
        ligne.value = 456
        self.assertEqual(ligne.value, 456)


if __name__ == '__main__':
    unittest.main()
