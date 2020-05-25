# -*- coding: utf-8 -*-
"""A few very basic tests for CS109 Python Assignment 2.

This does not test for all the requirements of the assignment! So make
sure you test it yourself.

Run this script using:
  python3.5 assignment2_tests.py
It should work if you are in the same directory as your assignment2.py
file. If this does not work you may want to try:
  PYTHONPATH=[directory containing assignment2.py] python3.5 assignment2_tests.py

This file contains UTF-8 encoded Unicode characters. This is really 
common these days and Python 3 is totally fine with it. If your editor
has problems with it you should fix your editor configuration.
"""

# DO NOT CHANGE THIS FILE. Grading will be done with an official
# version, so make sure your code work with this exact version.

from contextlib import contextmanager
import csv
import os
import tempfile
import unittest
import random
import itertools

import assignment2

@contextmanager
def nonexistant_filename(suffix=""):
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", suffix=suffix, delete=False) as fi:
        filename = fi.name
    os.remove(filename)
    try:
        yield filename
    finally:
        try:
            os.remove(filename)
        except FileNotFoundError:
            pass
            
@contextmanager
def filled_filename(content, encoding="utf-8", suffix=""):
    with tempfile.NamedTemporaryFile(mode="w", encoding=encoding, suffix=suffix, delete=False) as fi:
        fi.write(content)
        filename = fi.name
    try:
        yield filename
    finally:
        os.remove(filename)

def read_file(fn):
    with open(fn, "rt") as fi:
        return fi.read()

large_datafile = """
ATGAGCAATAGC GA TGA

AGC GA TGAAGC GA TGA
TGATATCGGATGCAGA\tCCACCACCT
"""

large_datastr = "ATGAGCAATAGCGATGAAGCGATGAAGCGATGATGATATCGGATGCAGACCACCACCT"
large_data = list(large_datastr)

unicode_datafile = """
A T
C\u2001AG\u3000
TGA 
"""
# Yes, that last character on the last line is a non-ascii character.
unicode_data = list("ATCAGTGA")


def random_strand(seed=42):
    state = seed
    while True:
        state = (25214903917 * state + 11) % (2**48)
        yield "AGTC"[(state >> 8) % 4]

        
class Assignment2Tests(unittest.TestCase):
    def test_load_dna_simple(self):
        with filled_filename("ATGAGCAATAGC") as fn:
            self.assertEqual(list(assignment2.load_dna(fn)), ["A","T","G","A","G","C","A","A","T","A","G","C"])

    def test_load_dna(self):
        with filled_filename(large_datafile) as fn:
            self.assertEqual(list(assignment2.load_dna(fn)), large_data)

    def test_load_dna_unicode(self):
        with filled_filename(unicode_datafile) as fn:
            self.assertEqual(list(assignment2.load_dna(fn)), unicode_data)

    def test_save_dna_simple(self):
        with nonexistant_filename() as fn:
            assignment2.save_dna(["A","T","G","A","G","C","A","A","T","A","G","C"], fn)
            self.assertEqual(read_file(fn), "ATGAGCAATAGC")

    def test_save_dna(self):
        with nonexistant_filename() as fn:
            assignment2.save_dna(large_data, fn)
            self.assertEqual(read_file(fn), large_datastr)

    def test_complement_dna_simple(self):
        self.assertEqual(list(assignment2.complement_dna("ACGGT")), list("TGCCA"))

    def test_complement_dna_large(self):
        print("If this test hangs you are not using generators correctly.")
        s = itertools.islice(assignment2.complement_dna(random_strand()), 1000)
        for b in s:
            self.assertIn(b, "ACGT")

    def test_load_save_large(self):
        print("""
Make sure you are not storing the entire dataset during loading or saving.
There is no portable way to test this, but you should make sure you
did it correctly since I will be testing it during grading. It should be 
easy to test by monitoring how much memory Python uses while running this
test suite.
""")
            
if __name__ == "__main__":
    unittest.main()
