from sapdl import INDENT
from ..base import Node


class StringAssignNode(Node):
    """String parameter assignment node (statement).

    Represents an assignment of a string parameter to a value.
    Generates APDL: STRI = 'value'
    """

    __slots__ = ["string_parameter", "value", "type"]

    def __init__(self, string_parameter, value):
        self.string_parameter = string_parameter
        self.value = value
        self.type = "statement"

    def apdl(self, indent_level: int) -> str:
        res = self.value.apdl(0) if hasattr(self.value, "apdl") else f"'{self.value}'"
        return f"{INDENT * indent_level}{self.string_parameter.apdl(0)} = {res}"
