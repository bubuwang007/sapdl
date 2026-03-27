"""Mac - APDL 命令流容器

将 APDL 命令收集到容器中，支持命令流生成和文件输出。
"""

from __future__ import annotations
import os
import yaml
from sapdl.lib import BuiltIn
from .commands import Commands
from .symbol_table import SymbolTable


class Mac(Commands, BuiltIn):
    """APDL 命令流容器

    将 APDL 命令收集到容器中，支持命令流生成和文件输出。

    Attributes:
        name: 宏文件名称（不含扩展名）
        workdir: 工作目录路径
        symbol_table: 符号表，用于管理本地和全局变量
    """

    name: str = "main"

    def __init__(self):
        """初始化 Mac 实例"""
        Commands.__init__(self)
        self.symbol_table = SymbolTable()

    @property
    def workdir(self):
        if not hasattr(self, "_workdir") or self._workdir is None:
            self._workdir = os.path.join(os.getcwd(), "workdir")

        if not os.path.exists(self._workdir):
            os.makedirs(self._workdir)
        return self._workdir

    @property
    def cached_macs(self):
        p = os.path.join(self.workdir, ".cached_macs.yaml")
        if os.path.exists(p):
            with open(p, "r", encoding="u8") as f:
                return set(yaml.safe_load(f))
        else:
            return set()

    def update_cached_macs(self, mac_name: str):
        p = os.path.join(self.workdir, ".cached_macs.yaml")
        cached = self.cached_macs
        cached.add(mac_name)
        with open(p, "w", encoding="u8") as f:
            yaml.safe_dump(list(cached), f)

    def import_mac(self, mac: type[Mac], *args, **kwargs):
        """导入另一个 Mac 的命令流

        Args:
            mac: 另一个 Mac 类
            *args: 传递给被调用 Mac 的位置参数
            **kwargs: 传递给被调用 Mac 的关键字参数
        """
        if mac.name in self.cached_macs:
            return
        instance = mac(*args, **kwargs)
        instance.apdl_body()
        instance._workdir = self._workdir
        instance.save()
        self.update_cached_macs(mac.name)

    def apdl_body(self):
        """留给子类实现的钩子方法"""
        pass

    def call(self, mac: type[Mac], *args):
        if mac.name not in self.cached_macs:
            self.import_mac(mac)
        self.fast_call(mac, *args)

    def fast_call(self, mac: type[Mac], *args):
        tmp = []
        for arg in args:
            if isinstance(arg, str):
                tmp.append(f"'{arg}'")
            else:
                tmp.append(str(arg))
        self.run(f"{mac.name}, {', '.join(tmp)}")

    def save(self) -> str:
        """保存 Mac 到 APDL 宏文件

        Returns:
            保存的文件路径
        """
        path = os.path.join(self.workdir, f"{self.name}.mac")

        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)

        with open(path, "w", encoding="u8") as f:
            # 写入文档注释
            if self.__doc__:
                lines = self.__doc__.strip().split("\n")
                for line in lines:
                    if line.startswith(" " * 4):
                        line = line[4:]
                    f.write(f"! {line}\n")

            # 写入块注释：清除本地变量
            self.add_block_comment("Clear local variables")
            for sym in self.symbol_table.iter_local():
                print("delete local variable:", sym.name)

            # 写入块注释：使用全局变量
            self.add_block_comment("Use global variable")
            for name in self.symbol_table.iter_global_names():
                self.add_comment(name)

            # 写入命令
            for cmd in self.body.apdl(0):
                f.write(f"{cmd}\n")

        return path
