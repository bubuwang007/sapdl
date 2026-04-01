from sapdl import INDENT
from ..base import Node


class StringDeleteNode(Node):
    """String parameter deletion node (statement).

    Represents the deletion of a string parameter.
    Generates APDL: STRI =
    """

    __slots__ = ["string_parameter", "type"]

    def __init__(self, string_parameter):
        self.string_parameter = string_parameter
        self.type = "statement"

    def apdl(self, indent_level: int) -> str:
        return f"{INDENT * indent_level}{self.string_parameter.apdl(0)} = "
