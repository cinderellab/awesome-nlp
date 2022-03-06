
#=======================================================================
#
#   Python Lexical Analyser
#
#
#   Scanning an input stream
#
#=======================================================================

import Errors
from Regexps import BOL, EOL, EOF

class Scanner:
  """
  A Scanner is used to read tokens from a stream of characters
  using the token set specified by a Plex.Lexicon.

  Constructor:

    Scanner(lexicon, stream, name = '')

      See the docstring of the __init__ method for details.

  Methods:

    See the docstrings of the individual methods for more
    information.

    read() --> (value, text)
      Reads the next lexical token from the stream.

    position() --> (name, line, col)
      Returns the position of the last token read using the
      read() method.
    
    begin(state_name)
      Causes scanner to change state.
    
    produce(value [, text])
      Causes return of a token value to the caller of the
      Scanner.

  """

  lexicon = None        # Lexicon
  stream = None         # file-like object
  name = ''
  buffer = ''
  buf_start_pos = 0     # position in input of start of buffer