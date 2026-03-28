from __future__ import annotations

from .number_parameter import NumberParameter


class ObjectsDefine:
    _var_index: int = 0

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
