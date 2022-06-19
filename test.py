from __future__ import annotations
from typing import List, Any, Optional, Set


class crass():
    id_a = 1000

    def __init__(self, id=None):
        self._id = id
        #self.set_id(id)
        self.is_5(self)
        print("my id a is", self.id_a)

    @property
    def id(self):
        return self._id

    @classmethod
    def get_id(cls):
        return cls.id_a
    @classmethod
    def set_id(cls, id):
        cls.id_a = id
        
    @staticmethod
    def is_5(cl: crass):
        if cl.id == 5:
            print("is 5")


cl = crass(5)

print(cl.get_id())

cl.set_id(9)

print(crass.get_id())
