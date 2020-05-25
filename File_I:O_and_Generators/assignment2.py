"""Assignment 2: Files and Streaming Data

Write code to read and process a large data file. In this case you
will be generating complement of a DNA strand. The problem is that the
DNA strand is very long (3 billion bases) so you cannot (or at least
should not) load it all into memory at once.

"""

def load_dna(filename):
    """Load a DNA strand from the given filename.

    The file is a sequence of letters ("A", "T", "C", "G") and white
    space. You should remove all white space leaving just the letters.

    For example, if the file contains:
      AG T
      CG
    The output of the returned generator should be "A", "G", "T", "C",
    "G".

    This function is a generator for the sequence. So instead of loading
    the whole sequence you should load one base at a time (or a few
    bases at a time) and yield the bases.

    """
    raise NotImplementedError

def complement_dna(strand):
    """Given a single DNA strand build the complement strand.

    The single DNA strand is represented as an iterable of strings
    ("A", "T", "C", "G").

    The output should be the complement of the input strand using the
    DNA pairing rules: A pairs with T, C pairs with G. For example:

    list(complement_dna(["A", "T", "G", "G", "C"])) ==
      ["T", "A", "C", "C", "G"]

    The input iterable could be a generator or iterator. So it can
    only be iterated once. Also the output should be a generator. This
    is critical because the input and output strands may be larger
    than system memory and if you use generators properly the entire
    thing never needs to be stored at the same time.

    Grading: 80% for correct answer, 100% for nice clean *declarative*
    answer using a single generator expression.

    """
    raise NotImplementedError

def save_dna(strand, filename):
    """Save a DNA strand to the given filename.

    Simply write each base to the file as a single character. You do
    not need to add any white space, but if you want to add a new line
    every 80 characters go ahead.

    Remember the input may be extremely long and you should NOT store
    the whole strand in memory at any point.
    """
    raise NotImplementedError
