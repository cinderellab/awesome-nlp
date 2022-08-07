
# -*- coding: utf-8 -*-
from collections import deque
import os
import sys
import pprint
import inspect
import glob
import time
import re

## pretty graphs
import networkx as nx
import matplotlib.pyplot as plt
import pylab

import lg_fsm as lgFSM
import linkGrammar

from debug import *
from structures.fsm import FSM
from utils.list import list_functions
from tree_utils import Print
from semantic_rules import semantic_rules
from containers import sentence

#from nltk.sem import logic
from grammar_fsm import Semantics
from grammar_fsm import NDPDA_FSM


### RELATIONSHIPS:
###   Wd(left, x) & Ss(y, z) & (x & y) -> subject(z, y)
###   TO(x, y) -> todo(x, y)
###   O(x, y) -> object(x, y)
###   Wi(x, y) -> imperative(x, y)


class grammarFSM:
    def fsm_setup(self):
        self.fsm = FSM('INIT', [])
        self.fsm.set_default_transition(lgFSM.Error, 'INIT')
        self.fsm.add_transition_any('INIT', None, 'INIT')
        self.fsm.add_transition('RW', 'INIT', lgFSM.Root)
        self.fsm.add_transition('Xp', 'INIT', lgFSM.Period)
        self.fsm.add_transition('Wd', 'INIT', lgFSM.Declarative, 'DECL')
        self.fsm.add_transition('Wd', 'DECL', lgFSM.Declarative, 'DECL')
        self.fsm.add_transition('Ss', 'DECL', lgFSM.Subject, 'INIT')
        self.fsm.add_transition('AF', 'DECL', lgFSM.Object, 'INIT')
        
        
    def fsm_run(self, input):
        debug(input)
        return self.fsm.process_list(input)
    
class Grammar:
    def __init__(self):
        self.g = grammarFSM()
        self.g.fsm_setup()

        ### One tree for sentences
        self.s_Tree = R_Tree()
        #self.s_root = self.s_Tree.addNode(0, 0, 0)
        
        ### One for constituents
        self.c_Tree = R_Tree()
        #self.c_root = self.c_Tree.addNode(0, 0, 0)

        
        ### and one for graphing
        self.G = nx.Graph()
        self.lists = list_functions()
        self.tree_print = Print()
        
    def sentenceFSM(self, sentence):
        if sentence:
            flat = self.lists.flatten(sentence[2])
            self.g.fsm_run(flat)
        
    def sentence_to_Tree(self, sentence, cur_node=1):
        if not sentence:
            return
        for x in sentence[2]:
            self.s_Tree.insert_onto_master(cur_node, data=[x[0], x[1]])
            cur_node += 1
            
    def lastOwner(self, nodes):
        f_owners = filter(lambda x: isinstance(x, Owner), t_nodes)
        return f_owners
    
    def const_toTree(self, constituent):        
        t_currentNode = 0
        t_constituent = [(constituent, -1)]
        t_visited     = set()
        t_output      = []
        
        while t_constituent:
            ## ->[X,x,x,x,x]
            item, level  = t_constituent.pop()
            if repr(item) in t_visited:
                continue
            
            t_visited.add(repr(item))
