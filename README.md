0.14.3: Fixed missing loading of debug setting.

This plugin for Sublime Text 2|3 allows you to have quick access to your own commonly used code through a context menu instead of copy/pasting from files or some other coding library.

After installing you will need to edit the Preferences -> Package Settings -> My Snippets -> Settings - User file.

Within your User settings:
Include the name and path for each folder that contains your library. Note that all sub-folders will also be automatically included.

Folders and files will appear in a context menu (Right click in windows) titled "My Snippets". Selecting a menu item will result in all text from the associated file being injected into your open document in place of the cursor(s) and any selected text.

The menu items are displayed with their exact file name, minus the extension. I recommend using descriptive file naming conventions. Note that for the 2nd snippet type - see below - file extensions are not needed, but I personally use them in my snippets for syntax highlighting when writing my snippets.

Snippets to be used in the context menu can have any extension.

For normal sublime snippets - with extension .sublime-snippet - follow normal rules for setting up the file, as detailed in the docs reference:
See http://docs.sublimetext.info/en/latest/reference/snippets.html for documentation on creating these snippets.

My Snippets also allows snippets with any other file extension. When using file extensions other than .sublime-snippet include only your exact snippet content in the file. Do not wrap your snippet with any XML. You can however use all environment variables - IE. $SELECTION, $1, etc - that you would use in a normal snippet.

My Snippets automatically excludes files from "binary_file_patterns" and "file_exclude_patterns" found in your Preferences.sublime-settings settings.

Version Update History:

0.14.3: Fixed missing loading of debug setting.

0.14.2: Whoops, forgot to include the updated settings file.

0.14.1: Fix bug from invalid character.

0.14.0: Add option for displaying "My Snippets" menu in top menu.

0.13.0: Add option for display file extensions in menu

0.12.0: Added option for main context menu folder's display

0.11.5: Reworked threading to fix ST2 issues

0.11.4: Fixed threading bug found in Sublime Text 2
