#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from analyse_immo.impots.ligne import Ligne, Ligne_Model


class TestLigne(unittest.TestCase):

    def testInit(self):
        _ = Ligne('0', 'name')
        _ = Ligne('0', 'name', 0)

    def testGetter(self):

        ligne = Ligne('abc123', 'name_abc123')
        self.assertEqual(ligne.code, 'abc123')
        self.assertEqual(ligne.value, 0)

    def testSetter(self):
        ligne = Ligne('abc123', 'name_abc123', 123)
        self.assertEqual(ligne.value, 123)
        ligne.value = 456
        self.assertEqual(ligne.value, 456)


class TestLigneModel(unittest.TestCase):

    def testInit(self):
        lm = Ligne_Model()
        self.assertEqual(len(lm._lignes), 0)

    def testAdd(self):

        L1 = Ligne('1', '111')
        L2 = Ligne('2', '222')
        L3 = Ligne('3', '333')

        lm = Ligne_Model()
        lm.add(L1, 123)
        lm.add(L2, 456)
        lm.add(L3, 789)

        with self.assertRaises(Exception):
            lm.add(L1, 111)

    def testAddIdentical(self):
        L1 = Ligne('1', '111')

        lm = Ligne_Model()
        lm.add(L1, 10)
        with self.assertRaises(Exception):
            lm.add(L1, 20)
        self.assertEqual(lm.sum(L1), 10)

    def testAddIdenticalCode(self):
        L10_a = Ligne('10', 'a')
        L10_b = Ligne('10', 'b')

        lm = Ligne_Model()
        lm.add(L10_a, 10)
        with self.assertRaises(Exception):
            lm.add(L10_b, 20)
        self.assertEqual(lm.sum(L10_a), 10)
        self.assertEqual(lm.sum(L10_b), 10)
        self.assertEqual(lm.sum([L10_a, L10_b]), 10)

    def testRemove(self):
        L1 = Ligne('1', '111')
        L2 = Ligne('2', '222')
        L3 = Ligne('3', '333')

        lm = Ligne_Model()
        lm.remove(L1)
        lm.add(L1, 1)
        lm.remove(L1)
        lm.add(L1, 2)
        self.assertEqual(lm.sum(L1), 2)

        lm.add(L2, 10)
        lm.add(L3, 20)
        self.assertEqual(lm.sum((L1, L2, L3)), 32)
        lm.remove(L2)
        self.assertEqual(lm.sum((L1, L2, L3)), 22)

    def testSum(self):
        L1 = Ligne('1', '111')
        L2 = Ligne('2', '222')
        L3 = Ligne('3', '333')

        lm = Ligne_Model()
        lm.add(L1, 123)
        self.assertEqual(lm.sum(L1), 123)

        lm.add(L2, 456)
        self.assertEqual(lm.sum(L2), 456)
        self.assertEqual(lm.sum((L1, L2)), 123 + 456)

        lm.add(L3, 789)
        self.assertEqual(lm.sum(L3), 789)
        self.assertEqual(lm.sum((L1, L2, L3)), 123 + 456 + 789)


if __name__ == '__main__':
    unittest.main()
