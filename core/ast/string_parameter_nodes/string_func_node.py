from sapdl import INDENT
from ..base import Node


class StringFuncNode(Node):

    __slots__ = ["name", "args", "type"]

    def __init__(self, name: str, *args: list[str]):
        self.name = name
        self.args = args
        self.type = "expr"

    def apdl(self, _: int) -> str:
        def fmt(arg):
            s = str(arg)
            return (
                f"'{s}'"
                if isinstance(arg, str) and not (s.startswith("'") and s.endswith("'"))
                else s
            )

        args_str = ", ".join([fmt(arg) for arg in self.args])
        return f"{self.name}({args_str})"
