from dashboard.git.git_diff_line import GitDiffLine
import logging

class GitDiff(object):

	def __init__(self):
		self.lines = []

	def set_file(self, name):
		self.file = name

	def get_file(self):
		return self.file

	def set_index(self, index):
		self.index = index

	def get_index(self):
		return self.index

	def set_old(self, old):
		self.old = old

	def get_old(self):
		return self.old

	def set_new(self, new):
		self.new = new

	def get_new(self):
		return self.new

	def add_line(self, line, oldNo, newNo):
		self.lines.append(GitDiffLine(line, oldNo, newNo))

	def get_lines(self):
		return self.lines
