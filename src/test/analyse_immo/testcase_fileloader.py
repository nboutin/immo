
import unittest
import os
import json


class TestCaseFileLoader(unittest.TestCase):

    def setUp(self):
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        self.input_pathname = os.path.join(__location__, 'data', 'input_test.json')
        with open(self.input_pathname, 'r') as file:
            input_data = json.load(file)

        self.input_data = input_data
        self.achat_data = input_data['achat']
        self.lots_data = input_data['lots']
        self.credit_data = input_data['credit']
        self.defaut_data = input_data['defaut']


if __name__ == "__main__":
    unittest.main()
