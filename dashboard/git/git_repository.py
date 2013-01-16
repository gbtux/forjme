import re
import os.path
import logging
import xml.dom.minidom
from datetime import datetime
from dashboard.git.git_tree import GitTree
from dashboard.git.git_commit import GitCommit


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
		#self.logger.debug(tags)
		return tags

	def get_client(self):
		return self.client

	def get_tree(self, branch):
		atree = GitTree(branch, self)
		#self.logger.debug(atree)
		atree.parse()
		return atree

	def get_commits(self, branch = None):
		command = "log --pretty=format:'<item><hash>%H</hash><short_hash>%h</short_hash><tree>%T</tree><parents>%P</parents><author>%an</author><author_email>%ae</author_email><date>%at</date><commiter>%cn</commiter><commiter_email>%ce</commiter_email><commiter_date>%ct</commiter_date><message><![CDATA[%s]]></message></item>'"
		if branch:
			command += " " + branch 
		#logs = self.get_pretty_format(command)
		output = self.client.run(self, command)
		output = "<result>" + output + "</result>"
		#self.logger.debug(output)
		dom = xml.dom.minidom.parseString(output)
		items = dom.getElementsByTagName("item")
		commits = []
		for item in items:
			commit = GitCommit()
			commit.set_hash(item.getElementsByTagName("hash")[0].firstChild.nodeValue)
			commit.set_short_hash(item.getElementsByTagName("short_hash")[0].firstChild.nodeValue)
			commit.set_tree(item.getElementsByTagName("tree")[0].firstChild.nodeValue)
			if item.getElementsByTagName("parents")[0].firstChild:
				commit.set_parents(item.getElementsByTagName("parents")[0].firstChild.nodeValue)
			else:
				commit.set_parents('')
			commit.set_author(item.getElementsByTagName("author")[0].firstChild.nodeValue)
			commit.set_author_email(item.getElementsByTagName("author_email")[0].firstChild.nodeValue)
			timestamp = item.getElementsByTagName("date")[0].firstChild.nodeValue
			date = datetime.fromtimestamp(float(timestamp))
			thedate = date.strftime("%s" % ("%m/%d/%Y"))
			commit.set_date(thedate)
			#self.logger.debug('date %s' % item.getElementsByTagName("date")[0].firstChild.nodeValue)
			commit.set_commiter(item.getElementsByTagName("commiter")[0].firstChild.nodeValue)
			commit.set_commiter_email(item.getElementsByTagName("commiter_email")[0].firstChild.nodeValue)
			commit.set_commiter_date(item.getElementsByTagName("commiter_date")[0].firstChild.nodeValue)
			commit.set_message(item.getElementsByTagName("message")[0].firstChild.nodeValue)
			commits.append(commit)

		return commits 

	def get_statistics(self, branch):
		data = self.client.run(self, 'ls-tree -r -l ' + branch)
		#self.logger.debug(data)
		lines = ''.join(data)
		#self.logger.debug(lines)
		lines = lines.split("\n")
		data = {'extensions': dict(), 'size': 0, 'files': 0, 'nbext':0}
		ext = dict()
		for afile in lines:
			thefile = re.findall(r'\w+', afile)
			if len(thefile) == 0:
				break 
			if thefile[1] == 'blob':
				data['files'] = data['files'] + 1
			if thefile[3].isdigit():
				data['size'] = data['size'] + int(thefile[3])

			if thefile[5]:
				extens = thefile[5]
				if extens in ext:
					ext[extens] = ext[extens] + 1
				else:
					ext[extens] = 1
					data['nbext']  = data['nbext'] + 1
		data['extensions'] = ext
		return data

	def get_author_statistics(self):
		data = self.client.run(self, 'log --pretty=format:"%an||%ae" ' + self.get_head())
		#self.logger.debug(data)
		lines = ''.join(data)
		lines = lines.split("\n")
		entries = []
		for alog in lines:
			hashed = alog.split("||")
			found = False
			for entry in entries:
				if entry['name'] == hashed[0]:
					entry['nbcommits'] = entry['nbcommits'] + 1
					found = True
			if not found:
				entries.append({'name': hashed[0], 'email': hashed[1], 'nbcommits':1})

		return entries

		