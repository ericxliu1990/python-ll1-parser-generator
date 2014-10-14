class SetTableGenerator(object):
	"""docstring for SetTableGenerator"""
	def __init__(self, grammar):
		self.grammar = grammar

	def build_first_set(self):
		def is_changing(old_first_set):
			for key, value in old_first_set.items():
				if len(value.symmetric_difference(first_set[key])) is not 0:
					return True
			return False
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
			changed = is_changing(old_first_set)
			# print old_first_set

		return first_set
		