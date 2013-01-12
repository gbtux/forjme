

class GitBlob(object):

	def __init__(self, branch, repository):
		self.branch = branch
		self.repository = repository

	def output(self):
		return self.repository.get_client().run(self.repository, 'show ' + self.get_branch())

	def set_mode(self, mode):
		self.mode = mode

	def get_mode(self):
		return self.mode

	def set_branch(self, branch):
		self.branch = branch

	def get_branch(self):
		return self.branch

	def set_name(self, name):
		self.name = name

	def get_name(self):
		return self.name

	def get_size(self):
		return self.size

	def set_size(self, size):
		self.size = size


