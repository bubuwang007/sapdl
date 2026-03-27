import os
import re
import random

from . import ANSYS_PATH, ANSYS_TEMPFILE_PATH


def find_ansys() -> str | None:
    """Find ANSYS installation path from environment variables.

    Searches for ANSYS*_DIR pattern in environment variables.
    If multiple versions found, returns the latest version.

    Returns:
        Path to ANSYS installation or None if not found.
    """
    re_ansys = re.compile(r"ANSYS(\d+)_DIR")
    ansyss = {}

    for key, value in os.environ.items():
        m = re_ansys.match(key)
        if m:
            ansyss[m.group(1)] = value

    if not ansyss:
        return None

    if len(ansyss) == 1:
        return next(iter(ansyss.values()))

    latest = max(ansyss.keys(), key=lambda x: int(x))
    return ansyss[latest]


def _find_ansys_path() -> str:
    """Get ANSYS base path, checking config first then environment.

    Returns:
        Path to ANSYS installation.

    Raises:
        Exception: If ANSYS path cannot be found.
    """
    path = ANSYS_PATH if ANSYS_PATH else find_ansys()
    if not path:
        raise Exception("ANSYS not found.")
    return path


def find_mechanical_apdl() -> str:
    """Find Mechanical APDL launcher executable.

    Returns:
        Path to launcher.exe.

    Raises:
        FileNotFoundError: If launcher.exe does not exist.
    """
    ansys_path = os.path.join(_find_ansys_path(), "bin", "winx64", "launcher.exe")
    if not os.path.exists(ansys_path):
        raise FileNotFoundError(f"ANSYS path {ansys_path} does not exist.")
    return ansys_path


def find_mapdl() -> str:
    """Find MAPDL executable.

    Returns:
        Path to MAPDL.exe.

    Raises:
        FileNotFoundError: If MAPDL.exe does not exist.
    """
    ansys_path = os.path.join(_find_ansys_path(), "bin", "winx64", "MAPDL.exe")
    if not os.path.exists(ansys_path):
        raise FileNotFoundError(f"MAPDL path {ansys_path} does not exist.")
    return ansys_path


def tempfile_path(filename: str) -> str:
    """Generate full path for a temporary file.

    Args:
        filename: Name of the temporary file.

    Returns:
        Full path combining ANSYS_TEMPFILE_PATH and filename.
    """
    return os.path.join(ANSYS_TEMPFILE_PATH, filename)


def stamp() -> tuple[str, str]:
    """Generate a unique stamp and corresponding result file path.

    Returns:
        Tuple of (APDL stamp commands, result file path).
    """
    stamp_value = random.randint(0, 999_999_999)
    resfile = tempfile_path(str(stamp_value))
    cmds = [
        f"_STAMP='{stamp_value}'",
        f"*CFOPEN,'{resfile}'",
        "*CFCLOS",
    ]
    return "\n".join(cmds), resfile


def write_tempfile(filename: str, content: str) -> str:
    """Write content to a temporary file.

    Args:
        filename: Name of the file.
        content: Content to write.

    Returns:
        Full path to the written file.
    """
    path = tempfile_path(filename)
    with open(path, "w", encoding="u8") as f:
        f.write(content)
    return path


def find_ansys_windows() -> dict[int, str]:
    """Find all visible, enabled windows and their titles.

    Returns:
        Dictionary mapping window handles to their titles (uppercase).
    """
    import win32gui

    hwnds = {}

    def enum_callback(hwnd, _):
        if all(
            fn(hwnd)
            for fn in [
                win32gui.IsWindow,
                win32gui.IsWindowEnabled,
                win32gui.IsWindowVisible,
            ]
        ):
            hwnds[hwnd] = win32gui.GetWindowText(hwnd).upper()

    win32gui.EnumWindows(enum_callback, 0)
    return hwnds


def write_with_stamp(filename: str, content: str) -> tuple[str, str]:
    """Write content to a temporary file with a stamp for result tracking.

    Args:
        filename: Name of the file.
        content: Content to write.

    Returns:
        Tuple of (full path to written file, result file path from stamp).
    """
    path = tempfile_path(filename)
    stamp_content, respath = stamp()
    with open(path, "w", encoding="u8") as f:
        f.write(content)
        f.write("\n")
        f.write(stamp_content)
    return path, respath
