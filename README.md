My Snippets
===========

This plugin for Sublime Text 2|3 allows you to have quick access to your own commonly used code through a context menu instead of copy/pasting from files or some other coding library.

After installing you will need to edit the Preferences -> Package Settings -> My Snippets -> Settings - User file.

Within your User settings:
Include the name and path for each folder that contains your library. Note that all sub-folders will also be automatically included.

Folders and files will appear in a context menu (Right click in windows) titled "My Snippets". Selecting a menu item will result in all text from the associated file being injected into your open document in place of the cursor(s) and any selected text.

The menu items are displayed with their exact file name, minus the extension. I recommend using descriptive file naming conventions. Note that for the 2nd snippet type - see below - file extensions are not needed, but I personally use them in my snippets for syntax highlighting when writing my snippets.


2 Types of Snippets:

There are 2 types of snippets that you can use. The 1st type is sublime's snippets (.sublime-snippet) which must be contained within your Sublime folder (IE ../Sublime Text 3/) of the sublime version being used.

These are powerful snippets for quickly adding and editing code templates. For use with this plugin I recommend storing these kinds of snippets in their own subfolder under the User subfolder. Make sure to include the full file path in the user settings to this folder.
See http://docs.sublimetext.info/en/latest/reference/snippets.html for documentation on creating these snippets.

The 2nd type of snippet is simpler. Each file must contain the exact code you want used for your snippet. While the features of using this type of snippet is less robust, they can be stored and pulled from any valid file path, such as a mapped network drive to a shared code repository.

Environment Variables:
Environment variables can be used in your snippets for extra functionality.

$SELECTION - Replaced with selected text if any.

$TM_FILENAME - The name of the current file being edited including extension.

$TM_FILEPATH - The full file path of the current file being edited.
