from .number_parameter import NumberParameter


class Table1Element(NumberParameter):
    """Table1 元素代理，继承 NumberParameter。

    支持通过 `<<` 赋值，如：`table[1, value] << 10.0`
    """

    def __init__(self, table, index):
        self._table = table
        self._index = index
        if isinstance(index, tuple) and len(index) == 2:
            self._name = f"{table.name}({index[0]},{index[1]})"
        else:
            self._name = f"{table.name}({index})"
        self.mac = table.mac
        self._alive = True

    def _new(self, value=None):
        raise NotImplementedError("Table1Element cannot be created with _new.")

    def delete(self):
        raise NotImplementedError("Table1Element cannot be deleted individually.")

    def _delete(self):
        raise NotImplementedError("Table1Element cannot be deleted individually.")
