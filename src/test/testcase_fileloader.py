
import unittest
import os
import json


class TestCaseFileLoader(unittest.TestCase):

    def __init__(self, input_filename=None):
        if not input_filename:
            self.input_filename = 'input_test.json'
        else:
            self.input_filename = input_filename

    def setUp(self):
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

        __INPUT_TEST_PATHNAME = os.path.join(__location__, 'data', self.input_filename)
        with open(__INPUT_TEST_PATHNAME, 'r') as file:
            input_data = json.load(file)

        self.achat_data = input_data['achat']
        self.lots_data = input_data['lots']
        self.credit_data = input_data['credit']
        self.defaut_data = input_data['defaut']


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
