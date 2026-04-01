from .apdl_object import ApdlObject
from sapdl.core.ast import (
    StringParameterNode,
    StringDeleteNode,
    StringAssignNode,
    StringFuncNode,
)


class StringParameter(ApdlObject):

    def _new(self, value=None):
        if value is not None:
            self.assign(value)
        return self

    def delete(self):
        self._delete()
        self.mac.symbol_table.remove(self.name)
        self._alive = False

    def _delete(self):
        self.mac.body.add(StringDeleteNode(StringParameterNode(self)))

    def assign(self, value):
        if not self._alive:
            raise RuntimeError(
                f"Cannot assign to deleted StringParameter '{self.name}'."
            )
        self.mac.body.add(StringAssignNode(StringParameterNode(self), value))

    def __lshift__(self, other):
        self.assign(other)

    # ==================== 字符串运算 ====================

    def __add__(self, other) -> StringFuncNode:
        """字符串连接 (+)

        Args:
            other: 右操作数（StringParameter 或字符串）

        Returns:
            StringFuncNode: 连接后的结果
        """
        return StringFuncNode("STRCAT", self, other)

    def __radd__(self, other) -> StringFuncNode:
        """反射加法 (other + self)"""
        return StringFuncNode("STRCAT", other, self)

    # ==================== 字符串变换（返回 StringFuncNode） ====================

    def upper(self) -> StringFuncNode:
        """转大写 UPCASE

        Returns:
            StringFuncNode: 大写字符串
        """
        return StringFuncNode("UPCASE", self)

    def lower(self) -> StringFuncNode:
        """转小写 LWCASE

        Returns:
            StringFuncNode: 小写字符串
        """
        return StringFuncNode("LWCASE", self)

    def substr(self, nloc, nchar) -> StringFuncNode:
        """提取子串 STRSUB

        Args:
            nloc: 起始位置（1-based）
            nchar: 提取字符数

        Returns:
            StringFuncNode: 子串
        """
        return StringFuncNode("STRSUB", self, nloc, nchar)

    def fill(self, str2, nloc) -> StringFuncNode:
        """在指定位置插入字符串 STRFILL

        Args:
            str2: 要插入的字符串
            nloc: 插入位置（1-based）

        Returns:
            StringFuncNode: 插入后的字符串
        """
        return StringFuncNode("STRFILL", self, str2, nloc)

    def length(self) -> StringFuncNode:
        """返回最后一个非空白字符的位置 STRLENG

        Returns:
            StringFuncNode: 最后非空字符位置
        """
        return StringFuncNode("STRLENG", self)

    def pos(self, str2) -> StringFuncNode:
        """返回子串位置 STRPOS

        Args:
            str2: 要搜索的子串

        Returns:
            StringFuncNode: 子串位置（1-based，未找到返回 0）
        """
        return StringFuncNode("STRPOS", self, str2)

    def compress(self) -> StringFuncNode:
        """移除所有空格 STRCOMP

        Returns:
            StringFuncNode: 无空格字符串
        """
        return StringFuncNode("STRCOMP", self)

    def left_justify(self) -> StringFuncNode:
        """左对齐 STRLEFT

        Returns:
            StringFuncNode: 左对齐字符串
        """
        return StringFuncNode("STRLEFT", self)

    # ==================== 赋值变换（变换结果写入自身） ====================

    def assign_upper(self):
        """转换为大写并赋值给自身"""
        self.assign(self.upper())

    def assign_lower(self):
        """转换为小写并赋值给自身"""
        self.assign(self.lower())

    def assign_compress(self):
        """移除所有空格并赋值给自身"""
        self.assign(self.compress())

    def assign_left_justify(self):
        """左对齐并赋值给自身"""
        self.assign(self.left_justify())

    def cat(self, str2):
        self.assign(self + str2)

    # ==================== 数值转换 ====================

    def to_number(self) -> StringFuncNode:
        """将数字字符串转换为数值 VALCHR

        适用于十进制数字字符串。

        Returns:
            StringFuncNode: 数值
        """
        return StringFuncNode("VALCHR", self)

    def oct_to_number(self) -> StringFuncNode:
        """将八进制数字字符串转换为数值 VALOCT

        Returns:
            StringFuncNode: 数值
        """
        return StringFuncNode("VALOCT", self)

    def hex_to_number(self) -> StringFuncNode:
        """将十六进制数字字符串转换为数值 VALHEX

        Returns:
            StringFuncNode: 数值
        """
        return StringFuncNode("VALHEX", self)

    # ==================== 输出 ====================

    def output(self, key=None, format="%C"):
        """输出字符串参数到文件。

        Args:
            key: 输出文件名的键，默认使用参数名。
            format: 格式化字符串，APDL *VWRITE 格式，默认 '%C'（字符格式）。
        """
        import os

        key = self.name if key is None else key
        p = os.path.join(self.mac.output_path, str(key))
        with self.mac.files.open(p) as f:
            f.write_c(self, format=format)
        self.mac.add_output(key, type="StringParameter")

    @classmethod
    def parse(cls, path):
        """从文件解析字符串值。

        Args:
            path: 文件路径。

        Returns:
            str: 解析出的字符串值。
        """
        with open(path, "r", encoding="u8") as f:
            value = f.read().strip()
        return value
