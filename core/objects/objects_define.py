from __future__ import annotations

from .args import Args
from .number_parameter import NumberParameter
from .string_parameter import StringParameter
from .array1 import Array1
from .array2 import Array2
from .char_array import CharArray


class ObjectsDefine:
    _var_index: int = 0
    objects = {
        "NumberParameter": NumberParameter,
        "StringParameter": StringParameter,
        "Array1": Array1,
        "Array2": Array2,
        "CharArray": CharArray,
    }

    def __init__(self):
        self.args = Args()

    def next_id(self):
        self._var_index += 1
        return f"{self.name.lower()}{self._var_index}"

    def NumberParameter(self, value=0, name=None):
        if name is None:
            name = self.next_id()
            scope = "local"
        else:
            scope = "global"
        num_param = NumberParameter(self, name=name)._new(value)
        self.symbol_table.define(name, type=NumberParameter, scope=scope, obj=num_param)
        return num_param

    def StringParameter(self, value=None, name=None):
        if name is None:
            name = self.next_id()
            scope = "local"
        else:
            scope = "global"
        str_param = StringParameter(self, name=name)._new(value)
        self.symbol_table.define(name, type=StringParameter, scope=scope, obj=str_param)
        return str_param

    def CharArray(self, length, name=None):
        if name is None:
            name = self.next_id()
            scope = "local"
        else:
            scope = "global"
        char_array = CharArray(self, name=name)._new(length)
        self.symbol_table.define(name, type=CharArray, scope=scope, obj=char_array)
        return char_array

    def char_array(self, data, name=None):
        """根据列表创建 CharArray。

        Args:
            data: 字符串列表。
            name: 数组名称。

        Returns:
            CharArray: 创建的字符数组。
        """
        char_arr = self.CharArray(len(data), name=name)
        char_arr.fill(data)
        return char_arr

    def Array1(self, length, name=None):
        if name is None:
            name = self.next_id()
            scope = "local"
        else:
            scope = "global"
        array = Array1(self, name=name)._new(length)
        self.symbol_table.define(name, type=Array1, scope=scope, obj=array)
        return array

    def array1(self, data, name=None):
        arr = self.Array1(len(data), name=name)
        arr.fill(data)
        return arr

    def Array2(self, row, col, name=None):
        if name is None:
            name = self.next_id()
            scope = "local"
        else:
            scope = "global"
        array = Array2(self, name=name)._new(row, col)
        self.symbol_table.define(name, type=Array2, scope=scope, obj=array)
        return array

    def array2(self, data, name=None):
        """根据二维列表创建 Array2。

        Args:
            data: 二维列表 [[row0_col0, row0_col1, ...], [row1_col0, ...], ...]。
            name: 数组名称。

        Returns:
            Array2: 创建的二维数组。
        """
        row = len(data)
        col = len(data[0])
        arr = self.Array2(row, col, name=name)
        arr.fill(data)
        return arr

    def array(self, data, name=None):
        """根据 data 自动创建 Array1 或 Array2。

        Args:
            data: 一维数据创建 Array1，二维数据创建 Array2。
            name: 数组名称。

        Returns:
            Array1 或 Array2: 根据 data 维度自动决定。
        """
        try:
            data[0][0]
            return self.array2(data, name=name)
        except (TypeError, IndexError):
            return self.array1(data, name=name)
