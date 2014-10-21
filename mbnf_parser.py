"""
a hand-coded recursive-descent parser for MBNF
"""
from collections import namedtuple
import re

class Production(namedtuple("Production",["left_hand", "right_hand"])):
	"""docstring for Production"""
	def __repr__(self):
		if isinstance(self.left_hand, Token):
			return "%s -> %s" % (self.left_hand.lexeme, " ".join([an_item.lexeme for an_item in self.right_hand]))
		else:
			return "%s -> %s" % (self.left_hand, self.right_hand)
		
Token = namedtuple("Token", ["type", "lexeme"])
Grammar = namedtuple("Grammar",["term", "non_term", "production", "goal"])

class MbnfParser():
	"""docstring for mbnf_parser"""
	def __init__(self, file):
		self.mbnf_input = file.read()

	def parse(self, rm_left_recur = False):
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
			""""""
			return set([production.left_hand for production in text])

		def build_term(text):
			""""""
			return set([a_item.lexeme for production in text for a_item in production.right_hand if a_item.type is "SYMBOL"])

		def build_goal(text):
			""""""
			return set(non_term_set) - set([a_item.lexeme for production in text for a_item in production.right_hand if a_item.type is "NON_TERM" and a_item.lexeme is not production.left_hand.lexeme])
		
		def is_goal_valid(goal_set):
			""""""
			if len(goal_set) == 1:
				return goal_set.pop()
			else:
				raise ValueError

		def remove_indirect_left_recursion(prodc_list, non_term_list):
			def build_non_term_map():
				non_term_prodc_map = {non_term: None for non_term in non_term_list}
				for idx, production in enumerate(prodc_list):
					if non_term_prodc_map[production.left_hand.lexeme] is None:
						non_term_prodc_map[production.left_hand.lexeme] = [idx]
					else:
						non_term_prodc_map[production.left_hand.lexeme].append(idx)
				return non_term_prodc_map

			def build_recur_map():
				first_right_non_term = {non_term1: { non_term2: None for non_term2 in non_term_list } for non_term1 in non_term_list}
				for idx, production in enumerate(prodc_list):
					if production.right_hand[0].type is "NON_TERM":
						first_right_non_term[production.left_hand.lexeme][production.right_hand[0].lexeme] = idx
				return first_right_non_term

			def expend_production(production):
				#have problem with this list index
				return Production(production.left_hand, prodc_list[non_term_prodc_map[production.right_hand[0].lexeme][0]].right_hand + production.right_hand[1 : ])
			
			def remove_left_recursion(prodc_list):
				def has_left_recur(prodc_idx):
					for idx in prodc_idx:
						if prodc_list[idx].left_hand.lexeme == prodc_list[idx].right_hand[0].lexeme:
							return True
					return False
				
				def get_alpha(prodc_idx):
					return [prodc_list[idx].right_hand[1:] for idx in prodc_idx if prodc_list[idx].left_hand.lexeme == prodc_list[idx].right_hand[0].lexeme]

				def get_beta(prodc_idx):
					for idx in prodc_idx:
						if not prodc_list[idx].left_hand.lexeme == prodc_list[idx].right_hand[0].lexeme:
							return prodc_list[idx].right_hand
					raise Exception
				remove_list = []
				for non_term, prodc_idx in non_term_prodc_map.items():
					if has_left_recur(prodc_idx):
						print "---"
						alpha = get_alpha(prodc_idx)
						beta = get_beta(prodc_idx)
						#add the new non terminal to the set
						new_non_term = non_term + "Prime"
						non_term_set.add(new_non_term)
						#update old from the list
						remove_list += prodc_idx
						#add productions
						prodc_list.append(Production(left_hand = Token("NON_TERM", non_term), right_hand = beta + [Token("NON_TERM", new_non_term)]))
						for item in alpha:
							prodc_list.append(Production(left_hand = Token("NON_TERM", new_non_term), right_hand = item + [Token("NON_TERM", new_non_term)]))
						prodc_list.append(Production(left_hand = Token("NON_TERM", new_non_term), right_hand = [Token("EPSILON", "EPSILON")]))
				return [prodc for idx, prodc in enumerate(prodc_list) if not idx in remove_list]

			non_term_prodc_map = build_non_term_map()
			
			# for idx, non_term1 in enumerate(non_term_list):
			# 	first_right_non_term = build_recur_map()
			# 	for non_term2 in non_term_list[: idx]:
			# 		production_idx = first_right_non_term[non_term1][non_term2]
			# 		if production_idx is not None:
			# 			print "before", prodc_list[production_idx]
			# 			prodc_list[production_idx] = expend_production(prodc_list[production_idx])
			# 			print "after", prodc_list[production_idx]
			# 	# print first_right_non_term
			# 	print prodc_list
			prodc_list = remove_left_recursion(prodc_list)
			print prodc_list
			return prodc_list

		production_list = tokzr_alsoderives(toker_production(tokzr_sent(self.mbnf_input)))
		non_term_set = build_non_term(production_list)
		production_list = tokzr_right_hand(production_list)
		if rm_left_recur:
			production_list = remove_indirect_left_recursion(production_list, list(non_term_set))
		term_set = build_term(production_list)
		goal = is_goal_valid(build_goal(production_list))
		return Grammar(term = term_set, non_term = non_term_set, production = production_list, goal = goal)
