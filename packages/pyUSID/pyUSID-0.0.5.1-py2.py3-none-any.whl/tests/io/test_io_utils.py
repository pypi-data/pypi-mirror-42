# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 15:07:16 2017

@author: Suhas Somnath
"""
from __future__ import division, print_function, unicode_literals, absolute_import
import unittest
import sys

sys.path.append("../../pyUSID/")
from pyUSID.io import io_utils


class TestIOUtils(unittest.TestCase):

    def test_formatted_str_to_number(self):
        self.assertEqual(io_utils.formatted_str_to_number("4.32 MHz", ["MHz", "kHz"], [1E+6, 1E+3]), 4.32E+6)

    def test_formatted_str_to_number_invalid(self):
        with self.assertRaises(ValueError):
            _ = io_utils.formatted_str_to_number("4.32 MHz", ["MHz"], [1E+6, 1E+3])
        with self.assertRaises(ValueError):
            _ = io_utils.formatted_str_to_number("4.32 MHz", ["MHz", "kHz"], [1E+3])
        with self.assertRaises(ValueError):
            _ = io_utils.formatted_str_to_number("4.32-MHz", ["MHz", "kHz"], [1E+6, 1E+3])
        with self.assertRaises(ValueError):
            _ = io_utils.formatted_str_to_number("haha MHz", ["MHz", "kHz"], [1E+6, 1E+3])
        with self.assertRaises(ValueError):
            _ = io_utils.formatted_str_to_number("1.2.3.4 MHz", ["MHz", "kHz"], [1E+6, 1E+3])
        with self.assertRaises(ValueError):
            _ = io_utils.formatted_str_to_number("MHz", ["MHz", "kHz"], [1E+6, 1E+3])

    def test_format_quantity(self):
        qty_names = ['sec', 'mins', 'hours', 'days']
        qty_factors = [1, 60, 3600, 3600*24]
        ret_val = io_utils.format_quantity(315, qty_names, qty_factors)
        self.assertEqual(ret_val, '5.25 mins')
        ret_val = io_utils.format_quantity(6300, qty_names, qty_factors)
        self.assertEqual(ret_val, '1.75 hours')

    def test_format_quantity_illegal(self):
        with self.assertRaises(ValueError):
            _ = io_utils.format_quantity(315, ['sec', 'mins', 'hours'], [1, 60, 3600, 3600*24])
        with self.assertRaises(ValueError):
            _ = io_utils.format_quantity(315, ['sec', 'mins', 'hours'], [1, 60])
        with self.assertRaises(TypeError):
            _ = io_utils.format_quantity(315, ['sec', 14, 'hours'], [1, 60, 3600*24])
        with self.assertRaises(TypeError):
            _ = io_utils.format_quantity('hello', ['sec', 'mins', 'hours'], [1, 60, 3600])

    def test_format_time(self):
        ret_val = io_utils.format_time(315)
        self.assertEqual(ret_val, '5.25 mins')
        ret_val = io_utils.format_time(6300)
        self.assertEqual(ret_val, '1.75 hours')

    def test_format_size(self):
        ret_val = io_utils.format_size(15.23)
        self.assertEqual(ret_val, '15.23 bytes')
        ret_val = io_utils.format_size(5830418104.32)
        self.assertEqual(ret_val, '5.43 GB')


if __name__ == '__main__':
    unittest.main()