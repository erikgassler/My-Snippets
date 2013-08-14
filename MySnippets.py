import os
import sublime
import sublime_plugin
import threading
import re

def setup():
	# Load all of our package settings into a global object
	settings = sublime.load_settings('MySnippets.sublime-settings')
	settings.add_on_change('changed',buildsnippets)
	# set 0 to make sure we always start out with an update
	latestupdates(0)

def buildfolder(path, nt):
	strReturn = ''
	strFolder = ''
	snips = os.listdir(path)
	i = 0
	f = 0
	for snip in snips:
		if os.path.isdir(path + snip):
			strTemp = buildfolder(path + snip + '/', nt + '\t\t')
			if strTemp != '':
				if f > 0:
					strFolder += ','
				strFolder += nt + '{' + nt + '\t"caption": "' + snip + '",' + nt + '\t"children": ['
				strFolder += strTemp
				strFolder += nt + '\t]' + nt + '}'
				f += 1
		else:
			if i > 0:
				strReturn += ','
			cap = re.sub('\..*','',snip)
			strReturn += nt + '{' + nt + '\t"caption": "' + cap + '",' + nt + '\t"command": "mysnippets",' + nt + '\t"args": {' + nt + '\t\t"snippet": "' + path + snip + '"' + nt + '\t}' + nt + '}'
			i += 1
	if strFolder != '' and strReturn != '':
		strFolder += ','
	return strFolder + strReturn

def buildsnippets():
	# Root path for This Package
	root = sublime.packages_path().replace('\\','/') + '/My Snippets/'

	settings = sublime.load_settings('MySnippets.sublime-settings')

	# Make sure user settings file exists
	if os.path.exists(sublime.packages_path().replace('\\','/') + '/User/MySnippets.sublime-settings') == False:
		debug("Creating: " + sublime.packages_path().replace('\\','/') + '/User/MySnippets.sublime-settings')
		subset = open(sublime.packages_path().replace('\\','/') + '/User/MySnippets.sublime-settings', 'w')
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
		subset.close()

	# Get folders as paths to sync snippets from
	paths = settings.get("folders")

	# Create the context submenu based on the current library of snippets

	# build menus from settings
	if paths != None:
		strPaths = ''
		nt = '\n\t\t\t'
		try:
			for path in paths:
				if "path" in path and path['path'] != '' and os.path.isdir(path['path']):
					strTemp = buildfolder(path['path'],nt + '\t\t')
					if strTemp != '':
						if strPaths != '':
							strPaths += ','
						if 'display' in path and path['display'] != '':
							strPaths += nt + '{'\
									 + nt + '\t"caption": "' + path['display'] + '",'\
									 + nt + '\t"children": ['
							strPaths += strTemp
							strPaths += nt + '\t]' + nt + '}'
						else:
							strPaths += strTemp
		except:
			debug('Invalid path')

		# build file for context menu
		if strPaths != '':
			# Make sure (Packages)/My Snippets/ folder exists
			if os.path.isdir(root) == False:
				os.makedirs(root)

			submen = open(root + "Context.sublime-menu", 'w')
			submen.write('[\n\t{\n\t\t"id":"my-snippets",\n\t\t"caption":"My Snippets",\n\t\t"children":[')
			submen.write(strPaths)
			submen.write("\n\t\t]\n\t}\n]\n")
			submen.close()
			debug('Snippets Menu Built.')
		else:
			debug('No snippets found: Context Menu not created.')
	else:
		debug('No "folders" found in settings.')

# This command gets run from the context menu selections
class mysnippetsCommand(sublime_plugin.TextCommand):
	def run(self, edit, **args):
		sels = self.view.sel()

		# Open the file dicated by args['snippet']
		if os.path.isfile(args['snippet']):
			with open(args['snippet']) as snippet:
				for sel in sels:

					# Determine the indent of the text
					(row, col) = self.view.rowcol(sel.begin())
					indent_region = self.view.find('^\s+', self.view.text_point(row, 0))
					if indent_region and self.view.rowcol(indent_region.begin())[0] == row:
						indent = self.view.substr(indent_region).replace('\n','')
					else:
						indent = ''
					txt = ''
					i = 0
					for line in snippet:
						txt += (indent if i > 0 else '') + line
						i += 1

					snippet.seek(0)

					self.view.replace(edit, sel, txt)
		else:
			sublime.error_message("File not found, has it been deleted?")
			buildsnippets()

class snippetbuilder(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		buildsnippets()

# This function gets the latest timestamp of files in the users folder paths
def latestupdates(lastdate):
	settings = sublime.load_settings('MySnippets.sublime-settings')
	ldat = lastdate

	# Get folders as paths to sync snippets from
	paths = settings.get("folders")
	fsync = settings.get("livesync", True)
	# If setting not found default wait time to 10 minutes
	stime = settings.get("syncewait", 10 * 60 * 1000)

	chkdate = 0

	debug("Checking for updates:\n\tSync Enabled: " + str(fsync) + "\n\tSync Timeout: " + str(stime) + "\n\tLatest Update at: " + str(ldat))

	if paths != None:
		try:
			for path in paths:
				if "path" in path and path['path'] != '' and os.path.isdir(path['path']):
					tmpdate = folderdate(path['path'])
					if tmpdate > 0 and (chkdate == 0 or tmpdate > chkdate):
						chkdate = tmpdate

		except:
			debug('My Snippets Error: Error checking paths for updated files.')


	if chkdate > 0 and (ldat == 0 or chkdate > ldat):
		buildsnippets()
		debug("My Snippets Updated:\n\tLast Update: " + str(ldat) + '\n\tCurrent Time: ' + str(chkdate))
		ldat = chkdate

	if fsync == True and stime > 0:
		sublime.set_timeout(lambda: latestupdates(ldat), stime)

def folderdate(path):
	chkdate = 0
	snips = os.listdir(path)
	for snip in snips:
		if os.path.isdir(path + snip):
			tmpdate = folderdate(path + snip + '/')
			if tmpdate != '' and (chkdate == '' or tmpdate > chkdate):
				chkdate = tmpdate
		else:
			tmpdate = os.path.getmtime(path + snip)
			if tmpdate != '' and (chkdate == '' or tmpdate > chkdate):
				chkdate = tmpdate

	return chkdate

def debug(debugtext):
	settings = sublime.load_settings('MySnippets.sublime-settings')
	dbg = settings.get("debug",True)
	if dbg == True:
		print(debugtext)


sublime.set_timeout(lambda: setup(), 2000)
