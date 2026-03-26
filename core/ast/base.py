"""Base classes for APDL AST nodes."""

from __future__ import annotations

from abc import ABC, abstractmethod
import warnings
from typing import List, Literal


class Node(ABC):
    """Abstract base class for all APDL AST nodes."""

    type: Literal["expr", "statement", "block"]

    @abstractmethod
    def apdl(self, indent_level: int = 0) -> list[str] | str:
        """Generate APDL representation.

        Args:
            indent_level: Current indentation level.

        Returns:
            The APDL command string or a list of APDL command strings.
        """
        pass


class Body:
    """Statement block container.

    Holds a sequence of nodes for sequential execution.
    """

    def __init__(self):
        self.nodes: List[Node] = []

    def add(self, node: Node) -> None:
        """Add a node to the body.

        Args:
            node: The node to add.
        """
        if not isinstance(node, Node):
            raise TypeError(f"Expected a Node instance, got {type(node).__name__}")
        self.nodes.append(node)

    def apdl(self, indent_level: int = 0) -> list[str]:
        """Generate APDL representation.

        Args:
            indent_level: Current indentation level.

        Returns:
            List of APDL command strings for all nodes in the body.
        """
        ret = []
        for node in self.nodes:
            if node.type == "expr":
                warnings.warn(
                    f"{node} is an expression node, which cannot be directly executed."
                )
                continue
            tmp = node.apdl(indent_level)
            if isinstance(tmp, list):
                ret.extend(tmp)
            else:
                ret.append(tmp)
        return ret

    def print_apdl(self, indent_level: int = 0) -> None:
        """Print the APDL representation of the body.

        Args:
            indent_level: Current indentation level.
        """
        for line in self.apdl(indent_level):
            print(line)
