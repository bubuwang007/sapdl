from sapdl import INDENT
from ..base import Node


class Array2DeleteNode(Node):
    """
    Represents the deletion of a 2D array parameter.
    This is used to allow statements like "delete A" where A is a 2D array parameter.
    The actual deletion will be handled during APDL code generation.
    """

    __slots__ = ["parameter", "type"]

    def __init__(self, parameter):
        self.parameter = parameter
        self.type = "statement"

    def apdl(self, indent_level: int) -> list[str]:
        parameter = self.parameter.parameter
        return [
            f"{INDENT * indent_level}{parameter.row}=",
            f"{INDENT * indent_level}{parameter.col}=",
            f"{INDENT * indent_level}{parameter}=",
        ]
