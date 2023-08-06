"""
Functions to help working with pathes.
If os.path is not enough.
"""




def make_path_abs_if_rel (path, base_dir):
	"""
	Makes path absolute (according to passed base dir) if it's relative.
	"""
	import os.path

	is_abs = os.path.isabs (path)
	if is_abs:
		return path

	abs_path = os.path.abspath (os.path.join (base_dir, path))
	return abs_path


def get_nested_key (dict_obj, keys = [], default_value = None):
	"""
	a = {1: {2: {3: 4, 5: 6}}}
	get_nested_key (a, [1, 2, 3])       == 4
	get_nested_key (a, [1, 2, 3, 4])    == None
	get_nested_key (a, [1, 2, 3, 4], 8) == 8
	"""
	value = default_value

	err_wrong_key                     = KeyError
	error_unable_get_keys_from_object = TypeError
	possible_errors                   = (err_wrong_key, error_unable_get_keys_from_object)

	try:
		last_nested_dict = dict_obj
		for key in keys:
			last_nested_dict = last_nested_dict [key]
		value = last_nested_dict
	except possible_errors:
		return default_value

	return value
