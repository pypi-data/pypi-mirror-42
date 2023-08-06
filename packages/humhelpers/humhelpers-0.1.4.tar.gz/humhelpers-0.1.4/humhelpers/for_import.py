"""
Functions to help importing other packages.
"""




def require (rel_or_abs_path, __file__ = None, reload = False):
	"""
	Import a file with absolute or relative path specification
	(relative to caller file (`__file__`)).

	Works similarily to `require()` in Node, but if you pass relative path to it -
	then you should also pass `__file__` variable from calling file.

	Parameters:
		. rel_or_abs_path	: relative path to package or module to be imported.
		. __file__			: path to file, from which import is launched.
							Usually you can pass `__file__` variable from calling file.

	Usage:
		import humhelpers as h
		customsockets = h.require ('/home/username/projects/difficult_project/customsockets.py')
		# or:
		customsockets = h.require ('../difficult_project/customsockets.py', __file__)
		# or:
		customsockets = h.require ('../difficult_project/customsockets.py', __file__, reload = True)
	"""
	import os.path
	import sys

	is_abs = os.path.isabs (rel_or_abs_path)

	if is_abs:
		fullpath	= rel_or_abs_path
	else:
		dir_of_file	= os.path.dirname (__file__)
		fullpath	= os.path.abspath (os.path.join (dir_of_file, rel_or_abs_path))

	path_to_module, filename	= os.path.split		(fullpath)
	module_name, ext			= os.path.splitext	(filename)

	sys.path.insert (0, path_to_module)
	module = __import__ (module_name)

	if reload:
		import imp
		imp.reload (module)

	index_of_path = sys.path.index (path_to_module)
	del sys.path [index_of_path]

	return module

