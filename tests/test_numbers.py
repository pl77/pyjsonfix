#!/usr/bin/python

import unittest
from jsonfix import fixJSON

class TestNumbers(unittest.TestCase):

    def doCheck(self, in_, out_):
        self.assertEqual(fixJSON(in_), out_)

    def test_simple_num(self):
        self.doCheck("{foo:0}", "{\"foo\":0}")

    def test_simple_num_b(self):
        self.doCheck("{foo:1}", "{\"foo\":1}")

    def test_hex_num(self):
        self.doCheck("{foo:0x7f}", "{\"foo\":127}")

    def test_hex_num_b(self):
        self.doCheck("{foo:0x00007f}", "{\"foo\":127}")

    def test_octal_num(self):
        self.doCheck("{foo:055}", "{\"foo\":45}")

    def test_octal_num_b(self):
        self.doCheck("{foo:0000055}", "{\"foo\":45}")

    def test_float_num(self):
        self.doCheck("{foo:1.23}", "{\"foo\":1.23}")

    def test_float_num_b(self):
        self.doCheck("{foo:.23}", "{\"foo\":.23}")

    def test_float_broken_num(self):
        self.assertRaises(ValueError, fixJSON, "{foo:0.1.2}")

    def test_float_broken_num_b(self):
        self.assertRaises(ValueError, fixJSON, "{foo:001.1.2}")

    def test_hex_broken_num(self):
        self.assertRaises(ValueError, fixJSON, "{foo:0x0q}")

    def test_hex_broken_num_b(self):
        self.assertRaises(ValueError, fixJSON, "{foo:0x}")

    def test_octal_broken_num(self):
        self.assertRaises(ValueError, fixJSON, "{foo:08}")

    def test_octal_broken_num_b(self):
        self.assertRaises(ValueError, fixJSON, "{foo:008}")

if __name__ == "__main__":
    unittest.main()
