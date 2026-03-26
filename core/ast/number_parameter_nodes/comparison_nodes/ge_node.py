from ..number_comparison_node import NumberComparisonNode


class GENode(NumberComparisonNode):
    """大于等于比较节点 (>=)"""

    __slots__ = []

    def __init__(self, left, right):
        super().__init__(left, "GE", right)
