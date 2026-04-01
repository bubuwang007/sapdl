"""ObjectsDefine - APDL 对象创建接口.

定义 APDL 参数对象的创建工厂方法，支持：
- NumberParameter：数值参数
- StringParameter：字符串参数
- Array1/Array2：数值数组
- CharArray/StringArray：字符/字符串数组
- Table1：插值表格

命名规范：
- PascalCase 方法（如 ``Array1``）：创建空对象，需指定维度
- snake_case 方法（如 ``array1``）：从数据自动推断维度并填充

作用域规则：
- 未指定 name → local 作用域，自动生成名称
- 指定 name → global 作用域
"""

from __future__ import annotations

from .args import Args
from .number_parameter import NumberParameter
from .string_parameter import StringParameter
from .array1 import Array1
from .array2 import Array2
from .char_array import CharArray
from .string_array import StringArray
from .table1 import Table1


class ObjectsDefine:
    """APDL 对象创建工厂类."""

    _var_index: int = 0
    objects = {
        "NumberParameter": NumberParameter,
        "StringParameter": StringParameter,
        "Array1": Array1,
        "Array2": Array2,
        "CharArray": CharArray,
        "StringArray": StringArray,
        "Table1": Table1,
    }

    def __init__(self):
        self.args = Args()

    def next_id(self):
        """生成下一个局部变量名称.

        Returns:
            str: 格式为 ``{name}{index}`` 的变量名，name 来自类属性。
        """
        self._var_index += 1
        return f"{self.name.lower()}{self._var_index}"

    # ==================== 标量参数 ====================

    def NumberParameter(self, value=0, name=None):
        """创建数值参数.

        Args:
            value: 初始值，默认 0。
            name: 参数名，默认自动生成局部名称。

        Returns:
            NumberParameter: 创建的数值参数。
        """
        if name is None:
            name = self.next_id()
            scope = "local"
        else:
            scope = "global"
        num_param = NumberParameter(self, name=name)._new(value)
        self.symbol_table.define(name, type=NumberParameter, scope=scope, obj=num_param)
        return num_param

    def StringParameter(self, value=None, name=None):
        """创建字符串参数.

        Args:
            value: 初始值，默认 None。
            name: 参数名，默认自动生成局部名称。

        Returns:
            StringParameter: 创建的字符串参数。
        """
        if name is None:
            name = self.next_id()
            scope = "local"
        else:
            scope = "global"
        str_param = StringParameter(self, name=name)._new(value)
        self.symbol_table.define(name, type=StringParameter, scope=scope, obj=str_param)
        return str_param

    # ==================== 字符/字符串数组 ====================

    def CharArray(self, length, name=None):
        """创建字符数组（CHAR）。

        字符数组每个元素存储单个字符或短字符串（≤8字符）。

        Args:
            length: 数组长度。
            name: 参数名，默认自动生成局部名称。

        Returns:
            CharArray: 创建的字符数组。
        """
        if name is None:
            name = self.next_id()
            scope = "local"
        else:
            scope = "global"
        char_array = CharArray(self, name=name)._new(length)
        self.symbol_table.define(name, type=CharArray, scope=scope, obj=char_array)
        return char_array

    def char_array(self, data, name=None):
        """根据列表创建字符数组。

        Args:
            data: 字符串列表。
            name: 参数名，默认自动生成局部名称。

        Returns:
            CharArray: 创建的字符数组。
        """
        char_arr = self.CharArray(len(data), name=name)
        char_arr.fill(data)
        return char_arr

    def StringArray(self, length, str_length=32, name=None):
        """创建字符串数组（STRING）。

        字符串数组每个元素可存储完整字符串（最长 248 字符）。

        Args:
            length: 数组长度。
            str_length: 每个元素最大字符串长度，默认 32。
            name: 参数名，默认自动生成局部名称。

        Returns:
            StringArray: 创建的字符串数组。
        """
        if name is None:
            name = self.next_id()
            scope = "local"
        else:
            scope = "global"
        str_array = StringArray(self, name=name)._new(length, str_length)
        self.symbol_table.define(name, type=StringArray, scope=scope, obj=str_array)
        return str_array

    def string_array(self, data, str_length=32, name=None):
        """根据列表创建字符串数组。

        Args:
            data: 字符串列表。
            str_length: 每个元素最大字符串长度，默认 32。
            name: 参数名，默认自动生成局部名称。

        Returns:
            StringArray: 创建的字符串数组。
        """
        str_arr = self.StringArray(len(data), str_length, name=name)
        str_arr.fill(data)
        return str_arr

    # ==================== 数值数组 ====================

    def Array1(self, length, name=None):
        """创建一维数值数组。

        Args:
            length: 数组长度。
            name: 参数名，默认自动生成局部名称。

        Returns:
            Array1: 创建的一维数组。
        """
        if name is None:
            name = self.next_id()
            scope = "local"
        else:
            scope = "global"
        array = Array1(self, name=name)._new(length)
        self.symbol_table.define(name, type=Array1, scope=scope, obj=array)
        return array

    def array1(self, data, name=None):
        """根据列表创建一维数值数组。

        Args:
            data: 数值列表。
            name: 参数名，默认自动生成局部名称。

        Returns:
            Array1: 创建的一维数组。
        """
        arr = self.Array1(len(data), name=name)
        arr.fill(data)
        return arr

    def Array2(self, row, col, name=None):
        """创建二维数值数组。

        Args:
            row: 行数。
            col: 列数。
            name: 参数名，默认自动生成局部名称。

        Returns:
            Array2: 创建的二维数组。
        """
        if name is None:
            name = self.next_id()
            scope = "local"
        else:
            scope = "global"
        array = Array2(self, name=name)._new(row, col)
        self.symbol_table.define(name, type=Array2, scope=scope, obj=array)
        return array

    def array2(self, data, name=None):
        """根据二维列表创建二维数值数组。

        Args:
            data: 二维列表 [[row0_col0, row0_col1, ...], [row1_col0, ...], ...]。
            name: 参数名，默认自动生成局部名称。

        Returns:
            Array2: 创建的二维数组。
        """
        row = len(data)
        col = len(data[0])
        arr = self.Array2(row, col, name=name)
        arr.fill(data)
        return arr

    # ==================== 表格 ====================

    def Table1(self, length, name=None):
        """创建一维插值表格（TABLE）。

        表格使用实数索引，支持线性插值。

        Args:
            length: 表格长度（数据点个数）。
            name: 参数名，默认自动生成局部名称。

        Returns:
            Table1: 创建的表格。
        """
        if name is None:
            name = self.next_id()
            scope = "local"
        else:
            scope = "global"
        table = Table1(self, name=name)._new(length)
        self.symbol_table.define(name, type=Table1, scope=scope, obj=table)
        return table

    def table1(self, index_values, data_values, name=None):
        """根据索引和数据创建一维插值表格。

        Args:
            index_values: 索引值列表。
            data_values: 数据值列表。
            name: 参数名，默认自动生成局部名称。

        Returns:
            Table1: 创建的表格。
        """
        table = self.Table1(len(index_values), name=name)
        table.fill(index_values, data_values)
        return table

    # ==================== 便捷方法 ====================

    def array(self, data, name=None):
        """根据 data 自动创建 Array1 或 Array2。

        Args:
            data: 一维数据创建 Array1，二维数据创建 Array2。
            name: 参数名，默认自动生成局部名称。

        Returns:
            Array1 或 Array2: 根据 data 维度自动决定。
        """
        try:
            data[0][0]
            return self.array2(data, name=name)
        except (TypeError, IndexError):
            return self.array1(data, name=name)
