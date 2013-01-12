import re
import os.path
import logging
from dashboard.git.git_tree import GitTree


class GitRepository(object):
	"""Repository class for git"""

	def __init__(self, path, client):
		self.path = path
		self.client = client
		self.logger = logging.getLogger('dashboard')

	def extract_ref(self, branch='', tree=''):
		branch = branch.strip("/")
		tree = tree.strip("/")
		input = branch + '/' + tree
		matches = re.search("/^([[:alnum:]]{40})(.+)/", input)
		if matches:
			branch = matches[1];
		else:
			valid_refs = self.get_branches() + self.get_tags()
			for k,v in valid_refs.iteritems():
				formatted = "#^%s/#" % re.escape(v)
				if not re.search(formatted, input):
					del valid_refs[k]

			if len(valid_refs) > 1:
				matches2 = re.search('/([^\/]+)(.*)/', input)
				branch = result = re.sub('/^\/|\/$/', '', matches2[1])
			else:
				branch = valid_refs.pop(0)

		tree = branch.replace("", input).strip("/")
		return {'branch': branch, 'tree': tree}

	def get_head(self):
		if os.path.exists(self.path + '/.git/HEAD'):
			thefile = open(self.path + '/.git/HEAD').read()
		else:
			if os.path.exists(self.path + '/HEAD'):
				thefile = open(self.path + '/HEAD').read()	
			else:
				return 'master'

		splitted = thefile.split("\n")
		for line in splitted:
			m = re.search('#ref:\srefs/heads/(.+)#', line)
			if m:
				if self.has_branch(m[1]):
					return m[1]

		branches = self.get_branches()
		if branches:
			return self.get_current_branch()

		return 'master'

	def get_branches(self):
		#return a list :
		items = self.client.run(self, "branch")
		branches = ''.join(items)
		branches = branches.split("\n")
		for branch in branches:
			branch.replace('/[\*\s]/', '')
		return filter(None, branches)

	def get_current_branch(self):
		items = self.client.run(self, "branch")
		branches = ''.join(items)
		branches = branches.split("\n")
		for branch in branches:
			if branch[0] == '*':
				return branch[2:2 + len(branch)]

	def get_tags(self):
		items = self.client.run(self, "tag")
		tags = ''.join(items)
		tags = tags.split("\n")
		self.logger.debug(tags)
		return tags

	def get_client(self):
		return self.client

	def get_tree(self, branch):
		atree = GitTree(branch, self)
		#self.logger.debug(atree)
		atree.parse()
		return atree
