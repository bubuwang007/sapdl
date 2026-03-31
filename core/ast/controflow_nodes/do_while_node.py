"""DoWhileNode - DO-WHILE 循环节点

*DO/*ENDDO 循环语句的 AST 节点（post-test loop）。
"""

from sapdl import INDENT
from ..base import Node, Body


class DoWhileNode(Node):
    """DO-WHILE loop node (*DO/*ENDDO with post-test condition).

    Attributes:
        condition: 继续循环的条件表达式。
        body: 循环体。
        type: Node type identifier ("block").
    """

    __slots__ = ["condition", "body", "type"]

    def __init__(self, condition):
        """初始化 DoWhileNode.

        Args:
            condition: 继续循环的条件（condition 为真时继续循环）。
        """
        self.condition = condition
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

        ret.append(f"{indent}*DOWHILE,{self.condition}")
        ret.extend(self.body.apdl(indent_level + 1))
        ret.append(f"{indent}*ENDDO")

        return ret
