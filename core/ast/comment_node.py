from sapdl import INDENT
from .base import Node


class CommentNode(Node):
    """Represents an APDL comment in the AST.

    Attributes:
        text: The comment text (without ! symbol).
    """

    __slots__ = ["text", "type"]

    def __init__(self, text: str):
        self.text = text
        self.type = "statement"

    def apdl(self, indent_level: int) -> str:
        return f"{INDENT * indent_level}! {self.text}"

    def __str__(self) -> str:
        return f"CommentNode(text={self.text!r})"
