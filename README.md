# My-Snippets

This plugin for Sublime Text 2|3 allows you to have quick access to your own commonly used code through a context menu instead of copy/pasting from files or some other coding library.

## Installation

Available via [Package Control](https://sublime.wbond.net/installation) - search for "My Snippets".

## Configuration

After installing you will need to edit the Preferences -> Package Settings -> My Snippets -> Settings - User file. Include the name and absolute path for each folder that contains your snippets library.
Note that all sub-folders will also be automatically included.
Note that folders will not appear in menu if they are empty.
Note that relative paths are relative from Sublime folder inside the settings and packages are contained. See example below for example of Windows paths.
Ex:

	"folders":[
		{//Example of including library with a full path
			"display": "Example1",
			"path": "C:/Users/Me/AppData/Roaming/Sublime Text 3/Packages/User/JSSnippets/"
		},
		{//Example of including same library from a relative path
			"display": "Example2",//Snippets and subfolders will appear directly in the main snippets folder or root context menu.
			"path": "./Packages/User/JSSnippets/"
		}

If you want all your snippets directly under "My Snippets" in the context menu, leave the `display` value as an empty string. Ex: `"display": "",`

## Most Recent Update:

0.16.1: Added ability for users to have relative paths for their library paths.

[Older updates](#version-history)

## Usage:

Folders and files will appear in a context menu (Right click in windows) titled "My Snippets". Selecting a menu item will result in all text from the associated file being injected into your open document at the cursor(s) and replacing any selected text.

The menu items are displayed with their exact file name, minus the extension. I recommend using descriptive file naming conventions. Note that for the 2nd snippet type - see below - file extensions are not needed, but I personally use them in my snippets for syntax highlighting when writing my snippets.

Snippets to be used in the context menu can have any extension.

For normal sublime snippets - with extension .sublime-snippet - follow normal rules for setting up the file, as detailed in the docs reference:
See http://docs.sublimetext.info/en/latest/reference/snippets.html for documentation on creating these snippets.

My Snippets also allows snippets with any other file extension. When using file extensions other than .sublime-snippet include only your exact snippet content in the file. Do not wrap your snippet with any XML. You can however use all environment variables - IE. $SELECTION, $1, etc - that you would use in a normal snippet.

My Snippets automatically excludes files from "binary_file_patterns" and "file_exclude_patterns" found in your Preferences.sublime-settings settings.

## Key Binding:

By default shift+enter is a key binding setup for initiating snippets based on tags.

To set a tag for a snippet include the tag value inside square brackets in the file name for the snippet - such as "My Snippet [mysnip].html".

Then in your code you can type in your tag followed by the key bind command (shift+enter) to replace the tag with the linked snippet.

If multiple snippets are loaded with the same tag only the last one loaded can use the key bind feature.

Please note that the text that is looked up as the tag will be deleted, regardless of whether or not a valid key was found from the tag.

Also note that if multiple cursor locations exist, all cursors will be scanned for tags and only the last valid snippet will be used; And any tags found preceding any of the cursors will be deleted, even if they were not the tag used for the loaded snippet.

## <a id="version-history"></a> Version Update History:

0.16.1: Added ability for users to have relative paths for their library paths.

0.15.1: Fixed ST2 bug when initiating snippet through a tag command.

0.15.0: Added ability to setup tab-like key bindings to initiate snippets.

0.14.3: Fixed missing loading of debug setting.

0.14.2: Whoops, forgot to include the updated settings file.

0.14.1: Fix bug from invalid character.

0.14.0: Add option for displaying "My Snippets" menu in top menu.

0.13.0: Add option for display file extensions in menu

0.12.0: Added option for main context menu folder's display

0.11.5: Reworked threading to fix ST2 issues

0.11.4: Fixed threading bug found in Sublime Text 2
