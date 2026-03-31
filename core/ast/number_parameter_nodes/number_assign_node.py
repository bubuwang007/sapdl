from sapdl import INDENT
from ..base import Node


class NumberAssignNode(Node):
    """
    Represents an assignment of a number parameter to a value or expression.
    This is used to allow statements like "A = 5" or "A = B + C" where A, B, and C are number parameters.
    The actual evaluation of the expression will be handled during APDL code generation.
    """

    __slots__ = ["number_parameter", "value", "type"]

    def __init__(self, number_parameter, value):
        self.number_parameter = number_parameter
        self.value = value
        self.type = "statement"

    def apdl(self, indent_level: int) -> str:
        from ..array1_nodes import Array1FuncRetNumberNode
        if isinstance(self.value, Array1FuncRetNumberNode):
            self.value.out = self.number_parameter.parameter
            return self.value.apdl(indent_level)
        else:
            res = self.value.apdl(0) if hasattr(self.value, "apdl") else str(self.value)
            return f"{INDENT * indent_level}{self.number_parameter.apdl(0)} = {res}"
