from sapdl.core.ast import (
    StringArrayNode,
    StringArrayDefineNode,
    StringArrayDeleteNode,
)
from .apdl_object import ApdlObject
from .number_parameter import NumberParameter
from .string_array_element import StringArrayElement


class StringArray(ApdlObject):
    """字符串数组（STRING Array）。

    字符串数组是一种参数数组，每个元素可以存储一个完整的字符串。
    与字符数组（CharArray）不同，字符数组每个元素只存储单个字符。
    """

    length: NumberParameter
    str_length: NumberParameter

    def _new(self, length=None, str_length=None):
        """创建字符串数组。

        Args:
            length: 数组长度（一维元素个数）。
            str_length: 每个元素的最大字符串长度，默认 32。
        """
        self.str_length = NumberParameter(self.mac, name=f"{self.name}_c")
        self.length = NumberParameter(self.mac, name=f"{self.name}_1")
        self.length._new(length)
        self.str_length._new(str_length)
        if length is not None:
            self.mac.body.add(StringArrayDefineNode(StringArrayNode(self)))
        return self

    def delete(self):
        self._delete()
        self.mac.symbol_table.remove(self.name)
        self._alive = False

    def _delete(self):
        self.mac.body.add(StringArrayDeleteNode(StringArrayNode(self)))

    # ==================== 元素获取 ====================

    def __getitem__(self, index):
        if isinstance(index, tuple) and len(index) == 2:
            return StringArrayElement(self, (index[0], index[1]))
        return StringArrayElement(self, (1, index))

    def __iter__(self):
        for i in self.mac.range(1, self.length):
            yield self[i]

    def enumerate(self, start=1):
        for i in self.mac.range(1, self.length):
            yield i + (start - 1), self[i]

    # ==================== 输出 ====================

    def output(self, key=None, format="%C"):
        """输出字符串数组到文件。

        Args:
            key: 输出文件名的键，默认使用参数名。
            format: 格式化字符串，APDL *VWRITE 格式，默认 '%C'（字符格式）。
        """
        import os

        key = self.name if key is None else key
        p = os.path.join(self.mac.output_path, str(key))
        with self.mac.files.open(p) as f:
            f.write_c(f"{self}(1)", format=format)
        self.mac.add_output(key, type="StringArray")

    @classmethod
    def parse(cls, path):
        """从文件解析字符串数组值。

        Args:
            path: 文件路径。

        Returns:
            list[str]: 解析出的字符串值列表。
        """
        with open(path, "r", encoding="u8") as f:
            values = [line.strip() for line in f if line.strip()]
        return values

    # ==================== 填充方法 ====================

    def fill(self, iter_values, start=1):
        """填充字符串数组。

        Args:
            iter_values: 一维可迭代对象。
            start: 起始索引（1-based），默认 1。

        Returns:
            self: 返回自身，支持链式调用。
        """
        for idx, value in enumerate(iter_values, start=start):
            row = 1
            if isinstance(value, str) and len(value) > 32:
                for pos in range(0, len(value), 32):
                    chunk = value[pos : pos + 32]
                    self[row, idx] << chunk
                    row += 32
            else:
                self[row, idx] << value
                row += 32
        return self
