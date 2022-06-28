import graph as gf

graph = gf.Graph()
# node = gf.Node()
graph.add_node()
for a in range(0, 5):
    graph.add_node(flag=a)

# node1 = graph.add_node(edges={1: 0})
# graph.nodes[1] = 5
graph.add_node(edges={0: 1, 6: 0})
for key, node in graph.nodes.items():
    print(key, node.edges)
print(graph.size)

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
