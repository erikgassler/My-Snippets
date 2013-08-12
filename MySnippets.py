import os
import sublime
import sublime_plugin
import threading
import re

# Create the context submenu based on the current library of snippets


def buildfolder(path):
	strReturn = ''
	strFolder = ''
	snips = os.listdir(path)
	i = 0
	f = 0
	for snip in snips:
		if os.path.isdir(path + snip):
			if f > 0:
				strFolder += ','
			strFolder += '{"caption":"' + snip + '","children":['
			strFolder += buildfolder(path + snip + '/')
			strFolder += ']}'
			f += 1
		else:
			if i > 0:
				strReturn += ','
			cap = re.sub('\..*','',snip)
			strReturn += '{"caption":"' + cap + '","command":"mysnippets","args":{"snippet":"' + path + snip + '"}}'
			i += 1
	if strFolder != '' and strReturn != '':
		strFolder += ','
	return strFolder + strReturn

submen = open(sublime.packages_path() + "\My Snippets\Context.sublime-menu", 'w')
submen.write('[{"id":"my-snippets","caption":"My Snippets","children":[')
submen.write(buildfolder(sublime.packages_path().replace('\\','/') + "/My Snippets/snippets/"))
submen.write("]}]")
submen.close()


class mysnippetsCommand(sublime_plugin.TextCommand):
	def run(self, edit, **args):
		sels = self.view.sel()

		# Open the file dicated by args['snippet']
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


	def popup(self, edit, args):
		sels = self.view.sel()
		print('My Snippets Popup starting')

