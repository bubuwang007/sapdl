from __future__ import annotations
from .base import Node


class NumberParameterNode(Node):

    __slots__ = ["parameter", "type"]

    def __init__(self, parameter):
        self.parameter = parameter
        self.type = "expr"

    def apdl(self, _: int) -> str:
        return str(self.parameter)
