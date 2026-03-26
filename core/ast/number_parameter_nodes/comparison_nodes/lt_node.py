from ..number_comparison_node import NumberComparisonNode


class LTNode(NumberComparisonNode):
    """小于比较节点 (<)"""

    __slots__ = []

    def __init__(self, left, right):
        super().__init__(left, "LT", right)
