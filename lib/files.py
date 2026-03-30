from .files_obj import File


class Files:

    def __init__(self, mac):
        self.mac = mac

    def open(
        self,
        fname: str,
        ext: str = "",
        mode: str = "w",
        append: bool = False,
    ):
        return File(fname, ext, mode, append, self.mac)
