"""DoBlock - DO 循环上下文管理器

提供 *DO/*ENDDO 循环块的上下文管理器接口。
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import TYPE_CHECKING

from sapdl.core.ast import DoNode

if TYPE_CHECKING:
    from sapdl.core.mac import Mac


class DoBlock:
    """DO 循环块构建器。

    通过上下文管理器方式构建 APDL *DO 循环语句。

    Attributes:
        mac: Mac 容器实例。
    """

    def __init__(self, mac: Mac, var, start, end, step=1):
        """初始化 DoBlock.

        Args:
            mac: Mac 容器实例。
        """
        self.mac = mac
        self.var = var
        self.start = start
        self.end = end
        self.step = step
        self.do_node: DoNode | None = None

    def __enter__(self):
        """DO 循环上下文管理器。

        Args:
            var: 循环变量名。
            start: 起始值。
            end: 结束值。
            step: 步长（默认 1）。

        Yields:
            Mac 容器实例。
        """
        self.do_node = DoNode(self.var, self.start, self.end, self.step)
        self.mac.body.add(self.do_node)

        self.prev_body = self.mac.body
        self.mac.body = self.do_node.body
        
        return self.var

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.mac.body = self.prev_body
