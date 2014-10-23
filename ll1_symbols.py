
from collections import namedtuple

EOF = "<EOF>"
EPSILON = "EPSILON"
ERROR_MARKER = "--"
SYMBOL = "SYMBOL"
NON_TERM = "NON_TERM"

class Production(namedtuple("Production",["left_hand", "right_hand"])):
	"""docstring for Production"""
	def __repr__(self):
		if isinstance(self.left_hand, Token):
			return "%s -> %s\n" % (self.left_hand.lexeme, " ".join([an_item.lexeme for an_item in self.right_hand]))
		else: 
			return "%s -> %s" % (self.left_hand, self.right_hand)
		
Token = namedtuple("Token", ["type", "lexeme"])
Grammar = namedtuple("Grammar",["term", "non_term", "production", "goal"])
