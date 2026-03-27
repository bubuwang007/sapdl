import os
from sapdl import GrpcLauncher, GUILauncher
from .mac import Mac


class Project:

    def __init__(self, workdir: str = None, main: Mac = None, lib_path: str = None):
        if workdir is None:
            workdir = os.path.join(os.getcwd(), "workdir")
        else:
            workdir = os.path.abspath(workdir)
        self.workdir = workdir

        if main is None:
            main = Mac()
        self.main = main

        main.cwd(self.workdir)
        if lib_path is not None:
            main.psearch(os.path.abspath(lib_path))

    @property
    def launcher(self):
        if not hasattr(self, "_launcher"):
            self._launcher = GrpcLauncher()
        return self._launcher

    def gui(self, connect: bool = True):
        self._launcher = GUILauncher(connect)
        return self

    def grpc(self, connect: bool = True):
        self._launcher = GrpcLauncher(connect)
        return self
        