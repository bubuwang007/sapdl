from sapdl import INDENT
from ..base import Node


class CharArrayDeleteNode(Node):
    """Character array deletion node (statement)."""

    __slots__ = ["parameter", "type"]

    def __init__(self, parameter):
        self.parameter = parameter
        self.type = "statement"

    def apdl(self, indent_level: int) -> list[str]:
        parameter = self.parameter.parameter
        return [
            f"{INDENT * indent_level}{parameter.length}=",
            f"{INDENT * indent_level}{parameter}=",
        ]
