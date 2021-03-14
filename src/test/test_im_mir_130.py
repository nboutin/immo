#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest


class TestImMir130(unittest.TestCase):
    
    def __init__(self):
        super().__init__('input_2021_im_mir_130.json')

    def testAll(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
