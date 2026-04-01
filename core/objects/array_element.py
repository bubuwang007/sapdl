from .number_parameter import NumberParameter


class ArrayElement(NumberParameter):

    def __init__(self, array, index):
        self.array = array
        self.index = index
        if isinstance(index, tuple) and len(index) == 2:
            self._name = f"{array.name}({index[0]},{index[1]})"
        else:
            self._name = f"{array.name}({index})"
        self.mac = array.mac

    def delete(self):
        raise NotImplementedError("Array elements cannot be deleted individually.")

    def _delete(self):
        raise NotImplementedError("Array elements cannot be deleted individually.")

    def _new(self, value=None):
        raise NotImplementedError("Array elements cannot be created individually.")
