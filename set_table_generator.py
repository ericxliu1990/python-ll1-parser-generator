from ll1_symbols import *

class SetTableGenerator(object):
	"""docstring for SetTableGenerator"""
	def __init__(self, grammar):
		self.grammar = grammar

	def build_first_set(self):
		changed = True
		first_set = {key: set([key]) for key in self.grammar.term}
		first_set.update({EOF: set([EOF]), EPSILON: set([EPSILON])})
		first_set.update({key: set([]) for key in self.grammar.non_term})
		# return first_set
		while changed:
			old_first_set = dict(first_set)
			for production in self.grammar.production:
				# if production.right_hand[0].type is not "EPSILON":
				right_hand = first_set[production.right_hand[0].lexeme] - set([EPSILON])
				idx = 0
				#search the right hand list to B(k-1)
				while EPSILON in first_set[production.right_hand[idx].lexeme] and idx <= len(production.right_hand) - 2:
					right_hand = right_hand.union(first_set[production.right_hand[idx + 1].lexeme] - set([EPSILON]))
					idx += 1
					# print right_hand, first_set[production.right_hand[idx].lexeme]
				#if the last item is still epsilon, it means epsilon should be in the set
				if idx == len(production.right_hand) - 1 and EPSILON in first_set[production.right_hand[-1].lexeme]:
					right_hand = right_hand.union(set([EPSILON]))
				first_set[production.left_hand.lexeme] = first_set[production.left_hand.lexeme].union(right_hand)
			changed = self.is_changing(first_set, old_first_set)
			# print "first_set", old_first_set
		return first_set

	def build_follow_set(self, first_set):
		follow_set = {key: set([]) for key in self.grammar.non_term}
		follow_set.update({self.grammar.goal: set([EOF])})
		changed = True
		while changed:
			old_follow_set = dict(follow_set)
			
			for production in self.grammar.production:
				#really important new deep copy the set
				trailer = set(follow_set[production.left_hand.lexeme])
				for idx in reversed(xrange(0, len(production.right_hand))): 
					if production.right_hand[idx].lexeme in self.grammar.non_term:
						follow_set[production.right_hand[idx].lexeme] = follow_set[production.right_hand[idx].lexeme].union(trailer)
						if EPSILON in first_set[production.right_hand[idx].lexeme]:
							trailer.update(first_set[production.right_hand[idx].lexeme] - set([EPSILON]))
						else:
							trailer = first_set[production.right_hand[idx].lexeme]
					else:
						trailer = set([production.right_hand[idx].lexeme])
			# print "old", old_follow_set
			changed = self.is_changing(follow_set, old_follow_set)

		return follow_set

	def build_first_plus_set(self, first_set, follow_set, test_grammar = True):
		def is_ll1_grammar():
			def build_non_term_map():
				non_term_idx_map = {non_term: [] for non_term in self.grammar.non_term}
				for idx, prodc in enumerate(self.grammar.production):
						non_term_idx_map[prodc.left_hand.lexeme].append(idx)
				return non_term_idx_map

			def sub_idx_list_test(sub_idx_list):
				if len(sub_idx_list) < 1:
					return True 
				else:
					for idx, itm_1 in enumerate(sub_idx_list):
						for itm_2 in sub_idx_list[idx + 1:]:
							if not len(first_plus_set[itm_1] & first_plus_set[itm_2]) == 0:
								# print first_plus_set[itm_1] & first_plus_set[itm_2], itm_1, itm_2
								return False
				return True

			return all([sub_idx_list_test(sub_idx_list) for non_term, sub_idx_list in build_non_term_map().items() if len(sub_idx_list) > 1])

		def get_first_plus_set(production):
			a_first_plus_set = set([])
			for item in production.right_hand:
				a_first_plus_set |= first_set[item.lexeme]
				if EPSILON not in first_set[item.lexeme]:
					break
				if item == production.right_hand[-1]:
					a_first_plus_set -= set([EPSILON])
					a_first_plus_set |= follow_set[production.left_hand.lexeme]
			return a_first_plus_set

		first_plus_set = {}
		production_map = {}
		production_left_hand_map = {}
		for idx, production in enumerate(self.grammar.production):
			production_map[idx] = production
			production_left_hand_map[idx] = production.left_hand.lexeme
			first_plus_set[idx] = get_first_plus_set(production)
		if test_grammar:
			if not is_ll1_grammar():
				raise Exception("This is not a LL(1) grammar.") 			
		return first_plus_set, production_map, production_left_hand_map

	def build_ll1_table(self, first_plus_set, production_left_hand_map):
		# ll1_table = OrderedDict({key: OrderedDict({key: ERROR_MARKER for key in self.grammar.term}) for key in self.grammar.non_term})
		ll1_table = {key: {key: ERROR_MARKER for key in list(self.grammar.term) + [EOF]} for key in self.grammar.non_term}
		# print "self.grammar.term", self.grammar.term
		for key, production in first_plus_set.items():
			for item in production:
					ll1_table[production_left_hand_map[key]][item] = key
		# print build_symbal_map()
		return ll1_table
	
	def is_changing(self, new_set, old_set):
		# print old_set
		for key, value in old_set.items():
			if not len(value.symmetric_difference(new_set[key])) == 0:
				return True
		return False		