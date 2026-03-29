from sapdl import INDENT
from .base import Node, Body

class BlockNode(Node):
    """Generic block node."""

    __slots__ = ["start", "body", "end", "type"]

    def __init__(self):
        self.type = "block"
        self.body = Body()
        self.start = None
        self.end = None

    def apdl(self, indent_level: int) -> list[str]:
        ret = []
        ret.append(self.start.apdl(indent_level))
        ret.extend(self.body.apdl(indent_level))
        ret.append(self.end.apdl(indent_level))
        return ret

    def __str__(self) -> str:
        return f"BlockNode(body={self.body!r})"
