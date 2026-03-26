from ..number_arith_node import NumberArithNode


class SubNode(NumberArithNode):
    """减法运算节点 (-)"""

    __slots__ = []
    priority = 4

    def __init__(self, left, right):
        super().__init__(left, "-", right)

    def apdl(self, indent: int) -> str:
        left_is_node = hasattr(self.left, 'apdl')
        right_is_node = hasattr(self.right, 'apdl')

        left_str = self.left.apdl(indent) if left_is_node else str(self.left)
        right_str = self.right.apdl(indent) if right_is_node else str(self.right)

        if left_is_node and getattr(self.left, 'priority', 0) > self.priority:
            left_str = f"({left_str})"
        if right_is_node and getattr(self.right, 'priority', 0) >= self.priority:
            right_str = f"({right_str})"

        return f"{left_str}-{right_str}"
