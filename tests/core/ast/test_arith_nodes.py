"""Tests for arithmetic nodes."""

import pytest

from sapdl.core.ast.number_parameter_nodes.arith_nodes import (
    AddNode,
    DivNode,
    MulNode,
    NegNode,
    PowNode,
    SubNode,
)


class TestAddNode:
    """Test cases for AddNode class."""

    def test_basic(self):
        """Test basic addition."""
        node = AddNode("A", "B")
        assert node.apdl(0) == "A+B"

    def test_with_numbers(self):
        """Test addition with number operands."""
        node = AddNode(1, 2)
        assert node.apdl(0) == "1+2"

    def test_priority(self):
        """Test priority attribute."""
        assert AddNode("A", "B").priority == 4


class TestSubNode:
    """Test cases for SubNode class."""

    def test_basic(self):
        """Test basic subtraction."""
        node = SubNode("A", "B")
        assert node.apdl(0) == "A-B"

    def test_with_numbers(self):
        """Test subtraction with number operands."""
        node = SubNode(5, 3)
        assert node.apdl(0) == "5-3"


class TestMulNode:
    """Test cases for MulNode class."""

    def test_basic(self):
        """Test basic multiplication."""
        node = MulNode("A", "B")
        assert node.apdl(0) == "A*B"

    def test_priority(self):
        """Test priority attribute."""
        assert MulNode("A", "B").priority == 3


class TestDivNode:
    """Test cases for DivNode class."""

    def test_basic(self):
        """Test basic division."""
        node = DivNode("A", "B")
        assert node.apdl(0) == "A/B"


class TestPowNode:
    """Test cases for PowNode class."""

    def test_basic(self):
        """Test basic power operation."""
        node = PowNode("A", "B")
        assert node.apdl(0) == "A**B"

    def test_priority(self):
        """Test priority attribute."""
        assert PowNode("A", "B").priority == 1

    def test_pow_neg_on_right(self):
        """a ** -b should be a**-b."""
        node = PowNode("a", NegNode("b"))
        assert node.apdl(0) == "a**(-b)"

    def test_pow_neg_on_left(self):
        """-a ** b is (-a) ** b due to NegNode having priority 1 < 2."""
        node = PowNode(NegNode("a"), "b")
        assert node.apdl(0) == "(-a)**b"


class TestNegNode:
    """Test cases for NegNode class."""

    def test_basic(self):
        """Test basic negation."""
        node = NegNode("A")
        assert node.apdl(0) == "-A"

    def test_priority(self):
        """Test priority attribute."""
        assert NegNode("A").priority == 2


class TestPrecedence:
    """Test cases for operator precedence and parentheses."""

    def test_add_mul_no_paren(self):
        """a + b * c should not have parentheses."""
        node = AddNode("a", MulNode("b", "c"))
        assert node.apdl(0) == "a+b*c"

    def test_mul_add_paren_left(self):
        """a * b + c — no parens needed, mul has higher priority."""
        node = AddNode(MulNode("a", "b"), "c")
        assert node.apdl(0) == "a*b+c"

    def test_sub_mul_no_paren(self):
        """a - b * c should not have parentheses."""
        node = SubNode("a", MulNode("b", "c"))
        assert node.apdl(0) == "a-b*c"

    def test_div_sub_no_paren(self):
        """a / b - c should not have parentheses."""
        node = SubNode(DivNode("a", "b"), "c")
        assert node.apdl(0) == "a/b-c"


class TestRightAssociativity:
    """Test cases for right associativity of power operator."""

    def test_pow_right_assoc(self):
        """a ** b ** c should be a ** (b ** c) — no parens on right."""
        node = PowNode("a", PowNode("b", "c"))
        assert node.apdl(0) == "a**(b**c)"

    def test_pow_left_assoc_needs_paren(self):
        """(a ** b) ** c needs parentheses on left."""
        node = PowNode(PowNode("a", "b"), "c")
        assert node.apdl(0) == "(a**b)**c"

    def test_pow_lower_on_right_no_paren(self):
        """a ** b + c should be a ** (b + c) — no parens needed on right."""
        node = PowNode("a", AddNode("b", "c"))
        assert node.apdl(0) == "a**(b+c)"

    def test_pow_lower_on_left_needs_paren(self):
        """a ** b * c needs parentheses because left has lower priority."""
        node = PowNode("a", MulNode("b", "c"))
        assert node.apdl(0) == "a**(b*c)"


class TestComplexExpressions:
    """Test cases for complex nested expressions."""

    def test_nested_add_mul_sub(self):
        """a + b * c - d."""
        node = SubNode(AddNode("a", MulNode("b", "c")), "d")
        assert node.apdl(0) == "a+b*c-d"

    def test_pow_mul_add(self):
        """a ** b * c + d."""
        node = AddNode(MulNode(PowNode("a", "b"), "c"), "d")
        assert node.apdl(0) == "a**b*c+d"

    def test_neg_pow(self):
        """-a ** b should be (-a) ** b."""
        node = PowNode(NegNode("a"), "b")
        assert node.apdl(0) == "(-a)**b"

    def test_neg_mul_pow(self):
        """-a * b ** c is (-a) * (b ** c), no extra parens on pow since right < priority."""
        node = MulNode(NegNode("a"), PowNode("b", "c"))
        assert node.apdl(0) == "-a*b**c"

    def test_pow_neg_on_left(self):
        """-a ** -b should be (-a)**(-b)."""
        node = PowNode(NegNode("a"), NegNode("b"))
        assert node.apdl(0) == "(-a)**(-b)"


class TestDeepNesting:
    """Test deeply nested expressions."""

    def test_triple_pow(self):
        """((a ** b) ** c) ** d needs parens on both inner pows."""
        node = PowNode(PowNode(PowNode("a", "b"), "c"), "d")
        assert node.apdl(0) == "((a**b)**c)**d"

    def test_add_mul_div_chain(self):
        """a + b * c / d - e."""
        node = SubNode(AddNode("a", DivNode(MulNode("b", "c"), "d")), "e")
        assert node.apdl(0) == "a+b*c/d-e"

    def test_mul_pow_mul(self):
        """a * b ** c * d is (a * (b ** c)) * d, no parens needed."""
        node = MulNode(MulNode("a", PowNode("b", "c")), "d")
        assert node.apdl(0) == "a*b**c*d"

    def test_div_pow_div(self):
        """a / b ** c / d is (a / (b ** c)) / d."""
        node = DivNode(DivNode("a", PowNode("b", "c")), "d")
        assert node.apdl(0) == "a/b**c/d"

    def test_complex_precedence_1(self):
        """a * b + c * d - e * f."""
        node = SubNode(AddNode(MulNode("a", "b"), MulNode("c", "d")), MulNode("e", "f"))
        assert node.apdl(0) == "a*b+c*d-e*f"

    def test_complex_precedence_2(self):
        """a + b ** c * d."""
        node = AddNode("a", MulNode(PowNode("b", "c"), "d"))
        assert node.apdl(0) == "a+b**c*d"

    def test_complex_precedence_3(self):
        """a ** b + c ** d."""
        node = AddNode(PowNode("a", "b"), PowNode("c", "d"))
        assert node.apdl(0) == "a**b+c**d"

    def test_complex_precedence_4(self):
        """a * b ** c + d * e ** f."""
        node = AddNode(MulNode("a", PowNode("b", "c")), MulNode("d", PowNode("e", "f")))
        assert node.apdl(0) == "a*b**c+d*e**f"

    def test_nested_pow_with_add(self):
        """a ** (b + c) ** d — right assoc, but left side is add which needs parens."""
        node = PowNode(PowNode("a", AddNode("b", "c")), "d")
        assert node.apdl(0) == "(a**(b+c))**d"

    def test_add_in_pow_right(self):
        """a ** (b + c) should produce a**(b+c)."""
        node = PowNode("a", AddNode("b", "c"))
        assert node.apdl(0) == "a**(b+c)"

    def test_sub_in_pow_right(self):
        """a ** (b - c) should produce a**(b-c)."""
        node = PowNode("a", SubNode("b", "c"))
        assert node.apdl(0) == "a**(b-c)"

    def test_mul_in_pow_right(self):
        """a ** (b * c) should produce a**(b*c)."""
        node = PowNode("a", MulNode("b", "c"))
        assert node.apdl(0) == "a**(b*c)"

    def test_div_in_pow_right(self):
        """a ** (b / c) should produce a**(b/c)."""
        node = PowNode("a", DivNode("b", "c"))
        assert node.apdl(0) == "a**(b/c)"

    def test_neg_in_pow_right(self):
        """a ** -b should produce a**(-b)."""
        node = PowNode("a", NegNode("b"))
        assert node.apdl(0) == "a**(-b)"

    def test_neg_in_pow_left(self):
        """-a ** b should produce (-a)**b."""
        node = PowNode(NegNode("a"), "b")
        assert node.apdl(0) == "(-a)**b"


class TestAssociativity:
    """Test associativity of operations."""

    def test_add_left_associative(self):
        """(a + b) + c = a + b + c."""
        node = AddNode(AddNode("a", "b"), "c")
        assert node.apdl(0) == "a+b+c"

    def test_add_right_associative(self):
        """a + (b + c) = a + b + c."""
        node = AddNode("a", AddNode("b", "c"))
        assert node.apdl(0) == "a+b+c"

    def test_sub_left_associative(self):
        """(a - b) - c = a - b - c."""
        node = SubNode(SubNode("a", "b"), "c")
        assert node.apdl(0) == "a-b-c"

    def test_sub_not_associative(self):
        """a - (b - c) = a - b + c, parens needed."""
        node = SubNode("a", SubNode("b", "c"))
        assert node.apdl(0) == "a-(b-c)"

    def test_mul_left_associative(self):
        """(a * b) * c = a * b * c."""
        node = MulNode(MulNode("a", "b"), "c")
        assert node.apdl(0) == "a*b*c"

    def test_mul_right_associative(self):
        """a * (b * c) = a * b * c."""
        node = MulNode("a", MulNode("b", "c"))
        assert node.apdl(0) == "a*b*c"

    def test_div_not_associative(self):
        """a / (b / c) = a * c / b, parens needed."""
        node = DivNode("a", DivNode("b", "c"))
        assert node.apdl(0) == "a/(b/c)"

    def test_pow_right_associative_chain(self):
        """a ** b ** c ** d = a ** (b ** (c ** d))."""
        node = PowNode("a", PowNode("b", PowNode("c", "d")))
        assert node.apdl(0) == "a**(b**(c**d))"


class TestMixedOperations:
    """Test mixed operations with various combinations."""

    def test_neg_add(self):
        """-(a + b) should be -(a+b)."""
        node = NegNode(AddNode("a", "b"))
        assert node.apdl(0) == "-(a+b)"

    def test_neg_mul(self):
        """-(a * b) should be -a*b."""
        node = NegNode(MulNode("a", "b"))
        assert node.apdl(0) == "-(a*b)"

    def test_neg_pow(self):
        """-(a ** b) should be -a**b."""
        node = NegNode(PowNode("a", "b"))
        assert node.apdl(0) == "-a**b"

    def test_add_neg(self):
        """a + -b should be a+-b."""
        node = AddNode("a", NegNode("b"))
        assert node.apdl(0) == "a+-b"

    def test_mul_neg(self):
        """a * -b should be a*-b."""
        node = MulNode("a", NegNode("b"))
        assert node.apdl(0) == "a*-b"

    def test_sub_neg(self):
        """a - -b should be a--b."""
        node = SubNode("a", NegNode("b"))
        assert node.apdl(0) == "a--b"

    def test_complex_expression_1(self):
        """(a + b) * (c + d)."""
        node = MulNode(AddNode("a", "b"), AddNode("c", "d"))
        assert node.apdl(0) == "(a+b)*(c+d)"

    def test_complex_expression_2(self):
        """(a - b) * (c - d)."""
        node = MulNode(SubNode("a", "b"), SubNode("c", "d"))
        assert node.apdl(0) == "(a-b)*(c-d)"

    def test_complex_expression_3(self):
        """(a + b) / (c - d)."""
        node = DivNode(AddNode("a", "b"), SubNode("c", "d"))
        assert node.apdl(0) == "(a+b)/(c-d)"

    def test_complex_expression_4(self):
        """a ** (b + c) * d."""
        node = MulNode(PowNode("a", AddNode("b", "c")), "d")
        assert node.apdl(0) == "a**(b+c)*d"

    def test_complex_expression_5(self):
        """d * a ** (b + c)."""
        node = MulNode("d", PowNode("a", AddNode("b", "c")))
        assert node.apdl(0) == "d*a**(b+c)"


class TestNumericOperands:
    """Test with numeric operands."""

    def test_add_numbers(self):
        """1 + 2."""
        node = AddNode(1, 2)
        assert node.apdl(0) == "1+2"

    def test_sub_numbers(self):
        """5 - 3."""
        node = SubNode(5, 3)
        assert node.apdl(0) == "5-3"

    def test_mul_numbers(self):
        """4 * 3."""
        node = MulNode(4, 3)
        assert node.apdl(0) == "4*3"

    def test_div_numbers(self):
        """10 / 2."""
        node = DivNode(10, 2)
        assert node.apdl(0) == "10/2"

    def test_pow_numbers(self):
        """2 ** 3."""
        node = PowNode(2, 3)
        assert node.apdl(0) == "2**3"

    def test_neg_number(self):
        """-5."""
        node = NegNode(5)
        assert node.apdl(0) == "-5"

    def test_mixed_operands(self):
        """a + 1."""
        node = AddNode("a", 1)
        assert node.apdl(0) == "a+1"

    def test_complex_numeric(self):
        """(1 + 2) * 3."""
        node = MulNode(AddNode(1, 2), 3)
        assert node.apdl(0) == "(1+2)*3"

    def test_pow_with_numbers(self):
        """2 ** 3 + 1."""
        node = AddNode(PowNode(2, 3), 1)
        assert node.apdl(0) == "2**3+1"

    def test_neg_pow_number(self):
        """-(2 ** 3) should be -2**3."""
        node = NegNode(PowNode(2, 3))
        assert node.apdl(0) == "-2**3"
