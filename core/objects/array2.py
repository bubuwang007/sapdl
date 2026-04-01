from sapdl.core.ast import (
    Array2Node,
    Array2DefineNode,
    Array2DeleteNode,
)
from .apdl_object import ApdlObject
from .number_parameter import NumberParameter
from .array_element import ArrayElement
from .array1view import Array1View


class Row:

    def __init__(self, array2, row_idx):
        self._array2 = array2
        self._row_idx = row_idx
        self.mac = array2.mac
        self.length = array2.col

    def __getitem__(self, index):
        return ArrayElement(self._array2, (self._row_idx, index))

    def __iter__(self):
        for col in self.mac.range(1, self._array2.col):
            yield self[col]


class Array2(ApdlObject):
    row: NumberParameter
    col: NumberParameter

    def _new(self, row=None, col=None):
        self.row = NumberParameter(self.mac, name=f"{self.name}_r")
        self.row._new(row)
        self.col = NumberParameter(self.mac, name=f"{self.name}_c")
        self.col._new(col)
        if row is not None and col is not None:
            self.mac.body.add(Array2DefineNode(Array2Node(self)))
        return self

    def delete(self):
        self._delete()
        self.mac.symbol_table.remove(self.name)
        self._alive = False

    def _delete(self):
        self.mac.body.add(Array2DeleteNode(Array2Node(self)))

    def assign(self, value):
        if isinstance(value, (int, float)):
            self.ones(value=value)
        elif isinstance(value, Array2):
            value.copy_to(self)
        else:
            raise ValueError("Unsupported assignment value type for Array2.")

    def __lshift__(self, other):
        self.assign(other)

    # ==================== 输出 ====================

    def output(self, key=None, format="ES20.12E3"):
        import os

        key = self.name if key is None else key
        p = os.path.join(self.mac.output_path, str(key))
        self.mac.mwrite(self, p)
        self.mac.run(f"({format})")

        p = os.path.join(self.mac.output_path, f"{key}_row")
        with self.mac.files.open(p) as f:
            f.write(self.row, format=format)

        p = os.path.join(self.mac.output_path, f"{key}_col")
        with self.mac.files.open(p) as f:
            f.write(self.col, format=format)

        self.mac.add_output(key, type="Array2")

    @classmethod
    def parse(cls, path):
        import os
        import numpy as np
        from .number_parameter import NumberParameter

        fname = os.path.basename(path)
        with open(path, "r", encoding="u8") as f:
            data = np.loadtxt(f)

        row_path = os.path.join(os.path.dirname(path), f"{fname}_row")
        row = NumberParameter.parse(row_path)

        col_path = os.path.join(os.path.dirname(path), f"{fname}_col")
        col = NumberParameter.parse(col_path)

        data = data.reshape((int(row), int(col)))
        return data

    # ==================== 元素获取 ====================

    def __getitem__(self, index):
        if isinstance(index, tuple) and len(index) == 2:
            return ArrayElement(self, index)
        else:
            return Array1View(self, index)

    def iter_row(self):
        for row_idx in self.mac.range(1, self.row):
            yield Row(self, row_idx)

    def iter_col(self):
        for col_idx in self.mac.range(1, self.col):
            yield Array1View(self, col_idx)

    def __iter__(self):
        return self.iter_col()

    def enumerate_row(self, start=1):
        for row_idx in self.mac.range(1, self.row):
            yield row_idx + (start - 1), Row(self, row_idx)

    def enumerate_col(self, start=1):
        for col_idx in self.mac.range(1, self.col):
            yield col_idx + (start - 1), Array1View(self, col_idx)

    # ==================== 初始化方法 ====================

    def fill(self, iter_iter, startrow=1, startcol=1):
        """填充二维数据。

        Args:
            iter_iter: 二维可迭代对象。
            startrow: 起始行（1-based）。
            startcol: 起始列（1-based）。

        Returns:
            self: 返回自身，支持链式调用。
        """
        for i in range(startcol, len(iter_iter[0]) + 1):
            startrow_cur = startrow
            for j in range(0, len(iter_iter), 10):
                if len(iter_iter) - j < 10:
                    d = ",".join(f"{k[i - 1]}" for k in iter_iter[j:])
                    self.mac.run(f"{self.name}({startrow_cur},{i})={d}")
                else:
                    d = ",".join(f"{k[i - 1]}" for k in iter_iter[j : j + 10])
                    self.mac.run(f"{self.name}({startrow_cur},{i})={d}")
                    startrow_cur += 10
        return self

    def zeros(self):
        """填充零数组。

        Returns:
            self: 返回自身，支持链式调用。
        """
        for col in self.iter_col():
            col.zeros()
        return self

    def ones(self, value=1):
        """填充指定值的数组。

        Args:
            value: 填充值。

        Returns:
            self: 返回自身，支持链式调用。
        """
        for col in self.iter_col():
            col.ones(value)
        return self

    def rand(self, lower=0, upper=1):
        """填充均匀分布随机数。

        Args:
            lower: 下界。
            upper: 上界。

        Returns:
            self: 返回自身，支持链式调用。
        """
        for col in self.iter_col():
            col.rand(lower, upper)
        return self

    def gaussian_distribution(self, mean=0.0, stddev=1.0):
        """填充高斯分布随机数。

        Args:
            mean: 均值。
            stddev: 标准差。

        Returns:
            self: 返回自身，支持链式调用。
        """
        for col in self.iter_col():
            col.gaussian_distribution(mean, stddev)
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
        for col in self.iter_col():
            col.triangular_distribution(lower, peak, upper)
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
        for col in self.iter_col():
            col.beta_distribution(lower, upper, alpha, beta)
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
        for col in self.iter_col():
            col.gamma_distribution(lower, alpha, beta)
        return self

    # ==================== 复制和克隆 ====================

    def zeros_like(self, name=None):
        """创建相同形状的零数组。

        Args:
            name: 新数组名称，默认使用原名称。

        Returns:
            Array2: 新的零数组。
        """
        return self.mac.Array2(self.row, self.col, name=name)

    def copy_to(self, other):
        """复制数据到另一个数组。

        Args:
            other: 目标数组。
        """
        self.mac.mfun(other, "COPY", self)

    def clone(self, name=None):
        """克隆数组。

        Args:
            name: 克隆数组的名称。

        Returns:
            Array2: 克隆的新数组。
        """
        other = self.zeros_like(name=name)
        self.copy_to(other)
        return other

    def transpose_like(self, name=None):
        """创建转置形状的数组。

        Args:
            name: 新数组名称。

        Returns:
            Array2: 转置形状的新数组。
        """
        return self.mac.Array2(self.col, self.row, name=name)

    def transpose_new(self, name=None):
        """创建转置后的副本。

        Args:
            name: 新数组名称。

        Returns:
            Array2: 转置后的新数组。
        """
        out = self.transpose_like(name=name)
        self.transpose(out=out)
        return out

    def transpose(self, out=None):
        """转置数组。

        Args:
            out: 输出数组，默认 self。

        Returns:
            out 数组。
        """
        out = self if out is None else out
        self.mac.mfun(out, "TRAN", self)
        return out

    def invert(self):
        """求逆矩阵。

        Args:
            out: 输出数组，默认 self。

        Returns:
            out 数组。
        """
        self.mac.moper(self, self, "INVERT")
        return self

    def solve(self, b, out=None):
        """求解线性方程组 Ax = b。

        Args:
            b: 右端向量（Array1）。
            out: 输出数组，默认新建。

        Returns:
            Array1: 解向量。
        """
        if out is None:
            out = self.mac.Array1(self.row)
        self.mac.moper(out, self, "SOLVE", b)
        return out

    def matrix_mul(self, other):
        """矩阵乘法。

        Args:
            other: 右乘矩阵（Array2）。

        Returns:
            Array2: 乘积矩阵。
        """
        out = self.mac.Array2(self.row, other.col)
        self.mac.moper(out, self, "MULT", other)
        return out

    # ==================== 统计数据（按列） ====================

    def _stat(self, func_name, out=None):
        """通用列统计方法。

        Args:
            func_name: APDL *VSCFUN 函数名。
            out: 输出数组，默认新建 Array1。

        Returns:
            Array1: 每列为该列的统计值。
        """
        if out is None:
            out = self.mac.Array1(self.col)
        for i, col_view in self.enumerate_col():
            out[i] << col_view._stat(func_name)
        return out

    def max(self, out=None):
        """每列最大值。

        Args:
            out: 输出数组，默认新建 Array1。

        Returns:
            Array1: 每列为该列的最大值。
        """
        return self._stat("MAX", out=out)

    def min(self, out=None):
        """每列最小值。

        Args:
            out: 输出数组，默认新建 Array1。

        Returns:
            Array1: 每列为该列的最小值。
        """
        return self._stat("MIN", out=out)

    def sum(self, out=None):
        """每列元素和。

        Args:
            out: 输出数组，默认新建 Array1。

        Returns:
            Array1: 每列为该列的元素和。
        """
        return self._stat("SUM", out=out)

    def mean(self, out=None):
        """每列元素均值。

        Args:
            out: 输出数组，默认新建 Array1。

        Returns:
            Array1: 每列为该列的均值。
        """
        return self._stat("MEAN", out=out)

    def median(self, out=None):
        """每列元素中位数。

        Args:
            out: 输出数组，默认新建 Array1。

        Returns:
            Array1: 每列为该列的中位数。
        """
        return self._stat("MEDI", out=out)

    def variance(self, out=None):
        """每列元素方差。

        Args:
            out: 输出数组，默认新建 Array1。

        Returns:
            Array1: 每列为该列的方差。
        """
        return self._stat("VARI", out=out)

    def std(self, out=None):
        """每列元素标准差。

        Args:
            out: 输出数组，默认新建 Array1。

        Returns:
            Array1: 每列为该列的标准差。
        """
        return self._stat("STDV", out=out)

    def rms(self, out=None):
        """每列元素均方根。

        Args:
            out: 输出数组，默认新建 Array1。

        Returns:
            Array1: 每列为该列的均方根。
        """
        return self._stat("RMS", out=out)

    def argmax(self, out=None):
        """每列最大值的行索引。

        Args:
            out: 输出数组，默认新建 Array1。

        Returns:
            Array1: 每列为该列最大值所在的行索引。
        """
        return self._stat("LMAX", out=out)

    def argmin(self, out=None):
        """每列最小值的行索引。

        Args:
            out: 输出数组，默认新建 Array1。

        Returns:
            Array1: 每列为该列最小值所在的行索引。
        """
        return self._stat("LMIN", out=out)

    def first_nonzero(self, out=None):
        """每列第一个非零值的行索引。

        Args:
            out: 输出数组，默认新建 Array1。

        Returns:
            Array1: 每列为该列第一个非零值的行索引。
        """
        return self._stat("FIRST", out=out)

    def last_nonzero(self, out=None):
        """每列最后一个非零值的行索引。

        Args:
            out: 输出数组，默认新建 Array1。

        Returns:
            Array1: 每列为该列最后一个非零值的行索引。
        """
        return self._stat("LAST", out=out)

    # ==================== *VFUN 一元数学函数（按列） ====================

    def _vfun_col(self, method_name, *args, out=None, **kwargs):
        """通用列级一元数学函数调用。

        Args:
            method_name: Array1View 方法名。
            *args: 位置参数。
            out: 输出数组，默认 self。
            **kwargs: 关键字参数。

        Returns:
            self 或 out。
        """
        for idx, col in self.enumerate_col():
            out_col = out[idx] if out is not None else None
            getattr(col, method_name)(*args, out=out_col, **kwargs)
        return self if out is None else out

    def sqrt(self, out=None):
        """平方根 SQRT（按列）。

        Args:
            out: 输出 Array2，默认 self。

        Returns:
            self 或 out。
        """
        return self._vfun_col("sqrt", out=out)

    def exp(self, out=None):
        """指数函数 EXP（按列）。

        Args:
            out: 输出 Array2，默认 self。

        Returns:
            self 或 out。
        """
        return self._vfun_col("exp", out=out)

    def log(self, out=None):
        """自然对数 LOG（按列）。

        Args:
            out: 输出 Array2，默认 self。

        Returns:
            self 或 out。
        """
        return self._vfun_col("log", out=out)

    def log10(self, out=None):
        """常用对数 LOG10（按列）。

        Args:
            out: 输出 Array2，默认 self。

        Returns:
            self 或 out。
        """
        return self._vfun_col("log10", out=out)

    def sin(self, out=None):
        """正弦 SIN（按列）。

        Args:
            out: 输出 Array2，默认 self。

        Returns:
            self 或 out。
        """
        return self._vfun_col("sin", out=out)

    def cos(self, out=None):
        """余弦 COS（按列）。

        Args:
            out: 输出 Array2，默认 self。

        Returns:
            self 或 out。
        """
        return self._vfun_col("cos", out=out)

    def tan(self, out=None):
        """正切 TAN（按列）。

        Args:
            out: 输出 Array2，默认 self。

        Returns:
            self 或 out。
        """
        return self._vfun_col("tan", out=out)

    def asin(self, out=None):
        """反正弦 ASIN（按列）。

        Args:
            out: 输出 Array2，默认 self。

        Returns:
            self 或 out。
        """
        return self._vfun_col("asin", out=out)

    def acos(self, out=None):
        """反余弦 ACOS（按列）。

        Args:
            out: 输出 Array2，默认 self。

        Returns:
            self 或 out。
        """
        return self._vfun_col("acos", out=out)

    def atan(self, out=None):
        """反正切 ATAN（按列）。

        Args:
            out: 输出 Array2，默认 self。

        Returns:
            self 或 out。
        """
        return self._vfun_col("atan", out=out)

    def sinh(self, out=None):
        """双曲正弦 SINH（按列）。

        Args:
            out: 输出 Array2，默认 self。

        Returns:
            self 或 out。
        """
        return self._vfun_col("sinh", out=out)

    def cosh(self, out=None):
        """双曲余弦 COSH（按列）。

        Args:
            out: 输出 Array2，默认 self。

        Returns:
            self 或 out。
        """
        return self._vfun_col("cosh", out=out)

    def tanh(self, out=None):
        """双曲正切 TANH（按列）。

        Args:
            out: 输出 Array2，默认 self。

        Returns:
            self 或 out。
        """
        return self._vfun_col("tanh", out=out)

    def nint(self, out=None):
        """四舍五入 NINT（按列）。

        Args:
            out: 输出 Array2，默认 self。

        Returns:
            self 或 out。
        """
        return self._vfun_col("nint", out=out)

    def not_(self, out=None):
        """逻辑非 NOT（按列）。

        Args:
            out: 输出 Array2，默认 self。

        Returns:
            self 或 out。
        """
        return self._vfun_col("not_", out=out)

    def powr(self, exponent, out=None):
        """幂函数 PWR（按列）。

        ParR = Par1 ** CON1

        Args:
            exponent: 指数 CON1。
            out: 输出 Array2，默认 self。

        Returns:
            self 或 out。
        """
        return self._vfun_col("powr", exponent, out=out)

    def comp(self, out=None):
        """压缩 COMP（按列）。

        选择性压缩数据集，"True"（*VMASK）的值被压缩写入 ParR。

        Args:
            out: 输出 Array2，默认 self。

        Returns:
            self 或 out。
        """
        return self._vfun_col("comp", out=out)

    def expa(self, out=None):
        """扩展 EXPA（按列）。

        COMP 的逆操作，将数据按 *VMASK 位置展开。

        Args:
            out: 输出 Array2，默认 self。

        Returns:
            self 或 out。
        """
        return self._vfun_col("expa", out=out)

    # ==================== *VOPER 二元运算（按列） ====================

    def _voper_col(self, method_name, other, *args, out=None, **kwargs):
        """通用列级二元运算调用。

        Args:
            method_name: Array1View 方法名。
            other: 右操作数。
            *args: 位置参数。
            out: 输出数组，默认 self。
            **kwargs: 关键字参数。

        Returns:
            self 或 out。
        """
        other_col = None
        if isinstance(other, Array2):
            for idx, col in self.enumerate_col():
                out_col = out[idx] if out is not None else None
                other_col = other[idx]
                getattr(col, method_name)(other_col, *args, out=out_col, **kwargs)
        else:
            for idx, col in self.enumerate_col():
                out_col = out[idx] if out is not None else None
                getattr(col, method_name)(other, *args, out=out_col, **kwargs)
        return self if out is None else out

    def add(self, other, out=None):
        """加法 ADD（按列）。

        ParR = Par1 + Par2

        Args:
            other: 右操作数（Array1、Array2、Array1View、标量或常量）。
            out: 输出 Array2，默认 self。

        Returns:
            self 或 out。
        """
        return self._voper_col("add", other, out=out)

    def sub(self, other, out=None):
        """减法 SUB（按列）。

        ParR = Par1 - Par2

        Args:
            other: 右操作数（Array1、Array2、Array1View、标量或常量）。
            out: 输出 Array2，默认 self。

        Returns:
            self 或 out。
        """
        return self._voper_col("sub", other, out=out)

    def mul(self, other, out=None):
        """乘法 MULT（按列）。

        ParR = Par1 * Par2

        Args:
            other: 右操作数（Array1、Array2、Array1View、标量或常量）。
            out: 输出 Array2，默认 self。

        Returns:
            self 或 out。
        """
        return self._voper_col("mul", other, out=out)

    def div(self, other, out=None):
        """除法 DIV（按列）。

        ParR = Par1 / Par2（除以零结果为 0）

        Args:
            other: 右操作数（Array1、Array2、Array1View、标量或常量）。
            out: 输出 Array2，默认 self。

        Returns:
            self 或 out。
        """
        return self._voper_col("div", other, out=out)

    def vmin(self, other, out=None):
        """逐元素最小值 MIN（按列）。

        ParR = min(Par1, Par2)，对每个元素取较小值。

        Args:
            other: 右操作数（Array1、Array2、Array1View、标量或常量）。
            out: 输出 Array2，默认 self。

        Returns:
            self 或 out。
        """
        return self._voper_col("vmin", other, out=out)

    def vmax(self, other, out=None):
        """逐元素最大值 MAX（按列）。

        ParR = max(Par1, Par2)，对每个元素取较大值。

        Args:
            other: 右操作数（Array1、Array2、Array1View、标量或常量）。
            out: 输出 Array2，默认 self。

        Returns:
            self 或 out。
        """
        return self._voper_col("vmax", other, out=out)

    def lt(self, other, out=None):
        """小于比较 LT（按列）。

        Par1 < Par2 时为 1.0，否则 0.0

        Args:
            other: 右操作数（Array1、Array2、Array1View、标量或常量）。
            out: 输出 Array2，默认 self。

        Returns:
            self 或 out。
        """
        return self._voper_col("lt", other, out=out)

    def le(self, other, out=None):
        """小于等于比较 LE（按列）。

        Par1 <= Par2 时为 1.0，否则 0.0

        Args:
            other: 右操作数（Array1、Array2、Array1View、标量或常量）。
            out: 输出 Array2，默认 self。

        Returns:
            self 或 out。
        """
        return self._voper_col("le", other, out=out)

    def eq(self, other, out=None):
        """等于比较 EQ（按列）。

        Par1 = Par2 时为 1.0，否则 0.0

        Args:
            other: 右操作数（Array1、Array2、Array1View、标量或常量）。
            out: 输出 Array2，默认 self。

        Returns:
            self 或 out。
        """
        return self._voper_col("eq", other, out=out)

    def ne(self, other, out=None):
        """不等于比较 NE（按列）。

        Par1 != Par2 时为 1.0，否则 0.0

        Args:
            other: 右操作数（Array1、Array2、Array1View、标量或常量）。
            out: 输出 Array2，默认 self。

        Returns:
            self 或 out。
        """
        return self._voper_col("ne", other, out=out)

    def ge(self, other, out=None):
        """大于等于比较 GE（按列）。

        Par1 >= Par2 时为 1.0，否则 0.0

        Args:
            other: 右操作数（Array1、Array2、Array1View、标量或常量）。
            out: 输出 Array2，默认 self。

        Returns:
            self 或 out。
        """
        return self._voper_col("ge", other, out=out)

    def gt(self, other, out=None):
        """大于比较 GT（按列）。

        Par1 > Par2 时为 1.0，否则 0.0

        Args:
            other: 右操作数（Array1、Array2、Array1View、标量或常量）。
            out: 输出 Array2，默认 self。

        Returns:
            self 或 out。
        """
        return self._voper_col("gt", other, out=out)

    def der1(self, other, out=None):
        """一阶导数 DER1（按列）。

        ParR = d(Par1) / d(Par2)
        Par2 必须升序排列。

        Args:
            other: 自变量数组（Par2）。
            out: 输出 Array2，默认 self。

        Returns:
            self 或 out。
        """
        return self._voper_col("der1", other, out=out)

    def der2(self, other, out=None):
        """二阶导数 DER2（按列）。

        ParR = d²(Par1) / d(Par2)²

        Args:
            other: 自变量数组（Par2）。
            out: 输出 Array2，默认 self。

        Returns:
            self 或 out。
        """
        return self._voper_col("der2", other, out=out)

    def int1(self, other, con1=0, out=None):
        """单积分 INT1（按列）。

        ParR = ∫Par1 d(Par2)，CON1 为积分常数。

        Args:
            other: 自变量数组（Par2）。
            con1: 积分常数。
            out: 输出 Array2，默认 self。

        Returns:
            self 或 out。
        """
        return self._voper_col("int1", other, con1=con1, out=out)

    def int2(self, other, con1=0, con2=0, out=None):
        """双积分 INT2（按列）。

        ParR = ∫∫Par1 d(Par2)，CON1/CON2 为第一/第二积分常数。
        若 Par1 包含加速度数据，CON1 为初速度，CON2 为初位移。

        Args:
            other: 自变量数组（Par2）。
            con1: 第一积分常数（初速度）。
            con2: 第二积分常数（初位移）。
            out: 输出 Array2，默认 self。

        Returns:
            self 或 out。
        """
        return self._voper_col("int2", other, con1=con1, con2=con2, out=out)

    def atn2(self, other, out=None):
        """二参数反正切 ATN2（按列）。

        ParR = arctan(Par1/Par2)，考虑各分量符号。

        Args:
            other: 右操作数（Array1、Array2、Array1View、标量或常量）。
            out: 输出 Array2，默认 self。

        Returns:
            self 或 out。
        """
        return self._voper_col("atn2", other, out=out)
