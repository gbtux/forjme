import os.path
import logging
from subprocess import call, check_output, Popen
from dashboard.git.git_repository import GitRepository 



class GitClient(object):
	"""Client class for git repositories"""

	def __init__(self):
		self.logger = logging.getLogger('dashboard')

	def create_repository(thepath, bare=None):
		if os.path.exists(thepath + '/.git/HEAD') and not os.path.exists(thepath + '/HEAD'):
			raise Exception('A GIT repository already exists at ' + thepath)

		repository = GitRepository(path, self)
		return repository.create(bare)
		
	def get_repository(self, thepath):
		if not os.path.exists(thepath) or not os.path.exists(thepath + '/.git/HEAD') and not os.path.exists(thepath + '/HEAD'):
			raise Exception('There is no GIT repository at ' + thepath)
		return GitRepository(thepath, self)

	def run(self, repository, command):
		os.chdir(repository.path)
		self.logger.debug(check_output('git tag', shell=True))
		#ret = check_output('git branch', shell=True)
		#self.logger.debug('first return %s' % ret[0])
		return check_output('git' + " " +  '-c "color.ui"=false' + " " + command, shell=True)

