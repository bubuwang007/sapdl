from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sapdl.core import Mac


class Custom:

    def __init__(self, mac: Mac):
        self.mac = mac
