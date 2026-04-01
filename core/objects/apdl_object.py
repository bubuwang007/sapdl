from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sapdl.core import Mac


class ApdlObject:
    _name: str
    mac: Mac
    _alive: bool = True

    def __init__(self, mac: Mac, name: str):
        self.mac = mac
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    def __str__(self):
        return self.name

    def _new(self):
        raise NotImplementedError("Subclasses must implement _new method.")

    def _delete(self):
        raise NotImplementedError("Subclasses must implement _delete method.")

    def delete(self):
        raise NotImplementedError("Subclasses must implement delete method.")

    def to_string(self):
        return f"'{self.name}'"
