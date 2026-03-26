from ..number_arith_node import NumberArithNode


class NegNode(NumberArithNode):
    """负号运算节点（一元减）"""

    __slots__ = []
    priority = 2

    def __init__(self, operand):
        super().__init__(operand, "-", None)

    def apdl(self, indent: int) -> str:
        operand_str = (
            self.left.apdl(indent) if hasattr(self.left, "apdl") else str(self.left)
        )

        if (
            hasattr(self.left, "priority")
            and getattr(self.left, "priority", 0) >= self.priority
        ):
            operand_str = f"({operand_str})"
        return f"-{operand_str}"
