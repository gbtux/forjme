
class GitCommit(object):

	def set_hash(self, hash):
		self.hash = hash

	def get_hash(self):
		return self.hash

	def set_short_hash(self, short_hash):
		self.short_hash = short_hash

	def get_short_hash(self):
		return self.short_hash

	def set_tree(self, tree):
		self.tree = tree

	def get_tree(self):
		return self.tree

	def set_parents(self, parents):
		self.parents = parents

	def get_parents(self):
		return self.parents

	def set_author(self, author):
		self.author = author

	def get_author(self):
		return self.author

	def set_author_email(self, author_email):
		self.author_email = author_email

	def get_author_email(self):
		return self.author_email

	def set_date(self, date= None):
		self.date = date

	def get_date(self):
		return self.date

	def set_commiter(self, commiter):
		self.commiter = commiter

	def get_commiter(self):
		return self.commiter

	def set_commiter_email(self, commiter_email):
		self.commiter_email = commiter_email

	def get_commiter_email(self):
		return self.commiter_email

	def set_commiter_date(self, commiter_date):
		self.commiter_date = commiter_date

	def get_commiter_date(self):
		return self.commiter_date

	def set_message(self, message):
		self.message = message

	def get_message(self):
		return self.message

