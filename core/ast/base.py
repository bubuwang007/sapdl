"""Base classes for APDL AST nodes."""

from abc import ABC, abstractmethod
from typing import List


class Node(ABC):
    """Abstract base class for all APDL AST nodes."""

    @abstractmethod
    def apdl(self, indent_level: int = 0) -> str:
        """Generate APDL representation.

        Args:
            indent_level: Current indentation level.

        Returns:
            The APDL command string.
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        """String representation of the node."""
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
        self.nodes.append(node)

    def apdl(self, indent_level: int = 0) -> str:
        """Generate APDL representation.

        Args:
            indent_level: Current indentation level.

        Returns:
            The APDL command string.
        """
        return "".join(node.apdl(indent_level) for node in self.nodes)
