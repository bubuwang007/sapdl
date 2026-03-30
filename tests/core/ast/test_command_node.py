"""Tests for CommandNode."""

import pytest

from sapdl.core.ast.command_node import CommandNode


class TestCommandNode:
    """Test cases for CommandNode class."""

    def test_init(self):
        """Test CommandNode initialization."""
        node = CommandNode("K,1,0,0,0")
        assert node.cmd == "K,1,0,0,0"

    def test_init_with_different_commands(self):
        """Test CommandNode with various APDL commands."""
        commands = [
            "K,1,0,0,0",
            "L,1,2",
            "A,1,2,3,4",
            "FINISH",
            "/PREP7",
        ]
        for cmd in commands:
            node = CommandNode(cmd)
            assert node.cmd == cmd

    def test_apdl_no_indent(self):
        """Test apdl() method without indentation."""
        node = CommandNode("K,1,0,0,0")
        assert node.apdl(0) == "K,1,0,0,0"

    def test_apdl_with_indent(self):
        """Test apdl() method with indentation."""
        node = CommandNode("K,1,0,0,0")
        assert node.apdl(indent_level=1) == "    K,1,0,0,0"

    def test_apdl_with_multiple_indent(self):
        """Test apdl() method with multiple indentation levels."""
        node = CommandNode("L,1,2")
        assert node.apdl(indent_level=2) == "        L,1,2"

    def test_apdl_zero_indent(self):
        """Test apdl() method with zero indent level."""
        node = CommandNode("FINISH")
        assert node.apdl(indent_level=0) == "FINISH"

    def test_cmd_attribute_is_string(self):
        """Test that cmd attribute is a string."""
        node = CommandNode("K,1")
        assert isinstance(node.cmd, str)

    def test_empty_command(self):
        """Test CommandNode with empty command string."""
        node = CommandNode("")
        assert node.cmd == ""
        assert node.apdl(0) == ""

    def test_command_with_comma_separated_values(self):
        """Test command with multiple comma-separated parameters."""
        node = CommandNode("K,1,0,0,0,1,2,3")
        assert node.cmd == "K,1,0,0,0,1,2,3"
        assert node.apdl(0) == "K,1,0,0,0,1,2,3"
