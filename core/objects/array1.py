from .apdl_object import ApdlObject
from .number_parameter import NumberParameter
from sapdl.core.ast import Array1DefineNode, Array1Node, Array1DeleteNode


class Array1(ApdlObject):
    length: NumberParameter

    def _new(self, length=None):
        self.length = NumberParameter(self.mac, name=f"{self.name}_1")
        self.length._new(length)
        if length is not None:
            self.mac.body.add(Array1DefineNode(Array1Node(self)))
        return self

    def delete(self):
        self._delete()
        self.mac.symbol_table.remove(self.name)
        self._alive = False

    def _delete(self):
        self.mac.body.add(Array1DeleteNode(Array1Node(self)))
