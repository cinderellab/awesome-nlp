
#
#   Plex - Transition Maps
#
#   This version represents state sets direcly as dicts
#   for speed.
#

from copy import copy
import string
from sys import maxint
from types import TupleType

class TransitionMap:
  """
  A TransitionMap maps an input event to a set of states.
  An input event is one of: a range of character codes, 
  the empty string (representing an epsilon move), or one 
  of the special symbols BOL, EOL, EOF.
  
  For characters, this implementation compactly represents 
  the map by means of a list:
  
    [code_0, states_0, code_1, states_1, code_2, states_2,
      ..., code_n-1, states_n-1, code_n]
    
  where |code_i| is a character code, and |states_i| is a 
  set of states corresponding to characters with codes |c|
  in the range |code_i| <= |c| <= |code_i+1|.
  
  The following invariants hold:
    n >= 1
    code_0 == -maxint
    code_n == maxint
    code_i < code_i+1 for i in 0..n-1
    states_0 == states_n-1
  
  Mappings for the special events '', BOL, EOL, EOF are
  kept separately in a dictionary.
  """
  
  map = None     # The list of codes and states
  special = None # Mapping for special events
  
  def __init__(self, map = None, special = None):
    if not map:
      map = [-maxint, {}, maxint]
    if not special:
      special = {}
    self.map = map
    self.special = special
    #self.check() ###
  
  def add(self, event, new_state,
    TupleType = TupleType):
    """
    Add transition to |new_state| on |event|.
    """
    if type(event) == TupleType:
      code0, code1 = event
      i = self.split(code0)
      j = self.split(code1)
      map = self.map
      while i < j:
        map[i + 1][new_state] = 1
        i = i + 2
    else:
      self.get_special(event)[new_state] = 1

  def add_set(self, event, new_set,
    TupleType = TupleType):
    """
    Add transitions to the states in |new_set| on |event|.
    """
    if type(event) == TupleType:
      code0, code1 = event
      i = self.split(code0)
      j = self.split(code1)
      map = self.map
      while i < j:
        map[i + 1].update(new_set)
        i = i + 2
    else:
      self.get_special(event).update(new_set)
  
  def get_epsilon(self):
    """
    Return the mapping for epsilon, or None.
    """
    return self.special.get('')
  
  def items(self,
    len = len):
    """
    Return the mapping as a list of ((code1, code2), state_set) and
    (special_event, state_set) pairs.
    """
    result = []
    map = self.map
    else_set = map[1]
    i = 0
    n = len(map) - 1
    code0 = map[0]
    while i < n:
      set = map[i + 1]
      code1 = map[i + 2]
      if set or else_set:
        result.append(((code0, code1), set))
      code0 = code1
      i = i + 2
    for event, set in self.special.items():
      if set:
        result.append((event, set))
    return result
  
  # ------------------- Private methods --------------------

  def split(self, code,
    len = len, maxint = maxint):
    """
    Search the list for the position of the split point for |code|, 
    inserting a new split point if necessary. Returns index |i| such 
    that |code| == |map[i]|.
    """
    # We use a funky variation on binary search.
    map = self.map
    hi = len(map) - 1
    # Special case: code == map[-1]
    if code == maxint:
      return hi
    # General case
    lo = 0
    # loop invariant: map[lo] <= code < map[hi] and hi - lo >= 2
    while hi - lo >= 4:
      # Find midpoint truncated to even index
      mid = ((lo + hi) / 2) & ~1
      if code < map[mid]:
        hi = mid
      else:
        lo = mid
    # map[lo] <= code < map[hi] and hi - lo == 2
    if map[lo] == code:
      return lo
    else:
      map[hi:hi] = [code, map[hi - 1].copy()]
      #self.check() ###
      return hi
  
  def get_special(self, event):