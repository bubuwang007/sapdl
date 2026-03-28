from .apdl_object import ApdlObject


class NumberParameter(ApdlObject):

    def _new(self, value=None):
        if value is not None:
            self.assign(value)
        return self

    def delete(self):
        self._delete()
        self._alive = False
        self.mac.symbol_table.remove(self.name)

    def _delete(self):
        from sapdl.core.ast import NumberDeleteNode, NumberParameterNode

        self.mac.body.add(NumberDeleteNode(NumberParameterNode(self)))

    def assign(self, value):
        from sapdl.core.ast import NumberAssignNode, NumberParameterNode

        self.mac.body.add(NumberAssignNode(NumberParameterNode(self), value))

    def __lshift__(self, other):
        self.assign(other)
