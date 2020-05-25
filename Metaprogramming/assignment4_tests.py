# -*- coding: utf-8 -*-
"""A few very basic tests for CS106 Python Assignment 4.

This does not test for all the requirements of the assignment! So make
sure you test it yourself.

Run this script using:
  python3.5 assignment4_tests.py
It should work if you are in the same directory as your assignment4.py
file. If this does not work you may want to try:
  PYTHONPATH=[directory containing assignment4.py] python3.5 assignment4_tests.py

During real grading you will get partial credit for getting close to
the currect output. Don't rely on this, but if you are nervous about
it, it should comfort you a little.
"""

# DO NOT CHANGE THIS FILE. Grading will be done with an official
# version, so make sure your code works with this exact version.

from io import StringIO
from contextlib import contextmanager
import os
import tempfile
import time
import unittest
import sys
import importlib
import imp
import warnings


import assignment4

# Copied from: http://stackoverflow.com/questions/26563711/disabling-python-3-2-resourcewarning
def ignore_warnings(test_func):
    def do_test(self, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            test_func(self, *args, **kwargs)
    return do_test

@contextmanager
def captured_output():
    new_err = StringIO()
    old_err = sys.stderr
    try:
        sys.stderr = new_err
        yield None, sys.stderr
    finally:
        sys.stderr = old_err

next_count = 0
def count_up(*args, **kws):
    global next_count
    next_count += 1
    return next_count

class Assignment4Tests(unittest.TestCase):

    def setUp(self):
        sys.stdout.flush()
        sys.stderr.flush()
        
        global next_count
        next_count = 0 # always count from 1 to make it easier to test

    def get_module(self, modname):
        return imp.load_module(modname, *imp.find_module(modname))

    def check_string(self, got, expected):
        """Check the string got against the list of strings in expected.
        Each string must appear as in got. The order is not important.
        """
        for exp in expected:
            self.assertIn(exp, got)

    def test_logcalls_positional(self):
        @assignment4.logcalls("test")
        def f(arg):
            return arg + 1
        with captured_output() as (_, err):
            f(41)
            self.check_string(err.getvalue(), [
                    "test: f(41)\ntest: f -> 42"])

    def test_logcalls_keyword(self):
        @assignment4.logcalls("test")
        def f(arg):
            return arg + 1
        with captured_output() as (_, err):
            f(arg=41)
            self.check_string(err.getvalue(), [
                    "test: f(arg=41)\ntest: f -> 42"])

    def test_logcalls_positional_multiple(self):
        @assignment4.logcalls("test")
        def f(arg, arg2):
            return arg + arg2
        with captured_output() as (_, err):
            f("41", "a")
            self.check_string(err.getvalue(), [
                    "test: f('41', 'a')\ntest: f -> '41a'"])

    def test_logcalls_keyword_multiple(self):
        @assignment4.logcalls("test")
        def f(arg, arg2):
            return arg + arg2
        with captured_output() as (_, err):
            f(arg="41", arg2="a")
            try:
                self.check_string(err.getvalue(), [
                    "test: f(arg='41', arg2='a')\ntest: f -> '41a'"])
            except AssertionError:
                self.check_string(err.getvalue(), [
                    "test: f(arg2='a', arg='41')\ntest: f -> '41a'"])

    def test_logcalls_ld(self):
        @assignment4.logcalls("levenshtein")
        def levenshtein_recursive(s, t):
            """A recursive implementation of levenshtein distance."""
            if not s: return len(t)
            if not t: return len(s)
            if s[0] == t[0]: return levenshtein_recursive(s[1:], t[1:])
            l1 = levenshtein_recursive(s, t[1:])
            l2 = levenshtein_recursive(s[1:], t)
            l3 = levenshtein_recursive(s[1:], t[1:])
            return 1 + min(l1, l2, l3)
        with captured_output() as (_, err):
            levenshtein_recursive("acb", "ab")
        self.check_string(err.getvalue(), [
                "levenshtein: levenshtein_recursive('acb', 'ab')\n"
                "levenshtein: levenshtein_recursive('cb', 'b')\n"
                "levenshtein: levenshtein_recursive('cb', '')\n"
                "levenshtein: levenshtein_recursive -> 2\n" 
                "levenshtein: levenshtein_recursive('b', 'b')\n"
                "levenshtein: levenshtein_recursive('', '')\n"
                "levenshtein: levenshtein_recursive -> 0\n" 
                "levenshtein: levenshtein_recursive -> 0\n" 
                "levenshtein: levenshtein_recursive('b', '')\n"
                "levenshtein: levenshtein_recursive -> 1\n" 
                "levenshtein: levenshtein_recursive -> 1\n" 
                "levenshtein: levenshtein_recursive -> 1\n"
                ])

    def test_logcalls_info(self):
        @assignment4.logcalls("levenshtein")
        def levenshtein_recursive(s, t):
            """A recursive implementation of levenshtein distance."""
            if not s: return len(t)
            if not t: return len(s)
            if s[0] == t[0]: return levenshtein_recursive(s[1:], t[1:])
            l1 = levenshtein_recursive(s, t[1:])
            l2 = levenshtein_recursive(s[1:], t)
            l3 = levenshtein_recursive(s[1:], t[1:])
            return 1 + min(l1, l2, l3)
        self.assertEqual(levenshtein_recursive.__doc__, "A recursive implementation of levenshtein distance.")
        self.assertEqual(levenshtein_recursive.__name__, "levenshtein_recursive")

    def test_logcalls_argtypes_onearg(self):
        cnt = assignment4.logcalls("tst")(count_up)
        global next_count
        next_count = 0
        with captured_output() as (_, err):
            cnt((1,))
            cnt(test=42)
            self.check_string(err.getvalue(), [
                "tst: count_up((1,))\n"
                "tst: count_up -> 1\n"
                "tst: count_up(test=42)\n"
                "tst: count_up -> 2\n"
                ])

    def test_logcalls_argtypes_otherargs(self):
        cnt = assignment4.logcalls("tst")(count_up)
        global next_count
        next_count = 0
        with captured_output() as (_, err):
            cnt("t", data=[1,2])
            cnt()
            cnt("t", data=[1,2])
            self.check_string(err.getvalue(), [
                "tst: count_up('t', data=[1, 2])\n"
                "tst: count_up -> 1\n"
                "tst: count_up()\n"
                "tst: count_up -> 2\n"
                "tst: count_up('t', data=[1, 2])\n"
                "tst: count_up -> 3\n"
                ])
       

if __name__ == "__main__":
    unittest.main()
