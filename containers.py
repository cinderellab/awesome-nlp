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
    tags         = None
    sub_links    = None
    atom         = None
    pos          = None
    tag_set      = None
    constituents = None
    diagram      = None
    
    def __init__(self, sentence, normal_words):
        self.words      = sentence[0]
        self.spans      = sentence[1]
        self.p_tags     = sentence[2]
        self.tags       = sentence[3]
        self.sub_links  = sentence[4]
        self.diagram    = sentence[5].split('\n')
        self.tag_set    = []
        
        self.tagged_words = braubt_tagger.tag(normal_words)
        self.has_right_wall = ('RIGHT-WALL' in sentence[0] and False or True)
        self.has_left_wall  = ('LEFT-WALL'  in sentence[0] and False or True)
        


    def __repr__(self):
        return '<sentence %s>' % (self.words)


class iterative_container:
    def __init__(self):
        self.hash_set = {}
        self.current_number = 1
        
    def _hash(self, word):
        for char in word:
            value = ord(char) << 7
           