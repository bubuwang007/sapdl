"""Tests for comparison nodes."""

from sapdl.core.ast.number_parameter_nodes.comparison_nodes import (
    EQNode,
    GENode,
    GTNode,
    LENode,
    LTNode,
    NENode,
)


class TestEQNode:
    """Test cases for EQNode class."""

    def test_basic(self):
        """Test basic equality comparison."""
        node = EQNode("A", "B")
        assert node.apdl(0) == "A,EQ,B"

    def test_with_numbers(self):
        """Test equality comparison with number operands."""
        node = EQNode(1, 2)
        assert node.apdl(0) == "1,EQ,2"

    def test_type(self):
        """Test type attribute."""
        assert EQNode("A", "B").type == "expr"


class TestNENode:
    """Test cases for NENode class."""

    def test_basic(self):
        """Test basic inequality comparison."""
        node = NENode("A", "B")
        assert node.apdl(0) == "A,NE,B"

    def test_with_numbers(self):
        """Test inequality comparison with number operands."""
        node = NENode(1, 2)
        assert node.apdl(0) == "1,NE,2"


class TestGTNode:
    """Test cases for GTNode class."""

    def test_basic(self):
        """Test basic greater-than comparison."""
        node = GTNode("A", "B")
        assert node.apdl(0) == "A,GT,B"

    def test_with_numbers(self):
        """Test greater-than comparison with number operands."""
        node = GTNode(5, 3)
        assert node.apdl(0) == "5,GT,3"


class TestGENode:
    """Test cases for GENode class."""

    def test_basic(self):
        """Test basic greater-than-or-equal comparison."""
        node = GENode("A", "B")
        assert node.apdl(0) == "A,GE,B"

    def test_with_numbers(self):
        """Test greater-than-or-equal comparison with number operands."""
        node = GENode(5, 3)
        assert node.apdl(0) == "5,GE,3"


class TestLTNode:
    """Test cases for LTNode class."""

    def test_basic(self):
        """Test basic less-than comparison."""
        node = LTNode("A", "B")
        assert node.apdl(0) == "A,LT,B"

    def test_with_numbers(self):
        """Test less-than comparison with number operands."""
        node = LTNode(1, 5)
        assert node.apdl(0) == "1,LT,5"


class TestLENode:
    """Test cases for LENode class."""

    def test_basic(self):
        """Test basic less-than-or-equal comparison."""
        node = LENode("A", "B")
        assert node.apdl(0) == "A,LE,B"

    def test_with_numbers(self):
        """Test less-than-or-equal comparison with number operands."""
        node = LENode(3, 5)
        assert node.apdl(0) == "3,LE,5"


class TestMixedOperands:
    """Test comparison nodes with mixed operand types."""

    def test_eq_mixed(self):
        """A == 1."""
        node = EQNode("A", 1)
        assert node.apdl(0) == "A,EQ,1"

    def test_ne_mixed(self):
        """A != 1."""
        node = NENode("A", 1)
        assert node.apdl(0) == "A,NE,1"

    def test_gt_mixed(self):
        """A > 1."""
        node = GTNode("A", 1)
        assert node.apdl(0) == "A,GT,1"

    def test_ge_mixed(self):
        """A >= 1."""
        node = GENode("A", 1)
        assert node.apdl(0) == "A,GE,1"

    def test_lt_mixed(self):
        """A < 1."""
        node = LTNode("A", 1)
        assert node.apdl(0) == "A,LT,1"

    def test_le_mixed(self):
        """A <= 1."""
        node = LENode("A", 1)
        assert node.apdl(0) == "A,LE,1"
