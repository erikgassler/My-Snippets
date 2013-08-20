import os
import sublime
import sublime_plugin
import threading
import re
import time
from threading import Lock
from threading import Timer
lock = Lock()

threads = { "bs":None, "bt":None }

# run initial setup - called at bottom of file
def setup():
	# Load all of our package settings into a global object
	settings = sublime.load_settings('MySnippets.sublime-settings')
	subsets = sublime.load_settings('Preferences.sublime-settings')
	settings.add_on_change('changed',settingschanged)
	subsets.add_on_change('changed',settingschanged)
	buildsettings()
	buildsnippets()
	buildthreads()

def settingschanged():
	buildsettings()
	buildsnippets()
	buildthreads()

glob_settings = {}

# returns settings object built from settings file
def buildsettings():
	global glob_settings
	# load_settings must be called on main thread
	if threading.current_thread().name == 'MainThread':
		fset = sublime.load_settings('MySnippets.sublime-settings')
		fsub = sublime.load_settings('Preferences.sublime-settings')
		glob_settings['ignore'] = fset.get('ignore',[])
		for s in fsub.get("binary_file_patterns",[]):
			glob_settings['ignore'].append(s)
		for s in fsub.get("file_exclude_patterns",[]):
			glob_settings['ignore'].append(s)
		glob_settings['folder_exclude'] = fset.get('folder_exclude',[])
		glob_settings['folders'] = fset.get('folders',[])
		glob_settings['livesync'] = fset.get('livesync',True)
		glob_settings['syncewait'] = fset.get('syncewait',10 * 60 * 1000)
		glob_settings['main'] = fset.get('main','My Snippets')
		glob_settings['showext'] = fset.get('showext',True)
	return glob_settings

# this builds json content for a folder and it's files, calling upon itself for subfolders - used in tbuildsnippets
def buildfolder(path, nt, ntt = ''):
	settings = buildsettings()
	strReturn = ''
	strFolder = ''
	# Root path for Sublime Text files - .sublime-snippet files must be within this folder or a subfolder of
	ignorfyl = settings.get("ignore",[])
	ignorfld = settings.get("folder_exclude",[])
	snips = os.listdir(path)
	if '\\' in path:
		delim = '\\'
	else:
		delim = '/'
	i = 0
	f = 0
	if not path[-1] == delim:
		path += delim
	for snip in snips:

		if os.path.isdir(path + snip):
			if not snip in ignorfld:
				myid = re.sub('[^A-Za-z]+','','mysnippets' + snip)
				strTemp = buildfolder(path + snip + delim, nt + '\t\t')
				if strTemp != '':
					if f > 0:
						strFolder += ','
					strFolder += nt + ntt + '{'\
						+ nt + '\t"id": "' + myid + '",'
					strFolder += nt + '\t"caption": "' + snip + '",'
					strFolder += nt + '\t"children": ['
					strFolder += strTemp
					strFolder += nt + '\t]' + nt + '}'
					f += 1
		else:
			incfyl = True
			if snip in ignorfyl:
				incfyl = False
			else:
				for pat in ignorfyl:
					regex = pat.replace('.','\.').replace('*','.*')
					if re.match(regex, snip, flags=re.I) != None:
						incfyl = False
						break
			if incfyl:
				if i > 0:
					strReturn += ','
				ext = re.sub('.*?\.','',snip)
				if ext == 'sublime-snippet':
					com = 'mysubsnippets'
					strSnip = path + snip
				else:
					com = 'mysnippets'
					strSnip = path + snip

				cap = re.sub('\..*','',snip)
				if settings.get('showext') == True and ext != '':
					cap += ' (' + ext + ')'
				strReturn += nt + '{' + nt + '\t"caption": "' + cap + '",' + nt + '\t"command": "' + com + '",' + nt + '\t"args": {' + nt + '\t\t"snippet": "' + strSnip + '"' + nt + '\t}' + nt + '}'
				i += 1

	if strFolder != '' and strReturn != '':
		strFolder += ','

	return strFolder + strReturn

# threading class for buildsnippets
class tbuildsnippets(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		settings = buildsettings()

		# Get folders as paths to sync snippets from
		paths = settings.get("folders",[])

		# Make sure user settings file exists
		if os.path.exists(sublime.packages_path().replace('\\','/') + '/User/MySnippets.sublime-settings') == False:
			debug("Creating: " + sublime.packages_path().replace('\\','/') + '/User/MySnippets.sublime-settings')
			with open(sublime.packages_path().replace('\\','/') + '/User/MySnippets.sublime-settings', 'w') as subset:
				subset.write('{'\
					+ '\n\t// Setup other folders that contain code snippets you want to include in your library'\
					+ '\n\t// Each folder setting must have a "display" and "path" name|value pair'\
					+ '\n\t// If path is empty, or if path is not an accessible directory, then that setting will be skipped'\
					+ '\n\t// Leaving display empty will place directory contents in root menu'\
					+ '\n\t"folders":['
					+ '\n\t\t{'\
					+ '\n\t\t\t"display": "",'\
					+ '\n\t\t\t"path": ""'\
					+ '\n\t\t}'\
					+ '\n\t]'\
					+ '\n}\n')

		# Root path for This Package
		root = sublime.packages_path().replace('\\','/') + '/My Snippets/'

		# Create the context submenu based on the current library of snippets

		# build menus from settings
		if paths != None:
			strPaths = ''
			nt = '\n\t\t\t'
			for path in paths:
				if "path" in path and path['path'] != '' and os.path.isdir(path['path']):
					if path['path'][-1] == '/' and '\\' in path['path']:
						path['path'] = path['path'].rstrip('/')

					strTemp = buildfolder(path['path'],nt + '')
					if strTemp != '':
						if strPaths != '':
							strPaths += ','
						if 'display' in path and path['display'] != '':
							strPaths += nt + '{'\
									 + nt + '\t"caption": "' + path['display'] + '",'\
									 + nt + '\t"children": ['
							strPaths += strTemp.replace('\n','\n\t\t')
							strPaths += nt + '\t]' + nt + '}'
						else:
							strPaths += strTemp

			# build file for context menu
			if strPaths != '':
				# Make sure (Packages)/My Snippets/ folder exists
				if os.path.isdir(root) == False:
					os.makedirs(root)

				try:
					title = settings.get('main','')
					with open(root + "Context.sublime-menu", 'w') as submen:
						submen.write('[')
						if title != '':
							submen.write('\n\t{\n\t\t"id":"' + title + '",\n\t\t"caption":"' + title + '",\n\t\t"children":[')
						else:
							strPaths = strPaths.replace('\n\t\t\t','\n\t')
						submen.write(strPaths.replace('\\','\\\\'))
						if title != '':
							submen.write("\n\t\t]\n\t}")
						submen.write('\n]\n')

					debug('Snippets Menu Built.')
				except:
					debug('Failed opening or writing to Context file.')
					sublime.set_timeout(lambda: buildsnippets(), 10000)
			else:
				debug('No snippets found: Context Menu not created.')
		else:
			debug('No "folders" found in settings.')
		return

def buildthreads():
	global threads
	bd = threadbuilder(0)
	threads['bd'] = bd.name
	debug('Starting buildthreads:' + bd.name)
	bd.start()

# this function handles building the My Snippets context menu
def buildsnippets():
	global threads
	if threads.get('bs',None) == None or threads['bs'].is_alive() == False:
		threads['bs'] = tbuildsnippets()
		threads['bs'].start()

# This command launches snippet
class mysubsnippetsCommand(sublime_plugin.TextCommand):
	def run(self, edit, **args):
		# Make sure file actually exists before trying to run snippet
		if 'snippet' in args and os.path.isfile(args['snippet']):
			debug("Requested Snippet(1): " + args['snippet'])
			with open(args['snippet']) as snippet:
				txt = ''
				for line in snippet:
					txt += line
				txt = re.sub('.*\<\!\[CDATA\[|\]\]\>.*','',txt,flags=re.S|re.I)
				debug("Running Snippet: " + txt)
				self.view.run_command('insert_snippet', {"contents": txt})

		else:
			sublime.error_message("File not found, has it been deleted?")
			buildsnippets()

# This command gets run from the context menu selections
class mysnippetsCommand(sublime_plugin.TextCommand):
	def run(self, edit, **args):
		# Open the file dicated by args['snippet']
		if 'snippet' in args and os.path.isfile(args['snippet']):
			debug("Requested Snippet(2): " + args['snippet'])
			with open(args['snippet']) as snippet:
				txt = ''
				for line in snippet:
					txt += line
				debug("Running Snippet: " + txt)
				self.view.run_command('insert_snippet', {"contents": txt})

		else:
			sublime.error_message("File not found, has it been deleted?")
			buildsnippets()

# This async threading function runs the update for building the context menu
class threadbuilder(threading.Thread):
	def __init__(self,lastdate=0):
		threading.Thread.__init__(self)
		self.lastdate = lastdate

	def run(self):
		latestupdates(self.lastdate)

# This function gets the latest timestamp of files in the users folder paths
def latestupdates(lastdate=0):
	global threads
	if threads['bd'] == threading.current_thread().name:
		ldat = lastdate
		settings = buildsettings()

		# Get folders as paths to sync snippets from
		paths = settings.get("folders")
		fsync = settings.get("livesync", True)
		# If setting not found default wait time to 10 minutes
		stime = settings.get("syncewait", 10 * 60 * 1000)

		chkdate = 0

		debug("Checking for updates:\n\tSync Enabled: " + str(fsync)\
			+ "\n\tSync Timeout: " + str(stime)\
			+ "\n\tLatest Update at: " + str(time.asctime(time.gmtime(ldat)))\
			+ "\n\tThread is: " + str(threading.current_thread().name)\
			+ "\n\tPaths: " + str(paths)\
			)

		if paths != None:
			try:
				for path in paths:
					if "path" in path and path['path'] != '' and os.path.isdir(path['path']):
						if '\\' in path:
							delim = '\\'
						else:
							delim = '/'
						if path['path'][-1] != delim:
							path['path'] += delim
						tmpdate = folderdate(path['path'])
						if tmpdate > 0 and (chkdate == 0 or tmpdate > chkdate):
							chkdate = tmpdate

			except:
				debug('My Snippets Error: Error checking paths for updated files.')

		if chkdate > 0 and (ldat == 0 or chkdate > ldat):
			buildsnippets()
			debug("My Snippets Updated:\n\tLast Update: " + str(time.asctime(time.gmtime(ldat)))\
				+ '\n\tCurrent Time: ' + str(time.asctime(time.gmtime(chkdate))))
			ldat = chkdate

		if fsync == True and stime > 1000:
			time.sleep(stime * 0.001)
			latestupdates(ldat)
			return
	return

# this function checks for the latest date of all files within - calls itself for subfolders
def folderdate(path):
	chkdate = 0
	if '\\' in path:
		delim = '\\'
	else:
		delim = '/'
	if path[-1] != delim:
		path += delim
	snips = os.listdir(path)
	for snip in snips:
		if os.path.isdir(path + snip):
			tmpdate = folderdate(path + snip + delim)
			if tmpdate != '' and (chkdate == '' or tmpdate > chkdate):
				chkdate = tmpdate
		else:
			tmpdate = os.path.getmtime(path + snip)
			if tmpdate != '' and (chkdate == '' or tmpdate > chkdate):
				chkdate = tmpdate

	return chkdate

# handle output of debug text, sending to console or status bar depending on settings
def debug(debugtext):
	settings = buildsettings()
	dbg = settings.get("debug",True)
	stat = settings.get("status",True)
	if dbg == True:
		print(debugtext)
	elif stat == True:
		sublime.set_timeout(lambda: sublime.status_message(debugtext.replace('\n',' | ')), 100)

# iniiate startup - delaying 2 seconds to allow sublime to get setup
sublime.set_timeout(lambda: setup(), 4000)
