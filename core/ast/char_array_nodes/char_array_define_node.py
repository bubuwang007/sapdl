from sapdl import INDENT
from ..base import Node


class CharArrayDefineNode(Node):
    """Character array definition node (statement)."""

    __slots__ = ["parameter", "type"]

    def __init__(self, parameter):
        self.parameter = parameter
        self.type = "statement"

    def apdl(self, indent_level: int) -> str:
        parameter = self.parameter.parameter
        return f"{INDENT * indent_level}*DIM,{parameter},CHAR,{parameter.length}"
