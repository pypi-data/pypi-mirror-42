"""
Tests for 'for_strings' module.
"""

import for_strings as h


def test ():
	"""
	Main function to launch all tests.
	"""
	test____replace ()


def check_result (result, expected_value, error_message):
	if not result == expected_value:
		raise ValueError (error_message)


def test____replace ():
	result1 = h.replace ('aaaa.py.py', '.py', '.js')
	result2 = h.replace ('aaaa.py.py', '.py', '.js', start_from_right = True)
	result3 = h.replace ('aaaa.py.py', '.py', '.js', amount = 1)
	result4 = h.replace ('aaaa.py.py', '.py', '.js', amount = 1, start_from_right = True)

	check_result (result1, 'aaaa.js.js', 'wrong replace 1')
	check_result (result2, 'aaaa.js.js', 'wrong replace 2')
	check_result (result3, 'aaaa.js.py', 'wrong replace 3')
	check_result (result4, 'aaaa.py.js', 'wrong replace 4')

