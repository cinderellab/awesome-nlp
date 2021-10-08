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

def lowercase_range(code1, code2):
	"""
	If the range of characters from code1 to code2-1 includes any
	upper case letters, return the corresponding lower case range.
	"""
	code3 = max(code1, ord('A'))
	code4 = min(code2, ord('Z') + 1)
	if code3 < code4:
		d = ord('a') - ord('A')
		return (code3 + d, code4 + d)
	else:
		return None

def CodeRanges(code_list):
	"""
	Given a list of codes as returned by chars_to_ranges, return
	an RE which will match a character in any of the ranges.
	"""
	re_list = []
	for i in xrange(0, len(code_list), 2):
		re_list.append(CodeRange(code_list[i], code_list[i + 1]))
	return apply(Alt, tuple(re_list))

def CodeRange(code1, code2):
	"""
	CodeRange(code1, code2) is an RE which matches any character
	with a code |c| in the range |code1| <= |c| < |code2|.
	"""
	if code1 <= nl_code < code2:
		return Alt(RawCodeRange(code1, nl_code), 
							 RawNewline, 
							 RawCodeRange(nl_code + 1, code2))
	else:
		return RawCodeRange(code1, code2)

#
#	 Abstract classes
#

class RE:
	"""RE is the base class for regular expression constructors.
	The following operators are defined on REs:

		 re1 + re2		 is an RE which matches |re1| followed by |re2|
		 re1 | re2		 is an RE which matches either |re1| or |re2|
	"""

	nullable = 1 # True if this RE can match 0 input symbols
	match_nl = 1 # True if this RE can match a string ending with '\n'
	str = None	 # Set to a string to override the class's __str__ result
	
	def build_machine(self, machine, initial_state, final_state, 
										match_bol, nocase):
		"""
		This method should add states to |machine| to implement this
		RE, starting at |initial_state| and ending at |final_state|.
		If |match_bol| is true, the RE must be able to match at the
		beginning of a line. If nocase is true, upper and lower case
		letters should be treated as equivalent.
		"""
		raise exceptions.UnimplementedMethod("%s.build_machine not implemented" % 
			self.__class__.__name__)
	
	def build_opt(self, m, initial_state, c):
		"