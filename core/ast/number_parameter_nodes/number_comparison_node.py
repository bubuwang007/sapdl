from ..base import Node


class NumberComparisonNode(Node):
    """
    Represents a comparison operation between two number parameters.
    This is used to allow expressions like "A > B" where A and B are number parameters.
    The actual evaluation of the expression will be handled during APDL code generation.
    """

    __slots__ = ["left", "operator", "right", "type"]

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
        self.type = "expr"
