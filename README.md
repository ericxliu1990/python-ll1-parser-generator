python-ll1-parser-generator
===========================
usage: II1_parser_generator.py [-h] [-t] [-s] [-r] filename

An LL(1) parser generator for COMP 412 Lab2. A scanner and a hand-coded
recursive-descent parser reads the Modified Backus-Naur Form (MBNF) grammar
and produces LL(1) tables in YAML format as well as related information in
human-readable format.

positional arguments:
  filename    This argument specifies the name of he input file. It is a valid
              Linux pathname elative to the current working directory.

optional arguments:
  -h, --help  show this help message and exit
  -t          print to stdout the LL(1) table in YAML format.
  -s          print in a human readable form to stdout and in the following
              order: 1) the productions, as recognized by the parser 2) the
              FIRST sets for each grammar symbol 3) the FOLLOW sets for each
              nonterminal, and 4) the FIRST+ sets for each production.
  -r          remove lefe recursion from the input grammar.
