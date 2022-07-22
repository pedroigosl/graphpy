from __future__ import annotations
from typing import Dict, Any, Union, List, Tuple
import logging
import warnings
import time
import copy
import os

# Needed for type checking
from typeguard import check_type
import numpy as np
import numpy.typing as npt

# General configs
# # Raise error whenever there is a mistake, even if not critical
MERCILESS = True
# # Writes graph on log whenever there is a change
VERBOSE = False

# Log configs
log_date = str(time.strftime("%d-%m-%y %H:%M:%S"))
log_dir = "logs/"
log_name = f"graphlog {log_date}.log"
print(f"Session log started at {log_dir}{log_name}")

# Warning configs
warnings.simplefilter("always")

# Import warning
warning = f" This library is a work in progress and not yet functional"

warnings.warn(warning, ImportWarning)

# =============================================================================


# Sets up log
def start_log():
    """
    Sets up log when import is made
    """
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt="%d-%m-%y %H:%M:%S",
                        filename=f"{log_dir}{log_name}",
                        # filename=f"{log_dir}testlog.log",
                        filemode='w', level=logging.DEBUG)


# Handles errors and warning messages
def error_handler(message, type):
    """
    Handles errors and warning messages, logging everything
    When MERCILESS == True, raises an error
    Args:
        message (str): Message to be thrown
        type (str): Error type to be thrown

    Raises:
        error: Error according to type
    """
    if type == 'Runtime':
        error = RuntimeError
        warning = RuntimeWarning

    if type == 'Type':
        error = TypeError
        warning = RuntimeWarning

    if type == 'Index':
        error = IndexError
        warning = RuntimeWarning

    if type == 'Key':
        error = KeyError
        warning = RuntimeWarning

    warnings.warn(message, warning)
    logging.warning(f" <'{type}Error'> {message}")
    if MERCILESS:
        logging.error(f" <'merciless == True'> Execution stopped")
        raise error(message)
        ...


# Start classes
def start_classes():
    """
    Start essential auxiliary classes at import
    """
    Type()
    Validator()
    Node()
    Converter()
    Builder()


# =============================================================================

# Type class. Determines lib specific data types. Used in type checks
class Type():
    """
    Type handler
    Determines lib specific data types 
    Used in type checks
    Each function checks a different type
    Calls error handler whenever an inconsistency is found

    Returns:
        Bool: Whether input is of predetermined type
    """
    @classmethod
    def __init__(cls):
        cls.idtype = int
        cls.datatype = Any
        cls.flagtype = Union[int, float, str]
        cls.nodetype = Node
        cls.weighttype = Union[int, float]
        cls.nodelisttype = Dict[cls.idtype, cls.nodetype]
        cls.edgelisttype = Dict[cls.idtype, cls.weighttype]

        cls.adjmatrixtype = Union[List[List[Union[cls.weighttype, None]]],
                                  npt.NDArray[npt.NDArray[Union[cls.weighttype, None]]]]

        cls.adjlisttype = Union[List[List[Tuple[cls.idtype, cls.weighttype]]],
                                npt.NDArray[npt.NDArray[Tuple[cls.idtype, cls.weighttype]]]]

        cls.adjdicttype = Dict[cls.idtype, Union[cls.edgelisttype, None]]

    @ classmethod
    def is_id(cls, id):
        try:
            check_type("id", id, cls.idtype)
            if not id >= 0:
                error_handler("Id out of bounds", "Key")
            return True
        except:
            error_handler("Id failed type check", "Type")
            return False

    @ classmethod
    def is_data(cls, data):
        # equation = check_type("data", data, cls.datatype)
        return True

    @ classmethod
    def is_flag(cls, flag):
        try:
            check_type("flag", flag, cls.flagtype)
            return True
        except:
            error_handler("Flag failed type check", "Type")
            return False

    @ classmethod
    def is_node(cls, node):
        try:
            check_type("node", node, cls.nodetype)
            return True
        except:
            error_handler("Node failed type check", "Type")
            return False

    @ classmethod
    def is_weight(cls, weight):
        try:
            check_type("weight", weight, cls.weighttype)
            return True
        except:
            error_handler("Weight failed type check", "Type")
            return False

    @ classmethod
    def is_nodelist(cls, nodelist):
        try:
            check_type("nodelist", nodelist, cls.nodelisttype)
            for key, val in nodelist.items():
                cls.is_id(key)
                cls.is_node(val)
            return True
        except:
            error_handler("nodelist failed type check", "Type")
            return False

    @ classmethod
    def is_edgelist(cls, edgelist):
        try:
            check_type("edgelist", edgelist, cls.edgelisttype)
            for key, weight in edgelist.items():
                cls.is_id(key)
                if weight != None:
                    cls.is_weight(weight)
            return True
        except:
            error_handler("edgelist failed type check", "Type")
            return False

    @ classmethod
    def is_adjmatrix(cls, adj_mat):
        try:
            check_type("adjmatrix", adj_mat, cls.adjmatrixtype)
            mat_n = len(adj_mat)
            for line in adj_mat:
                if len(line) != mat_n:
                    error_handler("Adjmatrix not homogeneous", "Index")
            return True
        except:
            error_handler("adjmatrix failed type check", "Type")
            return False

    @ classmethod
    def is_adjlist(cls, adj_list):
        try:
            check_type("adjlist", adj_list, cls.adjlisttype)
            return True
        except:
            error_handler("adjlist failed type check", "Type")
            return False

    @ classmethod
    def is_adjdict(cls, adj_dict):
        try:
            check_type("adjdict", adj_dict, cls.adjdicttype)
            return True
        except:
            error_handler("adjdict failed type check", "Type")
            return False

# =============================================================================


# Node class. Creates node objects with data, flag and edges
class Node():
    """
    Node class
    Creates node objects with data, flag and edges
    Creates empty edges as an empty dictionary when no edge is called 
    """

    def __init__(self,
                 data: Type.datatype = None,
                 flag: Type.flagtype = None,
                 edges: Type.edgelisttype = None):
        """
        Initializes a node

        Args:
            data (Type.datatype, optional): Internal node data. Defaults to None.
            flag (Type.flagtype, optional): Node flag. Defaults to None.
            edges (Type.edgelisttype, optional): Node edges. Defaults to None.
        """
        # your object
        self.data = data
        # int, float or str. May be used for node markings
        self.flag = flag
        # Dict{id : weight}
        # Check and attribution necessary due to dictionary particulars
        if edges == None:
            edges = {}
        self.edges = edges

    def __len__(self):
        return len(self.edges)

    def set_data(self, data: Type.datatype):
        raise NotImplementedError

    def get_data(self):
        raise NotImplementedError

    def set_flag(self, flag: Type.flagtype):
        raise NotImplementedError

    def get_flag(self):
        raise NotImplementedError

    def set_edges(self):
        raise NotImplementedError

# =============================================================================


# Graph class. Handles graphs and operations on them
class Graph():
    """
    Graph class
    Handles graphs and operations on them
    Keeps object count
    Keeps class specific toggles
    """

    # Each graph has a specific class id for logging purposes
    graph_count = 0

    # Advanced settings. Only touch when sure
    # Checks new graph by default. Can be toggled for performance
    check_graph_at_initialization = True
    # Raise exception whenever a mistake is made by default, whether fatal or not

    def __init__(self, nodes: Type.nodelisttype = None):
        """
        Initializes new graph objects and call validators
        Calls class specific functions to deal with class attributes

        Args:
            nodes (Type.nodelisttype, optional): Dict {id: Node} of nodes. Defaults to None.
        """

        # Dict{id : Node}
        # Check and attribution necessary due to dictionary particulars
        if nodes == None:
            nodes = {}

        # Sets graph id
        self.graph_id = self.set_graph_id()

        # Dict{id : Node}
        self.nodes = nodes
        # Registers last used id
        self.last_id = self.size - 1

        # Check whether starter graph is valid
        if self.check_graph_at_initialization:
            Validator.is_graph(self)

        logging.info(
            f" Graph #{self.graph_id} initialized with size {self.size}")
        if VERBOSE:
            logging.info(str(Converter.to_adjdict(self)))

    def __len__(self):
        return len(self.nodes)

    @ property
    def size(self):
        return self.__len__()

    @ classmethod
    def set_graph_id(cls):
        cls.graph_count += 1
        return cls.graph_count - 1

    # Adds edge main_id -> dest_id with weight when applicable
    def add_edge(self, main_id: Type.idtype,
                 dest_id: Type.idtype,
                 weight: Type.weighttype = 0,
                 symmetric: bool = False):
        """
        Adds edge main_id -> dest_id with weight when applicable
        Adds edge symmetrically (if (a,b) in edges, then (b, a) also in edges)) when toggled

        Args:
            main_id (Type.idtype): Edge origin node. Where edge is stored
            dest_id (Type.idtype): Edge destiny node. Key on edges in node[main_id]
            weight (Type.weighttype, optional): Edge weight. Defaults to 0.
            symmetric (bool, optional): Whether edge is to be added symmetrically. Defaults to False.

        Returns:
            Bool: Whether edge was added or not
        """
        try:
            Type.is_id(main_id)
            Type.is_id(dest_id)
            Type.is_weight(weight)
            if not isinstance(symmetric, bool):
                error_handler("Symmetric is not bool", "Type")

            if not (main_id in self.nodes and dest_id in self.nodes):
                error_handler("Edge id not found", "Key")

            self.nodes[main_id].edges[dest_id] = weight
            logging.info(
                f" Edge ({main_id}->{dest_id} [{weight}]) added to graph #{self.graph_id}")
            if VERBOSE:
                logging.info(str(Converter.to_adjdict(self)))
            if symmetric:
                self.add_edge(dest_id, main_id, weight)
            return True

        except:
            error_handler("Edge's id(s) not in nodes", "Key")
            return False

    def remove_edge(self, main_id: Type.idtype, dest_id: Type.idtype, symmetric: bool = False):
        """
        Removes edge main_id -> dest_id
        Removes edge symmetrically (if (a,b) in edges, then (b, a) also in edges)) when toggled

        Args:
            main_id (Type.idtype): Edge origin node. Where edge is stored
            dest_id (Type.idtype): Edge destiny node. Key on edges in node[main_id]
            symmetric (bool, optional): Whether edge is to be removed symmetrically. Defaults to False.

        Returns:
            Bool: Whether edge was removed or not
        """
        try:
            Type.is_id(main_id)
            Type.is_id(dest_id)
            if not isinstance(symmetric, bool):
                error_handler("Symmetric is not bool", "Type")

            if not (main_id in self.nodes and dest_id in self.nodes):
                error_handler("Edge id not found", "Key")

            if symmetric:
                self.remove_edge(dest_id, main_id)

            node = self.nodes[main_id]
            if node.edges:
                if dest_id in node.edges:
                    node.edges.pop(dest_id)
                    logging.info(
                        f" Edge ({main_id}->{dest_id}) removed from graph #{self.graph_id}")
                    if VERBOSE:
                        logging.info(str(Converter.to_adjdict(self)))
                    return True
            error_handler("Edge not found", "Key")
        except:
            error_handler("Edge not found", "Key")
            return False

    # Adds nodes with data, flag and edges when applicable
    def add_node(self, data: Type.datatype = None,
                 flag: Type.flagtype = None,
                 edges: Type.edgelist = None):
        """
        Adds nodes with data, flag and edges when applicable

        Args:
            data (Type.datatype, optional): Node data. Defaults to None.
            flag (Type.flagtype, optional): Node flag. Defaults to None.
            edges (Type.edgelist, optional): Node edges. Defaults to None.

        Returns:
            Node: Returns added node object when valid
            Bool: Returns False when failed adding node
        """
        if edges == None:
            edges = {}
        new_node = Node(data, flag, edges)
        new_id = self.last_id + 1
        try:
            Validator.check_node(new_node, self, adding=True)
            self.nodes[new_id] = new_node
            self.last_id += 1

            logging.info(f" Node #{new_id} added to graph #{self.graph_id}")
            if VERBOSE:
                logging.info(str(Converter.to_adjdict(self)))

            return new_node
        except:
            error_handler("Node not valid. Was not added", "Key")
            return False

    # Removes nodes and all edges pointing to it
    def remove_node(self, id: Type.idtype):
        """
        Removes nodes and all edges pointing to it

        Args:
            id (Type.idtype): Id of the node to be removed

        Returns:
            Node: Node removed when valid
            Bool: False when failed to find node
        """
        try:
            Type.is_id(id)
            if id in self.nodes:
                popped = self.nodes.pop(id)
                if self.size > 0:
                    for node in self.nodes.values():
                        if node.edges:
                            if id in node.edges:
                                node.edges.pop(id)
                logging.info(
                    f" Node #{id} removed from graph #{self.graph_id}")
                if VERBOSE:
                    logging.info(
                        str(Converter.to_adjdict(self)))
                return popped
        except:
            error_handler("Node not found", "Key")
            return False

    def get_nodes(self):
        return self.nodes

    def copy(self):
        """
        Returns deep copy (identical copy of object and its internal objects)

        Returns:
            Graph: New graph object identical to original
        """
        return copy.deepcopy(self)

# =============================================================================


# Validators
class Validator():
    """
    Validator class. Checks graph, nodes and edges to ensure all properties are
    valid
    """

    # Checks whether graph is valid
    @ staticmethod
    def is_graph(graph: Graph):
        """
        Validates the entire graph

        Args:
            graph (Graph): Graph to be checked

        Returns:
            Bool: Whether the graph is valid or not
        """
        try:
            nodes = graph.nodes

            last_id = graph.last_id

            if not nodes:
                # Empty graph is a valid graph
                return True

            Type.is_nodelist(nodes)
            for key, node in nodes.items():
                id_range = key <= last_id
                id_checks = id_range
                if not id_checks:
                    error_handler("Id not in graph range", "Index")
                Validator.check_node(node, graph)
            return True
        except:
            error_handler("Graph failed type check", "Type")
            return False

    # Checks whether node is valid
    @ staticmethod
    def check_node(node: Type.nodetype, graph: Graph, _adding=False):
        """
        Checks whether node is valid
        Also used internally by Graph to check new nodes
        Hence the adding parameter (shouldn't be used externally)

        Args:
            node (Type.nodetype): Node to be checked
            graph (Graph): Graph to which node belongs
            _adding (bool, optional): Used internally when adding new node. Defaults to False.

        Returns:
            Bool: Whether or not node is valid
        """
        try:
            Type.is_node(node)
            check_type("graph", graph, Graph)
            Type.is_nodelist(graph.nodes)
            flag = node.flag
            if flag:
                Type.is_flag(flag)
            if node.edges != {}:
                Type.is_edgelist(node.edges)
                for key, weight in node.edges.items():
                    if key not in graph.nodes:
                        if not (_adding and key == graph.last_id + 1):
                            error_handler("Edge node not in nodes", "Key")
                    Type.is_weight(weight)
            return True
        except:
            error_handler("Node failed type check", "Type")
            return False

# =============================================================================


# Graph builders
class Builder():
    """
    Graph building methods
    """

    # Advanced method to build graph from adjacency matrix
    @ staticmethod
    def adj_matrix(adj_mat: Type.adjmatrixtype,
                   obj_list: List[Any] = None):
        """
        Advanced method to build graph from adjacency matrix

        Args:
            adj_mat (Type.adjmatrixtype): Source adjacency matrix
            obj_list (List[Any], optional): Object list to go on 'node.data'. Defaults to None.

        Returns:
            Graph: Built and checked graph
            Bool: False if failed building graph
        """
        nodes = {}

        try:
            Type.is_adjmatrix(adj_mat)
            for i, line in enumerate(adj_mat):
                if obj_list:
                    nodes[i] = Node(data=obj_list[i])
                else:
                    nodes[i] = Node()
                for j, weight in enumerate(line):
                    if weight != None:
                        nodes[i].edges[j] = weight

            logging.info(f" Adjacency matrix is valid. Graph is being built")
            return Graph(nodes=nodes)

        except:
            error_handler("Broken adjacency matrix", "Runtime")
            return False

    # Advanced method to build graph from adjacency list
    @ staticmethod
    def adj_list(adj_list: Type.adjlisttype,
                 obj_list: List[Any] = None):
        """
        Advanced method to build graph from adjacency list

        Args:
            adj_list (Type.adjlisttype): Source adjacency list
            obj_list (List[Any], optional): Object list to go on 'node.data'. Defaults to None.

        Returns:
            Graph: Built and checked graph
            Bool: False if failed building graph
        """
        nodes = {}

        try:
            Type.is_adjlist(adj_list)
            for i, edgelist in enumerate(adj_list):
                if obj_list:
                    nodes[i] = Node(data=obj_list[i])
                else:
                    nodes[i] = Node()
                for j, weight in edgelist:
                    nodes[i].edges[j] = weight

            logging.info(f" Adjacency list is valid. Graph is being built")
            return Graph(nodes=nodes)
        except:
            error_handler("Broken adjacency list", "Runtime")
            return False

    # Advanced method to build graph from adjacency dictionary
    @ staticmethod
    def adj_dict(adj_dict: Type.adjdicttype,
                 obj_list: List[Any] = None):
        """
        Advanced method to build graph from adjacency dictionary

        Args:
            adj_dict (Type.adjdicttype): Source adjacency dictionary
            obj_list (List[Any], optional): Object list to go on 'node.data'. Defaults to None.

        Returns:
            Graph: Built and checked graph
            Bool: False if failed building graph
        """
        nodes = {}

        try:
            Type.is_adjdict(adj_dict)
            for i, edgelist in adj_dict.items():
                if obj_list:
                    nodes[i] = Node(data=obj_list[i])
                else:
                    nodes[i] = Node(edges=edgelist)
            logging.info(
                f" Adjacency dictionary is valid. Graph is being built")
            return Graph(nodes=nodes)
        except:
            error_handler("Broken adjacency dictionary", "Runtime")
            return False

    # Refactors graph to clean "waste"
    @ staticmethod
    def refactor(graph: Graph):
        """
        Refactors graph to clean "waste"
        Clears node flags
        Removes unused node ids

        Args:
            graph (Graph): Graph to be cleaned

        Returns:
            Graph: Refactored graph
            Bool: False when failed to refactor
        """
        try:
            Validator.is_graph(graph)
            new_nodes = {}
            for new_id, node in enumerate(graph.nodes.values()):
                node.flag = new_id
                new_nodes[new_id] = Node(data=node.data)

            for new_id, node in enumerate(graph.nodes.values()):
                for eid, weight in node.edges.items():
                    new_nodes[new_id].edges[graph.nodes[eid].flag] = weight

            refac = Graph(new_nodes)
            return refac
        except:
            error_handler("Broken graph in refactor", "Runtime")
            return False

# =============================================================================


# Converts graphs to native data types
class Converter():
    """
    Converts graphs to native data types for printing, exporting and all
    """
    # Returns an equivalent adjacency matrix and node data list
    @ staticmethod
    def to_adjmatrix(graph: Graph, get_nodes=False):
        """
        Returns an equivalent adjacency matrix and node data list
        Args:
            graph (Graph): Graph to be converted
            get_nodes (bool, optional): Whether to get data list from 'node.data' . Defaults to False.

        Returns:
            adjmatrixtype, list: Resulting adjacency matrix and data list
            adjmatrixtype: Resulting adjacency matrix
            Bool: False when failed to convert
        """
        try:
            Validator.is_graph(graph)
            if not isinstance(get_nodes, bool):
                error_handler("get_nodes is not bool", "Type")
            adjmatrix = [[None for j in range(0, graph.last_id + 1)]
                         for i in range(0, graph.last_id + 1)]
            nodes = [None for i in range(0, graph.last_id + 1)]
            for main_id, node in graph.nodes.items():
                nodes[main_id] = node.data
                for dest_id, weight in node.edges.items():
                    adjmatrix[main_id][dest_id] = weight

            if get_nodes:
                return adjmatrix, nodes
            return adjmatrix

        except:
            error_handler("Wrong parameters in converter", "Runtime")
            return False

    @ staticmethod
    def to_adjlist(graph: Graph, get_nodes=False):
        """
        Returns an equivalent adjacency list and node data list
        Edges returned as tuples due to duck typing
        Args:
            graph (Graph): Graph to be converted
            get_nodes (bool, optional): Whether to get data list from 'node.data' . Defaults to False.

        Returns:
            adjlisttype, list: Resulting adjacency list and data list
            adjlisttype: Resulting adjacency list
            Bool: False when failed to convert
        """
        try:
            Validator.is_graph(graph)
            if not isinstance(get_nodes, bool):
                error_handler("get_nodes is not bool", "Type")

            adjlist = [None for i in range(0, graph.last_id + 1)]
            nodes = [None for i in range(0, graph.last_id + 1)]
            for id, node in graph.nodes.items():
                nodes[id] = node.data
                adjlist[id] = list(node.edges.items())
            if get_nodes:
                return adjlist, nodes
            return adjlist

        except:
            error_handler("Wrong parameters in converter", "Runtime")
            return False

    @ staticmethod
    def to_adjdict(graph: Graph, get_nodes=False):
        """
        Returns an equivalent adjacency dict and node data list
        Args:
            graph (Graph): Graph to be converted
            get_nodes (bool, optional): Whether to get data list from 'node.data' . Defaults to False.

        Returns:
            adjdicttype, list: Resulting adjacency dict and data list
            adjdicttype: Resulting adjacency dict
            Bool: False when failed to convert
        """
        try:
            Validator.is_graph(graph)
            if not isinstance(get_nodes, bool):
                error_handler("get_nodes is not bool", "Type")
            adjdict = {}
            nodes = [None for i in range(0, graph.last_id + 1)]
            for id, node in graph.nodes.items():
                nodes[id] = node.data
                adjdict[id] = node.edges
            if get_nodes:
                return adjdict, nodes
            return adjdict

        except:
            error_handler("Wrong parameters in converter", "Runtime")
            return False


# =============================================================================
# Starters
start_log()
start_classes()
