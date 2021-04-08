#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from analyse_immo.bien_immo.commun import Commun


class TestCommun(unittest.TestCase):

    def testInit(self):
        com = Commun()
        self.assertFalse(com.travaux is None)


if __name__ == '__main__':
    unittest.main()
