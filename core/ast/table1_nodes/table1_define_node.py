from sapdl import INDENT
from ..base import Node


class Table1DefineNode(Node):
    """Table1 definition node (statement)."""

    __slots__ = ["parameter", "type"]

    def __init__(self, parameter):
        self.parameter = parameter
        self.type = "statement"

    def apdl(self, indent_level: int) -> str:
        parameter = self.parameter.parameter
        return f"{INDENT * indent_level}*DIM,{parameter},TABLE,{parameter.length}"
