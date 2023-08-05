"""Useful and simple miscellaneous methods."""


def num(value):
	"""Returns a float or an int representation of value
	after defining which should be the case.

	Keyword arguments:

	a : string representation of a value or numerical value."""

	if '.' in str(value) and not str(value).endswith('.0'):
		return float(value)
	else:
		return int(value)

def isanumber(string):
	"""Returns true if the string is representing a number"""

	if string.isdigit():
		return True

	if string.startswith('-') and string[1:].isdigit():
		return True

	return False

def if_assign(condition, if_true, if_false):
	"""Method for conditional assignments.
	If condition is true returns if_true,
else returns if_false. Saves lines and ugly if-else use."""

	return if_true if condition else if_false

