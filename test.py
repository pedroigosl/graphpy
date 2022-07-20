
import graph as gr
from graph import Graph, Builder, Converter, Type
import numpy as np

graph = Graph()


# node = gf.Node()
graph.add_node()
# graph.add_edge(0, 0, 5)
graph.add_node()
graph.add_edge(0, 1, 5)
for a in range(0, 5):
    graph.add_node(data=a)

# node1 = graph.add_node(edges={1: 0})
# graph.nodes[1] = 5
graph.add_node(edges={0: 1, 5: 0})
graph.add_node()

graph.add_edge(7, 3)
# print("original", Converter.to_adjdict(graph))
graph.remove_node(2)
print("refactored", Converter.to_adjlist(graph))

adjmat = [[0, 1, 2],
          [None, 4, 5],
          [6, None, 8]]
# adjmat = np.array([[0, 1, 2],
#                    [None, 4, 5],
#                    [6, None, 8]])
# adjmat = "dgdf"

# for i, line in enumerate(adjmat):
#     for j, weight in enumerate(line):
#         print(i, j, weight)
# gr.MERCILESS = False
# graph2 = Builder.adj_matrix(5)  # adjmat)
graph2 = Builder.adj_matrix(adjmat)
graph2.add_node(data=5)
adj_list = Converter.to_adjlist(graph2, get_nodes=True)[0]
adj_list[0].append((9, 3))
# adj_dict = {0: {0: 0, 1: 1, 2: 2}, 1: {1: 4, 2: 5}, 2: {0: 6, 2: 8}, 3: None}
adj_dict = Converter.to_adjdict(graph2, get_nodes=True)[0]
print(adj_dict)
graph3 = Builder.adj_dict(adj_dict)

print(Type.is_adjlist(adj_list))
graph.add_edge(7, 8, 5, symmetric=True)
# graph.merciless = False
# gr.MERCILESS = False
# graph.remove_edge(5, 7)
graph.add_edge(8, 8)
# graph2.remove_node(2)

for key, node in graph.nodes.items():
    print(key, node.data, node.edges)
print(graph.size, graph.last_id)
print("---")
# graph = Builder.refactor(graph)
# graph.remove_edge(7, 8)
# graph.remove_edge(8, 7, symmetric=True)
for key, node in graph.nodes.items():
    print(key, node.data, node.edges)

print(graph.size, graph.last_id)
# print(graph2.size)

# for tup in graph.nodes[7].edges.items():
#     print(tup)
# dic = {0: 1}

# if 0 in dic:
#     print("blah")
# dic = {1: 2, 2: 3}
# print(type(dic))
# for key, val in dic.items():
#     print(key, val)
# from graph import start_log
# import logging
# import warnings
# import time
# # raise TypeError("wrong type")

# # Warning configs
# warnings.simplefilter("always")

# # Import warning
# warning = f" This library is a work in progress and not yet functional"
# warnings.warn(warning, ImportWarning)

# # Log configs
# log_date = str(time.strftime("%d-%m-%y %H:%M:%S"))
# log_name = f"logs/graphlog {log_date}.log"
# print(f"Session log started at {log_name}")

# # Warning configs
# # warnings.simplefilter("always")

# def start_log():
#     logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                         datefmt="%d-%m-%y %H:%M:%S",
#                         filename=log_name,
#                         filemode='w', level=logging.DEBUG)

# def f(c):
#     if c == 1:
#         raise RuntimeError
#     return True

# start_log()
# txt = f"{TypeError} test"
# logging.error(txt)

# time.sleep(1)
# logging.error(txt)
# warnings.warn("terst")
# f(2)
# print("h")
