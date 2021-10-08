#=======================================================================
#
#	 Python Lexical Analyser
#
#	 Regular Expressions
#
#=======================================================================

import array
import string
import types
from sys import maxint

import Errors

#
#	 Constants
#

BOL = 'bol'
EOL = 'eol'
EOF = 'eof'

nl_code = ord('\n')

#
#	 Helper functions
#

def chars_to_ranges(s):
	"""
	Return a list of character codes consisting of pairs
	[code1a, code1b, code2a, code2b,...] which cover all
	the characters in |s|.
	"""
	char_list = list(s)
	char_list.sort()
	i = 0
	n = len(char_list)
	result = []
	while i < n:
		code1 = ord(char_list[i])
		code2 = code1 + 1
		i = i + 1
		while i < n and code2 >= ord(char_list[i]):
			code2 = code2 + 1
			i = i + 1
		result.append(code1)
		result.append(code2)
	return result

def uppercase_range(code1, code2):
	"""
	If the range of characters from code1 to code2-1 includes any
	lower case letters, return the corresponding upper case range.
	"""
	code3 = max(code1, ord('a'))
	code4 = min(code2, ord('z') + 1)
	if code3 < code4:
		d = ord('A') - ord('a')
		return (code3 + d, code4 + d)
	else:
		return None

def lowercase_range(c