#! /usr/bin/python3
"""
Tests for 'for_paths' module.
"""

import for_paths as h


def test ():
	"""
	Main function to launch all tests.
	"""
	test____return_valid_result ()


def check_result (result, expected_value, error_message):
	if not result == expected_value:
		raise ValueError (error_message)


def test____return_valid_result ():
	a = {1: {2: {3: 4, 5: 6}}}

	res1 = h.get_nested_key (a, [1, 2, 3])
	res2 = h.get_nested_key (a, [1, 2, 3, 4])
	res3 = h.get_nested_key (a, [1, 2, 3, 4], 8)

	check_result (res1, 4,    '1')
	check_result (res2, None, '2')
	check_result (res3, 8,    '3')

