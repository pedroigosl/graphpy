from typing import List, Any, Optional, Set
from __future__ import annotations
import logging
import warnings
import time

# Log configs
log_date = str(time.strftime("%d-%m-%y_%H:%M:%S"))
log_name = f"logs/graph_{log_date}.log"
print(f"Session log started at {log_name}")

# Warning configs
warnings.simplefilter("always")

# Import warning
warning = f" This library is a work in progress and not yet functional"
warnings.warn(warning, ImportWarning)

# Time flag for warnings, errors and logs
def time_flag():
    return str(time.strftime("%d-%m-%y_%H:%M:%S"))
class Node():
    def __init__(self, id: int, value: Any = None, flag: Any = None):
        # int
        self.id = id
        # your object
        self.value = value
        #int
        self.flag = flag
        # set
        
    def __eq__(self, node):
        return isinstance(node, Node) and self.id == node.id
    
    def __hash__(self):
        return hash(self.id)
    
    def set_value(self, value):
        self.value = value
        
    def get_value(self):
        if not self.value:
            warning = f" ({time_flag()}) RuntimeWarning - get_value called, but no value declared in node #{self.id}"
            logging.warning(warning)
            warnings.warn(warning, RuntimeWarning)
        return self.value
    
    def set_id(self, id):
        self.id = id
    
    def get_id(self, id):
        return self.id
        
    def set_flag(self, flag):
        self.flag = flag
        
    def get_flag(self):
        return self.flag

"""
class Edge():
    def __init__(self, node_a: Node, node_b: Node, weight: int = 0):
        self.node_a = node_a
        self.node_b = node_b
        self.weight = weight
        
    def __eq__(self, edge):
        a_eq = self.node_a == edge.node_a
        b_eq = self.node_b == edge.node_b
        eq = isinstance(edge, Edge) and a_eq and b_eq
        return eq
    
    def __hash__(self):
        tup = (self.node_a, self.node_b)
        return hash(tup)
    
    def get_node_a(self):
        return self.node_a
    
    def get_node_b(self):
        return self.node_b
    
    def set_weight(self, weight):
        self.weight = weight
    
    def get_weight(self):
        return self.weight     
"""

class Graph():
    def __init__(self, root:Optional[Node] = None, 
                nodes: Optional[Set[Node]] = None, 
                edges: Optional[Set[Edge]] = None,
                weighted = False, 
                reflexive = False, 
                symmetric = False, 
                transitive = False):
        
        # Start logging
        logging.basicConfig(filename=log_name, filemode='w', level=logging.DEBUG)
        
        self.root = root
        self.nodes = set()
        self.edges = set()
        self.last_id = 0
        
        # Graph characteristics
        self.weighted = weighted
        
        # Relation characteristics
        self.reflexive = reflexive
        self.symmetric = symmetric
        self.transitive = transitive
        
        if nodes or edges:
            self.start_graph(nodes, edges)
        
    # Internal method    
    def start_graph(self, nodes, edges):        
        # Setting up new nodes and using flags to correlate with old ones
        if nodes:
            for id, node in enumerate(nodes):
                new_value = node.get_value
                new_flag = node.get_id()
                self.add_node(new_value, new_flag)
            
        # Setting up new edges equivalent to old ones
        if edges:
            for edge in edges:
                new_na = None
                new_nb = None
                new_weight = edge.get_weight()
                
                old_na = edge.get_node_a()
                old_nb = edge.get_node_b()
                
                if len(self.nodes) > 0:
                    for node in self.nodes:
                        flag = node.get_flag()
                        if (old_na.get_id() == flag):
                            new_na = node
                        if (old_nb.get_id() == flag):
                            new_nb = node
                
                if not new_na:
                    new_value = old_na.get_value()
                    new_flag = old_na.get_id()
                    new_na = self.add_node(new_value, new_flag)
                    
                if not new_nb:
                    new_value = old_nb.get_value()
                    new_flag = old_nb.get_id()
                    new_nb = self.add_node(new_value, new_flag)
                
                ###### ATTENTION!! need to be refactored after new adge func is created
                new_edge = Edge(new_na, new_nb, new_weight)
                self.edges.add(new_edge)
            
        
        # Cleaning flags
        if len(self.nodes) > 0:
            for node in self.nodes:
                node.set_flag(None)
            
        
    def set_relations(self, reflexive = False, symmetric = False, transitive = False):
        if  ((self.reflexive != reflexive) or 
            (self.symmetric != symmetric) or 
            (self.transitive != transitive)):
            
            self.reflexive = reflexive
            self.symmetric = symmetric
            self.transitive = transitive
            
            info = (f" ({time_flag()}) Relations' properties changed. New properties are:\n"
                    f" reflexive:     {reflexive}\n"
                    f" symmetric:     {symmetric}\n"
                    f" transitive:    {transitive}")             
            logging.info(info)
            
        else:
            info = (f" ({time_flag()}) set_relations called, but no changes made. Current relations:"
                    f" reflexive:     {reflexive}\n"
                    f" symmetric:     {symmetric}\n"
                    f" transitive:    {transitive}")
            logging.info(info)
            warning = f" ({time_flag()}) Relations already as defined"
            warnings.warn(warning, RuntimeWarning)
            
    def refactor(self):
        raise NotImplementedError
        ...
        
    #def()    
        
    def add_node(self, value: Any = None, flag: Any = None):
        new_node = Node(self.last_id, value, flag)
        self.nodes.add(new_node)
        self.last_id += 1
        return new_node

    
    """
    def add_node(self, node: Node):
        warning = f" Using function with incomplete functionalities"
        warnings.warn(warning, ResourceWarning)
        
        if node.id < 0 or not isinstance(node.id, int):
            error = f" IndexError - id #{node.id} out of bounds"
            logging.error(error)
            raise IndexError
        elif node.id <= self.last_id:
            warning = f" ResourceWarning - node id #{node.id} not new"
            warnings.warn(warning, ResourceWarning)
            logging.warning(warning)
            if node in self.nodes:
                warning = f" ResourceWarning - node id #{node.id} in use, replacing node"
                warnings.warn(warning, ResourceWarning)
                logging.warning(warning)
                self.remove_node(node.id)
                
            self.nodes.add(node)
                
        self.last_id = node.id + 1
        info = f" Node with id #{node.id} added"
        logging.info(info)
    """ 
        
    def remove_node(self, id):
        raise NotImplementedError
        ...
        
    def is_connected(self):
        raise NotImplementedError
        ...