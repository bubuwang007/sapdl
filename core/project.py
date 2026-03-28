"""Project - ANSYS APDL 项目管理

提供项目级别的工作目录管理、宏管理和运行启动器配置。
"""

import os
from .mac import Mac


class Project:
    """ANSYS APDL 项目管理器

    管理项目级的工作目录、主宏对象和运行启动器。

    Attributes:
        workdir: 项目工作目录路径
        main: 项目的主 Mac 对象，用于聚合所有 APDL 命令

    Example:
        >>> project = Project(workdir="./my_project")
        >>> project.main.k(1, 0, 0, 0)  # 创建关键点
        >>> project.generate()  # 生成 APDL 命令流文件
        >>> project.run()  # 运行项目
    """

    def __init__(
        self,
        workdir: str | None = None,
        main: Mac | None = None,
        lib_path: str | None = None,
    ):
        """初始化 Project 实例

        Args:
            workdir: 工作目录路径，默认为 `<当前目录>/workdir`
            main: 主 Mac 对象，默认为新建的 Mac 实例
            lib_path: 库文件搜索路径，会传递给 main.psearch()
        """
        if workdir is None:
            workdir = os.path.join(os.getcwd(), "workdir")
        else:
            workdir = os.path.abspath(workdir)
        self.workdir = workdir

        if main is None:
            main = Mac()
        self.main = main

        main.add_block_comment("Project Initialization")
        main.cwd(self.workdir)
        if lib_path is not None:
            main.psearch(os.path.abspath(lib_path))
        main.add_block_comment("End of Initialization")

        if not os.path.exists(self.workdir):
            os.makedirs(self.workdir)

        if os.path.exists(self.cached_path):
            os.remove(self.cached_path)

    @property
    def cached_path(self) -> str:
        """缓存文件路径

        返回 `<workdir>/.cached.yaml`，用于存储已导入宏的信息。
        """
        return os.path.join(self.workdir, ".cached.yaml")

    @property
    def launcher(self):
        """gRPC 启动器（延迟初始化）

        首次访问时创建 GrpcLauncher 实例，后续访问返回同一实例。
        """
        from sapdl import GrpcLauncher

        if not hasattr(self, "_launcher"):
            self._launcher = GrpcLauncher()
        return self._launcher

    def gui(self, connect: bool = True) -> "Project":
        """配置 GUI 启动器

        Args:
            connect: 是否自动连接到已运行的 ANSYS 实例

        Returns:
            返回 self，支持链式调用
        """
        from sapdl import GUILauncher

        self._launcher = GUILauncher(connect)
        return self

    def grpc(self, connect: bool = True) -> "Project":
        """配置 gRPC 启动器

        Args:
            connect: 是否自动连接到 gRPC 服务器

        Returns:
            返回 self，支持链式调用
        """
        from sapdl import GrpcLauncher

        self._launcher = GrpcLauncher(connect)
        return self

    def generate(self) -> str:
        """生成 APDL 命令流文件

        调用 main.save() 将命令流写入文件。

        Returns:
            保存的文件路径
        """
        return self.main.save()

    def run(self) -> None:
        """运行项目

        使用配置的启动器运行生成的 APDL 文件。
        """
        self.launcher.run_file(self.generate())
