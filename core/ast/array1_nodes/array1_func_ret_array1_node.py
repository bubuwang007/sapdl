from sapdl import INDENT
from ..base import Node


class Array1FuncRetArray1Node(Node):
    """Array1 function returning Array1 node (*VFUN).

    用于 *VFUN 命令，函数操作返回数组参数。
    例如 ASORT, DSORT, COPY, ABS, SIN, COS 等。
    """

    __slots__ = ["func_name", "array_parameter", "type", "out"]

    def __init__(
        self, func_name, array_parameter, out=None, con1=None, con2=None, con3=None
    ):
        self.func_name = func_name
        self.array_parameter = array_parameter
        self.type = "statement"
        self.out = out
        self.con1 = con1
        self.con2 = con2
        self.con3 = con3

    def apdl(self, indent_level: int) -> str:
        if self.out is None:
            raise ValueError(
                "Output parameter is required for function return value assignment."
            )
        args = [self.con1, self.con2, self.con3]
        args_str = ",".join(str(arg) for arg in args if arg is not None)
        return f"{INDENT * indent_level}*VFUN,{self.out.name},{self.func_name},{self.array_parameter.parameter},{args_str}"
