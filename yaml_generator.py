from ll1_symbols import * 

USE_LIBRARY = True
if USE_LIBRARY:
	import yaml

YAML_OUTPUT = """terminals: %s
non-terminals: %s
eof-marker: %s
error-marker: %s
start-symbol: %s
productions: %s
table: %s"""

class YamlGenerator(object):
	"""docstring for yaml_generator"""
	def __init__(self, grammar):
		self.grammar = grammar

	# def print_yaml(self, ll1_table):
	# 	return yaml.dump({"terminals": list(self.grammar.term), 
	# 			"non-terminals" : list(self.grammar.non_term), 
	# 			"eof-marker" : EOF,
	# 			"error-marker" : ERROR_MARKER,
	# 			"start-symbol" : self.grammar.goal,
	# 			"productions" : self.convert_production(),
	# 			"table" : ll1_table})

	def print_yaml(self, ll1_table):
		def convert_list_str(a_list):
			return "[%s]" % (", ".join(a_list))

		def convert_dict_str(a_dict):
			return "{%s}" % ", ".join(["%s: %s" % (key, value) 
				for key, value in a_dict.items()])

		def convert_dict_dict_str(a_dict):
			return "\n\t%s" % ("\n\t".join(["%s: %s" % (key, convert_dict_str(value)) 
				for key, value in a_dict.items()]))

		def convert_dict_list_str(a_dict):
			return "{%s}" % (", \n\t".join(["%s: %s" % (key, convert_list_str(value)) 
				for key, value in a_dict.items()]))

		def convert_dict_dict_list_str(a_dict):
			return "\n\t%s" % ("\n\t".join(["%s: %s" % (key, convert_dict_list_str(value)) 
				for key, value in a_dict.items()]))
		
		return YAML_OUTPUT % (convert_list_str(list(self.grammar.term)), 
								convert_list_str(list(self.grammar.non_term)), 
								EOF, 
								ERROR_MARKER, 
								self.grammar.goal, 
								convert_dict_dict_list_str(self.convert_production()), 
								convert_dict_dict_str(ll1_table))

	def convert_production(self):
				return {idx : {production.left_hand.lexeme : [item.lexeme 
					for item in production.right_hand]} 
					for idx, production in enumerate(self.grammar.production)}
