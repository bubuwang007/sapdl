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
