from __future__ import annotations
from typing import List, Any, Optional, Set, Dict, Union
from pydantic import BaseModel
from typeguard import check_type, typechecked

# class crass():
#     id_a = 1000

#     def __init__(self, id=None):
#         self._id = id
#         # self.set_id(id)
#         self.is_5(self)
#         print("my id a is", self.id_a)

#     @property
#     def id(self):
#         return self._id

#     @classmethod
#     def get_id(cls):
#         return cls.id_a

#     @classmethod
#     def set_id(cls, id):
#         cls.id_a = id

#     @staticmethod
#     def is_5(cl: crass):
#         if cl.id == 5:
#             print("is 5")


# cl = crass(5)

# print(cl.get_id())

# cl.set_id(9)

# print(crass.get_id())

# a = set()

# if a:
#     print("A IS TRUE")

# b = set()
# print(len(b))


# c = None
# if c or c == 0:
#     print("fsdgsfgs")


class Node():
    def __init__(self, id, text=None):
        self.id = id
        self.text = text

    def __eq__(self, node: Node):
        return isinstance(node, Node) and self.id == node.id

    def __hash__(self):
        return hash(self.id)


nodes = set()

nodes.add(Node(0, '0'))
nodes.add(Node(1))
# a = nodes.remove(Node(1))
# print(Node(0).text in nodes)
for node in nodes:
    print(node.text)


class types():
    mytype = Dict[int, str]

    @classmethod
    def __init__(self):
        self.testtype = Node


typer = types()
print(isinstance(Node(5), types.testtype))

a = {"blah": ['a', 'b']}
print(list(a.keys())[0])

dic = {1: "a",
       2: "b",
       3: "c"
       }
A = [isinstance(key, int) for key in dic.keys()]
# if A:
# print("yay")
# if {}:
#     print("yas")

dic[4] = "hey"

mytype = {"a": "b"}


if check_type('gfdsgdf', dic, types.mytype):
    print("yay")

if None != 0:
    print("whaaaat")

# def test(dic={}):
#     thisdic = dic
#     return thisdic


# print(test(None))
