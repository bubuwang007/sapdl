from sapdl import INDENT
from .base import Node


class FunctionCallNode(Node):
    """Represents a function definition in the AST.

    Attributes:
        name: The function name.
        args: List of argument names.
        body: The function body block.
    """

    __slots__ = ["name", "args", "type"]

    def __init__(self, name: str, *args: list[str]):
        self.name = name
        self.args = args
        self.type = "expr"

    def apdl(self, _: int) -> str:
        args_str = ", ".join([str(arg) for arg in self.args])
        return f"{self.name}({args_str})"