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
        cls.edgetype = Dict[type.idtype, type.weighttype]
        cls.weighttype = Union[int, float]

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
    def is_edge(cls, edge):
        equation = (isinstance(edge, cls.edgetype) and
                    cls.is_id(list(edge.keys())[0]))
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
                 edges: Dict[type.idtype, type.edgetype] = {}):
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

    def set_data(self, data: Any):
        self.data = data
        return self.data

    def get_data(self):
        if not self.data:
            warning = f" ({time_flag()}) RuntimeWarning - get_data called, but no data declared in node #{self.id}"
            logging.warning(warning)
            warnings.warn(warning, RuntimeWarning)
        return self.data

    def set_flag(self, flag: Union[int, float, str]):
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
                 nodes: Dict[type.idtype, type.nodetype] = {},
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
            if not isinstance(root, int):
                return False
            root_node = Node(root)
            try:
                if not root_node in nodes:
                    # Broken graph, root isn't one of its nodes
                    return False
            except:
                # node typing wrong, but still shouldn't crash here
                return False
        if not isinstance(nodes, set):
            return False
        for node in nodes:

            is_node = isinstance(node, Node)
            id_int = isinstance(node.id, int)
            id_positive = node.id >= 0
            id_range = node.id < size
            id_checks = (is_node and
                         id_int and
                         id_positive and
                         id_range)
            if not id_checks:
                return False

            if node.flag or node.flag == 0:
                flag_check = (isinstance(node.flag, int) or
                              isinstance(node.flag, float) or
                              isinstance(node.flag, str))
                if not flag_check:
                    return False

            if node.edges:
                if not isinstance(node.edges, set):
                    return False
                for edge in node.edges:
                    if not isinstance(edge, Edge):
                        return False
                    if not isinstance(edge.node, Node):
                        return False
                    if edge.node not in nodes:
                        return False
                    weight_check = (isinstance(edge.weight, int) or
                                    isinstance(edge.weight, float))
                    if not weight_check:
                        return False
        return True

    def check_node(self, node: Node):
        is_node = isinstance(node, Node)
        id_int = isinstance(node.id, int)
        id_positive = node.id >= 0
        id_range = node.id < self.size
        id_checks = (is_node and
                     id_int and
                     id_positive and
                     id_range)
        if not id_checks:
            return False

        if node.flag or node.flag == 0:
            flag_check = (isinstance(node.flag, int) or
                          isinstance(node.flag, float) or
                          isinstance(node.flag, str))
            if not flag_check:
                return False

        if node.edges:
            if not isinstance(node.edges, set):
                return False
            for edge in node.edges:
                if not isinstance(edge, Edge):
                    return False
                if not isinstance(edge.node, Node):
                    return False
                if edge.node not in self.nodes:
                    return False
                weight_check = (isinstance(edge.weight, int) or
                                isinstance(edge.weight, float))
                if not weight_check:
                    return False
        return True

    def add_node(self, data: Any = None, flag: Union[int, float, str] = None):
        self.size += 1
        new_node = Node(self.size - 1, data, flag)
        if self.check_node(new_node):
            self.nodes.add(new_node)
            return new_node
        self.size -= 1
        return False

    def remove_node(self, id: int):
        aux_node = Node(id)
        if self.nodes:
            if aux_node in self.nodes:
                self.nodes.remove(aux_node)
                self.size -= 1
                if self.size > 0:
                    for node in self.nodes:
                        if node.edges:
                            aux_edge = Edge(aux_node)
                            if aux_edge in node.edges:
                                node.edges.remove(aux_edge)
                return True
            return False
        return False

    def build_graph(self, adj_matrix: np.ndarray[Union[int, float, None]],
                    obj_list: np.ndarray[Any] = None):
        try:
            for i, line in adj_matrix:
                if obj_list:
                    self.nodes.add(Node(i, obj_list[i]))
                else:
                    self.nodes.add(Node(i))
                for j, weight in line:
                    if j != i and weight != None:
                        self.nodes(Node(i)).edges.add(Edge(Node(j), weight))

        except:
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
