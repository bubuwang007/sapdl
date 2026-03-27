from dataclasses import dataclass, field
from typing import Dict, Optional, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .mac import Mac


@dataclass
class Symbol:
    name: str
    type: str
    scope: str
    _mac: "Mac" = field(default=None, repr=False)

    def _delete(self):
        """从符号表中删除此符号，并生成 APDL 删除命令"""
        if self._mac and hasattr(self._mac, 'symbol_table'):
            self._mac.symbol_table.remove(self.name)
        if self._mac and hasattr(self._mac, 'run'):
            self._mac.run(f"*DEL,{self.name}")


class SymbolTable:
    def __init__(self):
        self.symbols: Dict[str, Symbol] = {}

    def define(self, name: str, type: str, scope: str = "local") -> Symbol:
        if name in self.symbols:
            raise ValueError(f"Symbol '{name}' is already defined.")
        symbol = Symbol(name, type, scope)
        self.symbols[name] = symbol
        return symbol

    def lookup(self, name: str) -> Optional[Symbol]:
        return self.symbols.get(name)

    def remove(self, name: str) -> None:
        """从符号表中移除指定名称的符号"""
        self.symbols.pop(name, None)

    def iter_local(self):
        """迭代本地变量符号"""
        for sym in self.symbols.values():
            if sym.scope == "local":
                yield sym

    def iter_global(self):
        """迭代全局变量符号"""
        for sym in self.symbols.values():
            if sym.scope == "global":
                yield sym

    def iter_global_names(self):
        """迭代全局变量名称"""
        for sym in self.iter_global():
            yield sym.name
