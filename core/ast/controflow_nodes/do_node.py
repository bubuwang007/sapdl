"""DoNode - DO 循环节点

*DO/*ENDDO 循环语句的 AST 节点。
"""

from sapdl import INDENT
from ..base import Node, Body


class DoNode(Node):
    """DO loop node (*DO/*ENDDO).

    Attributes:
        var: Loop variable name.
        start: Start value.
        end: End value.
        step: Step value (default "1").
        type: Node type identifier ("block").
    """

    __slots__ = ["var", "start", "end", "step", "body", "type"]

    def __init__(self, var, start, end, step = 1):
        """初始化 DoNode.

        Args:
            var: 循环变量名。
            start: 起始值。
            end: 结束值。
            step: 步长（默认 1）。
        """
        self.var = var
        self.start = start
        self.end = end
        self.step = step
        self.body = Body()
        self.type = "block"

    def apdl(self, indent_level: int) -> list[str]:
        """生成 APDL 字符串表示。

        Args:
            indent_level: 缩进级别。

        Returns:
            APDL 命令列表。
        """
        ret: list[str] = []
        indent = INDENT * indent_level

        ret.append(f"{indent}*DO,{self.var},{self.start},{self.end},{self.step}")
        ret.extend(self.body.apdl(indent_level + 1))
        ret.append(f"{indent}*ENDDO")

        return ret

    def __str__(self) -> str:
        return (
            f"DoNode(var={self.var!r}, "
            f"start={self.start!r}, "
            f"end={self.end!r}, "
            f"step={self.step!r})"
        )
