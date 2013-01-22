import re
import os.path
import logging
import xml.dom.minidom
from datetime import datetime
from dashboard.git.git_tree import GitTree
from dashboard.git.git_commit import GitCommit
from dashboard.git.git_blob import GitBlob


class GitRepository(object):
	"""Repository class for git"""

	#extension: lexer class
	defaultTypes = { \
		'croc':'croc','dg':'dg','factor':'factor','fy':'fancy','fancypack':'fancy',\
		'io':'io','lua':'lua','wlua':'lua','md':'minid','moon':'moon','pl':'perl','pm':'perl',\
		'py3tb':'py3tb','py':'python', 'pyw':'python', 'sc':'python', 'SConstruct':'python', \
		'SConscript':'python', 'tac':'python', 'sage':'python','pytb':'pytb','tcl':'tcl',\
		'rb':'ruby', 'rbw':'ruby', 'Rakefile':'ruby', 'rake':'ruby', 'gemspec':'ruby', \
		'rbx':'ruby', 'duby':'ruby','c-objdump':'c-objdump','s':'ca65','cpp-objdump':'cpp-objdump',\
		'c++-objdump':'cpp-objdump', 'cxx-objdump':'cpp-objdump','d-objdump':'d-objdump','S':'gas',\
		'll':'llvm', 'asm':'nasm', 'ASM':'nasm','objdump':'objdump', 'adb':'ada', 'ads':'ada', \
		'ada':'ada', 'bmx':'blitzmax','c':'c', 'h':'c','idc':'c','cbl':'cobolfree', 'CBL':'cobolfree', \
		'cob':'cobol', 'COB':'cobol', 'cpy':'cobol', 'CPY':'cobol', 'cpp':'cpp', 'hpp':'cpp', 'c++':'cpp', \
		'h++':'cpp', 'cc':'cpp', 'hh':'cpp', 'cxx':'cpp', 'hxx':'cpp', 'C':'cpp', 'H':'cpp', 'cp':'cpp', 'CPP':'cpp', \
		'cu':'cuda', 'cuh':'cuda', 'pyx':'pyx', 'pxd':'pyx', 'pxi':'pyx','d':'d', 'di':'d', \
		'pas':'pascal','dylan':'dylan', 'dyl':'dylan', 'intr':'dylan', 'lid':'dylan-lid', 'hdp':'dylan-lid', \
		'ec':'ec', 'eh':'ec', 'fan':'fan', 'flx':'felix', 'flxh':'felix', 'f':'fortran', 'f90':'fortran', \
		'F':'fortran', 'F90':'fortran', 'vert':'glsl', 'frag':'glsl', 'geo':'glsl', 'go':'go', 'def':'modula2', \
		'mod':'modula2', 'monkey':'monkey', 'nim':'nim', 'nimrod':'nim', 'mm':'objective-c,', 'hh':'objective-c', \
		'ooc':'ooc', 'prolog':'prolog', 'pro':'prolog', 'rs':'rust', 'rc':'rust', 'vala':'vala', 'vapi':'vala', \
		'smali':'smali', 'boo':'boo', 'aspx':'aspx-cs', 'asax':'aspx-cs', 'ascx':'aspx-cs', 'ashx':'aspx-cs', \
		'asmx':'aspx-cs', 'axd':'aspx-cs', 'cs':'csharp', 'fs':'fsharp', 'fsi':'fsharp', 'n':'nemerle', 'vb':'vbnet', 'bas':'vbnet', \
		'prg':'Clipper', 'PRG':'Clipper', 'cl':'cl', 'lisp':'common-lisp', 'el':'cl', 'v':'coq', 'ex':'elixir', 'exs':'elixir', \
		'erl':'erlang', 'hrl':'erlang', 'es':'erlang', 'escript':'erlang', 'erl-sh':'erl', 'hs':'haskell', \
		'kk':'koka', 'kki':'koka', 'lhs':'lhs', 'lsp':'newlisp', 'nl':'newlisp', 'ml':'ocaml', 'mli':'ocaml', \
		'mll':'ocaml', 'mly':'ocaml', 'opa':'opa', 'rkt':'racket', 'rktl':'racket', 'sml':'sml', 'sig':'sml', 'fun':'sml', \
		'scm':'scheme', 'ss':'scheme', 'sv':'sv', 'svh':'sv', 'vhdl':'vhdl','vhd':'vhdl', 'aj':'aspectj', 'ceylon':'ceylon', \
		'clj':'clojure', 'gs':'gosu', 'gsx':'gosu', 'gsp':'gosu', 'vark':'gosu','gst':'gst', 'groovy':'groovy', \
		'ik':'ioke', 'java':'java', 'kt':'kotlin', 'scala':'scala', 'xtend':'xtend', 'bug':'bugs', 'pro':'idl', \
		'jag':'jags', 'jl':'julia', 'm':'matlab', 'mu':'mupad', 'Rout':'rconsole', 'Rd':'rd', 'sci':'scilab', \
		'sce':'scilab', 'tst':'scilab', 'stan': 'stan', 'abap':'abap', 'applescript':'applescript', 'asy':'asy', \
		'au3':'autoit', 'ahk':'ahk', 'ahkl':'ahk', 'awk':'awk', 'befunge':'befunge', 'bf':'brainfuck', 'b':'brainfuck', \
		'bro':'bro', 'cf':'cfengine3', 'ecl':'ecl', 'feature':'Cucumber', 'plot':'gnuplot', 'plt':'gnuplot', \
		'gdc':'gooddata-cl', 'hy':'hybris', 'hyb':'hybris', 'Kconfig':'kconfig', 'lgt':'logtalk', 'moo':'moocode', \
		'maql':'maql', 'mo':'modelica', 'msc':'mscgen', 'nsi':'nsis', 'nsh':'nsis', 'ns2':'newspeak', 'p':'openedge', \
		'cls':'openedge', 'ps':'postscript', 'eps':'postscript', 'pov':'pov', 'proto':'protobuf', 'pp':'puppet', \
		'spec':'spec', 'r':'rebol', 'r3':'rebol', 'cw':'redcode', 'st':'smalltalk', 'snobol':'snobol', 'sp':'sp', \
		'u':'urbiscript', 'rpf':'vgl', 'g':'antlr-as', 'G':'antlr-as', 'rl':'ragel-c', 'treetop':'treetop', \
		'sh':'bash', 'ksh':'bash', 'bash':'bash', 'ebuild':'bash', 'eclass':'bash', 'bashrc':'bash', 'bashrc':'bash', \
		'sh-session':'console', 'bat':'bat', 'cmd':'bat','ps1':'powershell','tcsh':'tcsh','csh':'csh', \
		'txt':'php', 'sql':'sql', 'sqlite3-console':'sqlite3', 'cfm':'cfm', 'cfml':'cfm', 'cfc':'cfm', \
		'jsp':'jsp', 'mao':'mako', 'rhtml':'rhtml', 'tpl':'smarty', 'ssp':'ssp', 'tea':'tea', 'htaccess':'apache', \
		'cmake':'cmake', 'html':'html', 'dpatch':'dpatch', 'control':'control', 'diff':'diff', 'patch':'diff', \
		'man':'man', 'ini':'ini','cfg':'cfg', 'properties':'properties', 'pypylog':'pypylog', 'rst':'rst', 'rest':'rst', \
		'tex':'tex', 'aux':'tex', 'toc':'tex', 'vim':'vim', 'vimrc':'vim', 'exrc':'vim', 'gvimrc':'vim', 'vimrc':'vim', \
		'exrc':'vim', 'gvimrc':'vim', 'vimrc':'vim', 'gvimrc':'vim', 'yaml':'yaml', 'yml':'yaml', 'as':'as', \
		'coffee':'coffee-script', 'css':'css', 'dart':'dart', 'dtd':'dtd', 'duel':'duel', 'jbst':'duel', \
		'hx':'hx', 'htm':'html', 'xhtml':'html', 'xslt':'html', 'jade':'jade', 'js':'js', 'json':'json', \
		'lasso':'lasso', 'ls':'livescript', 'mxml':'mxml', 'j':'objective-j', 'php':'php','php3':'php', 'php4':'php', 'php5':'php', \
		'qml':'qml', 'sass':'sass', 'scaml':'scaml', 'scss':'scss', 'ts':'ts', 'xqy':'xqy', 'xquery':'xquery', 'xq':'xq', \
		'xql':'xql', 'xqm':'xqm', 'xml':'xml', 'xsl':'xml', 'rss':'xml', 'xslt':'xml', 'xsd':'xml', 'wsdl':'xml' \
	}

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

	def get_blob(self, file):
		return GitBlob(file, self)

	def get_file_type(self, file):
		#self.logger.debug(file)
		if file.rindex('.') != -1:
			pos = file.rindex('.')
			ext = file[pos+1:]
			#self.logger.debug('ext : %s' % ext)
			#self.logger.debug(self.defaultTypes)
			if ext in self.defaultTypes:
				return self.defaultTypes[ext] 
		return 'php'

	def get_breadcrumbs(self, dir):
		#self.logger.debug('dir : %s' % dir) 
		paths = dir.split('/')
		breadcrumbs = []
		oldpath = ''
		for path in paths:
			if oldpath != '':
				oldpath = oldpath + '/' + path
			else:
				oldpath = path
			breadcrumbs.append({'dir': path, 'path': oldpath})
		return breadcrumbs

		