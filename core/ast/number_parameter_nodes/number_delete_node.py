from sapdl import INDENT
from ..base import Node


class NumberDeleteNode(Node):
    """
    Represents the deletion of a number parameter.
    This is used to allow statements like "delete A" where A is a number parameter.
    The actual deletion will be handled during APDL code generation.
    """

    __slots__ = ["number_parameter", "type"]

    def __init__(self, number_parameter):
        self.number_parameter = number_parameter
        self.type = "statement"

    def apdl(self, indent_level: int) -> str:
        return f"{INDENT * indent_level}{self.number_parameter.apdl(0)}="
