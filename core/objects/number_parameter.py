from .apdl_object import ApdlObject
from sapdl.core.ast import (
    AddNode,
    DivNode,
    MulNode,
    NegNode,
    PowNode,
    SubNode,
)
from sapdl.core.ast import (
    EQNode,
    GENode,
    GTNode,
    LENode,
    LTNode,
    NENode,
)


class NumberParameter(ApdlObject):

    def _new(self, value=None):
        if value is not None:
            self.assign(value)
        return self

    def delete(self):
        self._delete()
        self.mac.symbol_table.remove(self.name)
        self._alive = False

    def _delete(self):
        from sapdl.core.ast import NumberDeleteNode, NumberParameterNode

        self.mac.body.add(NumberDeleteNode(NumberParameterNode(self)))

    def assign(self, value):
        from sapdl.core.ast import NumberAssignNode, NumberParameterNode

        self.mac.body.add(NumberAssignNode(NumberParameterNode(self), value))

    def __lshift__(self, other):
        self.assign(other)

    def to_range(self):
        yield from self.mac.range(1, self, 1)

    # ==================== 输出 ====================

    def output(self, key=None, format="ES20.12E3"):
        import os

        key = self.name if key is None else key
        p = os.path.join(self.mac.output_path, str(key))
        with self.mac.files.open(p) as f:
            f.write(self, format=format)
        self.mac.add_output(key, type="NumberParameter")

    @classmethod
    def parse(cls, path):
        with open(path, "r", encoding="u8") as f:
            value = float(f.read().strip())
        return value

    # ==================== 一元运算 ====================

    def __neg__(self) -> NegNode:
        """负号运算 (-x)"""
        return NegNode(self)

    # ==================== 二元运算 ====================

    def __add__(self, other) -> AddNode:
        """加法 (+)

        Args:
            other: 右操作数，可以是 NumberParameter、数字或其他支持运算的对象

        Returns:
            AddNode: 加法节点
        """
        return AddNode(self, other)

    def __radd__(self, other) -> AddNode:
        """反射加法 (other + self)"""
        return AddNode(other, self)

    def __sub__(self, other) -> SubNode:
        """减法 (-)

        Args:
            other: 右操作数

        Returns:
            SubNode: 减法节点
        """
        return SubNode(self, other)

    def __rsub__(self, other) -> SubNode:
        """反射减法 (other - self)"""
        return SubNode(other, self)

    def __mul__(self, other) -> MulNode:
        """乘法 (*)

        Args:
            other: 右操作数

        Returns:
            MulNode: 乘法节点
        """
        return MulNode(self, other)

    def __rmul__(self, other) -> MulNode:
        """反射乘法 (other * self)"""
        return MulNode(other, self)

    def __truediv__(self, other) -> DivNode:
        """除法 (/)

        Args:
            other: 右操作数

        Returns:
            DivNode: 除法节点
        """
        return DivNode(self, other)

    def __rtruediv__(self, other) -> DivNode:
        """反射除法 (other / self)"""
        return DivNode(other, self)

    def __pow__(self, other) -> PowNode:
        """幂运算 (**)

        Args:
            other: 右操作数

        Returns:
            PowNode: 幂运算节点
        """
        return PowNode(self, other)

    def __rpow__(self, other) -> PowNode:
        """反射幂运算 (other ** self)"""
        return PowNode(other, self)

    # ==================== 增强赋值 ====================

    def __iadd__(self, other) -> "NumberParameter":
        """增强赋值 +=

        Args:
            other: 右操作数

        Returns:
            self: 返回自身，支持链式调用
        """
        self.assign(AddNode(self, other))
        return self

    def __isub__(self, other) -> "NumberParameter":
        """增强赋值 -="""
        self.assign(SubNode(self, other))
        return self

    def __imul__(self, other) -> "NumberParameter":
        """增强赋值 *="""
        self.assign(MulNode(self, other))
        return self

    def __itruediv__(self, other) -> "NumberParameter":
        """增强赋值 /="""
        self.assign(DivNode(self, other))
        return self

    def __ipow__(self, other) -> "NumberParameter":
        """增强赋值 **="""
        self.assign(PowNode(self, other))
        return self

    # ==================== 比较运算 ====================

    def __eq__(self, other) -> EQNode:
        """等于 (==)"""
        return EQNode(self, other)

    def __req__(self, other) -> EQNode:
        """反射等于 (other == self)"""
        return EQNode(other, self)

    def __ne__(self, other) -> NENode:
        """不等于 (!=)"""
        return NENode(self, other)

    def __rne__(self, other) -> NENode:
        """反射不等于 (other != self)"""
        return NENode(other, self)

    def __lt__(self, other) -> LTNode:
        """小于 (<)"""
        return LTNode(self, other)

    def __rlt__(self, other) -> GTNode:
        """反射小于 (other < self) -> GTNode"""
        return GTNode(other, self)

    def __le__(self, other) -> LENode:
        """小于等于 (<=)"""
        return LENode(self, other)

    def __rle__(self, other) -> GENode:
        """反射小于等于 (other <= self) -> GENode"""
        return GENode(other, self)

    def __gt__(self, other) -> GTNode:
        """大于 (>)"""
        return GTNode(self, other)

    def __rgt__(self, other) -> LTNode:
        """反射大于 (other > self) -> LTNode"""
        return LTNode(other, self)

    def __ge__(self, other) -> GENode:
        """大于等于 (>=)"""
        return GENode(self, other)

    def __rge__(self, other) -> LENode:
        """反射大于等于 (other >= self) -> LENode"""
        return LENode(other, self)
