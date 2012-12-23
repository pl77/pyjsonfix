#!/usr/bin/python

import unittest
from jsonfix import fixJSON

class TestStrings(unittest.TestCase):

    def doCheck(self, in_, out_):
        self.assertEqual(fixJSON(in_), out_)

    def test_double_quote_str(self):
        self.doCheck("{foo:\"bar\"}", "{\"foo\":\"bar\"}")

    def test_single_quote_str(self):
        self.doCheck("{foo:'bar'}", "{\"foo\":\"bar\"}")

    def test_no_quote_str(self):  # We're not here to fix broken JavaScript
        self.doCheck("{foo:bar}", "{\"foo\":bar}")

    def test_double_quote_no_end_str(self):
        self.assertRaises(ValueError, fixJSON, "{foo:\"bar}")

    def test_single_quote_no_end_str(self):
        self.assertRaises(ValueError, fixJSON, "{foo:'bar}")

    def test_double_quote_no_start_str(self):
        self.assertRaises(ValueError, fixJSON, "{foo:bar\"}")

    def test_single_quote_no_start_str(self):
        self.assertRaises(ValueError, fixJSON, "{foo:bar'}")

    def test_single_in_single_quote_escape(self):
        self.doCheck("{foo:'b\\'ar'}", "{\"foo\":\"b'ar\"}")

    def test_single_in_double_quote(self):
        self.doCheck("{foo:\"b'ar\"}", "{\"foo\":\"b'ar\"}")

    def test_double_in_single_quote(self):
        self.doCheck("{foo:'b\"ar'}", "{\"foo\":\"b\\\"ar\"}")

    def test_hex_escape(self):
        self.doCheck("{foo:'b\\x20ar'}", "{\"foo\":\"b\\u0020ar\"}")

    def test_octal_escape(self):
        self.doCheck("{foo:'b\\40ar'}", "{\"foo\":\"b\\u0020ar\"}")

    def test_invalid_escape(self):  # Again, we aren't validating JavaScript
        self.doCheck("{foo:'b\\ar'}", "{\"foo\":\"b\\ar\"}")


if __name__ == "__main__":
    unittest.main()
