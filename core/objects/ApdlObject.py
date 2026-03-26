from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sapdl.core import Mac


class ApdlObject:
    _name: str
    mac: Mac
    _alive: bool = True

    def __init__(self, mac: Mac, name: str):
        self._mac = mac
        self._name = name

    @property
    def name(self) -> str:
        if not self._alive:
            raise RuntimeError(f"Object {self._name} is not alive.")
        return self._name

    def __str__(self):
        return self.name

    def _new(self):
        raise NotImplementedError("Subclasses must implement _new method.")

    def _delete(self):
        raise NotImplementedError("Subclasses must implement _delete method.")
