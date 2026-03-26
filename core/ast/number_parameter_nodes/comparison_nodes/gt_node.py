from ..number_comparison_node import NumberComparisonNode


class GTNode(NumberComparisonNode):
    """大于比较节点 (>)"""

    __slots__ = []

    def __init__(self, left, right):
        super().__init__(left, "GT", right)
