from __future__ import annotations
from typing import List, Set, Dict, Tuple, Any, Union
import logging
import warnings
import time
import copy

from typeguard import check_type
import numpy as np

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


# =============================================================================
# Type setting
class Type():

    idtype = int
    datatype = Any
    flagtype = Union[int, float, str]
    nodetype = Node
    nodelisttype = Dict[Type.idtype, Type.nodetype]
    edgelisttype = Dict[Type.idtype, Type.weighttype]
    weighttype = Union[int, float]

    adjmatrixtype = np.ndarray[np.ndarray[Union[int, float, None]]]

    @classmethod
    def is_id(cls, id):
        equation = check_type("id", id, cls.idtype) and id >= 0
        return equation

    @classmethod
    def is_data(cls, data):
        #equation = check_type("data", data, cls.datatype)
        return True

    @classmethod
    def is_flag(cls, flag):
        equation = check_type("flag", flag, cls.flagtype)
        return equation

    @classmethod
    def is_node(cls, node):
        equation = check_type("node", node, cls.nodetype)
        return equation

    @classmethod
    def is_nodelist(cls, nodelist):
        node_check = True
        try:
            for key, val in nodelist:
                if not (cls.is_id(key) and cls.is_node(val)):
                    node_check = False
        except:
            return False
        equation = check_type("nodelist", nodelist,
                              cls.nodelisttype) and node_check
        return equation

    @classmethod
    def is_edgelist(cls, edgelist):
        edge_check = True
        try:
            for key, weight in edgelist:
                if not cls.is_id(key):
                    edge_check = False
                if weight != None:
                    if not cls.is_weight(weight):
                        edge_check = False
        except:
            return False
        equation = check_type("edgelist", edgelist,
                              cls.edgelisttype) and edge_check
        return equation

    @classmethod
    def is_weight(cls, weight):
        equation = check_type("weight", weight, cls.weighttype)
        return equation

    @classmethod
    def is_adjmatrix(cls, adj_mat):
        mat_check = True
        try:
            mat_n = len(adj_mat)
            for i, line in enumerate(adj_mat):
                if len(line) != mat_n:
                    mat_check = False
                for j, weight in enumerate(line):
                    if weight != None:
                        if not cls.is_weight(weight):
                            mat_check = False
        except:
            return False
        equation = check_type("adjmatrix", adj_mat,
                              cls.adjmatrixtype) and mat_check
        return equation

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
        self.data = data
        return self.data

    def get_data(self):
        if not self.data:
            warning = f" ({time_flag()}) RuntimeWarning - get_data called, but no data declared in node #{self.id}"
            logging.warning(warning)
            warnings.warn(warning, RuntimeWarning)
        return self.data

    def set_flag(self, flag: Type.flagtype):
        self.flag = flag
        return self.flag

    def get_flag(self):
        return self.flag

    def set_edges(self):
        ...


class Graph():
    # Start logging
    logging.basicConfig(filename=log_name, filemode='w', level=logging.DEBUG)

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
            if not Validator.is_graph(self):
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
        if not (Type.is_id(main_id) and
                Type.is_id(dest_id) and
                Type.is_weight(weight)):
            return False
        if not (main_id in self.nodes and dest_id in self.nodes):
            return False

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
        return False

    def remove_node(self, id: Type.idtype):

        if id in self.nodes:
            self.nodes.pop(id)
            self.size -= 1
            if self.size > 0:
                for key, node in self.nodes:
                    if node.edges:
                        if id in node.edges:
                            node.edges.pop(id)
            return True
        return False

    def set_relations(self, reflexive=False, symmetric=False, transitive=False):
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


class Validator():

    @staticmethod
    def is_graph(graph: Graph):

        root = graph.root
        nodes = graph.nodes

        size = graph.size

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
            if root != None:
                # broken graph, has root, but no node
                return False
            # Empty graph is a valid graph
            return True

        if root != None:
            if not Type.is_id(root):
                return False
            try:
                if not root in nodes:
                    # Broken graph, root isn't one of its nodes
                    return False
            except:
                # node typing wrong, but still shouldn't crash here
                return False
        if not Type.is_nodelist(nodes):
            return False
        for key, node in nodes:
            id_range = key < size
            id_checks = id_range
            if not id_checks:
                return False
            if not Validator.check_node(node, nodes):
                return False
        return True

    @staticmethod
    def check_node(node: Type.nodetype, nodes: Type.nodelisttype):
        if not Type.is_node(node):
            return False
        if not Type.is_nodelist(nodes):
            return False

        flag = node.flag
        if flag != None:
            if not Type.is_flag(flag):
                return False
        if node.edges:
            if not Type.is_edgelist(node.edges):
                return False
            for key, weight in node.edges:
                if key not in nodes:
                    return False
                if not Type.is_weight(weight):
                    return False
        return True


class Builder():

    # Advanced method to build graph from adjacency matrix
    @staticmethod
    def adj_matrix(adj_mat: Type.adjmatrixtype,
                   obj_list: np.ndarray[Any] = None):
        nodes = {}
        if not Type.is_adjmatrix(adj_mat):
            return False
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
            raise
        return Graph(nodes)

    # Shouldn't be needed. Maybe to delete unused id
    @staticmethod
    def refactor():
        raise NotImplementedError
        ...


class Logger():

    @staticmethod
    def start_log():
        ...
