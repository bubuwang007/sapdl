from .string_parameter import StringParameter


class StrArrayElement(StringParameter):
    """字符数组元素代理，继承 StringParameter。

    支持通过 `<<` 赋值，如：`char_array[1] << 'value'`
    """

    def __init__(self, array, index):
        self._array = array
        self._index = index
        self._name = f"{array.name}({index})"
        self.mac = array.mac
        self._alive = True

    def _new(self, value=None):
        raise NotImplementedError("StrArrayElement cannot be created with _new.")

    def delete(self):
        raise NotImplementedError("StrArrayElement cannot be deleted individually.")

    def _delete(self):
        raise NotImplementedError("StrArrayElement cannot be deleted individually.")
