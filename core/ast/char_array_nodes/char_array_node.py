from __future__ import annotations
from ..base import Node


class CharArrayNode(Node):
    """Character array reference node (expression)."""

    __slots__ = ["parameter", "type"]

    def __init__(self, parameter):
        self.parameter = parameter
        self.type = "expr"

    def apdl(self, _: int) -> str:
        return str(self.parameter)
