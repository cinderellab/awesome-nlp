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
		"""
		Given a state |s| of machine |m|, return a new state
		reachable from |s| on character |c| or epsilon.
		"""
		s = m.new_state()
		initial_state.link_to(s)
		initial_state.add_transition(c, s)
		return s

	def __add__(self, other):
		return Seq(self, other)

	def __or__(self, other):
		return Alt(self, other)

	def __str__(self):
		if self.str:
			return self.str
		else:
			return self.calc_str()

	def check_re(self, num, value):
		if not isinstance(value, RE):
			self.wrong_type(num, value, "Plex.RE instance")

	def check_string(self, num, value):
		if type(value) <> type(''):
			self.wrong_type(num, value, "string")
	
	def check_char(self, num, value):
		self.check_string(num, value)
		if len(value) <> 1:
			raise Errors.PlexValueError("Invalid value for argument %d of Plex.%s."
				"Expected a string of length 1, got: %s" % (
					num, self.__class__.__name__, repr(value)))

	def wrong_type(self, num, value, expected):
		if type(value) == types.InstanceType:
				got = "%s.%s instance" % (
					value.__class__.__module__, value.__class__.__name__)
		else:
			got = type(value).__name__
		raise Errors.PlexTypeError("Invalid type for argument %d of Plex.%s "
										"(expected %s, got %s" % (
											num, self.__class__.__name__, expected, got))
	
#
#	 Primitive RE constructors
#	 -------------------------
#
#	 These are the basic REs from which all others are built.
#

## class Char(RE):
##	 """
##	 Char(c) is an RE which matches the character |c|.
##	 """
	
##	 nullable = 0
	
##	 def __init__(self, char):
##		 self.char = char
##		 self.match_nl = char == '\n'
		
##	 def build_machine(self, m, initial_state, final_state, match_bol, nocase):
##		 c = self.char
##		 if match_bol and c <> BOL:
##			 s1 = self.build_opt(m, initial_state, BOL)
##		 else:
##			 s1 = initial_state
##		 if c == '\n' or c == EOF:
##			 s1 = self.build_opt(m, s1, EOL)
##		 if len(c) == 1:
##			 code = ord(self.char)
##			 s1.add_transition((code, code+1), final_state)
##			 if nocase and is_letter_code(code):
##				 code2 = other_case_code(code)
##				 s1.add_transition((code2, code2+1), final_state)
##		 else:
##			 s1.add_transition(c, final_state)

##	 def calc_str(self):
##		 return "Char(%s)" % repr(self.char)

def Char(c):
	"""
	Char(c) is an RE which matches the character |c|.
	"""
	if len(c) == 1:
		result = CodeRange(ord(c), ord(c) + 1)
	else:
		result = SpecialSymbol(c)
	result.str = "Char(%s)" % repr(c)
	return result

class RawCodeRange(RE):
	"""
	RawCodeRange(code1, code2) is a low-level RE which matches any character
	with a code |c| in the range |code1| <= |c| < |code2|, where the range
	does not include newline. For internal use only.
	"""
	nullable = 0
	match_nl = 0
	range = None					 # (code, code)
	uppercase_range = None # (code, code) or None
	lowercase_range = None # (code, code) or None
	
	def __init__(self, code1, code2):
		self.range = (code1, code2)
		self.uppercase_range = uppercase_range(code1, code2)
		self.lowercase_range = lowercase_range(code1, code2)
	
	def build_machine(self, m, initial_state, final_state, match_bol, nocase):
		if match_bol:
			initial_state = self.build_opt(m, initial_state, BOL)
		initial_state.add_transition(self.range, final_state)
		if nocase:
			if self.uppercase_range:
				initial_state.add_transition(self.uppercase_range, final_state)
			if self.lowercase_range:
				initial_state.add_transition(self.lowercase_range, final_state)
	
	def calc_str(self):
		return "CodeRange(%d,%d)" % (self.code1, self.code2)

class _RawNewline(RE):
	"""
	RawNewline is a low-level RE which matches a newline character.
	For internal use only.
	"""
	nullable = 0
	match_nl = 1

	def build_machine(self, m, initial_state, final_state, match_bol, nocase):
		if match_bol:
			initial_state = self.build_opt(m, initial_state, BOL)
		s = self.build_opt(m, initial_state, EOL)
		s.add_transition((nl_code, nl_code + 1), final_state)

RawNewline = _RawNewline()


class SpecialSymbol(RE):
	"""
	SpecialSymbol(sym) is an RE which matches the special input
	symbol |sym|, which is one of BOL, EOL or EOF.
	"""
	nullable = 0
	match_nl = 0
	sym = None

	def __init__(self, sym):
		self.sym = sym

	def build_machine(self, m, initial_state, final_state, match_bol, nocase):
		# Sequences 'bol bol' and 'bol eof' are impossible, so only need
		# to allow for bol if sym is eol
		if match_bol and self.sym == EOL:
			initial_state = self.build_opt(m, initial_state, BOL)
		initial_state.add_transition(self.sym, final_state)


class Seq(RE):
	"""Seq(re1, re2, re3...) is an RE which matches |re1| followed by
	|re2| followed by |re3|..."""

	def __init__(self, *re_list):
		nullable = 1
		for i in xrange(len(re_list)):
			re = re_list[i]
			self.check_re(i, re)
			nullable = nullable and re.nullable
		self.re_list = re_list
		self.nullable = nullable
		i = len(re_list)
		match_nl = 0
		while i:
			i = i - 1
	