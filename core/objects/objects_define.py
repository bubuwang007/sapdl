from __future__ import annotations

from .args import Args
from .number_parameter import NumberParameter
from .array1 import Array1

class ObjectsDefine:
    _var_index: int = 0
    objects = {
        "NumberParameter": NumberParameter,
    }

    def __init__(self):
        self.args = Args()

    def next_id(self):
        self._var_index += 1
        return f"{self.name.lower()}{self._var_index}"

    def NumberParameter(self, value=0, name=None):
        if name is None:
            name = self.next_id()
            scope = "local"
        else:
            scope = "global"
        num_param = NumberParameter(self, name=name)._new(value)
        self.symbol_table.define(name, type=NumberParameter, scope=scope, obj=num_param)
        return num_param

    def Array1(self, length, name=None):
        if name is None:
            name = self.next_id()
            scope = "local"
        else:
            scope = "global"
        array = Array1(self, name=name)._new(length)
        self.symbol_table.define(name, type=Array1, scope=scope, obj=array)
        return array