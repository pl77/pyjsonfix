#!/usr/bin/python

import unittest
from jsonfix import fixJSON

class TestDicts(unittest.TestCase):

    def doCheck(self, in_, out_):
        self.assertEqual(fixJSON(in_), out_)

    def test_empty_dict(self):
        self.doCheck("{}", "{}")

    def test_empty_dict_b(self):
        self.doCheck("{foo:{}}", "{\"foo\":{}}")

    def test_simple_dict(self):
        self.doCheck("{foo:{foo:null}}", "{\"foo\":{\"foo\":null}}")

    def test_complex_dict(self):
        self.doCheck("{foo:{foo:null,bar:0,baz:{foo:1}},bar:null,baz:{foo:\"bar\"}}", '{"foo":{"foo":null,"bar":0,"baz":{"foo":1}},"bar":null,"baz":{"foo":"bar"}}')

    #def test_octal_broken_num_b(self):
        #self.assertRaises(ValueError, fixJSON, "{foo:008}")

if __name__ == "__main__":
    unittest.main()
