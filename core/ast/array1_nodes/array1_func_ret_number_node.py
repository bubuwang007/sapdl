from sapdl import INDENT
from ..base import Node


class Array1FuncRetNumberNode(Node):

    __slots__ = ["func_name", "array_parameter", "type", "out"]

    def __init__(self, func_name, array_parameter, out=None):
        self.func_name = func_name
        self.array_parameter = array_parameter
        self.type = "statement"
        self.out = out

    def apdl(self, indent_level: int) -> str:
        if self.out is None:
            raise ValueError(
                "Output parameter is required for function return value assignment."
            )
        return f"{INDENT * indent_level}*VSCFUN,{self.out.name},{self.func_name},{self.array_parameter.parameter}"
