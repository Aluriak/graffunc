"""
Unit tests about the whole package.

"""

import unittest

from conspread import ConvertionSpreader


class TestConSpreadWidely(unittest.TestCase):

    def setUp(self):
        def my_a_to_b_converter(a):
            b = a.upper()
            return b
        def my_b_to_c_converter(b):
            c = 'payload: ' + b + '/payload'
            return c

        # creation of the main object
        self.cp = ConvertionSpreader({
            'a': {'b': my_a_to_b_converter},
        })
        # dynamic modification of the object
        self.cp.add(my_b_to_c_converter, source='b', target='c')


    def test_a_to_b(self):
        b_data = self.cp.convert('data', source='a', target='b')
        self.assertEqual(b_data, 'DATA')

    def test_a_to_c(self):
        c_data = self.cp.convert('data', source='a', target='c')
        self.assertEqual(c_data, 'payload: DATA/payload')
