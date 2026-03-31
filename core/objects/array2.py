from sapdl.core.ast import (
    Array2Node,
    Array2DefineNode,
    Array2DeleteNode,
)
from .apdl_object import ApdlObject
from .number_parameter import NumberParameter


class Array2(ApdlObject):
    row: NumberParameter
    col: NumberParameter

    def _new(self, row=None, col=None):
        self.row = NumberParameter(self.mac, name=f"{self.name}_r")
        self.row._new(row)
        self.col = NumberParameter(self.mac, name=f"{self.name}_c")
        self.col._new(col)
        if row is not None and col is not None:
            self.mac.body.add(Array2DefineNode(Array2Node(self)))
        return self

    def delete(self):
        self._delete()
        self.mac.symbol_table.remove(self.name)
        self._alive = False

    def _delete(self):
        self.mac.body.add(Array2DeleteNode(Array2Node(self)))

    def assign(self, value):
        if isinstance(value, (int, float)):
            self.ones(value=value)
        elif isinstance(value, Array2):
            value.copy_to(self)
        else:
            raise ValueError("Unsupported assignment value type for Array2.")

    def __lshift__(self, other):
        self.assign(other)
