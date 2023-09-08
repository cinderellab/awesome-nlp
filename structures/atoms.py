from collections import deque

## Original: http://www.ece.arizona.edu/~denny/python_nest/graph_lib_1.0.1.html
## Modifications: Alex Toney
class Queue:
    def __init__(self):
        self.queue = deque()

    def empty(self):
        if(len(self.queue) > 0):
            return False
        else:
            return True

    def count(self):
        return len(self.queue)

    def add(self, item):
        self.queue.append(item)	

    def remove(self):
        item = self.queue[0]
        self.queue = self.queue[1:]
        return item

class Stack:
    def __init__(self):
        self.s=[]

    def empty(self):
        if(len(self.s)>0):
            return 0
        else:
            return 1

    def count(self):
        return len(self.s)

    def push(self, item):
        ts=[item]
        for i in self.s:
            ts.append(i)
        self.s=ts

    def pop(self):
        item=self.s[0]
        self.s=self.s[1:]
        return item


class GraphException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Atoms:
    ## Atoms are a basic hypergraph
    def __init__(self):
        self.next_edge