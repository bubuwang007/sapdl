"""Mac - APDL 命令流容器

将 APDL 命令收集到容器中，支持命令流生成和文件输出。
"""

from __future__ import annotations
from sapdl.lib import BuiltIn
from .commands import Commands


class Mac(Commands, BuiltIn):
    pass
