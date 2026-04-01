from sapdl.core.ast import (
    Table1Node,
    Table1DefineNode,
    Table1DeleteNode,
)
from .apdl_object import ApdlObject
from .number_parameter import NumberParameter
from .table1_element import Table1Element


class Table1(ApdlObject):
    """Table1（1维表格）。

    APDL TABLE 是一种特殊的参数数组，使用实数（非整数）作为索引。
    表格的第一行（行0）存储索引值，用于插值查找。
    """

    length: NumberParameter

    def _new(self, length=None):
        """创建 Table1。

        Args:
            length: 表格长度（数据点个数）。
        """
        self.length = NumberParameter(self.mac, name=f"{self.name}_1")
        self.length._new(length)
        if length is not None:
            self.mac.body.add(Table1DefineNode(Table1Node(self)))
        return self

    def delete(self):
        self._delete()
        self.mac.symbol_table.remove(self.name)
        self._alive = False

    def _delete(self):
        self.mac.body.add(Table1DeleteNode(Table1Node(self)))

    # ==================== 元素获取 ====================

    def __getitem__(self, index):
        return Table1Element(self, index)

    def __iter__(self):
        for i in self.mac.range(1, self.length):
            yield self[i]

    def enumerate(self, start=1):
        for i in self.mac.range(1, self.length):
            yield i + (start - 1), self[i]

    # ==================== 填充方法 ====================

    def fill(self, index_values, data_values, start=1):
        """填充表格数据。

        Args:
            index_values: 索引值列表（一维可迭代对象）。
            data_values: 数据值列表（一维可迭代对象）。

        Returns:
            self: 返回自身，支持链式调用。
        """
        for idx, (idx_val, data_val) in enumerate(zip(index_values, data_values), start=start):
            self[start + idx - 1] << data_val
            self[start + idx - 1, 0] << idx_val
        return self
