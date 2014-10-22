"""
a hand-coded recursive-descent parser for MBNF
"""

import re
import rm_recur
from ll1_symbols import * 

class MbnfParser():
	"""docstring for mbnf_parser"""
	def __init__(self, file):
		self.mbnf_input = file.read()

	def parse(self, rm_left_recur = False):
		def tokzr_sent(text):
			return [sent for sent in 
				re.findall(r'(?ms)\s*(.*?(?=\s*;))', text) if not sent == ""]

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
			""""""
			return set([production.left_hand for production in text])

		def build_term(text):
			""""""
			return set([a_item.lexeme for production in text for a_item in production.right_hand if a_item.type == "SYMBOL"])

		def build_goal(text):
			""""""
			return set(non_term_set) - set([a_item.lexeme for production in text for a_item in production.right_hand if a_item.type == "NON_TERM" and not a_item.lexeme == production.left_hand.lexeme])
		
		def is_goal_valid(goal_set):
			""""""
			if len(goal_set) == 1:
				return goal_set.pop()
			else:
				raise ValueError(goal_set)

		production_list = tokzr_alsoderives(toker_production(tokzr_sent(self.mbnf_input)))
		non_term_set = build_non_term(production_list)
		production_list = tokzr_right_hand(production_list)
		term_set = build_term(production_list)
		goal = is_goal_valid(build_goal(production_list))
		if rm_left_recur:
			rm_recur_engine = rm_recur.RmRecurEngine(production_list, non_term_set)
			rm_recur_engine.remove_recur(rm_indirect_recur = True)
			production_list = rm_recur_engine.get_prodc_list()
			non_term_set = rm_recur_engine.get_non_term_set()

		return Grammar(term = term_set, non_term = non_term_set, production = production_list, goal = goal)
