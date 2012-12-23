#!/usr/bin/python

import unittest
from jsonfix import fixJSON

class TestLists(unittest.TestCase):

    def doCheck(self, in_, out_):
        self.assertEqual(fixJSON(in_), out_)

    def test_empty_list(self):
        self.doCheck("{foo:[]}", "{\"foo\":[]}")

    def test_single_comma_list(self):
        self.doCheck("{foo:[,]}", "{\"foo\":[null]}")

    def test_double_comma_list(self):
        self.doCheck("{foo:[,,]}", "{\"foo\":[null,null]}")

    def test_comma_spaces_list(self):
        self.doCheck("{foo:[,   ,, ,,,       ,     ]}", "{\"foo\":[null,   null,null, null,null,null,       null]}")

    def test_single_element_list(self):
        self.doCheck("{foo:[0]}", "{\"foo\":[0]}")

    def test_number_list(self):
        self.doCheck("{foo:[0,1,2,3,4,5]}", "{\"foo\":[0,1,2,3,4,5]}")

    def test_number_comma_end_list(self):
        self.doCheck("{foo:[0,1,2,3,4,5,]}", "{\"foo\":[0,1,2,3,4,5]}")

    def test_strings_with_braces_list(self):
        self.doCheck("{foo:[']', '[[}{', ')()][][]', '[']}", '{"foo":["]", "[[}{", ")()][][]", "["]}')

    def test_list_of_lists_list(self):
        self.doCheck("{foo:[[],[],[]]}", '{"foo":[[],[],[]]}')

    def test_list_of_lists_of_numbers_list(self):
        self.doCheck("{foo:[[0,1],[2,3],[4,5]]}", '{"foo":[[0,1],[2,3],[4,5]]}')

    # These are invalid JavaScript, so really we don't care if they fail or not.
    def test_missing_brace_list(self):
        self.assertRaises(ValueError, fixJSON, "{foo:[0,1,2}")

    def test_missing_brace_list_b(self):
        self.assertRaises(ValueError, fixJSON, "{foo:[}")

    def test_missing_brace_list_c(self):
        self.assertRaises(ValueError, fixJSON, "{foo:[")

if __name__ == "__main__":
    unittest.main()
