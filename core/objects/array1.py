from sapdl.core.ast import (
    Array1DefineNode,
    Array1Node,
    Array1DeleteNode,
    Array1FuncRetNumberNode,
)
from .apdl_object import ApdlObject
from .number_parameter import NumberParameter
from .array_element import ArrayElement


class Array1(ApdlObject):
    length: NumberParameter

    def _new(self, length=None):
        self.length = NumberParameter(self.mac, name=f"{self.name}_1")
        self.length._new(length)
        if length is not None:
            self.mac.body.add(Array1DefineNode(Array1Node(self)))
        return self

    def delete(self):
        self._delete()
        self.mac.symbol_table.remove(self.name)
        self._alive = False

    def _delete(self):
        self.mac.body.add(Array1DeleteNode(Array1Node(self)))

    def assign(self, value):
        if not self._alive:
            raise RuntimeError(f"Cannot assign to deleted Array1 '{self.name}'.")
        if isinstance(value, (int, float)):
            self.ones(value=value)
        elif isinstance(value, Array1):
            value.copy_to(self)
        else:
            raise ValueError("Unsupported assignment value type for Array1.")

    def __lshift__(self, other):
        self.assign(other)

    # ==================== 输出 ====================

    def output(self, key=None, format="ES20.12E3"):
        """输出数组到文件。

        Args:
            key: 输出文件名的键，默认使用数组名。
            format: 格式化字符串，APDL *VWRITE 格式。
        """
        import os

        key = self.name if key is None else key
        p = os.path.join(self.mac.output_path, str(key))
        with self.mac.files.open(p) as f:
            f.write(f"{self}(1)", format=format)
        self.mac.add_output(key, type="Array1")

    @classmethod
    def parse(cls, path):
        """从文件解析数组值。

        Args:
            path: 文件路径。

        Returns:
            numpy.ndarray: 解析出的数值数组。
        """
        import numpy as np

        return np.loadtxt(path, dtype=float)

    # ==================== 元素获取 ====================

    def __getitem__(self, index):
        return ArrayElement(self, index)

    def __iter__(self):
        for i in self.mac.range(1, self.length):
            yield self[i]

    def enumerate(self, start=1):
        for i in self.mac.range(start, self.length):
            yield i + (start - 1), self[i]

    # ==================== 初始化方法 ====================

    def ramp(self, start, step=0, cumulative=False):
        """填充等差数列。

        Args:
            start: 起始值。
            step: 步长。
            cumulative: 是否累积。

        Returns:
            self: 返回自身，支持链式调用。
        """
        if cumulative:
            self.mac.vcum(1)
        self.mac.vfill(self, "RAMP", start, step)
        return self

    def zeros(self):
        """填充零数组。

        Returns:
            self: 返回自身，支持链式调用。
        """
        return self.ramp(0)

    def ones(self, value=1):
        """填充指定值的数组。

        Args:
            value: 填充值。

        Returns:
            self: 返回自身，支持链式调用。
        """
        return self.ramp(value)

    def rand(self, lower=0, upper=1):
        """填充均匀分布随机数。

        Args:
            lower: 下界。
            upper: 上界。

        Returns:
            self: 返回自身，支持链式调用。
        """
        self.mac.vfill(self, "RAND", lower, upper)
        return self

    def fill(self, iterable, start=1):
        """填充数据。

        Args:
            iterable: 可迭代对象。
            start: 起始索引。

        Returns:
            self: 返回自身，支持链式调用。
        """
        for i in range(0, len(iterable), 10):
            if len(iterable) - i < 10:
                self.mac.vfill(f"{self}({start})", "DATA", *iterable[i:])
            else:
                self.mac.vfill(f"{self}({start})", "DATA", *iterable[i : i + 10])
                start += 10
        return self

    def gaussian_distribution(self, mean=0.0, stddev=1.0):
        """填充高斯分布随机数。

        Args:
            mean: 均值。
            stddev: 标准差。

        Returns:
            self: 返回自身，支持链式调用。
        """
        self.mac.vfill(self, "GDIS", mean, stddev)
        return self

    def triangular_distribution(self, lower, peak, upper):
        """填充三角分布随机数。

        Args:
            lower: 下界。
            peak: 峰值。
            upper: 上界。

        Returns:
            self: 返回自身，支持链式调用。
        """
        self.mac.vfill(self, "TRIA", lower, peak, upper)
        return self

    def beta_distribution(self, lower, upper, alpha, beta):
        """填充贝塔分布随机数。

        Args:
            lower: 下界。
            upper: 上界。
            alpha: alpha 参数。
            beta: beta 参数。

        Returns:
            self: 返回自身，支持链式调用。
        """
        self.mac.vfill(self, "BETA", lower, upper, alpha, beta)
        return self

    def gamma_distribution(self, lower, alpha, beta):
        """填充伽马分布随机数。

        Args:
            lower: 下界。
            alpha: alpha 参数。
            beta: beta 参数。

        Returns:
            self: 返回自身，支持链式调用。
        """
        self.mac.vfill(self, "GAMM", lower, alpha, beta)
        return self

    # ==================== 复制和克隆 ====================

    def zeros_like(self, name=None):
        """创建相同长度的零数组。

        Args:
            name: 新数组名称，默认使用原名称。

        Returns:
            Array1: 新的零数组。
        """
        return self.mac.Array1(self.length, name=name)

    def copy_to(self, other):
        """复制数据到另一个数组。

        Args:
            other: 目标数组。
        """
        self.mac.vfun(other, "COPY", self)

    def clone(self, name=None):
        """克隆数组。

        Args:
            name: 克隆数组的名称。

        Returns:
            Array1: 克隆的新数组。
        """
        other = self.zeros_like(name=name)
        self.copy_to(other)
        return other

    # ==================== 排序和反转 ====================

    def sort(self, reverse=False):
        """对数组排序。

        Args:
            reverse: 是否降序（True 时使用 DSORT）。

        Returns:
            排序后的数组。
        """
        if reverse:
            self.mac.vfun(self, "DSORT", self)
        else:
            self.mac.vfun(self, "ASORT", self)
        return self

    def reverse(self):
        """原地反转数组。

        Returns:
            self: 返回自身，支持链式调用。
        """
        tmp_val = self.mac.NumberParameter(value=0)
        half = self.length / 2
        for i in self.mac.range(1, half):
            tmp_val << self[i]
            self[i] << self[self.length - i + 1]
            self[self.length - i + 1] << tmp_val
        return self

    # ==================== 统计数据 ====================

    @property
    def max(self):
        """数组最大值。"""
        return Array1FuncRetNumberNode(
            func_name="MAX", func_type="vscfun", array_parameter=Array1Node(self)
        )

    @property
    def min(self):
        """数组最小值。"""
        return Array1FuncRetNumberNode(
            func_name="MIN", func_type="vscfun", array_parameter=Array1Node(self)
        )

    @property
    def argmax(self):
        """最大值的索引。"""
        return Array1FuncRetNumberNode(
            func_name="LMAX", func_type="vscfun", array_parameter=Array1Node(self)
        )

    @property
    def argmin(self):
        """最小值的索引。"""
        return Array1FuncRetNumberNode(
            func_name="LMIN", func_type="vscfun", array_parameter=Array1Node(self)
        )

    @property
    def first_nonzero(self):
        """第一个非零值的索引。"""
        return Array1FuncRetNumberNode(
            func_name="FIRST", func_type="vscfun", array_parameter=Array1Node(self)
        )

    @property
    def last_nonzero(self):
        """最后一个非零值的索引。"""
        return Array1FuncRetNumberNode(
            func_name="LAST", func_type="vscfun", array_parameter=Array1Node(self)
        )

    @property
    def sum(self):
        """数组元素和。"""
        return Array1FuncRetNumberNode(
            func_name="SUM", func_type="vscfun", array_parameter=Array1Node(self)
        )

    @property
    def mean(self):
        """数组元素均值。"""
        return Array1FuncRetNumberNode(
            func_name="MEAN", func_type="vscfun", array_parameter=Array1Node(self)
        )

    @property
    def median(self):
        """数组元素中位数。"""
        return Array1FuncRetNumberNode(
            func_name="MEDI", func_type="vscfun", array_parameter=Array1Node(self)
        )

    @property
    def variance(self):
        """数组元素方差。"""
        return Array1FuncRetNumberNode(
            func_name="VARI", func_type="vscfun", array_parameter=Array1Node(self)
        )

    @property
    def std(self):
        """数组元素标准差。"""
        return Array1FuncRetNumberNode(
            func_name="STDV", func_type="vscfun", array_parameter=Array1Node(self)
        )

    @property
    def rms(self):
        """数组元素均方根。"""
        return Array1FuncRetNumberNode(
            func_name="RMS", func_type="vscfun", array_parameter=Array1Node(self)
        )

    # ==================== *VFUN 一元数学函数 ====================

    def sqrt(self, out=None):
        """平方根 SQRT。

        Args:
            out: 输出数组，默认 self。

        Returns:
            out 数组。
        """
        out = self if out is None else out
        self.mac.vfun(out, "SQRT", self)
        return out

    def exp(self, out=None):
        """指数函数 EXP。

        Args:
            out: 输出数组，默认 self。

        Returns:
            out 数组。
        """
        out = self if out is None else out
        self.mac.vfun(out, "EXP", self)
        return out

    def log(self, out=None):
        """自然对数 LOG。

        Args:
            out: 输出数组，默认 self。

        Returns:
            out 数组。
        """
        out = self if out is None else out
        self.mac.vfun(out, "LOG", self)
        return out

    def log10(self, out=None):
        """常用对数 LOG10。

        Args:
            out: 输出数组，默认 self。

        Returns:
            out 数组。
        """
        out = self if out is None else out
        self.mac.vfun(out, "LOG10", self)
        return out

    def sin(self, out=None):
        """正弦 SIN。

        Args:
            out: 输出数组，默认 self。

        Returns:
            out 数组。
        """
        out = self if out is None else out
        self.mac.vfun(out, "SIN", self)
        return out

    def cos(self, out=None):
        """余弦 COS。

        Args:
            out: 输出数组，默认 self。

        Returns:
            out 数组。
        """
        out = self if out is None else out
        self.mac.vfun(out, "COS", self)
        return out

    def tan(self, out=None):
        """正切 TAN。

        Args:
            out: 输出数组，默认 self。

        Returns:
            out 数组。
        """
        out = self if out is None else out
        self.mac.vfun(out, "TAN", self)
        return out

    def asin(self, out=None):
        """反正弦 ASIN。

        Args:
            out: 输出数组，默认 self。

        Returns:
            out 数组。
        """
        out = self if out is None else out
        self.mac.vfun(out, "ASIN", self)
        return out

    def acos(self, out=None):
        """反余弦 ACOS。

        Args:
            out: 输出数组，默认 self。

        Returns:
            out 数组。
        """
        out = self if out is None else out
        self.mac.vfun(out, "ACOS", self)
        return out

    def atan(self, out=None):
        """反正切 ATAN。

        Args:
            out: 输出数组，默认 self。

        Returns:
            out 数组。
        """
        out = self if out is None else out
        self.mac.vfun(out, "ATAN", self)
        return out

    def sinh(self, out=None):
        """双曲正弦 SINH。

        Args:
            out: 输出数组，默认 self。

        Returns:
            out 数组。
        """
        out = self if out is None else out
        self.mac.vfun(out, "SINH", self)
        return out

    def cosh(self, out=None):
        """双曲余弦 COSH。

        Args:
            out: 输出数组，默认 self。

        Returns:
            out 数组。
        """
        out = self if out is None else out
        self.mac.vfun(out, "COSH", self)
        return out

    def tanh(self, out=None):
        """双曲正切 TANH。

        Args:
            out: 输出数组，默认 self。

        Returns:
            out 数组。
        """
        out = self if out is None else out
        self.mac.vfun(out, "TANH", self)
        return out

    def nint(self, out=None):
        """四舍五入 NINT。

        Args:
            out: 输出数组，默认 self。

        Returns:
            out 数组。
        """
        out = self if out is None else out
        self.mac.vfun(out, "NINT", self)
        return out

    def not_(self, out=None):
        """逻辑非 NOT。

        Args:
            out: 输出数组，默认 self。

        Returns:
            out 数组。
        """
        out = self if out is None else out
        self.mac.vfun(out, "NOT", self)
        return out

    def powr(self, exponent, out=None):
        """幂函数 PWR。

        ParR = Par1 ** CON1

        Args:
            exponent: 指数 CON1。
            out: 输出数组，默认 self。

        Returns:
            out 数组。
        """
        out = self if out is None else out
        self.mac.vfun(out, "PWR", self, con1=exponent)
        return out

    def comp(self, out=None):
        """压缩 COMP。

        选择性压缩数据集，"True"（*VMASK）的值被压缩写入 ParR。

        Args:
            out: 输出数组，默认 self。

        Returns:
            out 数组。
        """
        out = self if out is None else out
        self.mac.vfun(out, "COMP", self)
        return out

    def expa(self, out=None):
        """扩展 EXPA。

        COMP 的逆操作，将数据按 *VMASK 位置展开。

        Args:
            out: 输出数组，默认 self。

        Returns:
            out 数组。
        """
        out = self if out is None else out
        self.mac.vfun(out, "EXPA", self)
        return out

    def dircos(self, out=None):
        """主应力方向余弦 DIRCOS。

        Par1 包含 nX6 分量应力，输出 nX9 方向余弦。

        Args:
            out: 输出数组（需 9 列），默认 self。

        Returns:
            out 数组。
        """
        out = self if out is None else out
        self.mac.vfun(out, "DIRCOS", self)
        return out

    def prin(self, out=None):
        """主应力 PRIN。

        Par1 包含 nX6 分量应力，输出 nX5 主应力。

        Args:
            out: 输出数组（需 5 列），默认 self。

        Returns:
            out 数组。
        """
        out = self if out is None else out
        self.mac.vfun(out, "PRIN", self)
        return out

    def euler(self, out=None):
        """欧拉角 EULER。

        Par1 包含 nX6 分量应力，输出 nX3 欧拉角。

        Args:
            out: 输出数组（需 3 列），默认 self。

        Returns:
            out 数组。
        """
        out = self if out is None else out
        self.mac.vfun(out, "EULER", self)
        return out

    # ==================== *VOPER 二元运算 ====================

    def add(self, other, out=None):
        """加法 ADD。

        ParR = Par1 + Par2

        Args:
            other: 右操作数（Array1、标量或常量）。
            out: 输出数组，默认 self。

        Returns:
            out 数组。
        """
        out = self if out is None else out
        self.mac.voper(out, self, "ADD", other)
        return out

    def sub(self, other, out=None):
        """减法 SUB。

        ParR = Par1 - Par2

        Args:
            other: 右操作数（Array1、标量或常量）。
            out: 输出数组，默认 self。

        Returns:
            out 数组。
        """
        out = self if out is None else out
        self.mac.voper(out, self, "SUB", other)
        return out

    def mul(self, other, out=None):
        """乘法 MULT。

        ParR = Par1 * Par2

        Args:
            other: 右操作数（Array1、标量或常量）。
            out: 输出数组，默认 self。

        Returns:
            out 数组。
        """
        out = self if out is None else out
        self.mac.voper(out, self, "MULT", other)
        return out

    def div(self, other, out=None):
        """除法 DIV。

        ParR = Par1 / Par2（除以零结果为 0）

        Args:
            other: 右操作数（Array1、标量或常量）。
            out: 输出数组，默认 self。

        Returns:
            out 数组。
        """
        out = self if out is None else out
        self.mac.voper(out, self, "DIV", other)
        return out

    def vmin(self, other, out=None):
        """逐元素最小值 MIN。

        ParR = min(Par1, Par2)，对每个元素取较小值。

        Args:
            other: 右操作数（Array1、标量或常量）。
            out: 输出数组，默认 self。

        Returns:
            out 数组。
        """
        out = self if out is None else out
        self.mac.voper(out, self, "MIN", other)
        return out

    def vmax(self, other, out=None):
        """逐元素最大值 MAX。

        ParR = max(Par1, Par2)，对每个元素取较大值。

        Args:
            other: 右操作数（Array1、标量或常量）。
            out: 输出数组，默认 self。

        Returns:
            out 数组。
        """
        out = self if out is None else out
        self.mac.voper(out, self, "MAX", other)
        return out

    def lt(self, other, out=None):
        """小于比较 LT。

        Par1 < Par2 时为 1.0，否则 0.0

        Args:
            other: 右操作数（Array1、标量或常量）。
            out: 输出数组，默认 self。

        Returns:
            out 数组。
        """
        out = self if out is None else out
        self.mac.voper(out, self, "LT", other)
        return out

    def le(self, other, out=None):
        """小于等于比较 LE。

        Par1 <= Par2 时为 1.0，否则 0.0

        Args:
            other: 右操作数（Array1、标量或常量）。
            out: 输出数组，默认 self。

        Returns:
            out 数组。
        """
        out = self if out is None else out
        self.mac.voper(out, self, "LE", other)
        return out

    def eq(self, other, out=None):
        """等于比较 EQ。

        Par1 = Par2 时为 1.0，否则 0.0

        Args:
            other: 右操作数（Array1、标量或常量）。
            out: 输出数组，默认 self。

        Returns:
            out 数组。
        """
        out = self if out is None else out
        self.mac.voper(out, self, "EQ", other)
        return out

    def ne(self, other, out=None):
        """不等于比较 NE。

        Par1 != Par2 时为 1.0，否则 0.0

        Args:
            other: 右操作数（Array1、标量或常量）。
            out: 输出数组，默认 self。

        Returns:
            out 数组。
        """
        out = self if out is None else out
        self.mac.voper(out, self, "NE", other)
        return out

    def ge(self, other, out=None):
        """大于等于比较 GE。

        Par1 >= Par2 时为 1.0，否则 0.0

        Args:
            other: 右操作数（Array1、标量或常量）。
            out: 输出数组，默认 self。

        Returns:
            out 数组。
        """
        out = self if out is None else out
        self.mac.voper(out, self, "GE", other)
        return out

    def gt(self, other, out=None):
        """大于比较 GT。

        Par1 > Par2 时为 1.0，否则 0.0

        Args:
            other: 右操作数（Array1、标量或常量）。
            out: 输出数组，默认 self。

        Returns:
            out 数组。
        """
        out = self if out is None else out
        self.mac.voper(out, self, "GT", other)
        return out

    def der1(self, other, out=None):
        """一阶导数 DER1。

        ParR = d(Par1) / d(Par2)
        Par2 必须升序排列。

        Args:
            other: 自变量数组（Par2）。
            out: 输出数组，默认 self。

        Returns:
            out 数组。
        """
        out = self if out is None else out
        self.mac.voper(out, self, "DER1", other)
        return out

    def der2(self, other, out=None):
        """二阶导数 DER2。

        ParR = d²(Par1) / d(Par2)²

        Args:
            other: 自变量数组（Par2）。
            out: 输出数组，默认 self。

        Returns:
            out 数组。
        """
        out = self if out is None else out
        self.mac.voper(out, self, "DER2", other)
        return out

    def int1(self, other, con1=0, out=None):
        """单积分 INT1。

        ParR = ∫Par1 d(Par2)，CON1 为积分常数。

        Args:
            other: 自变量数组（Par2）。
            con1: 积分常数。
            out: 输出数组，默认 self。

        Returns:
            out 数组。
        """
        out = self if out is None else out
        self.mac.voper(out, self, "INT1", other, con1=con1)
        return out

    def int2(self, other, con1=0, con2=0, out=None):
        """双积分 INT2。

        ParR = ∫∫Par1 d(Par2)，CON1/CON2 为第一/第二积分常数。
        若 Par1 包含加速度数据，CON1 为初速度，CON2 为初位移。

        Args:
            other: 自变量数组（Par2）。
            con1: 第一积分常数（初速度）。
            con2: 第二积分常数（初位移）。
            out: 输出数组，默认 self。

        Returns:
            out 数组。
        """
        out = self if out is None else out
        self.mac.voper(out, self, "INT2", other, con1=con1, con2=con2)
        return out

    def dot(self, other, out=None):
        """点积 DOT。

        Par1 和 Par2 必须都是 3 列数据（i, j, k 向量分量）。
        ParR = Par1 · Par2（标量结果，每个向量行输出一个点积值）。

        Args:
            other: 右操作数向量数组（3 列）。
            out: 输出数组，默认 self。

        Returns:
            out 数组。
        """
        out = self if out is None else out
        self.mac.voper(out, self, "DOT", other)
        return out

    def cross(self, other, out=None):
        """叉积 CROSS。

        Par1、Par2 和 ParR 都必须是 3 列数据（i, j, k 向量分量）。
        ParR = Par1 × Par2

        Args:
            other: 右操作数向量数组（3 列）。
            out: 输出数组（3 列），默认 self。

        Returns:
            out 数组。
        """
        out = self if out is None else out
        self.mac.voper(out, self, "CROSS", other)
        return out

    def atn2(self, other, out=None):
        """二参数反正切 ATN2。

        ParR = arctan(Par1/Par2)，考虑各分量符号。

        Args:
            other: 右操作数（Array1、标量或常量）。
            out: 输出数组，默认 self。

        Returns:
            out 数组。
        """
        out = self if out is None else out
        self.mac.voper(out, self, "ATN2", other)
        return out

    def gath(self, other, out=None):
        """Gather 收集操作。

        根据 Par2 中的位置编号，从 Par1 收集对应位置的值到 ParR。
        例如 Par1 = 10,20,30,40，Par2 = 2,4,1，则 ParR = 20,40,10。

        Args:
            other: 位置编号数组（Par2）。
            out: 输出数组，默认 self。

        Returns:
            out 数组。
        """
        out = self if out is None else out
        self.mac.voper(out, self, "GATH", other)
        return out

    def scat(self, other, out=None):
        """Scatter 散布操作。

        根据 Par2 中的位置编号，将 Par1 的值散布到 ParR。
        例如 Par1 = 10,20,30,40,50，Par2 = 2,1,0,5,3，
        则 ParR = 20,10,50,0,40。

        Args:
            other: 位置编号数组（Par2）。
            out: 输出数组，默认 self。

        Returns:
            out 数组。
        """
        out = self if out is None else out
        self.mac.voper(out, self, "SCAT", other)
        return out
