ANSYS_PATH = ""
ANSYS_TEMPFILE_PATH = "C:\\ANSYSAPDL\\temp"
MAPDL_INITIAL_WORKDIR = "C:\\ANSYSAPDL\\workdir"
MAPDL_IP = "127.0.0.1"
MAPDL_PORT = 50001

import os

os.makedirs(ANSYS_TEMPFILE_PATH, exist_ok=True)
os.makedirs(MAPDL_INITIAL_WORKDIR, exist_ok=True)
for f in os.listdir(ANSYS_TEMPFILE_PATH):
    try:
        os.remove(os.path.join(ANSYS_TEMPFILE_PATH, f))
    except:
        pass

from .gui_launcher import GUILauncher
from .grpc_launcher import GrpcLauncher

__all__ = ["GUILauncher", "GrpcLauncher"]
