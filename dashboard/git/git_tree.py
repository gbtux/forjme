import logging
import re
from dashboard.git.git_symlink import GitSymlink
from dashboard.git.git_blob import GitBlob

class GitTree(object):
	"""Tree class for git"""

	def __init__(self, branch, repository):
		self.branch = branch
		self.repository = repository
		self.logger = logging.getLogger('dashboard')

	def parse(self):
		self.logger.debug(self.repository)
		data = self.repository.get_client().run(self.repository, 'ls-tree -l ' + self.branch)
		self.logger.debug(data)
		lines = ''.join(data)
		lines = lines.split("\n")

        	files = [] 
        	root = []
		for line in lines:
			files.append(re.split("/[\s]+/", line, 5))

		for afile in lines:
			#if afile[1] == 'commit' :FIXME
			thefile = re.findall(r'\w+', afile)
			if len(thefile) == 0:
				break 
			#self.logger.debug('afile : %s' % test[0])
			#self.logger.debug('afile1 : %s' % test[1])
			#self.logger.debug('afile2 : %s' % test[2])
			self.logger.debug('thefile : %s' % thefile)
			if thefile[0] == '120000':
				show = sel.repository().get_client().run(self.repository, 'show ' + thefile[2])
				atree = GitSymlink()
                		atree.set_mode(thefile[0])
                		atree.set_name(thefile[4])
		                atree.set_path(show)
                		root.append(atree)
                		continue

            		if thefile[1] == 'blob':
				blob = GitBlob(thefile[2], self.repository)
				blob.set_mode(thefile[0])
                		blob.set_name(thefile[4])
                		blob.set_size(thefile[3])
                		root.append(blob)
                		continue;

            		antree = GitTree(thefile[2], self.repository)
            		antree.set_mode(thefile[0])
            		antree.set_name(thefile[4])
            		root.append(antree)

        	self.data = root

	def output(self):
		files = []
		folders = []
    		for node in self.data:
    			if isinstance(node, GitBlob):
    				afile = {}
				afile['type'] = 'blob';
                		afile['name'] = node.get_name()
                		afile['size'] = node.get_size()
                		afile['mode'] = node.get_mode()
                		afile['hash'] = node.get_branch()
                		files.append(afile)
                		continue

            		if isinstance(node, GitTree):
            			afolder['type'] = 'folder'
                		afolder['name'] = node.get_name()
                		afolder['size'] = ''
                		afolder['mode'] = node.get_mode()
                		afolder['hash'] = node.get_branch()
                		folders.append(afolder)
                		continue

            		if isinstance(node, GitSymlink):
            			afolder['type'] = 'symlink';
                		afolder['name'] = node.get_name();
                		afolder['size'] = '';
               			afolder['mode'] = node.get_mode();
                		afolder['hash'] = '';
                		afolder['path'] = node.get_path()
                		folders.append(afolder)

        	#result = dict(folders, **files)
		result = folders + files
        	return result

	def set_mode(self, mode):
		self.mode = mode
		
	def get_mode(self):
		return self.mode
		
	def set_name(self, name):
		self.name = name
		
	def get_name(self):
		return self.name
		
	def set_branch(self, branch):
		self.branch = branch
		
	def get_branch(self):
		return self.branch
		
