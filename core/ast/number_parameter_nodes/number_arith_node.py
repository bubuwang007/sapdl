from ..base import Node


class NumberArithNode(Node):
    """
    Represents an arithmetic operation between two number parameters.
    This is used to allow expressions like "A + B" where A and B are number parameters.
    The actual evaluation of the expression will be handled during APDL code generation.
    """

    __slots__ = ["left", "operator", "right", "type", "priority"]

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
        self.type = "expr"

    def __str__(self):
        return self.apdl(0)

    # ==================== 二元运算 ====================

    def __add__(self, other) -> "AddNode":
        """加法 (+)

        Args:
            other: 右操作数

        Returns:
            AddNode: 加法节点
        """
        from sapdl.core.ast.number_parameter_nodes.arith_nodes import AddNode
        return AddNode(self, other)

    def __radd__(self, other) -> "AddNode":
        """反射加法 (other + self)"""
        from sapdl.core.ast.number_parameter_nodes.arith_nodes import AddNode
        return AddNode(other, self)

    def __sub__(self, other) -> "SubNode":
        """减法 (-)"""
        from sapdl.core.ast.number_parameter_nodes.arith_nodes import SubNode
        return SubNode(self, other)

    def __rsub__(self, other) -> "SubNode":
        """反射减法 (other - self)"""
        from sapdl.core.ast.number_parameter_nodes.arith_nodes import SubNode
        return SubNode(other, self)

    def __mul__(self, other) -> "MulNode":
        """乘法 (*)"""
        from sapdl.core.ast.number_parameter_nodes.arith_nodes import MulNode
        return MulNode(self, other)

    def __rmul__(self, other) -> "MulNode":
        """反射乘法 (other * self)"""
        from sapdl.core.ast.number_parameter_nodes.arith_nodes import MulNode
        return MulNode(other, self)

    def __truediv__(self, other) -> "DivNode":
        """除法 (/)"""
        from sapdl.core.ast.number_parameter_nodes.arith_nodes import DivNode
        return DivNode(self, other)

    def __rtruediv__(self, other) -> "DivNode":
        """反射除法 (other / self)"""
        from sapdl.core.ast.number_parameter_nodes.arith_nodes import DivNode
        return DivNode(other, self)

    def __pow__(self, other) -> "PowNode":
        """幂运算 (**)"""
        from sapdl.core.ast.number_parameter_nodes.arith_nodes import PowNode
        return PowNode(self, other)

    def __rpow__(self, other) -> "PowNode":
        """反射幂运算 (other ** self)"""
        from sapdl.core.ast.number_parameter_nodes.arith_nodes import PowNode
        return PowNode(other, self)

    # ==================== 比较运算 ====================

    def __eq__(self, other) -> "EQNode":
        """等于 (==)"""
        from sapdl.core.ast.number_parameter_nodes.comparison_nodes import EQNode
        return EQNode(self, other)

    def __req__(self, other) -> "EQNode":
        """反射等于 (other == self)"""
        from sapdl.core.ast.number_parameter_nodes.comparison_nodes import EQNode
        return EQNode(other, self)

    def __ne__(self, other) -> "NENode":
        """不等于 (!=)"""
        from sapdl.core.ast.number_parameter_nodes.comparison_nodes import NENode
        return NENode(self, other)

    def __rne__(self, other) -> "NENode":
        """反射不等于 (other != self)"""
        from sapdl.core.ast.number_parameter_nodes.comparison_nodes import NENode
        return NENode(other, self)

    def __lt__(self, other) -> "LTNode":
        """小于 (<)"""
        from sapdl.core.ast.number_parameter_nodes.comparison_nodes import LTNode
        return LTNode(self, other)

    def __rlt__(self, other) -> "GTNode":
        """反射小于 (other < self) -> GTNode"""
        from sapdl.core.ast.number_parameter_nodes.comparison_nodes import GTNode
        return GTNode(other, self)

    def __le__(self, other) -> "LENode":
        """小于等于 (<=)"""
        from sapdl.core.ast.number_parameter_nodes.comparison_nodes import LENode
        return LENode(self, other)

    def __rle__(self, other) -> "GENode":
        """反射小于等于 (other <= self) -> GENode"""
        from sapdl.core.ast.number_parameter_nodes.comparison_nodes import GENode
        return GENode(other, self)

    def __gt__(self, other) -> "GTNode":
        """大于 (>)"""
        from sapdl.core.ast.number_parameter_nodes.comparison_nodes import GTNode
        return GTNode(self, other)

    def __rgt__(self, other) -> "LTNode":
        """反射大于 (other > self) -> LTNode"""
        from sapdl.core.ast.number_parameter_nodes.comparison_nodes import LTNode
        return LTNode(other, self)

    def __ge__(self, other) -> "GENode":
        """大于等于 (>=)"""
        from sapdl.core.ast.number_parameter_nodes.comparison_nodes import GENode
        return GENode(self, other)

    def __rge__(self, other) -> "LENode":
        """反射大于等于 (other >= self) -> LENode"""
        from sapdl.core.ast.number_parameter_nodes.comparison_nodes import LENode
        return LENode(other, self)
