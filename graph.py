from typing import List, Set, Tuple, Any, Optional
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
    def __init__(self, id: int, data: Any = None, flag: Any = None, edges: Set[Edge] = None):
        # int
        self._id = id
        # your object
        self.data = data
        #int
        self.flag = flag
        # set
        self.edges = edges
        
    def __eq__(self, node):
        return isinstance(node, Node) and self.id == node.id
    
    def __hash__(self):
        return hash(self.id)
    
    @property
    def id(self):
        return self._id
    
    def get_id(self):
        return self._id
    
    def set_data(self, data: Any) -> Any:
        self.data = data
        return self.data
        
    def get_data(self):
        if not self.data:
            warning = f" ({time_flag()}) RuntimeWarning - get_data called, but no data declared in node #{self.id}"
            logging.warning(warning)
            warnings.warn(warning, RuntimeWarning)
        return self.data
        
    def set_flag(self, flag: Any):
        self.flag = flag
        return self.flag
        
    def get_flag(self):
        return self.flag
    
    def set_edges(self):
        ...


class Edge():
    def __init__(self, node: Node, weight: int = 0):
        self.node = node
        self.weight = weight
        
    def __eq__(self, edge):
        eq = isinstance(edge, Edge) and self.node == edge.node
        return eq
    
    def __hash__(self):
        return hash(self.node)
    
    def set_weight(self, weight):
        self.weight = weight
    
    def get_weight(self):
        return self.weight     


class Graph():
    # Start logging
    logging.basicConfig(filename=log_name, filemode='w', level=logging.DEBUG)
    
    # Each graph has a specific class id for logging purposes
    graph_id = -1
    
    check_graph_at_initialization = True
    
    def __init__(self, root: Optional[int] = None, 
                nodes: Optional[Set[Node]] = None, 
                weighted = False, 
                reflexive = False, 
                symmetric = False, 
                transitive = False):
    
        # Sets graph id
        self.graph_id = self.set_graph_id()
        
        self.root = root
        self.nodes = set()
        self.last_id = 0
        
        # Graph characteristics
        self.weighted = weighted
        
        # Relation characteristics
        self.reflexive = reflexive
        self.symmetric = symmetric
        self.transitive = transitive
        
        # Check whether a graph is valid
        if self.check_graph_at_initialization:
            if not self.is_valid(self):
                # MUST KILL GRAPH OR TRIGGER ERROR
                ...
            
    def __del__(self):
        # Ensures the id class attribute doubles as graph count
        self.del_graph_id()
    
    @classmethod        
    def set_graph_id(cls):
        cls.graph_id += 1
        return cls.graph_id - 1
    
    @classmethod
    def del_graph_id(cls):
        cls.graph_id -= 1
        
    # Internal method
    @staticmethod    
    def is_valid(graph: Graph):
        
        root = graph.root
        nodes = graph.nodes
        
        last_id = graph.last_id
        
        weighted = graph.weighted
        if not isinstance(weighted, bool):
            return False
        reflexive = graph.reflexive
        if not isinstance(reflexive, bool):
            return False
        symmetric = graph.symmetric
        if not isinstance(symmetric, bool):
            return False
        transitive = graph.transitive
        if not isinstance(transitive, bool):
            return False
        
        if not nodes:
            if root:
                # broken graph, has root, but no node
                return False
            # Empty graph is a valid graph  
            return True
        
        if root:
            if not isinstance(root, int):
                return False
            root_node = Node(root)
            try:
                if not root_node in nodes:
                    # Broken graph, root isn't one of its nodes
                    return False
            except:
                #node typing wrong
                return False
        if not isinstance(nodes, set):
            return False
        
        for id, node in enumerate(nodes):
            is_node = isinstance(node, Node)
            id_int = isinstance(node.id, int)
            id_positive = node.id >= 0
            id_range = node.id < last_id
            if not (is_node and
                    id_int and
                    id_positive and
                    id_range):
                return False
            
            if node.edges:
                if not isinstance(node.edges, set):
                    return False
                for edge in node.edges:
                    if not isinstance(edge, Edge):
                        return False
                    if edge.node not in nodes:
                        return False
                    if not isinstance(edge.weight, int):
                        return False
            
                
    
            
            
    @classmethod    
    def check_node(cls, node: Node):
        ...
        
        """     
        # Setting up new nodes and using flags to correlate with old ones
        for id, node in enumerate(nodes):
            
            is_int = isinstance(node.id, int)
            is_positive = node.id >= 0
            if not is_int or not is_positive:
                
                #invalid node
                break  
            
            aux_node =           
            for edge in node.edges:
                if node.
                
            new_data = node.get_data
            new_flag = node.get_id()
            self.add_node(new_data, new_flag)
        """
                
    def build_graph(self):
        raise NotImplementedError
        ...
        
    # Shouldn't be needed. Maybe to delete unused id
    def refactor(self):
        raise NotImplementedError
        ...
    
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
            
        
    #def()    
        
    def add_node(self, data: Any = None, flag: Any = None):
        new_node = Node(self.last_id, data, flag)
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
        
    def get_nodes(self):
        raise NotImplementedError
        ...
        
    def copy():
        raise NotImplementedError
        ...