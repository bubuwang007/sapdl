from sapdl.core.ast import Array1DefineNode, Array1Node, Array1DeleteNode
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
