import copy
import json

from stilus.nodes.node import Node


class Each(Node):

    def __init__(self, value, key, expr, block=None):
        super().__init__()
        self.value = value
        self.key = key
        self.expr = expr
        self.block = block

    def __str__(self):
        return f'{self.value}: {self.key} [{self.expr}] {self.block}'

    def __repr__(self):
        return self.__str__()

    def __key(self):
        return self.node_name, self.value, self.key, self.expr, self.block

    def __eq__(self, other):
        if isinstance(other, Each):
            return self.__key() == other.__key()
        return False

    def __hash__(self):
        return hash(self.__key())

    def clone(self):
        return copy.deepcopy(self)

    def to_json(self):
        return json.dumps({'__type': 'Each',
                           'val': self.value,
                           'key': self.key,
                           'expr': self.expr,
                           'block': self.block,
                           'lineno': self.lineno,
                           'column': self.column,
                           'filename': self.filename})
