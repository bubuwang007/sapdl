from sapdl import INDENT
from .base import Node


class CommandNode(Node):
    """Represents a single APDL command in the AST.

    Attributes:
        cmd: The command string (e.g., "K,1,0,0,0").
    """

    __slots__ = ["cmd"]

    def __init__(self, cmd: str):
        self.cmd = cmd

    def apdl(self, indent_level: int = 0) -> str:
        return f"{INDENT * indent_level}{self.cmd}"

    def __str__(self) -> str:
        return f"CommandNode(cmd={self.cmd!r})"
