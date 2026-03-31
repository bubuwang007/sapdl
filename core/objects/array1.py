from sapdl.core.ast import (
    Array1DefineNode,
    Array1Node,
    Array1DeleteNode,
    Array1FuncRetNumberNode,
    Array1AssignNode,
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
        if isinstance(value, (int, float)):
            self.ones(value=value)
        elif isinstance(value, Array1):
            value.copy_to(self)
        else:
            self.mac.body.add(Array1AssignNode(Array1Node(self), value))

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
