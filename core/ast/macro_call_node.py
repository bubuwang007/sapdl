from sapdl import INDENT
from .base import Node


class MacroCallNode(Node):
    """Represents a macro call in the AST.

    Attributes:
        name: The macro name.
        args: List of argument values.
    """

    __slots__ = ["name", "args", "type"]

    def __init__(self, name: str, *args: list[str]):
        self.name = name
        self.args = args
        self.type = "statement"

    def apdl(self, indent_level: int = 0) -> str:
        args_str = ", ".join([str(arg) for arg in self.args])
        return f"{INDENT * indent_level}{self.name},{args_str}"
