#!/usr/bin/python

import unittest
from jsonfix import fixJSON

class TestKeys(unittest.TestCase):

    def doCheck(self, in_, out_):
        self.assertEqual(fixJSON(in_), out_)

    def test_no_quote_key(self):
        self.doCheck("{foo:null}", "{\"foo\":null}")

    def test_single_quote_key(self):
        self.doCheck("{'foo':null}", "{\"foo\":null}")

    def test_double_quote_key(self):
        self.doCheck("{\"foo\":null}", "{\"foo\":null}")

    def test_double_quote_with_escape_key(self):
        self.doCheck("{\"f\\\"oo\":null}", "{\"f\\\"oo\":null}")

    def test_single_quote_with_escape_key(self):
        self.doCheck("{'f\\'oo':null}", "{\"f'oo\":null}")

    def test_invalid_character_key(self):
        self.assertRaises(ValueError, fixJSON, "{foo%bar:null}")

    def test_invalid_space_key(self):
        self.assertRaises(ValueError, fixJSON, "{foo bar:null}")

    def test_invalid_start_num_key(self):
        self.assertRaises(ValueError, fixJSON, "{5foobar:null}")

    def test_invalid_start_num_key_b(self):
        self.assertRaises(ValueError, fixJSON, "{5qux:null}")

    def test_underscore_end_key(self):
        self.doCheck("{foobar_:null}", "{\"foobar_\":null}")

    def test_underscore_mid_key(self):
        self.doCheck("{foo_bar:null}", "{\"foo_bar\":null}")

    def test_underscore_start_key(self):
        self.doCheck("{_foobar:null}", "{\"_foobar\":null}")


if __name__ == "__main__":
    unittest.main()
