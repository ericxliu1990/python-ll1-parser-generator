"""
a hand-coded recursive-descent parser for MBNF
"""
from collections import namedtuple
import re

class Production(namedtuple("Production",["left_hand", "right_hand"])):
	"""docstring for Production"""
	def __repr__(self):
		return "%s -> " % self.left_hand.lexeme + " ".join([an_item.lexeme for an_item in self.right_hand])

Token = namedtuple("Token", ["type", "lexeme"])
Grammar = namedtuple("Grammar",["term", "non_term", "production", "goal"])

class MbnfParser():
	"""docstring for mbnf_parser"""
	def __init__(self, file):
		self.mbnf_input = file.read()

	def remove_left_recursion(self):
		pass

	def parse(self):
		def tokzr_sent(text):
			return [sent for sent in 
				re.findall(r'(?ms)\s*(.*?(?=\s*;))', text) if sent is not ""]

		def toker_production(text):
			return [Production(sent.split(":")[0].strip(), sent.split(":")[1].strip()) 
				for sent in text]

		def tokzr_alsoderives(text):
			new_text = []
			for production in text:
				if "|" in production.right_hand:
				 	right_hand_list = [a_right_hand.strip() 
				 		for a_right_hand in production.right_hand.split("|")]
				 	for a_right_hand in right_hand_list:
				 		text.append(Production(left_hand = production.left_hand, right_hand = a_right_hand))
				else:
					new_text.append(production)
			return new_text

		def tokzr_right_hand(text):
			def tokenize(lexeme):
				"""check the token type"""
				def is_valid(lexeme):
					"""check if it is a valid symbol"""
					return re.match(r"[^\W]+$", lexeme)
				if not is_valid(lexeme):
					raise TypeError("%s is not a valid MBNF symbol." % lexeme)
				if lexeme in non_term_set:
					return Token("NON_TERM", lexeme)
				elif lexeme in ["EPSILON", "epsilon","Epsilon"]:
					return Token("EPSILON", "EPSILON")
				else:
					return Token("SYMBOL", lexeme)

			return [Production(tokenize(production.left_hand),
				[tokenize(an_item.strip()) for an_item in production.right_hand.split()]) 
			for production in text]

		def build_non_term(text):
			return set([production.left_hand for production in text])

		def build_term(text):
			return set([a_item.lexeme for production in text for a_item in production.right_hand if a_item.type is not "NON_TERM"])

		def build_goal(text):
			return set(non_term_set) - set([a_item.lexeme for production in text for a_item in production.right_hand if a_item.type is "NON_TERM"])
		def is_goal_valid(goal_set):
			if len(goal_set) == 1:
				return goal_set.pop()
			else:
				raise ValueError
		production_list = tokzr_alsoderives(toker_production(tokzr_sent(self.mbnf_input)))
		non_term_set = build_non_term(production_list)
		production_list = tokzr_right_hand(production_list)
		term_set = build_term(production_list)
		goal = is_goal_valid(build_goal(production_list))
		return Grammar(term = term_set, non_term = non_term_set, production = production_list, goal = goal)
