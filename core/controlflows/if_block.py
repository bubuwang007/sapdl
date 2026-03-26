"""IfBlock - 条件语句上下文管理器

提供 *IF/*ELIF/*ELSE/*ENDIF 条件块的上下文管理器接口。
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import TYPE_CHECKING

from sapdl.core.ast import IfNode, NumberComparisonNode

if TYPE_CHECKING:
    from sapdl.core.mac import Mac


class IfBlock:
    """IF 条件块构建器。

    通过上下文管理器方式构建 APDL *IF 条件语句。

    Attributes:
        mac: Mac 容器实例。
    """

    def __init__(self, mac: Mac):
        """初始化 IfBlock.

        Args:
            mac: Mac 容器实例。
        """
        self.mac = mac
        self.if_node: IfNode | None = None
        self._state: str | None = None

    def __enter__(self) -> IfBlock:
        """进入上下文，返回 IfBlock 实例。"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """退出上下文，异常自动传播。"""
        return

    @contextmanager
    def if_(self, condition: NumberComparisonNode):
        """IF 分支上下文管理器。

        Args:
            condition: APDL 条件表达式（如 "val,GT,0"）。

        Yields:
            Mac 容器实例。

        Raises:
            RuntimeError: 如果已存在 IF 块（不支持嵌套）。
        """
        if self._state is not None:
            raise RuntimeError("Nested if blocks are not supported.")

        self.if_node = IfNode()
        self.if_node.if_condition = condition
        self.mac.body.add(self.if_node)

        prev_body = self.mac.body
        self.mac.body = self.if_node.if_body
        yield self.mac
        self.mac.body = prev_body
        self._state = "if"

    @contextmanager
    def elif_(self, condition: NumberComparisonNode):
        """ELIF 分支上下文管理器。

        Args:
            condition: APDL 条件表达式（如 "val,LT,-1"）。

        Yields:
            Mac 容器实例。

        Raises:
            RuntimeError: 如果前面没有 IF 块，或已有 ELSE 块。
        """
        if self._state is None:
            raise RuntimeError("elif block must follow an if block.")
        if self._state == "else":
            raise RuntimeError("elif block cannot follow an else block.")

        elif_body = self.if_node.add_elif(condition)

        prev_body = self.mac.body
        self.mac.body = elif_body
        yield self.mac
        self.mac.body = prev_body
        self._state = "elif"

    @contextmanager
    def else_(self):
        """ELSE 分支上下文管理器。

        Yields:
            Mac 容器实例。

        Raises:
            RuntimeError: 如果前面没有 IF 块，或已有 ELSE 块。
        """
        if self._state is None:
            raise RuntimeError("else block must follow an if block.")
        if self._state == "else":
            raise RuntimeError("Multiple else blocks are not allowed.")

        else_body = self.if_node.add_else()

        prev_body = self.mac.body
        self.mac.body = else_body
        yield self.mac
        self.mac.body = prev_body
        self._state = "else"
