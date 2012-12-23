#!/usr/bin/python

from unittest import defaultTestLoader as loader, TextTestRunner

suite = loader.discover(".", "test_*.py")

TextTestRunner().run(suite)
