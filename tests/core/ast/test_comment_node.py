"""Tests for CommentNode."""

import pytest

from sapdl.core.ast.comment_node import CommentNode


class TestCommentNode:
    """Test cases for CommentNode class."""

    def test_init(self):
        """Test CommentNode initialization."""
        node = CommentNode("This is a comment")
        assert node.text == "This is a comment"

    def test_init_with_various_comment_texts(self):
        """Test CommentNode with various comment texts."""
        texts = [
            "Material definition",
            "Mesh control",
            "Boundary conditions",
            "",
            "Multi-word comment",
        ]
        for text in texts:
            node = CommentNode(text)
            assert node.text == text

    def test_apdl_no_indent(self):
        """Test apdl() method without indentation."""
        node = CommentNode("Material definition")
        assert node.apdl() == "! Material definition"

    def test_apdl_with_indent(self):
        """Test apdl() method with indentation."""
        node = CommentNode("Mesh control")
        assert node.apdl(indent_level=1) == "    ! Mesh control"

    def test_apdl_with_multiple_indent(self):
        """Test apdl() method with multiple indentation levels."""
        node = CommentNode("Boundary conditions")
        assert node.apdl(indent_level=2) == "        ! Boundary conditions"

    def test_apdl_zero_indent(self):
        """Test apdl() method with zero indent level."""
        node = CommentNode("Simple comment")
        assert node.apdl(indent_level=0) == "! Simple comment"

    def test_str_repr(self):
        """Test __str__() method returns correct representation."""
        node = CommentNode("This is a comment")
        assert str(node) == "CommentNode(text='This is a comment')"

    def test_str_repr_with_special_chars(self):
        """Test __str__() with special characters in text."""
        node = CommentNode("Comment with 'quotes'")
        assert str(node) == "CommentNode(text=\"Comment with 'quotes'\")"

    def test_text_attribute_is_string(self):
        """Test that text attribute is a string."""
        node = CommentNode("Test")
        assert isinstance(node.text, str)

    def test_empty_comment(self):
        """Test CommentNode with empty comment text."""
        node = CommentNode("")
        assert node.text == ""
        assert node.apdl() == "! "

    def test_comment_with_leading_space(self):
        """Test comment text with leading spaces in the text itself."""
        node = CommentNode("  indented text")
        assert node.apdl() == "!   indented text"

    def test_comment_with_multiple_words(self):
        """Test comment with multiple words."""
        node = CommentNode("This is a multi-word comment")
        assert node.apdl() == "! This is a multi-word comment"

    def test_comment_preserves_exclamation_in_text(self):
        """Test that text is stored as-is (exclamation is added by apdl)."""
        node = CommentNode("! Already has exclamation in text")
        assert node.text == "! Already has exclamation in text"
        assert node.apdl() == "! ! Already has exclamation in text"
