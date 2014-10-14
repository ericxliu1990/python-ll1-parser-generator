class SetTableGenerator(object):
	"""docstring for SetTableGenerator"""
	def __init__(self, grammar):
		self.grammar = grammar

	def build_first_set(self):
		changed = True
		first_set = {key: set([key]) for key in self.grammar.term}
		first_set.update({"EOF": set(["EOF"])})
		first_set.update({key: set([]) for key in self.grammar.non_term})
		# return first_set
		while changed:
			old_first_set = dict(first_set)
			for production in self.grammar.production:
				# if production.right_hand[0].type is not "EPSILON":
				right_hand = first_set[production.right_hand[0].lexeme] - set(["EPSILON"])
				idx = 0
				#search the right hand list to B(k-1)
				for idx in xrange(0, len(production.right_hand) - 2):
					while "EPSILON" in first_set[production.right_hand[idx].lexeme]:
						right_hand = right_hand.union(first_set(production.right_hand[idx + 1].lexeme) - set(["EPSILON"]))
				#if the last item is still epsilon, it means epsilon should be in the set
				if idx == len(production.right_hand) - 1 and "EPSILON" in first_set[production.right_hand[-1].lexeme]:
					right_hand = right_hand.union(set(["EPSILON"]))
				first_set[production.left_hand.lexeme] = first_set[production.left_hand.lexeme].union(right_hand)
			changed = self.is_changing(first_set, old_first_set)
			# print "first_set", old_first_set
		return first_set

	def build_follow_set(self, first_set):
		follow_set = {key: set([]) for key in self.grammar.non_term}
		follow_set.update({self.grammar.goal.pop(): set(["EOF"])})
		changed = True
		while changed:
			old_follow_set = dict(follow_set)
			
			for production in self.grammar.production:
				#really important new deep copy the set
				trailer = set(follow_set[production.left_hand.lexeme])
				for idx in reversed(xrange(0, len(production.right_hand))): 
					if production.right_hand[idx].lexeme in self.grammar.non_term:
						follow_set[production.right_hand[idx].lexeme] = follow_set[production.right_hand[idx].lexeme].union(trailer)
						if "EPSILON" in first_set[production.right_hand[idx].lexeme]:
							trailer.update(first_set[production.right_hand[idx].lexeme] - set(["EPSILON"]))
						else:
							trailer = first_set[production.right_hand[idx].lexeme]
					else:
						trailer = set([production.right_hand[idx].lexeme])
			# print "old", old_follow_set
			changed = self.is_changing(follow_set, old_follow_set)

		return follow_set

	def build_first_plus_set(self, first_set, follow_set):
		first_plus_set = {}
		for idx, production in enumerate(self.grammar.production):
			if "EPSILON" in first_set[production.right_hand[0].lexeme]:
				first_plus_set[idx] = first_set[production.right_hand[0].lexeme].union(follow_set[production.left_hand.lexeme])
			else:
				first_plus_set[idx] = set(first_set[production.right_hand[0].lexeme])
		return first_plus_set

	def is_changing(self, new_set, old_set):
		# print old_set
		for key, value in old_set.items():
			if len(value.symmetric_difference(new_set[key])) is not 0:
				return True
		return False		