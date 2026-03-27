"""GUI-based ANSYS launcher for Mechanical APDL.

This module provides a GuiLauncher class that interfaces with ANSYS Mechanical APDL
through GUI automation using pywin32.
"""

import os
import time
import win32con
import win32gui

from .launcher import Launcher
from sapdl.launcher.utils import (
    find_ansys_windows,
    find_mechanical_apdl,
    write_with_stamp,
)


ANSYS_CLIENTS = ["ANSYS MECHANICAL", "MECHANICAL APDL"]


class GUILauncher(Launcher):
    """Launcher for ANSYS Mechanical APDL via GUI automation.

    Connects to a running ANSYS Mechanical instance or launches a new one.
    Uses window messages to send commands to ANSYS.

    Attributes:
        ansys_path: Path to the ANSYS launcher executable.
    """

    def __init__(self, connect: bool = True):
        self.ansys_path = find_mechanical_apdl()
        self.hwnds: dict[int, str] = {}
        self.hwnd_main: int | None = None
        self.hwnd_input: list[int] = []
        self._init(connect)

    def _init(self, connect: bool):
        if connect:
            self.connect()
        elif not self.check_ansys_is_running():
            raise Exception("ANSYS is not running.")

    def connect(self):
        """Connect to ANSYS, launching it if necessary."""
        if not self.check_ansys_is_running():
            self._open_ansys()
        if not self.check_ansys_is_ready():
            raise Exception("ANSYS is not ready.")
        print("Connected to ANSYS.")

    def _open_ansys(self):
        """Launch ANSYS Mechanical APDL."""
        if self.check_ansys_is_running():
            return

        print("Opening ANSYS...")
        os.system(f'SET ANSYS_LOCK=OFF &"{self.ansys_path}" -runae')

        while not self.check_ansys_is_running():
            time.sleep(0.3)

    def check_ansys_is_running(self) -> bool:
        """Check if ANSYS Mechanical windows are running.

        Populates self.hwnds, self.hwnd_main, and self.hwnd_input as side effect.

        Returns:
            True if both main window and input window are found.
        """
        self.hwnds = find_ansys_windows()
        self.hwnd_main = None
        self.hwnd_input = []

        foreground = win32gui.GetForegroundWindow()
        foreground_title = self.hwnds.get(foreground, "")

        if ANSYS_CLIENTS[0] in foreground_title:
            self.hwnd_main = foreground

        has_main = self.hwnd_main is not None
        has_input = False

        for hwnd, title in self.hwnds.items():
            if not self.hwnd_main and ANSYS_CLIENTS[0] in title:
                self.hwnd_main = hwnd
                has_main = True

            if ANSYS_CLIENTS[1] in title and "DISTRIBUTED" not in title:
                self.hwnd_input.append(hwnd)
                has_input = True

        return has_main and has_input

    def check_ansys_is_ready(self, timeout: int = 10) -> bool:
        """Check if ANSYS is ready to receive commands by writing a stamp file.

        Args:
            timeout: Maximum number of seconds to wait.

        Returns:
            True if ANSYS creates the result file within timeout.
        """
        filepath, resfile = write_with_stamp("_check.apdl", "")
        self._send_input(filepath)

        while not os.path.exists(resfile):
            time.sleep(1)
            timeout -= 1
            if timeout <= 0:
                return False
            self._send_input(filepath)

        return True

    def _send_input(self, input_file: str) -> bool:
        """Send an input file path to ANSYS via window messages.

        Args:
            input_file: Path to the APDL input file.

        Returns:
            True if the message was sent successfully.
        """
        if self.hwnd_main is None:
            return False

        cmd = f"/INPUT,'{input_file}'"

        try:
            win32gui.ShowWindow(self.hwnd_main, win32con.SW_MAXIMIZE)
            win32gui.ShowWindow(self.hwnd_main, win32con.SW_SHOW)

            for hwnd in self.hwnd_input:
                win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

            win32gui.SetForegroundWindow(self.hwnd_main)
            time.sleep(0.3)

            for char in cmd:
                win32gui.SendMessage(self.hwnd_main, win32con.WM_CHAR, ord(char), None)
            win32gui.SendMessage(
                self.hwnd_main, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0
            )

        except Exception:
            return False

        return True

    def waiting(
        self, resfile: str, timeout: float = 60.0, interval: float = 0.5
    ) -> bool:
        """Wait for a result file to be created.

        Args:
            resfile: Path to the result file to wait for.
            timeout: Maximum seconds to wait (default 60).
            interval: Seconds between checks.

        Returns:
            True if file exists before timeout.
        """
        while not os.path.exists(resfile):
            timeout -= interval
            if timeout <= 0:
                return False
            time.sleep(interval)
        return True

    def run(self, input_string: str):
        """Run an APDL command string and wait for completion.

        Args:
            input_string: APDL commands to execute.

        Raises:
            Exception: If execution fails or times out.
        """
        filepath, resfile = write_with_stamp("_wait.apdl", input_string)
        self._send_input(filepath)

        if not self.waiting(resfile):
            raise Exception("Running failed.")

        print("Run completed.")

    def run_file(self, filename: str):
        """Run an APDL script file.

        Args:
            filename: Path to the APDL script file.
        """
        print(f"Running file {filename}")
        self.run(f"/INPUT,'{filename}'")

    def run_str(self, string: str):
        """Run an APDL command string.

        Args:
            string: APDL commands to execute.
        """
        self.run(string)
