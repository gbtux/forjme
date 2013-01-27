from dashboard.git.switch import switch

class GitDiffLine(object):

	def __init__(self, data, numOld, numNew):
		if data:
			for case in switch(data[0]):
				if case('@'):
					self.numOld = '...'
					self.numNew = '...'
					self.set_type('chunk')
					break
				if case('-'):
					self.numOld = numOld
					self.numNew = ''
					self.set_type('old')
					break
				if case('+'):
					self.numOld = ''
					self.numNew = numNew
					self.set_type('new')
					break
				if case():
					self.numNew = numNew
					self.numOld = numOld
			self.set_line(data)
		else:
			self.numNew = numNew
			self.numOld = numOld

	def set_line(self, line):
		self.line = line

	def get_line(self):
		return self.line

	def set_type(self, type):
		self.type = type

	def get_type(self):
		return self.type

	def get_numOld(self):
		return self.numOld

	def set_numOld(self, numOld):
		self.numOld = numOld

	def set_numNew(self, numNew):
		self.numNew = numNew

	def get_numNew(self):
		return self.numNew

					

