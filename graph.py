from __future__ import annotations
from turtle import goto
from typing import List, Set, Dict, Tuple, Any, Union
import logging
import warnings
import time
import copy

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
class type():

    @classmethod
    def __init__(cls):
        cls.idtype = int
        cls.datatype = Any
        cls.flagtype = Union[int, float, str]
        cls.nodetype = Node
        cls.nodelisttype = Dict[type.idtype, type.nodetype]
        cls.edgelisttype = Dict[type.idtype, type.weighttype]
        cls.weighttype = Union[int, float]

        cls.adjmatrixtype = np.ndarray[Union[int, float, None]]

    @classmethod
    def is_id(cls, id):
        equation = isinstance(id, cls.idtype) and id >= 0
        return equation

    @classmethod
    def is_data(cls, data):
        equation = isinstance(data, cls.datatype)
        return equation

    @classmethod
    def is_flag(cls, flag):
        equation = isinstance(flag, cls.flagtype)
        return equation

    @classmethod
    def is_node(cls, node):
        equation = isinstance(node, cls.nodetype)
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
        equation = isinstance(nodelist, cls.nodelisttype) and node_check
        return equation

    @classmethod
    def is_edgelist(cls, edgelist):
        id_check = True
        try:
            for key in edgelist.keys():
                if not cls.is_id(key):
                    id_check = False
        except:
            return False
        equation = isinstance(edgelist, cls.edgelisttype) and id_check
        return equation

    @classmethod
    def is_weight(cls, weight):
        equation = isinstance(weight, cls.weighttype)
        return equation

        # =============================================================================


class Node():
    def __init__(self,
                 data: type.datatype = None,
                 flag: type.flagtype = None,
                 edges: type.edgelisttype = {}):
        # your object
        self.data = data
        # int
        self.flag = flag
        # set
        self.edges = edges

    # def __eq__(self, node: Node):
    #     return isinstance(node, Node) and self.id == node.id

    # def __hash__(self):
    #     return hash(self.id)

    # @property
    # def id(self):
    #     return self._id

    # def get_id(self):
    #     return self._id

    def set_data(self, data: type.datatype):
        self.data = data
        return self.data

    def get_data(self):
        if not self.data:
            warning = f" ({time_flag()}) RuntimeWarning - get_data called, but no data declared in node #{self.id}"
            logging.warning(warning)
            warnings.warn(warning, RuntimeWarning)
        return self.data

    def set_flag(self, flag: type.flagtype):
        self.flag = flag
        return self.flag

    def get_flag(self):
        return self.flag

    def set_edges(self):
        ...


# class Edge():
#     def __init__(self, node: int, weight: Union[int, float] = 0):
#         self.node = node
#         self.weight = weight

#     def __eq__(self, edge: Edge):
#         eq = isinstance(edge, Edge) and self.node == edge.node
#         return eq

#     def __hash__(self):
#         return hash(self.node)

#     def set_weight(self, weight: Union[int, float]):
#         self.weight = weight

#     def get_weight(self):
#         return self.weight


class Graph():
    # Start logging
    logging.basicConfig(filename=log_name, filemode='w', level=logging.DEBUG)

    # Each graph has a specific class id for logging purposes
    graph_count = 0

    # True by standard, but can be toggled for performance
    check_graph_at_initialization = True

    def __init__(self, root: type.idtype = None,
                 nodes: type.nodelisttype = {},
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
            if not self.is_valid(self):
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

    # Internal method
    @staticmethod
    def is_valid(graph: Graph):

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
            if root or root == 0:
                # broken graph, has root, but no node
                return False
            # Empty graph is a valid graph
            return True

        if root or root == 0:
            if not type.is_id(root):
                return False
            try:
                if not root in nodes:
                    # Broken graph, root isn't one of its nodes
                    return False
            except:
                # node typing wrong, but still shouldn't crash here
                return False
        if not type.is_nodelist(nodes):
            return False
        for key, node in nodes:
            id_range = key < size
            id_checks = id_range
            if not id_checks:
                return False
            flag = node.flag
            if flag or flag == 0:
                if not type.is_flag(flag):
                    return False

            if node.edges:
                if not type.is_edgelist(node.edges):
                    return False
                for key, weight in node.edges:
                    if key not in nodes:
                        return False
                    if not type.is_weight(weight):
                        return False
        return True

    def check_node(self, node: type.nodetype):
        if not type.is_node(node):
            return False
        if node.flag or node.flag == 0:
            if not type.is_flag():
                return False
            flag = node.flag
            if flag or flag == 0:
                if not type.is_flag(flag):
                    return False
            if node.edges:
                if not type.is_edgelist(node.edges):
                    return False
                for key, weight in node.edges:
                    if key not in self.nodes:
                        return False
                    if not type.is_weight(weight):
                        return False
        return True

    def add_node(self, data: type.datatype = None,
                 flag: type.flagtype = None,
                 edges: type.edgelist = {}):

        new_node = Node(data, flag, edges)
        new_id = self.size

        if self.check_node(new_node):
            self.nodes[new_id] = new_node
            self.size += 1
            return new_node
        return False

    def remove_node(self, id: type.idtype):

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

    # Advanced method to build graph from adjacency matrix
    def build_graph(self, adj_matrix: type.adjmatrixtype,
                    obj_list: np.ndarray[Any] = None):
        if self.size == 0:
            try:
                for i, line in enumerate(adj_matrix):
                    if obj_list:
                        self.add_node(data=obj_list[i])
                    else:
                        self.add_node()
                    for j, weight in enumerate(line):
                        if j != i and weight != None:
                            self.nodes[i].edges[j] = weight
            except:
                raise
        else:
            raise

        if self.check_graph_at_initialization:
            if not self.is_valid(self):
                # MUST KILL GRAPH OR TRIGGER ERROR
                ...

    # Shouldn't be needed. Maybe to delete unused id
    def refactor(self):
        raise NotImplementedError
        ...

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
