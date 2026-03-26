from sapdl import INDENT
from .base import Node


class CommandNode(Node):
    """Represents a single APDL command in the AST.

    Attributes:
        cmd: The command string (e.g., "K,1,0,0,0").
    """

    __slots__ = ["cmd", "type"]

    def __init__(self, cmd: str):
        self.cmd = cmd
        self.type = "statement"

    def apdl(self, indent_level: int) -> str:
        return f"{INDENT * indent_level}{self.cmd}"
