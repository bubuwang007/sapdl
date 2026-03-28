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
