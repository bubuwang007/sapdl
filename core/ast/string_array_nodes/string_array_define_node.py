from sapdl import INDENT
from ..base import Node


class StringArrayDefineNode(Node):
    """String array definition node (statement)."""

    __slots__ = ["parameter", "type"]

    def __init__(self, parameter):
        self.parameter = parameter
        self.type = "statement"

    def apdl(self, indent_level: int) -> str:
        parameter = self.parameter.parameter
        return f"{INDENT * indent_level}*DIM,{parameter},STRING,{parameter.str_length},{parameter.length}"
