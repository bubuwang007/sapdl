from .string_parameter import StringParameter


class StringArrayElement(StringParameter):
    """字符串数组元素代理，继承 StringParameter。

    支持通过 `<<` 赋值，如：`string_array[1] << 'value'`
    """

    def __init__(self, array, index):
        self._array = array
        self._index = index
        if isinstance(index, tuple) and len(index) == 2:
            self._name = f"{array.name}({index[0]},{index[1]})"
        else:
            self._name = f"{array.name}({index})"
        self.mac = array.mac
        self._alive = True

    def _new(self, value=None):
        raise NotImplementedError("StringArrayElement cannot be created with _new.")

    def delete(self):
        raise NotImplementedError("StringArrayElement cannot be deleted individually.")

    def _delete(self):
        raise NotImplementedError("StringArrayElement cannot be deleted individually.")
