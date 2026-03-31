"""DoWhileBlock - DO-WHILE 循环上下文管理器

提供 DO-WHILE 循环块的上下文管理器接口。
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from sapdl.core.ast import DoWhileNode

if TYPE_CHECKING:
    from sapdl.core.mac import Mac


class DoWhileBlock:
    """DO-WHILE 循环块构建器。

    通过上下文管理器方式构建 APDL DO-WHILE 循环语句。
    循环体先执行，再判断条件是否继续（post-test loop）。

    Attributes:
        mac: Mac 容器实例。
    """

    def __init__(self, mac: Mac, condition):
        """初始化 DoWhileBlock.

        Args:
            mac: Mac 容器实例。
            condition: 继续循环的条件（condition 为真时继续）。
        """
        self.mac = mac
        self.condition = condition
        self.do_while_node: DoWhileNode | None = None

    def __enter__(self):
        """进入 DO-WHILE 循环上下文。

        Yields:
            Mac 容器实例。
        """
        self.do_while_node = DoWhileNode(self.condition)
        self.mac.body.add(self.do_while_node)

        self.prev_body = self.mac.body
        self.mac.body = self.do_while_node.body

        return self.mac

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """退出上下文，恢复之前的 body。"""
        self.mac.body = self.prev_body