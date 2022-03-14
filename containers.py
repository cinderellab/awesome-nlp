from tagger import braubt_tagger

class tag:
    left  = None
    right = None
    tag   = None
    
    def __init__(self, left, right, tag):
        self.left  = left
        self.right = right
        self.tag   = tag

class sentence:
    has_left_wall  = None
    has_right_wall = None
    words        = None
    spans        = None
    p_tags       = None
    ta