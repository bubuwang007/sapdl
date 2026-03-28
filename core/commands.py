"""Commands - APDL 命令流生成器

基于 APDL 命令封装，聚合所有命令并生成命令流。
"""

from sapdl.apdl import Commands as APDLCommands
from .ast import Body, CommandNode, CommentNode
from .symbol_table import SymbolTable
from .controlflows import Controlflows
from .objects import ObjectsDefine


class Commands(APDLCommands, Controlflows, ObjectsDefine):
    """APDL 命令流生成器

    将 APDL 命令收集到 Body 中，支持命令流生成。

    Attributes:
        body: 命令流容器，存储所有命令节点
    """

    def __init__(self):
        """初始化 Commands 实例"""
        self.body = Body()
        self.symbol_table = SymbolTable()

    def run(self, cmd: str, **kwargs) -> None:
        """添加 APDL 命令到命令流

        Args:
            cmd: APDL 命令字符串，如 "K,1,0,0,0"
            **kwargs: 额外的关键字参数（暂未使用）
        """
        if isinstance(cmd, str):
            self.body.add(CommandNode(cmd))

    def add_comment(self, text: str) -> None:
        """添加注释到命令流

        Args:
            text: 注释文本，不需要包含 "!" 符号
        """
        self.body.add(CommentNode(text))

    def add_blank_line(self) -> None:
        """在命令流中添加空行"""
        self.body.add(CommandNode(""))

    def add_block_comment(
        self, content: str, star_num: int = 55, line_length: int = 55
    ) -> None:
        """添加块注释到命令流

        生成带边框的块注释，自动处理文本换行。
        中文字符宽度计为2，ASCII字符宽度为1。

        Args:
            content: 注释内容
            star_num: 边框星号数量，默认为55
            line_length: 每行最大字符宽度，默认为55
        """
        self.add_blank_line()
        self.add_comment("*" * star_num)

        pos = 0  # 当前字符位置
        line_start = 0  # 当前行起始位置
        line_width = 0  # 当前行字符宽度

        for char in content:
            # 计算字符宽度：ASCII为1，非ASCII为2
            char_width = 1 if ord(char) < 128 else 2

            if line_width + char_width > line_length:
                # 达到行宽限制，输出当前行
                self.add_comment(content[line_start:pos])
                line_start = pos
                line_width = char_width
            else:
                line_width += char_width
            pos += 1

        # 输出最后一行
        if line_start < pos:
            self.add_comment(content[line_start:])

        self.add_comment("*" * star_num)
        self.add_blank_line()
