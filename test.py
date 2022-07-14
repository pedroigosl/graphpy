from graph import Graph, Builder, Converter
import numpy as np

graph = Graph()


# node = gf.Node()
graph.add_node()
# graph.add_edge(0, 0, 5)
graph.add_node()
graph.add_edge(0, 1, 5)
for a in range(0, 5):
    graph.add_node(flag=a)

# node1 = graph.add_node(edges={1: 0})
# graph.nodes[1] = 5
graph.add_node(edges={0: 1, 5: 0})
graph.add_node()

graph.add_edge(7, 3)
graph.remove_node(2)

graph.merciless = False

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

graph2 = Builder.adj_matrix(adjmat)
graph2.add_node(data=5)
print(Converter.to_adjlist(graph2, get_nodes=True)[0])
graph.add_edge(7, 8, 5, symmetric=True)
graph.remove_edge(5, 7)
graph.add_edge(8, 8)
graph2.remove_node(2)

for key, node in graph2.nodes.items():
    print(key, node.flag, node.edges)

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
