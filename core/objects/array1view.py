from .array1 import Array1
from .array_element import ArrayElement


class Array1View(Array1):
    """Array1 的视图，指向 Array2 的某一列。"""

    def __init__(self, array2, col_idx):
        self._array2 = array2
        self._col_idx = col_idx
        self._name = f"{array2.name}(1,{col_idx})"
        self.mac = array2.mac
        self.length = array2.row

    def _new(self, length=None):
        raise NotImplementedError("Array1View cannot be created with _new.")

    def delete(self):
        raise NotImplementedError("Array1View cannot be deleted individually.")

    def _delete(self):
        raise NotImplementedError("Array1View cannot be deleted individually.")

    def __getitem__(self, index):
        return ArrayElement(self._array2, (index, self._col_idx))

    def __str__(self):
        return self._name
