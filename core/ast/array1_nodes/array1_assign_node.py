from sapdl import INDENT
from ..base import Node


class Array1AssignNode(Node):
    """Array1 assignment node.

    用于数组元素的赋值操作，如 ARR(1) = value。
    """

    __slots__ = ["array1_node", "value", "type"]

    def __init__(self, array1_node, value):
        self.array1_node = array1_node
        self.value = value
        self.type = "statement"

    def apdl(self, indent_level: int) -> str:
        from ..array1_nodes import Array1FuncRetArray1Node

        if isinstance(self.value, Array1FuncRetArray1Node):
            self.value.out = self.array1_node.parameter
            return self.value.apdl(indent_level)
        else:
            pass
