#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from analyse_immo.tools import interets_compose


class TestTools(unittest.TestCase):

    def testInteretCompose(self):
        self.assertAlmostEqual(interets_compose(1000, 0.05, 4), 1215.51, 2)


if __name__ == '__main__':
    unittest.main()
