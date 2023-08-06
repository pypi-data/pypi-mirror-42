"""
Functions with shortcuts to help dealing with lists.
"""




def get (collection, index):
	"""
	Returns or element from collection by index (key), or None if not found.
	"""
	try:
		return collection [index]
	except (IndexError, KeyError, TypeError):
		# TypeError: 'NoneType' object is not subscriptable - when instead of collection, None is passed
		return None




def delete (collection, key):
	"""
	Deletes element by key from collection if it's present.
	"""
	try:
		del collection [key]
	except KeyError:
		pass
