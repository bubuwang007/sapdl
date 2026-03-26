"""Literal value nodes for APDL AST."""

from __future__ import annotations

from typing import Union

from .base import Node


class NumberLiteral(Node):
    """Numeric literal node.

    Represents a numeric constant in APDL expressions.
    APDL doesn't have explicit numeric literals in the same way as Python,
    but numbers can appear directly in expressions.
    """

    __slots__ = ["value", "type"]

    def __init__(self, value: Union[int, float]):
        self.value = value
        self.type = "expr"

    def apdl(self, _: int) -> str:
        return str(self.value)


class StringLiteral(Node):
    """String literal node.

    Represents a string constant in APDL.
    In APDL, strings are typically enclosed in single quotes.
    """

    __slots__ = ["value", "type"]

    def __init__(self, value: str):
        self.value = value
        self.type = "expr"

    def apdl(self, _: int) -> str:
        return f"'{self.value}'"
