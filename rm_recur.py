from ll1_symbols import * 

class RmRecurEngine(object):
	"""docstring for RmRecurEngine"""
	def __init__(self, prodc_list, non_term_set):
		self.prodc_list = prodc_list
		self.non_term_list = list(non_term_set)
		# self.non_term_prodc_map = {non_term: [] for non_term in self.non_term_list}
		# self.update_non_term_map()

	def get_prodc_list(self):
		""""""
		return self.prodc_list

	def get_non_term_set(self):
		""""""
		return set(self.non_term_list)

	def prodc_list_by_lefthand(self, non_term):
		""""""
		return [prodc for prodc in self.prodc_list if prodc.left_hand.lexeme == non_term]

	def remove_recur(self, rm_indirect_recur = True):
		if rm_indirect_recur:
			for idx, non_term1 in enumerate(self.non_term_list):
				for non_term2 in self.non_term_list[:idx]:
					found_prodc_list = self.find_prodc(non_term1, non_term2)
					# print non_term1, non_term2, found_prodc_list
					if not len(found_prodc_list) == 0:
						self.expend_production(found_prodc_list)
					# print "before",idx, self.prodc_list, self.non_term_list
				self.remove_direct_recur()
				# print "after",idx, self.prodc_list, self.non_term_list
				# print ""
		else:
			self.remove_direct_recur()

	def find_prodc(self, non_term1, non_term2):
		""""""
		return [prodc for prodc in self.prodc_list if prodc.left_hand.lexeme == non_term1 and prodc.right_hand[0].lexeme == non_term2]

	def expend_production(self, found_prodc_list):
		for prodc in found_prodc_list:
			another_found_prodc_list = self.prodc_list_by_lefthand(prodc.right_hand[0].lexeme)
			for another_prodc in another_found_prodc_list:
				#here modified prodc_list
				self.prodc_list.append(Production(prodc.left_hand, another_prodc.right_hand + prodc.right_hand[1 : ])) 
			self.prodc_list.remove(prodc)

	def remove_direct_recur(self):
		def build_non_term_map():
			non_term_prodc_map = {non_term: [] for non_term in self.non_term_list}
			for prodc in self.prodc_list:
					non_term_prodc_map[prodc.left_hand.lexeme].append(prodc)
			return non_term_prodc_map

		def has_left_recur(sub_prodc_list):
			for prodc in sub_prodc_list:
				if prodc.left_hand.lexeme == prodc.right_hand[0].lexeme:
					return True
			return False
		
		def get_alpha(sub_prodc_list):
			""""""
			return [prodc.right_hand[1:] for prodc in sub_prodc_list if prodc.left_hand.lexeme == prodc.right_hand[0].lexeme]

		def get_beta(sub_prodc_list):
			""""""
			return [prodc.right_hand for prodc in sub_prodc_list if not prodc.left_hand.lexeme == prodc.right_hand[0].lexeme]

		remove_list = []
		non_term_prodc_map = build_non_term_map()
		for non_term, sub_prodc_list in non_term_prodc_map.items():
			if has_left_recur(sub_prodc_list):
				# print "---"
				alpha = get_alpha(sub_prodc_list)
				beta = get_beta(sub_prodc_list)
				#add the new non terminal to the set
				#here modifed non_term_list
				new_non_term = non_term + "Prime"
				self.non_term_list.append(new_non_term)
				#update old from the list
				remove_list += sub_prodc_list
				#add productions
				for item in beta:
					self.prodc_list.append(Production(left_hand = Token("NON_TERM", non_term), right_hand = item + [Token("NON_TERM", new_non_term)]))
				for item in alpha:
					self.prodc_list.append(Production(left_hand = Token("NON_TERM", new_non_term), right_hand = item + [Token("NON_TERM", new_non_term)]))
				self.prodc_list.append(Production(left_hand = Token("NON_TERM", new_non_term), right_hand = [Token("EPSILON", "EPSILON")]))
		#here update the whole list
		self.prodc_list = [prodc for prodc in self.prodc_list if not prodc in remove_list]


