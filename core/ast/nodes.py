"""Concrete APDL AST node types."""

from typing import Optional, List
from sapdl import INDENT
from .base import Node, Body


class Command(Node):
    """Represents a single APDL command.

    Attributes:
        cmd: The command string (e.g., "K,1,0,0,0").
    """

    __slots__ = ["cmd"]

    def __init__(self, cmd: str):
        self.cmd = cmd

    def apdl(self, indent_level: int = 0) -> str:
        return f"{INDENT * indent_level}{self.cmd}\n"


class Comment(Node):
    """Represents an APDL comment.

    Attributes:
        text: The comment text (without ! symbol).
    """

    __slots__ = ["text"]

    def __init__(self, text: str):
        self.text = text

    def apdl(self, indent_level: int = 0) -> str:
        return f"{INDENT * indent_level}! {self.text}\n"


class Do(Node):
    """DO loop node (*DO/*ENDDO).

    Attributes:
        var: Loop variable name.
        start: Start value.
        end: End value.
        step: Step value (default "1").
        body: Loop body block.
    """

    __slots__ = ["var", "start", "end", "step", "body"]

    def __init__(
        self, var: str, start: str, end: str, step: str = "1"
    ):
        self.var = var
        self.start = start
        self.end = end
        self.step = step
        self.body = Body()

    def apdl(self, indent_level: int = 0) -> str:
        indent = INDENT * indent_level
        result = f"{indent}*DO,{self.var},{self.start},{self.end},{self.step}\n"
        result += self.body.apdl(indent_level + 1)
        result += f"{indent}*ENDDO\n"
        return result


class If(Node):
    """IF conditional node (*IF/*ELIF/*ELSE/*ENDIF).

    Attributes:
        condition: Condition expression (e.g., "val,GT,0").
        then_body: THEN branch block.
        elif_conditions: List of (condition, body) tuples for *ELIF.
        else_body: ELSE branch block (optional).
    """

    __slots__ = ["condition", "then_body", "elif_conditions", "else_body"]

    def __init__(self, condition: str):
        self.condition = condition
        self.then_body = Body()
        self.elif_conditions: List[tuple[str, Body]] = []
        self.else_body: Optional[Body] = None

    def apdl(self, indent_level: int = 0) -> str:
        indent = INDENT * indent_level
        result = f"{indent}*IF,{self.condition},THEN\n"
        result += self.then_body.apdl(indent_level + 1)

        for cond, body in self.elif_conditions:
            result += f"{indent}*ELIF,{cond}\n"
            result += body.apdl(indent_level + 1)

        if self.else_body is not None:
            result += f"{indent}*ELSE\n"
            result += self.else_body.apdl(indent_level + 1)

        result += f"{indent}*ENDIF\n"
        return result


class Macro(Node):
    """Macro definition node.

    Attributes:
        name: Macro name.
        params: Parameter names list (optional).
        body: Macro body block.
    """

    __slots__ = ["name", "params", "body"]

    def __init__(self, name: str, params: Optional[List[str]] = None):
        self.name = name
        self.params = params
        self.body = Body()

    def apdl(self, indent_level: int = 0) -> str:
        indent = INDENT * indent_level
        result = ""
        if self.params:
            param_str = ",".join(self.params)
            result += f"{indent}*ARG,{param_str}\n"
        result += self.body.apdl(indent_level)
        result += f"{indent}*RETURN\n"
        return result
