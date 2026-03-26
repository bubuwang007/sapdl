from sapdl import INDENT
from ..base import Node, Body


class IfNode(Node):
    """IF conditional node (*IF/*ELIF/*ELSE/*ENDIF)."""

    __slots__ = [
        "if_condition",
        "if_body",
        "elif_conditions",
        "elif_bodies",
        "else_body",
        "type",
    ]

    def __init__(self):
        self.type = "block"
        self.if_condition = ""
        self.if_body = Body()
        self.elif_conditions = []
        self.elif_bodies = []
        self.else_body = None

    def add_elif(self, condition: str):
        new_body = Body()
        self.elif_conditions.append(condition)
        self.elif_bodies.append(new_body)
        return new_body

    def add_else(self):
        self.else_body = Body()
        return self.else_body

    def apdl(self, indent_level: int) -> list[str]:
        ret = []
        indent = INDENT * indent_level
        ret.append(f"{indent}*IF,{self.if_condition},THEN")
        ret.extend(self.if_body.apdl(indent_level + 1))
        for cond, body in zip(self.elif_conditions, self.elif_bodies):
            ret.append(f"{indent}*ELIF,{cond}")
            ret.extend(body.apdl(indent_level + 1))
        if self.else_body:
            ret.append(f"{indent}*ELSE")
            ret.extend(self.else_body.apdl(indent_level + 1))
        ret.append(f"{indent}*ENDIF")
        return ret

    def __str__(self) -> str:
        return (
            f"IfNode(if_condition={self.if_condition!r}, "
            f"if_body={self.if_body!r}, "
            f"elif_conditions={self.elif_conditions!r}, "
            f"elif_bodies={self.elif_bodies!r}, "
            f"else_body={self.else_body!r})"
        )
