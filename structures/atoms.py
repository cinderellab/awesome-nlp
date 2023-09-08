from collections import deque

## Original: http://www.ece.arizona.edu/~denny/python_nest/graph_lib_1.0.1.html
## Modifications: Alex Toney
class Queue:
    def __init__(self):
        self.queue = deque()

    def empty(self):
        if(len(self