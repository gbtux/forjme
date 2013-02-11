import os.path
import logging
#from subprocess import call, check_output, Popen
from dashboard.git.git_repository import GitRepository
import subprocess

if "check_output" not in dir( subprocess ): # duck punch it in!
    def f(*popenargs, **kwargs):
        if 'stdout' in kwargs:
            raise ValueError('stdout argument not allowed, it will be overridden.')
        process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
        output, unused_err = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get("args")
            if cmd is None:
                cmd = popenargs[0]
            raise CalledProcessError(retcode, cmd)
        return output
    subprocess.check_output = f

class GitClient(object):
	"""Client class for git repositories"""

	def __init__(self):
		self.logger = logging.getLogger('dashboard')

	def create_repository(self, thepath, bare=None):
		if os.path.exists(thepath + '/.git/HEAD') or os.path.exists(thepath + '/HEAD'):
			raise Exception('A GIT repository already exists at ' + thepath)

		repository = GitRepository(thepath, self)
		return repository.create(bare)
		
	def get_repository(self, thepath):
		if not os.path.exists(thepath) or not os.path.exists(thepath + '/.git/HEAD') and not os.path.exists(thepath + '/HEAD'):
			raise Exception('There is no GIT repository at ' + thepath)
		return GitRepository(thepath, self)

	def run(self, repository, command):
		os.chdir(repository.path)
		#self.logger.debug(subprocess.check_output('git tag', shell=True))
		#ret = check_output('git branch', shell=True)
		#self.logger.debug('first return %s' % ret[0])
		return subprocess.check_output('git' + " " +  '-c "color.ui"=false' + " " + command, shell=True)

