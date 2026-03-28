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

    继承自 Commands（提供命令流生成能力）和 BuiltIn（提供数学/自定义函数）。

    Attributes:
        name: 宏文件名称（不含扩展名），默认为 "main"
        workdir: 工作目录路径，用于存储生成的宏文件
        symbol_table: 符号表，用于管理本地和全局变量
    """

    name: str = "main"

    def __init__(self):
        """初始化 Mac 实例"""
        Commands.__init__(self)
        self.symbol_table = SymbolTable()

    @property
    def workdir(self) -> str:
        """工作目录路径

        首次访问时自动创建，默认值为 `<当前目录>/workdir`。
        """
        if not hasattr(self, "_workdir") or self._workdir is None:
            self._workdir = os.path.join(os.getcwd(), "workdir")

        if not os.path.exists(self._workdir):
            os.makedirs(self._workdir)
        return self._workdir

    @property
    def cached(self) -> dict:
        """缓存数据（YAML 持久化）

        用于存储全局信息。
        数据存储在 `<workdir>/.cached.yaml` 文件中。

        Returns:
            缓存的字典数据。
        """
        p = os.path.join(self.workdir, ".cached.yaml")
        if os.path.exists(p):
            with open(p, "r", encoding="u8") as f:
                return yaml.safe_load(f) or {}
        else:
            return {}

    @cached.setter
    def cached(self, value: dict) -> None:
        """设置缓存数据

        Args:
            value: 要写入的字典数据
        """
        p = os.path.join(self.workdir, ".cached.yaml")
        with open(p, "w", encoding="u8") as f:
            yaml.safe_dump(value, f)

    def _has_mac(self, mac_name: str) -> bool:
        """检查宏是否已缓存

        Args:
            mac_name: 宏名称

        Returns:
            如果宏已在缓存中返回 True，否则返回 False
        """
        return mac_name in set(self.cached.get("macs", []))

    def update_cached_macs(self, mac_name: str) -> None:
        """更新已缓存宏列表

        将指定宏名添加到缓存中。

        Args:
            mac_name: 宏名称
        """
        cached = self.cached
        cached.setdefault("macs", []).append(mac_name)
        self.cached = cached

    def import_mac(self, mac: type[Mac], *args, **kwargs) -> None:
        """导入另一个 Mac 的命令流

        将另一个 Mac 类的命令流导入到当前实例，包括实例化、
        执行 apdl_body 和保存到文件。

        Args:
            mac: 另一个 Mac 类
            *args: 传递给被调用 Mac 的位置参数
            **kwargs: 传递给被调用 Mac 的关键字参数
        """
        if self._has_mac(mac.name):
            return
        instance = mac(*args, **kwargs)
        instance.apdl_body()
        instance._workdir = self._workdir
        instance.save()
        self.update_cached_macs(mac.name)

    def apdl_body(self) -> None:
        """留给子类实现的钩子方法

        子类应重写此方法，在其中添加 APDL 命令。
        默认实现为空，不生成任何命令。
        """
        pass

    def call(self, mac: type[Mac], *args) -> None:
        """调用宏（完整调用）

        先导入宏（如果未导入），然后通过 APDL CALL 命令调用。

        Args:
            mac: 要调用的 Mac 类
            *args: 传递给被调用宏的位置参数
        """
        self.import_mac(mac)
        self.fast_call(mac, *args)

    def fast_call(self, mac: type[Mac], *args) -> None:
        """快速调用宏（仅生成 CALL 命令）

        直接生成 APDL CALL 命令字符串，不执行导入逻辑。
        字符串参数会自动添加引号。

        Args:
            mac: 要调用的 Mac 类
            *args: 传递给被调用宏的位置参数，会转换为 APDL 格式
        """
        tmp = []
        for arg in args:
            if isinstance(arg, str):
                tmp.append(f"'{arg}'")
            else:
                tmp.append(str(arg))
        self.run(f"{mac.name}, {', '.join(tmp)}")

    def save(self) -> str:
        """保存 Mac 到 APDL 宏文件

        将命令流写入 `<workdir>/<name>.mac` 文件。
        文件内容包含：文档注释、块注释（本地变量清理、全局变量声明）、APDL 命令。

        Returns:
            保存的文件路径

        Raises:
            OSError: 当目录创建或文件写入失败时
        """
        path = os.path.join(self.workdir, f"{self.name}.mac")

        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)

        with open(path, "w", encoding="u8") as f:
            # 写入文档注释（从类 docstring 转换）
            if self.__doc__:
                lines = self.__doc__.strip().split("\n")
                for line in lines:
                    if line.startswith(" " * 4):
                        line = line[4:]
                    f.write(f"! {line}\n")

            self.add_block_comment("Clear local variables")
            for sym in self.symbol_table.iter_local():
                sym.obj._delete()

            # 写入块注释：使用全局变量
            self.add_block_comment("Use global variable")
            for name in self.symbol_table.iter_global_names():
                self.add_comment(name)

            # 写入命令
            for cmd in self.body.apdl(0):
                f.write(f"{cmd}\n")

        return path
