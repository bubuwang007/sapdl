from sapdl import INDENT
from .base import Node


class CommentNode(Node):
    """Represents an APDL comment in the AST.

    Attributes:
        text: The comment text (without ! symbol).
    """

    __slots__ = ["text"]

    def __init__(self, text: str):
        self.text = text

    def apdl(self, indent_level: int = 0) -> str:
        return f"{INDENT * indent_level}! {self.text}"

    def __str__(self) -> str:
        return f"CommentNode(text={self.text!r})"
