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


# Sets up log when import is made
def start_log():
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt="%d-%m-%y %H:%M:%S",
                        filename=f"{log_dir}{log_name}",
                        filemode='w', level=logging.DEBUG)


# Starts essential auxiliary classes
def start_classes():
    Type()
    Validator()
    Node()

# =============================================================================


# Type setting
class Type():

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

    @ classmethod
    def is_id(cls, id):
        try:
            check_type("id", id, cls.idtype)
            if not id >= 0:
                raise
        except:
            logging.error(f" <'TypeError'> Id failed type check")
            raise TypeError("Id failed type check")
        return True

    @ classmethod
    def is_data(cls, data):
        # equation = check_type("data", data, cls.datatype)
        return True

    @ classmethod
    def is_flag(cls, flag):
        try:
            check_type("flag", flag, cls.flagtype)
        except:
            logging.error(f" <'TypeError'> Flag failed type check")
            raise TypeError("Flag failed type check")
        return True

    @ classmethod
    def is_node(cls, node):
        try:
            check_type("node", node, cls.nodetype)
        except:
            logging.error(f" <'TypeError'> Node failed type check")
            raise TypeError("Node failed type check")
        return True

    @ classmethod
    def is_weight(cls, weight):
        try:
            check_type("weight", weight, cls.weighttype)
        except:
            logging.error(f" <'TypeError'> Weight failed type check")
            raise TypeError("Weight failed type check")
        return True

    @ classmethod
    def is_nodelist(cls, nodelist):
        try:
            check_type("nodelist", nodelist, cls.nodelisttype)
        except:
            logging.error(f" <'TypeError'> Nodelist failed type check")
            raise TypeError("Nodelist failed type check")
        for key, val in nodelist.items():
            cls.is_id(key)
            cls.is_node(val)

        return True

    @ classmethod
    def is_edgelist(cls, edgelist):
        try:
            check_type("edgelist", edgelist, cls.edgelisttype)
        except:
            logging.error(f" <'TypeError'> Edgelist failed type check")
            raise TypeError("Edgelist failed type check")
        for key, weight in edgelist.items():
            cls.is_id(key)
            if weight != None:
                cls.is_weight(weight)
        return True

    @ classmethod
    def is_adjmatrix(cls, adj_mat):
        try:
            check_type("adjmatrix", adj_mat, cls.adjmatrixtype)
        except:
            logging.error(f" <'TypeError'> Adjmatrix failed type check")
            raise TypeError("Adjmatrix failed type check")
        mat_n = len(adj_mat)
        for i, line in enumerate(adj_mat):
            if len(line) != mat_n:
                logging.error(f" <'IndexError'> Adjmatrix not homogeneous")
                raise IndexError("Adjmatrix not homogeneous")
        return True

    @ classmethod
    def is_adjlist(cls, adj_list):
        try:
            check_type("adjlist", adj_list, cls.adjlisttype)
        except:
            logging.error(f" <'TypeError'> Adjlist failed type check")
            raise TypeError("Adjlist failed type check")
        return True

# =============================================================================


class Node():
    def __init__(self,
                 data: Type.datatype = None,
                 flag: Type.flagtype = None,
                 edges: Type.edgelisttype = None):
        # your object
        self.data = data
        # int, float or str. May be used for node markings
        self.flag = flag
        # Dict{id : weight}
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


class Graph():
    # Each graph has a specific class id for logging purposes
    graph_count = 0

    # Advanced settings. Only touch when sure
    # Checks new graph by default. Can be toggled for performance
    check_graph_at_initialization = True
    # Raise exception whenever a mistake is made by default, whether fatal or not
    merciless = True

    def __init__(self,
                 nodes: Type.nodelisttype = None):
        if nodes == None:
            nodes = {}

        # Sets graph id
        self.graph_id = self.set_graph_id()

        # Dict{id : node}
        self.nodes = nodes
        # Registers last used id
        self.last_id = self.size - 1

        # Check whether starter graph is valid
        if self.check_graph_at_initialization:
            Validator.is_graph(self)

        logging.info(
            f" Graph #{self.graph_id} initialized with size {self.size}")

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
        try:
            Type.is_id(main_id)
            Type.is_id(dest_id)
            Type.is_weight(weight)
            if not isinstance(symmetric, bool):
                logging.error(f" <'TypeError'> Symmetric is not bool")
                raise TypeError("Symmetric is not bool")

            if not (main_id in self.nodes and dest_id in self.nodes):
                raise KeyError("Edge id not found")

            self.nodes[main_id].edges[dest_id] = weight
            logging.info(
                f" Edge ({main_id}->{dest_id} [{weight}]) added to graph #{self.graph_id}")
            if symmetric:
                self.add_edge(dest_id, main_id, weight)
            return True

        except:
            warnings.warn(f" <'KeyError'> Edge not added", RuntimeWarning)
            logging.warning(f" <'KeyError'> Edge not added")
            if self.merciless:
                logging.error(f" <'merciless == True'> Execution stopped")
                raise KeyError("Edge's id(s) not in nodes")

    def remove_edge(self, main_id: Type.idtype, dest_id: Type.idtype, symmetric: bool = False):
        try:
            Type.is_id(main_id)
            Type.is_id(dest_id)
            if not isinstance(symmetric, bool):
                logging.error(f" <'TypeError'> Symmetric is not bool")
                raise TypeError("Symmetric is not bool")

            if not (main_id in self.nodes and dest_id in self.nodes):
                raise KeyError("Edge id not found")

            popped = False

            node = self.nodes[main_id]
            if node.edges:
                if dest_id in node.edges:
                    node.edges.pop(dest_id)
                    logging.info(
                        f" Edge ({main_id}->{dest_id}) removed from graph #{self.graph_id}")
                    popped = True

            if symmetric:
                if self.remove_edge(dest_id, main_id):
                    popped = True

            if not popped:
                raise KeyError("Edge not found")
            return True
        except:
            warnings.warn(f" <'KeyError'> Edge not found", RuntimeWarning)
            logging.warning(f" <'KeyError'> Edge not found")
            if self.merciless:
                logging.error(f" <'merciless == True'> Execution stopped")
                raise KeyError("Edge not found")

    # Adds nodes with data, flag and edges when applicable
    def add_node(self, data: Type.datatype = None,
                 flag: Type.flagtype = None,
                 edges: Type.edgelist = None):
        if edges == None:
            edges = {}
        new_node = Node(data, flag, edges)
        new_id = self.last_id + 1
        try:
            Validator.check_node(new_node, self, adding=True)
            self.nodes[new_id] = new_node
            self.last_id += 1

            logging.info(f" Node #{new_id} added to graph #{self.graph_id}")

            return new_node
        except:
            warnings.warn(
                f" <'KeyError'> Node not valid. Was not added", RuntimeWarning)
            logging.warning(f" <'KeyError'> Node not valid. Was not added")

            if self.merciless:
                logging.error(f" <'merciless == True'> Execution stopped")
                raise KeyError("Node not valid")
            return False

    # Removes nodes and all edges pointing to it
    def remove_node(self, id: Type.idtype):
        try:
            Type.is_id(id)
            if id in self.nodes:
                popped = self.nodes.pop(id)
                if self.size > 0:
                    for key, node in self.nodes.items():
                        if node.edges:
                            if id in node.edges:
                                node.edges.pop(id)
                logging.info(
                    f" Node #{id} removed from graph #{self.graph_id}")
                return popped
        except:
            warnings.warn(f" <'KeyError'> Node not found", RuntimeWarning)
            logging.warning(f" <'KeyError'> Node not found")

            if self.merciless:
                logging.error(f" <'merciless == True'> Execution stopped")
                raise KeyError("Node not found")
            return False

    def get_nodes(self):
        return self.nodes

    def copy(self):
        return copy.deepcopy(self)

# =============================================================================


# Validators
class Validator():

    # Checks whether graph is valid
    @ staticmethod
    def is_graph(graph: Graph):

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
                logging.error(f" <'IndexError'> Id not in graph range")
                raise IndexError("Id not in graph range")
            Validator.check_node(node, graph)
        return True

    # Checks whether node is valid. Also used internally by Graph to check
    # new nodes. Hence the adding parameter (shouldn't be used externally)
    @ staticmethod
    def check_node(node: Type.nodetype, graph: Graph, adding=False):
        Type.is_node(node)

        try:
            check_type("graph", graph, Graph)
        except:
            logging.error(f" <'TypeError'> Graph failed type check")
            raise TypeError("Graph failed type check")

        Type.is_nodelist(graph.nodes)
        flag = node.flag
        if flag:
            Type.is_flag(flag)
        if node.edges != None:
            Type.is_edgelist(node.edges)
            for key, weight in node.edges.items():
                if key not in graph.nodes:
                    if not (adding and key == graph.last_id + 1):
                        logging.error(f" <'KeyError'> Edge node not in nodes")
                        raise KeyError("Edge node not in nodes")
                Type.is_weight(weight)
        return True

# =============================================================================


# Graph builders
class Builder():

    # Advanced method to build graph from adjacency matrix
    @ staticmethod
    def adj_matrix(adj_mat: Type.adjmatrixtype,
                   obj_list: List[Any] = None):
        nodes = {}
        Type.is_adjmatrix(adj_mat)

        try:
            for i, line in enumerate(adj_mat):
                if obj_list:
                    nodes[i] = Node(data=obj_list[i])
                else:
                    nodes[i] = Node()
                for j, weight in enumerate(line):
                    if weight != None:
                        nodes[i].edges[j] = weight
                # print(nodes.edges)
        except:
            logging.error(f" <'RuntimeError'> Broken adjacency matrix")
            raise RuntimeError("Broken adjacency matrix")

        logging.info(f" Adjacency matrix is valid. Graph is being built")
        return Graph(nodes=nodes)

# Advanced method to build graph from adjacency list
    @ staticmethod
    def adj_list(adj_list: Type.adjlisttype,
                 obj_list: List[Any] = None):
        nodes = {}
        Type.is_adjlist(adj_list)

        # From here is just fodder to delete
        try:
            for i, edgelist in enumerate(adj_list):
                if obj_list:
                    nodes[i] = Node(data=obj_list[i])
                else:
                    nodes[i] = Node()
                for j, weight in edgelist:
                    nodes[i].edges[j] = weight
        except:
            logging.error(f" <'RuntimeError'> Broken adjacency list")
            raise RuntimeError("Broken adjacency list")

        logging.info(f" Adjacency list is valid. Graph is being built")
        return Graph(nodes=nodes)
    # Shouldn't be needed. Maybe to delete unused id

    @ staticmethod
    def refactor():
        raise NotImplementedError
        ...

# =============================================================================


class Converter():

    # Returns an equivalent adjacency matrix and node data list
    @ staticmethod
    def to_adjmatrix(graph: Graph, get_nodes=False):
        try:
            Validator.is_graph(graph)
            if not isinstance(get_nodes, bool):
                logging.error(f" <'TypeError'> get_nodes is not bool")
                raise TypeError("get_nodes is not bool")

            adjmatrix = [[None for j in range(0, graph.size)]
                         for i in range(0, graph.size)]
            nodes = [None for i in range(0, graph.size)]
            for main_id, node in graph.nodes.items():
                nodes[main_id] = node.data
                for dest_id, weight in node.edges.items():
                    adjmatrix[main_id][dest_id] = weight

            if get_nodes:
                return adjmatrix, nodes
            return adjmatrix

        except:
            logging.error(f" <'RuntimeError'> Wrong parameters in converter")
            raise RuntimeError("Wrong parameters in converter")

    @ staticmethod
    def to_adjlist(graph: Graph, get_nodes=False):
        try:
            Validator.is_graph(graph)
            if not isinstance(get_nodes, bool):
                logging.error(f" <'TypeError'> get_nodes is not bool")
                raise TypeError("get_nodes is not bool")

            adjlist = [None for i in range(0, graph.size)]
            nodes = [None for i in range(0, graph.size)]
            for id, node in graph.nodes.items():
                nodes[id] = node.data
                adjlist[id] = list(node.edges.items())
            if get_nodes:
                return adjlist, nodes
            return adjlist

        except:
            logging.error(f" <'RuntimeError'> Wrong parameters in converter")
            raise RuntimeError("Wrong parameters in converter")


# =============================================================================
# Starters
start_log()
start_classes()
