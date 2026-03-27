"""gRPC-based ANSYS launcher via ansys.mapdl.core.

This module provides a GrpcLauncher class that connects to ANSYS Mechanical APDL
through the gRPC interface using the ansys-mapdl-core library.
"""

import os

import psutil

from .launcher import Launcher
from sapdl.launcher import MAPDL_INITIAL_WORKDIR
from sapdl.launcher.utils import find_mapdl


class GrpcLauncher(Launcher):
    """Launcher for ANSYS Mechanical APDL via gRPC.

    Connects to a MAPDL instance using the ansys-mapdl-core library.

    Attributes:
        ansys_path: Path to the MAPDL executable.
        workdir: Working directory for MAPDL.
        jobname: Job name for MAPDL.
        mapdl: The MAPDL instance.
    """

    def __init__(self, workdir: str | None = None, jobname: str = "file"):
        self.ansys_path = find_mapdl()
        self._init(workdir, jobname)

    def _init(self, workdir: str | None, jobname: str):
        self.workdir = MAPDL_INITIAL_WORKDIR if workdir is None else workdir
        os.makedirs(self.workdir, exist_ok=True)
        self.jobname = jobname
        self.connect()

    def connect(self):
        """Connect to MAPDL instance."""
        from ansys.mapdl.core import launch_mapdl

        print(f"Connecting to MAPDL in {self.workdir}...")

        self.mapdl = launch_mapdl(
            exec_file=self.ansys_path,
            run_location=self.workdir,
            jobname=self.jobname,
            nproc=psutil.cpu_count(logical=False),
            override=True,
        )

    def run(self, command: str):
        """Run an APDL command string.

        Args:
            command: APDL commands to execute.

        Returns:
            The result from MAPDL input_strings.
        """
        return self.mapdl.input_strings(str(command))

    def run_file(self, filename: str):
        """Run an APDL script file.

        Args:
            filename: Path to the APDL script file.

        Returns:
            The result from MAPDL.
        """
        print(f"Running file {filename}")
        res = self.run(f"/INPUT,'{filename}'")
        print("File run complete.")
        return res

    def run_str(self, string: str):
        """Run an APDL command string.

        Args:
            string: APDL commands to execute.

        Returns:
            The result from MAPDL.
        """
        return self.run(string)
