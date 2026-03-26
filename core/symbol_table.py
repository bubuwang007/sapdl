from dataclasses import dataclass
from typing import Dict, Optional, Any


@dataclass
class Symbol:
    name: str
    type: str
    scope: str


class SymbolTable:
    def __init__(self):
        self.symbols: Dict[str, Symbol] = {}

    def define(self, name: str, type: str, scope: str = "local") -> None:
        if name in self.symbols:
            raise ValueError(f"Symbol '{name}' is already defined.")
        self.symbols[name] = Symbol(name, type, scope)

    def lookup(self, name: str) -> Optional[Symbol]:
        return self.symbols.get(name)
