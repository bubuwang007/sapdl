from sapdl.core.ast import (
    CharArrayNode,
    CharArrayDefineNode,
    CharArrayDeleteNode,
)
from .apdl_object import ApdlObject
from .number_parameter import NumberParameter
from .str_array_elememt import StrArrayElement


class CharArray(ApdlObject):
    """字符数组（CHAR Array）。"""

    length: NumberParameter

    def _new(self, length=None):
        """创建字符数组。

        Args:
            length: 数组长度（一维元素个数）。
        """
        self.length = NumberParameter(self.mac, name=f"{self.name}_1")
        self.length._new(length)
        if length is not None:
            self.mac.body.add(CharArrayDefineNode(CharArrayNode(self)))
        return self

    def delete(self):
        self._delete()
        self.mac.symbol_table.remove(self.name)
        self._alive = False

    def _delete(self):
        self.mac.body.add(CharArrayDeleteNode(CharArrayNode(self)))

    # ==================== 元素获取 ====================

    def __getitem__(self, index):
        return StrArrayElement(self, index)

    def __iter__(self):
        for i in self.mac.range(1, self.length):
            yield self[i]

    def enumerate(self, start=1):
        for i in self.mac.range(1, self.length):
            yield i + (start - 1), self[i]

    # ==================== 输出 ====================

    def output(self, key=None, format="%C"):
        """输出字符数组到文件。

        Args:
            key: 输出文件名的键，默认使用参数名。
            format: 格式化字符串，APDL *VWRITE 格式，默认 '%C'（字符格式）。
        """
        import os

        key = self.name if key is None else key
        p = os.path.join(self.mac.output_path, str(key))
        with self.mac.files.open(p) as f:
            f.write_c(f"{self}(1)", format=format)
        self.mac.add_output(key, type="CharArray")

    @classmethod
    def parse(cls, path):
        """从文件解析字符数组值。

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
        """填充字符数组。

        Args:
            iter_values: 一维可迭代对象。
            start: 起始索引（1-based），默认 1。

        Returns:
            self: 返回自身，支持链式调用。
        """
        values = list(iter_values)
        batch_size = 10
        for i in range(0, len(values), batch_size):
            batch = values[i : i + batch_size]
            vals = []
            for v in batch:
                if isinstance(v, str):
                    vals.append(f"'{v}'")
                else:
                    vals.append(str(v))
            if len(values) - i < batch_size:
                self.mac.run(f"{self.name}({start})={','.join(vals)}")
            else:
                self.mac.run(f"{self.name}({start})={','.join(vals)}")
                start += batch_size
        return self
