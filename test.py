
import graph as gr
from graph import Graph, Builder, Converter, Type
import numpy as np

graph = Graph()
# gr.VERBOSE = True
# gr.MERCILESS = False
# node = gf.Node()
graph.add_node()
# graph.add_edge(0, 0, 5)
graph.add_node()
graph.add_edge(0, 1, 5)
for a in range(0, 5):
    graph.add_node(data=a, flag='red')

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

graph2 = Builder.adj_matrix(adjmat)
graph2.add_node(data=5)
adj_list = Converter.to_adjlist(graph2, get_nodes=True)[0]
adj_list[0].append((9, 3))

adj_dict = Converter.to_adjdict(graph2, get_nodes=True)[0]
print(adj_dict)
graph3 = Builder.adj_dict(adj_dict)

print(Type.is_adjlist(adj_list))
graph.add_edge(7, 8, 5, symmetric=True)
# gr.MERCILESS = False
# graph.remove_edge(5, 7)
graph.add_edge(8, 8)
graph2.remove_node(2)

for key, node in graph.nodes.items():
    print(key, node.data, node.edges)
print(graph.size, graph.last_id)
print("---")
# graph = Builder.refactor(graph)
graph.remove_edge(7, 8)  # , symmetric=True)

for key, node in graph.nodes.items():
    print(key, node.data, node.edges)

print(graph.size, graph.last_id)
