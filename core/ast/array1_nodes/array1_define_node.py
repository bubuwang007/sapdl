from sapdl import INDENT
from ..base import Node


class Array1DefineNode(Node):
    """
    Represents the definition of a 1D array parameter.
    This is used to allow statements like "A(10) = 0" where A is a 1D array parameter.
    The actual definition will be handled during APDL code generation.
    """

    __slots__ = ["parameter", "type"]

    def __init__(self, parameter):
        self.parameter = parameter
        self.type = "statement"

    def apdl(self, indent_level: int) -> str:
        parameter = self.parameter.parameter
        return f"{INDENT * indent_level}*DIM,{parameter},ARRAY,{parameter.length},,,,,,"
