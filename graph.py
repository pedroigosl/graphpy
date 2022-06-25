from __future__ import annotations
from typing import Dict, Any, Union
import logging
import warnings
import time
import copy

from typeguard import check_type
import numpy as np

# Log configs
log_date = str(time.strftime("%d-%m-%y %H:%M:%S"))
log_name = f"logs/graphlog {log_date}.log"
print(f"Session log started at {log_name}")

# Warning configs
warnings.simplefilter("always")

# Import warning
warning = f" This library is a work in progress and not yet functional"
warnings.warn(warning, ImportWarning)

# =============================================================================


def start_log():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt="%d-%m-%y %H:%M:%S",
                        filename=log_name,
                        filemode='w', level=logging.DEBUG)
# Time flag for warnings, errors and logs


def time_flag():
    return str(time.strftime("%d-%m-%y %H:%M:%S"))

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

        cls.adjmatrixtype = np.ndarray[np.ndarray[Union[int, float, None]]]

    @classmethod
    def is_id(cls, id):
        try:
            check_type("id", id, cls.idtype)
            equation = id >= 0
        except:
            raise TypeError("Id failed type check")
        return equation

    @classmethod
    def is_data(cls, data):
        #equation = check_type("data", data, cls.datatype)
        return True

    @classmethod
    def is_flag(cls, flag):
        try:
            check_type("flag", flag, cls.flagtype)
        except:
            raise TypeError("Flag failed type check")
        return True

    @classmethod
    def is_node(cls, node):
        try:
            check_type("node", node, cls.nodetype)
        except:
            raise TypeError("Node failed type check")
        return True

    @classmethod
    def is_weight(cls, weight):
        try:
            check_type("weight", weight, cls.weighttype)
        except:
            raise TypeError("Weight failed type check")
        return True

    @classmethod
    def is_nodelist(cls, nodelist):
        try:
            check_type("nodelist", nodelist, cls.nodelisttype)
        except:
            raise TypeError("Nodelist failed type check")
        for key, val in nodelist:
            cls.is_id(key)
            cls.is_node(val)

        return True

    @classmethod
    def is_edgelist(cls, edgelist):
        try:
            check_type("edgelist", edgelist, cls.edgelisttype)
        except:
            raise TypeError("Edgelist failed type check")
        for key, weight in edgelist:
            cls.is_id(key)
            if weight != None:
                cls.is_weight(weight)
        return True

    @classmethod
    def is_adjmatrix(cls, adj_mat):
        try:
            check_type("adjmatrix", adj_mat, cls.adjmatrixtype)
        except:
            raise TypeError("Adjmatrix failed type check")
        mat_n = len(adj_mat)
        for i, line in enumerate(adj_mat):
            if len(line) != mat_n:
                raise IndexError("Adjmatrix not homogeneous")
            for j, weight in enumerate(line):
                if weight != None:
                    cls.is_weight(weight)
        return True

# =============================================================================


class Node():
    def __init__(self,
                 data: Type.datatype = None,
                 flag: Type.flagtype = None,
                 edges: Type.edgelisttype = {}):
        # your object
        self.data = data
        # int
        self.flag = flag
        # set
        self.edges = edges

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
    # Start logging
    start_log()
    # Each graph has a specific class id for logging purposes
    graph_count = 0

    # True by standard, but can be toggled for performance
    check_graph_at_initialization = True

    def __init__(self, root: Type.idtype = None,
                 nodes: Type.nodelisttype = {},
                 weighted: bool = False,
                 reflexive: bool = False,
                 symmetric: bool = False,
                 transitive: bool = False):

        # Sets graph id
        self.graph_id = self.set_graph_id()

        self.root = root
        self.nodes = nodes
        self.size = len(self.nodes)

        # Graph characteristics
        self.weighted = weighted

        # Relation characteristics
        self.reflexive = reflexive
        self.symmetric = symmetric
        self.transitive = transitive

        # Check whether a graph is valid
        if self.check_graph_at_initialization:
            try:
                Validator.is_graph(self)
            except:
                raise RuntimeError("Graph instanced wrong!")
                # MUST KILL GRAPH OR TRIGGER ERROR
                ...

    def __del__(self):
        # Ensures the id class attribute doubles as graph count
        self.del_graph_id()

    @classmethod
    def set_graph_id(cls):
        cls.graph_count += 1
        return cls.graph_count - 1

    @classmethod
    def del_graph_id(cls):
        cls.graph_count -= 1

    def add_edge(self, main_id: Type.idtype,
                 dest_id: Type.idtype,
                 weight: Type.weighttype):
        Type.is_id(main_id)
        Type.is_id(dest_id)
        Type.is_weight(weight)
        if not (main_id in self.nodes and dest_id in self.nodes):
            raise KeyError("Broken edge")
        self.nodes[main_id].edges[dest_id] = weight
        return True

    def add_node(self, data: Type.datatype = None,
                 flag: Type.flagtype = None,
                 edges: Type.edgelist = {}):

        new_node = Node(data, flag, edges)
        new_id = self.size

        if Validator.check_node(new_node, self.nodes):
            self.nodes[new_id] = new_node
            self.size += 1
            return new_node
        raise RuntimeError("Broken node")

    def remove_node(self, id: Type.idtype):
        Type.is_id(id)
        if id in self.nodes:
            self.nodes.pop(id)
            self.size -= 1
            if self.size > 0:
                for key, node in self.nodes:
                    if node.edges:
                        if id in node.edges:
                            node.edges.pop(id)
            return True
        raise KeyError("Node not found")

    def set_relations(self, reflexive=False, symmetric=False, transitive=False):
        if not isinstance(reflexive, bool):
            raise TypeError("Reflexive is not bool")
        if not isinstance(symmetric, bool):
            raise TypeError("Symmetric is not bool")
        if not isinstance(transitive, bool):
            raise TypeError("Transitive is not bool")

        if ((self.reflexive != reflexive) or
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

    def get_nodes(self):
        return self.nodes

    def copy(self):
        return copy.deepcopy(self)

# =============================================================================


class Validator():

    @staticmethod
    def is_graph(graph: Graph):

        root = graph.root
        nodes = graph.nodes

        size = graph.size

        weighted = graph.weighted
        if not isinstance(weighted, bool):
            raise TypeError("Weighted is not bool")
        reflexive = graph.reflexive
        if not isinstance(reflexive, bool):
            raise TypeError("Reflexive is not bool")
        symmetric = graph.symmetric
        if not isinstance(symmetric, bool):
            raise TypeError("Symmetric is not bool")
        transitive = graph.transitive
        if not isinstance(transitive, bool):
            raise TypeError("Transitive is not bool")

        if not nodes:
            if root != None:
                # broken graph, has root, but no node
                raise RuntimeError("Broken graph, root without nodes")
            # Empty graph is a valid graph
            return True

        if root != None:
            Type.is_id(root)
            try:
                if not root in nodes:
                    # Broken graph, root isn't one of its nodes
                    raise KeyError("Root not in nodes")
            except:
                # node typing wrong, but still shouldn't crash here
                raise TypeError("Broken nodes")
        Type.is_nodelist(nodes)
        for key, node in nodes:
            id_range = key < size
            id_checks = id_range
            if not id_checks:
                raise IndexError("Id not in graph range")
            if not Validator.check_node(node, nodes):
                raise RuntimeError("Broken node")
        return True

    @staticmethod
    def check_node(node: Type.nodetype, nodes: Type.nodelisttype):
        Type.is_node(node)
        Type.is_nodelist(nodes)
        flag = node.flag
        if flag != None:
            Type.is_flag(flag)
        if node.edges != None:
            Type.is_edgelist(node.edges)
            for key, weight in node.edges:
                if key not in nodes:
                    raise KeyError("Edge node not in nodes")
                Type.is_weight(weight)
        return True

# =============================================================================


class Builder():

    # Advanced method to build graph from adjacency matrix
    @staticmethod
    def adj_matrix(adj_mat: Type.adjmatrixtype,
                   obj_list: np.ndarray[Any] = None):
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
        except:
            raise RuntimeError("Broken adjacency matrix")
        return Graph(nodes)

    # Shouldn't be needed. Maybe to delete unused id
    @staticmethod
    def refactor():
        raise NotImplementedError
        ...
