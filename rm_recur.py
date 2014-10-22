
from ll1_symbols import * 

class RmRecurEngine(object):
	"""docstring for RmRecurEngine"""
	def __init__(self, prodc_list, non_term_set):
		self.prodc_list = prodc_list
		self.non_term_list = list(non_term_set)
		self.non_term_prodc_map = {non_term: None for non_term in self.non_term_list}
		self.update_non_term_map()

	def get_prodc_list(self):
		return self.prodc_list

	def get_non_term_set(self):
		return set(self.non_term_list)

	def remove_recur(self, rm_indirect_recur = True):
		if rm_indirect_recur:
			for idx, non_term1 in enumerate(non_term_list):
				for non_term2 in list(non_term_list[:idx]):
					prodc_idx_list = self.find_prodc(non_term1, non_term2)
					if not len(prodc_idx_list) == 0:
						self.expend_production(prodc_idx)
				print "before",idx, self.prodc_list, non_term_list
				self.remove_direct_recur()
				print "after",idx, prodc_list, non_term_list
				print ""
		else:
			self.remove_direct_recur()

	def update_non_term_map(self):
		for idx, prodc in enumerate(self.prodc_list):
			if self.non_term_prodc_map[prodc.left_hand.lexeme] is None:
				self.non_term_prodc_map[prodc.left_hand.lexeme] = [idx]
			else:
				self.non_term_prodc_map[prodc.left_hand.lexeme].append(idx)

	def find_prodc(self, non_term1, non_term2):
		prodc_idx_list = []
		for idx, prodc in enumerate(self.prodc_list):
			# print prodc
			if prodc.left_hand.lexeme is non_term1 and prodc.right_hand[0].lexeme is non_term2:
				prodc_idx_list.append(idx)
		return prodc_idx_list

	def expend_production(self, prodc_idx):
		#have problem with this list index
		for idx in prodc_idx:
			prodc = self.prodc_list[idx]
			another_prodc_idx_list = self.non_term_prodc_map[prodc.right_hand[0].lexeme]
			# print "prodc.right_hand[0].lexeme", prodc, another_prodc_idx_list
			for another_prodc_idx in another_prodc_idx_list:
				#here modified prodc_list
				self.prodc_list.append(Production(prodc.left_hand, prodc_list[another_prodc_idx].right_hand + prodc.right_hand[1 : ])) 
			self.prodc_list.remove(prodc)
			self.update_non_term_map()

	def remove_direct_recur(self):
		def has_left_recur(prodc_idx):
			for idx in prodc_idx:
				if self.prodc_list[idx].left_hand.lexeme == self.prodc_list[idx].right_hand[0].lexeme:
					return True
			return False
		
		def get_alpha(prodc_idx):
			return [self.prodc_list[idx].right_hand[1:] for idx in prodc_idx if self.prodc_list[idx].left_hand.lexeme == self.prodc_list[idx].right_hand[0].lexeme]

		def get_beta(prodc_idx):
			beta_list = []
			for idx in prodc_idx:
				if not self.prodc_list[idx].left_hand.lexeme == self.prodc_list[idx].right_hand[0].lexeme:
					beta_list.append(self.prodc_list[idx].right_hand)
			return beta_list

		remove_list = []
		for non_term, prodc_idx in self.non_term_prodc_map.items():
			if has_left_recur(prodc_idx):
				# print "---"
				alpha = get_alpha(prodc_idx)
				beta = get_beta(prodc_idx)
				#add the new non terminal to the set
				#here modifed non_term_list
				new_non_term = non_term + "Prime"
				self.non_term_list.append(new_non_term)
				#update old from the list
				remove_list += prodc_idx
				#add productions
				for item in beta:
					self.prodc_list.append(Production(left_hand = Token("NON_TERM", non_term), right_hand = item + [Token("NON_TERM", new_non_term)]))
				for item in alpha:
					self.prodc_list.append(Production(left_hand = Token("NON_TERM", new_non_term), right_hand = item + [Token("NON_TERM", new_non_term)]))
				self.prodc_list.append(Production(left_hand = Token("NON_TERM", new_non_term), right_hand = [Token("EPSILON", "EPSILON")]))
		#here update the whole list
		self.prodc_list = [prodc for idx, prodc in enumerate(self.prodc_list) if not idx in remove_list]


