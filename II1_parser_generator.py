import argparse, os
import mbnf_parser
import set_table_generator
import yaml_generator

DESCRIPTION = """
An LL(1) parser generator for COMP 412 Lab2.
A scanner and a hand-coded recursive-descent parser reads the Modified
Backus-Naur Form (MBNF) grammar and produces LL(1) tables in YAML format as 
well as related information in human-readable format.
"""
T_HELP = """
print to stdout the LL(1) table in YAML format.
"""

S_HELP = """
print in a human readable form to stdout and in the following order:
1) the productions, as recognized by the parser
2) the FIRST sets for each grammar symbol
3) the FOLLOW sets for each nonterminal, and 
4) the FIRST+ sets for each production.
"""

R_HELP = """
remove left recursion from the input grammar.
"""
FILENAME_HELP = """
This argument specifies  the name of he input file. It is a valid Linux pathname 
elative to the current working directory.
"""

FILENAME_ERROR = """
usage: ILOC_compiler.py [-h] k filename
ILOC_compiler.py: %s
"""

def arguments_parse():
	def is_valid_file(parser, arg):
		if not os.path.exists(arg):
			parser.error("The file %s does not exist!" % arg)
		else:
			return open(arg,"r")

	argument_parser = argparse.ArgumentParser(prog = "llgen", 
											description = DESCRIPTION)
	argument_parser.add_argument("-t", help = T_HELP, action = "store_true")
	argument_parser.add_argument("-s", help = S_HELP, action = "store_true")
	argument_parser.add_argument("-r", help = R_HELP, action = "store_true")
	argument_parser.add_argument("filename", help = FILENAME_HELP, 
		type = lambda x: is_valid_file(argument_parser, x))
	arguments = argument_parser.parse_args()
	# print arguments.t,arguments.s,arguments.r, arguments.filename
	return arguments, argument_parser.print_help

def main():
	arguments, print_argument_help = arguments_parse()
	a_mbnf_parser = mbnf_parser.MbnfParser(arguments.filename)
	grammar = a_mbnf_parser.parse(arguments.r)
	if arguments.r:
		yaml_gen = yaml_generator.YamlGenerator(grammar)
		print yaml_gen.print_yaml()
	elif arguments.t or arguments.s:
		tbl_gen = set_table_generator.SetTableGenerator(grammar)
		first_set = tbl_gen.build_first_set()
		follow_set = tbl_gen.build_follow_set(first_set)
		first_plus_set, production_map, production_left_hand_map = tbl_gen.build_first_plus_set(first_set, follow_set, test_grammar = True)
		ll1_table = tbl_gen.build_ll1_table(first_plus_set,production_left_hand_map)
		yaml_gen = yaml_generator.YamlGenerator(grammar)
		if arguments.t:
			print yaml_gen.print_yaml(ll1_table)
		if arguments.s:
			print "production_map", production_map
			print "first_set:", first_set
			print "follow_set:", follow_set
			print "first_plus_set", first_plus_set
	else:
		print_argument_help()

if __name__ == '__main__':
	main()