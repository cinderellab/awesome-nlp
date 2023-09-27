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
        self.next_edge_id = 0
        self.nodes = {}
        self.edges = {}
        self.hidden_edges = {}
        self.hidden_nodes = {}


    #--Performs a copy of the graph, G, into self.
    #--hidden edges and hidden nodes are not copied.
    #--node_id's remain consistent across self and G, 
    #--however edge_id's do not remain consistent.
    #--Need to implement copy operator on node_data
    #--and edge data.
    def copy(self, G):
        #--Blank self.
        self.nodes = {}
        self.edges = {}
        self.hidden_edges = {}
        self.hidden_nodes = {}
        self.next_edge_id = 0
        #--Copy nodes.
        G_node_list = G.node_list()
        for G_node in G_node_list:
            self.add_node(G_node,G.node_data(G_node))
        #--Copy edges.
        for G_node in G_node_list:
            out_edges = G.out_arcs(G_node)
            for edge in out_edges:
                tail_id=G.tail(edge)
                self.add_edge(G_node, tail_id, G.edge_data(edge))

    #--Creates a new node with id node_id.  Arbitrary data can be attached
    #--to the node via the node_data parameter.
    def add_node(self, node_id, node_data=None, ignore_dupes=False):
        if (not self.nodes.has_key(node_id)) and (not self.hidden_nodes.has_key(node_id)):
            self.nodes[node_id]=([],[],node_data)
        else:
            if not ignore_dupes:
                raise GraphException('Duplicate Node: %s', node_id)

    #--Deletes the node and all in and out arcs.
    def delete_node(self, node_id):
        #--Remove fanin connections.
        in_edges=self.in_arcs(node_id)
        for edge in in_edges:
            self.delete_edge(edge)
        #--Remove fanout connections.
        out_edges = self.out_arcs(node_id)
        for edge in out_edges:
            self.delete_edge(edge)
        #--Delete node.
        del self.nodes[node_id]

    #--Delets the edge.
    def delete_edge(self, edge_id):
        head_id = self.head(edge_id)
        tail_id = self.tail(edge_id)
        head_data = map(None, self.nodes[head_id])
        tail_data = map(None, self.nodes[tail_id])
        head_data[1].remove(edge_id)
        tail_data[0].remove(edge_id)
        del self.edges[edge_id]

    #--Adds an edge (head_id, tail_id).
    #--Arbitrary data can be attached to the edge via edge_data
    def add_edge(self, head_id, tail_id, edge_data=None):
        edge_id = self.next_edge_id
        self.next_edge_id = self.next_edge_id + 1
        self.edges[edge_id] = (head_id, tail_id, edge_data)
        try:
            mapped_head_data = map(None, self.nodes[head_id])
            mapped_head_data[1].append(edge_id)
            mapped_tail_data = map(None, self.nodes[tail_id])
            mapped_tail_data[0].append(edge_id)
        except Exception, E:
            raise GraphException('Exception %s nodes: %s' % (E, self.nodes))
        
        return edge_id

    #--Removes the edge from the normal graph, but does not delete
    #--its information.  The edge is held in a separate structure
    #--and can be unhidden at some later time.
    def hide_edge(self, edge_id):
        self.hidden_edges[edge_id]=self.edges[edge_id]
        ed=map(None, self.edges[edge_id])
        head_id=ed[0]
        tail_id=ed[1]
        hd=map(None, self.nodes[head_id])
        td=map(None, self.nodes[tail_id])
        hd[1].remove(edge_id)
        td[0].remove(edge_id)
        del self.edges[edge_id]

    #--Similar to above.
    #--Stores a tuple of the node data, and the edges that are incident to and from
    #--the node.  It also hides the incident edges.
    def hide_node(self, node_id):	    
        degree_list = self.arc_list(node_id)
        self.hidden_nodes[node_id] = (self.nodes[node_id],degree_list)
        for edge in degree_list:
            self.hide_edge(edge)
        del self.nodes[node_id]

    #--Restores a previously hidden edge back into the graph.
    def restore_edge(self, edge_id):
        self.edges[edge_id] = self.hidden_edges[edge_id]
        ed = map(None,self.hidden_edges[edge_id])
        head_id = ed[0]
        tail_id = ed[1]
        hd=map(None,self.nodes[head_id])
        td=map(None,self.nodes[tail_id])
        hd[1].append(edge_id)
        td[0].append(edge_id)
        del self.hidden_edges[edge_id]

    #--Restores all hidden edges.
    def restore_all_edges(self):
        hidden_edge_list=self.hidden_edges.keys()
        for edge in hidden_edge_list:
            self.restore_edge(edge)

    #--Restores a previously hidden node back into the graph
    #--and restores all of the hidden incident edges, too.	
    def restore_node(self, node_id):
        hidden_node_data=map(None,self.hidden_nodes[node_id])
        self.nodes[node_id]=hidden_node_data[0]
        degree_list=hidden_node_data[1]
        for edge in degree_list:
            self.restore_edge(edge)
        del self.hidden_nodes[node_id]

    #--Restores all hidden nodes.
    def restore_all_nodes(self):
        hidden_node_list=self.nodes.keys()
        for node in hidden_node_list:
            self.nodes[node]=self.hidden_nodes[node]
  