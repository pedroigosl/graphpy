# Graphpy

Library for creating and manipulating graphs

## +++ WARNING: Work in Progress +++

This is a barebones graph lib. It has all critical foundations, but is still far from finished and as of now, probably riddled with small bugs

# Structure

The library models graph objects with nodes and edges, supporting node flags and edge weights, fully decked with logging, warnings and error handling

Composed of a single **graph.py** file to be imported. It is defined by 6 main classes: Type, Node, Graph, Validator, Builder and Converter. 

## graph.py structure

<details>
<summary>Click to expand!</summary>

- const MERCILESS 
  > Toggles merciless mode (default True)

- const VERBOSE 
  > Toggles verbose mode (default False)

- class Type() 
  > Responsible for type checks
  - def is_id(id)
  - def is_data(data)
  - def is_flag(flag)
  - def is_node(node)
  - def is_weight(weight)
  - def is_nodelist(nodelist)
  - def is_edgelist(edgelist)
  - def is_adjmatrix(adj_mat)
  - def is_adjlist(adj_list)
  - def is_adjdict(adj_dict)

- class Node(data, flag, edges) 
  > Models nodes

  > All inputs optional
  - var data
  - var flag
  - var edges

- class Graph(nodes) 
  > Models graphs

  > Input optional
  - var nodes
  - def add_edge(source_id, target_id, weight, symmetric)
    > weight and symmetric optional

    > symmetric determines whether to add edge symmetrically
  - def remove_edge(source_id, target_id, symmetric)
    > symmetric optional

    > symmetric determines whether to remove edge symmetrically
  - def add_node(data, flag, edges)
    > All inputs optional
  - def remove_node(id)
  - def copy()

- class Validator() 
  > Checks structure integrity and validity
  - def is_graph(graph)
  - def check_node(node, graph, _adding)
    > _adding is an internal variable, shouldn't be touched

- class Builder() 
  > Models graph constructors
  - def adj_matrix(adj_mat, obj_list)
    > obj_list optional. Determines node data
  - def adj_list(adj_list, obj_list)
    > obj_list optional. Determines node data
  - def adj_dict(adj_dict, obj_list)
    > obj_list optional. Determines node data
  - def refactor(graph)
    > refactors graph and removes unused ids

- class Converter()
  > Converts graphs to native data types
  - def to_adjmatrix(graph, get_nodes)
    > get_nodes optional. Determines whether to get data from nodes
  - def to_adjlist(graph, get_nodes)
    > get_nodes optional. Determines whether to get data from nodes  
  - def to_adjdict(graph, get_nodes)
    > get_nodes optional. Determines whether to get data from nodes

> Any method or variable not listed above is either supposed to be internal, or a work in progress

</details>

## Default types
This library does not follow duck typing, it is designed with strong typing in mind. 

> More on it at *Duck typing and MERCILESS toggle* in the *Logs, warnings and error handling* section

Types supported:

<details>
<summary>Click to expand!</summary>

```python
idtype = int
datatype = Any
flagtype = Union[int, float, str]
nodetype = Node
weighttype = Union[int, float]
nodelisttype = Dict[cls.idtype, cls.nodetype]
edgelisttype = Dict[cls.idtype, cls.weighttype]

adjmatrixtype = Union[List[List[Union[cls.weighttype, None]]],
                                  npt.NDArray[npt.NDArray[Union[cls.weighttype, None]]]]

adjlisttype = Union[List[List[Tuple[cls.idtype, cls.weighttype]]],
                                npt.NDArray[npt.NDArray[Tuple[cls.idtype, cls.weighttype]]]]

adjdicttype = Dict[cls.idtype, Union[cls.edgelisttype, None]]
```

</details>

# Logs, warnings and error handling

## Logging

This lib has a standard **always on** logging feature with negligible impact on performance. 

**Log type**

<details>
<summary>Click to expand!</summary>

It comes predefined as DEBUG, but may be changed to WARNING or ERROR in code at *line 48* in **graph.py**:

```python
37 # Sets up log
38 def start_log():
39     """
40     Sets up log when import is made
41     """
42     if not os.path.exists(log_dir):
43         os.mkdir(log_dir)
44     logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
45                         datefmt="%d-%m-%y %H:%M:%S",
46                         filename=f"{log_dir}{log_name}",
47                         # filename=f"{log_dir}testlog.log",
48                         filemode='w', level=logging.DEBUG)
```

Example log:

```
24-07-22 16:19:55 - INFO -  Graph #0 initialized with size 0
24-07-22 16:19:55 - INFO -  Node #0 added to graph #0
24-07-22 16:19:55 - INFO -  Node #1 added to graph #0
24-07-22 16:19:55 - INFO -  Edge (0->1 [5]) added to graph #0
24-07-22 16:19:55 - INFO -  Node #2 added to graph #0
24-07-22 16:19:55 - INFO -  Node #3 added to graph #0
24-07-22 16:19:55 - INFO -  Node #4 added to graph #0
24-07-22 16:19:55 - INFO -  Node #5 added to graph #0
24-07-22 16:19:55 - INFO -  Node #6 added to graph #0
24-07-22 16:19:55 - INFO -  Node #7 added to graph #0
24-07-22 16:19:55 - INFO -  Node #8 added to graph #0
24-07-22 16:19:55 - INFO -  Edge (7->3 [0]) added to graph #0
24-07-22 16:19:55 - INFO -  Node #2 removed from graph #0
24-07-22 16:19:55 - INFO -  Adjacency matrix is valid. Graph is being built
24-07-22 16:19:55 - INFO -  Graph #1 initialized with size 3
24-07-22 16:19:55 - INFO -  Node #3 added to graph #1
24-07-22 16:19:55 - INFO -  Adjacency dictionary is valid. Graph is being built
24-07-22 16:19:55 - INFO -  Graph #2 initialized with size 4
24-07-22 16:19:55 - INFO -  Edge (7->8 [5]) added to graph #0
24-07-22 16:19:55 - INFO -  Edge (8->7 [5]) added to graph #0
24-07-22 16:19:55 - INFO -  Edge (8->8 [0]) added to graph #0

```

</details>

**VERBOSE toggle**

There is an optional VERBOSE toggle where the graphs present state is registered in the log after each operation.

WARNING: VERBOSE parses the entire graph into an adjacency dictionary after each operation (O(n) in time and O(n²) in space). Not suitable for performance sensitive applications 

<details>
<summary>Click to expand!</summary>

Example:
```python
import graph

graph.VERBOSE = True
```
Log output with VERBOSE:
```
24-07-22 16:40:57 - INFO -  Node #8 added to graph #0
24-07-22 16:40:57 - INFO - {0: {1: 5}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}, 7: {0: 1, 5: 0}, 8: {}}
24-07-22 16:40:57 - INFO -  Edge (7->3 [0]) added to graph #0
24-07-22 16:40:57 - INFO - {0: {1: 5}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}, 7: {0: 1, 5: 0, 3: 0}, 8: {}}
24-07-22 16:40:57 - INFO -  Node #2 removed from graph #0
24-07-22 16:40:57 - INFO - {0: {1: 5}, 1: {}, 3: {}, 4: {}, 5: {}, 6: {}, 7: {0: 1, 5: 0, 3: 0}, 8: {}}
24-07-22 16:40:57 - INFO -  Adjacency matrix is valid. Graph is being built
24-07-22 16:40:57 - INFO -  Graph #1 initialized with size 3
24-07-22 16:40:57 - INFO - {0: {0: 0, 1: 1, 2: 2}, 1: {1: 4, 2: 5}, 2: {0: 6, 2: 8}}
24-07-22 16:40:57 - INFO -  Node #3 added to graph #1
24-07-22 16:40:57 - INFO - {0: {0: 0, 1: 1, 2: 2}, 1: {1: 4, 2: 5}, 2: {0: 6, 2: 8}, 3: {}}
24-07-22 16:40:57 - INFO -  Adjacency dictionary is valid. Graph is being built
```
</details>


**Log defaults**

By default, whenever it is imported, the lib will automatically create a log file in a logs/ folder located in the main file directory. If no folder is found, it will create the folder first. 

<details>
<summary>Click to expand!</summary>

Presets may be changed in **graph.py** at:

```python
20 # Log configs
21 log_date = str(time.strftime("%d-%m-%y %H:%M:%S"))
22 log_dir = "logs/"
23 log_name = f"graphlog {log_date}.log"
24 print(f"Session log started at {log_dir}{log_name}")
   ...
37 # Sets up log
38 def start_log():
39     """
40     Sets up log when import is made
41     """
42     if not os.path.exists(log_dir):
43         os.mkdir(log_dir)
44     logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
45                         datefmt="%d-%m-%y %H:%M:%S",
46                         filename=f"{log_dir}{log_name}",
47                         # filename=f"{log_dir}testlog.log",
48                         filemode='w', level=logging.DEBUG)
```
</details>

## MERCILESS toggle

By default, all mistakes are "punished" by raising an error. Even when not critical or relevant. This behaviour can be changed by toggling MERCILESS off.

**WARNING:** By toggling MERCILESS off, all error handling is turned off, and as such, may present erratic and unexpected behaviour.

```python
import graph

graph.MERCILESS = False
```

## Duck typing and MERCILESS toggle
This lib is designed to work natively with predefined types, as a way of enforcing certain graph characteristics and ensuring proper behaviours, both from its internal methods and future external algorithms in future releases. It is also planned to be extended to C++ in the future, being designed with it in mind.

Although not recommended, duck typing can be used by toggling MERCILESS off. Despite so, it has not been tested and will turn off all error handling, and as such, may present erratic and unexpected behaviour.

Enforced types:
<details>
<summary>Click to expand!</summary>

```python
idtype = int
datatype = Any
flagtype = Union[int, float, str]
nodetype = Node
weighttype = Union[int, float]
nodelisttype = Dict[cls.idtype, cls.nodetype]
edgelisttype = Dict[cls.idtype, cls.weighttype]

adjmatrixtype = Union[List[List[Union[cls.weighttype, None]]],
                                  npt.NDArray[npt.NDArray[Union[cls.weighttype, None]]]]

adjlisttype = Union[List[List[Tuple[cls.idtype, cls.weighttype]]],
                                npt.NDArray[npt.NDArray[Tuple[cls.idtype, cls.weighttype]]]]

adjdicttype = Dict[cls.idtype, Union[cls.edgelisttype, None]]
```
</details>

# How to use

1. Start by importing the library
   > Modules can be imported directly from graph

```python
import graph
```
2. Instantiate a graph object
   > Graph can be jumpstarted with a nodelist, a dictionary {id: Node}

```python
import graph

my_graph = graph.Graph()
```

   * Similarly, you can start with a constructor


```python
import graph
from graph import Builder

adjmat = [[0, 1, 2],
          [None, 4, 5],
          [6, None, 8]]

my_graph = Builder.adj_matrix(adjmat)
```
3. Now operate using its built in functions

```python
my_graph.add_node(edges={0: 1, 5: 0})
my_graph.add_node()
my_graph.add_edge(7, 3)
my_graph.remove_node(2)
```


## Example code:

<details>
<summary>Click to expand!</summary>

```python
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
print(Converter.to_adjlist(graph))

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

```

Output:
```
>ImportWarning:  This library is a work in progress and may work unexpectedly
  warnings.warn(warning, ImportWarning)
[[(1, 5)], [], None, [], [], [], [], [(0, 1), (5, 0), (3, 0)], []]
{0: {0: 0, 1: 1, 2: 2}, 1: {1: 4, 2: 5}, 2: {0: 6, 2: 8}, 3: {}}
True
0 None {1: 5}
1 None {}
3 1 {}
4 2 {}
5 3 {}
6 4 {}
7 None {0: 1, 5: 0, 3: 0, 8: 5}
8 None {7: 5, 8: 0}
8 8
---
0 None {1: 5}
1 None {}
3 1 {}
4 2 {}
5 3 {}
6 4 {}
7 None {0: 1, 5: 0, 3: 0}
8 None {7: 5, 8: 0}
8 8
```
</details>

## License
[GNU AGPLv3](https://choosealicense.com/licenses/agpl-3.0/)