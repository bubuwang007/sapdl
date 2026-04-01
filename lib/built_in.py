"""Built-in functions for APDL.

提供 APDL 封装函数库。
"""

from functools import cached_property
from sapdl.custom import Custom
from .math import Math
from .files import Files
from .string import String


class BuiltIn:

    @cached_property
    def math(self) -> Math:
        """数学函数库"""
        return Math

    @cached_property
    def custom(self) -> Custom:
        return Custom(self)

    @cached_property
    def files(self) -> Files:
        return Files(self)

    @cached_property
    def string(self) -> String:
        """字符串函数库"""
        return String
