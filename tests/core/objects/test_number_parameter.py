"""Tests for NumberParameter arithmetic and comparison operations."""

import pytest
from sapdl.core import Mac
from sapdl.core.objects import NumberParameter
from sapdl.core.ast.number_parameter_nodes.arith_nodes import (
    AddNode,
    DivNode,
    MulNode,
    NegNode,
    PowNode,
    SubNode,
)
from sapdl.core.ast.number_parameter_nodes.comparison_nodes import (
    EQNode,
    GENode,
    GTNode,
    LENode,
    LTNode,
    NENode,
)


class TestNumberParameterNeg:
    """Test cases for unary negation."""

    def test_neg_parameter(self):
        """Test negation of NumberParameter."""
        mac = Mac()
        A = NumberParameter(mac, "A")
        result = -A
        assert isinstance(result, NegNode)
        assert result.apdl(0) == "-A"


class TestNumberParameterAdd:
    """Test cases for addition (+)."""

    def test_add_two_parameters(self):
        """Test parameter + parameter."""
        mac = Mac()
        A = NumberParameter(mac, "A")
        B = NumberParameter(mac, "B")
        result = A + B
        assert isinstance(result, AddNode)
        assert result.apdl(0) == "A+B"

    def test_add_with_literal(self):
        """Test parameter + number."""
        mac = Mac()
        A = NumberParameter(mac, "A")
        result = A + 5
        assert result.apdl(0) == "A+5"

    def test_radd_with_literal(self):
        """Test number + parameter (reflected)."""
        mac = Mac()
        A = NumberParameter(mac, "A")
        result = 5 + A
        assert result.apdl(0) == "5+A"

    def test_iadd(self):
        """Test += operator."""
        mac = Mac()
        A = NumberParameter(mac, "A")
        A += 5
        # Check that body contains the assignment
        lines = mac.body.apdl(0)
        assert any("A+5" in line for line in lines)


class TestNumberParameterSub:
    """Test cases for subtraction (-)."""

    def test_sub_two_parameters(self):
        """Test parameter - parameter."""
        mac = Mac()
        A = NumberParameter(mac, "A")
        B = NumberParameter(mac, "B")
        result = A - B
        assert isinstance(result, SubNode)
        assert result.apdl(0) == "A-B"

    def test_sub_with_literal(self):
        """Test parameter - number."""
        mac = Mac()
        A = NumberParameter(mac, "A")
        result = A - 5
        assert result.apdl(0) == "A-5"

    def test_rsub_with_literal(self):
        """Test number - parameter (reflected)."""
        mac = Mac()
        A = NumberParameter(mac, "A")
        result = 5 - A
        assert result.apdl(0) == "5-A"

    def test_isub(self):
        """Test -= operator."""
        mac = Mac()
        A = NumberParameter(mac, "A")
        A -= 5
        lines = mac.body.apdl(0)
        assert any("A-5" in line for line in lines)


class TestNumberParameterMul:
    """Test cases for multiplication (*)."""

    def test_mul_two_parameters(self):
        """Test parameter * parameter."""
        mac = Mac()
        A = NumberParameter(mac, "A")
        B = NumberParameter(mac, "B")
        result = A * B
        assert isinstance(result, MulNode)
        assert result.apdl(0) == "A*B"

    def test_mul_with_literal(self):
        """Test parameter * number."""
        mac = Mac()
        A = NumberParameter(mac, "A")
        result = A * 5
        assert result.apdl(0) == "A*5"

    def test_rmul_with_literal(self):
        """Test number * parameter (reflected)."""
        mac = Mac()
        A = NumberParameter(mac, "A")
        result = 5 * A
        assert result.apdl(0) == "5*A"

    def test_imul(self):
        """Test *= operator."""
        mac = Mac()
        A = NumberParameter(mac, "A")
        A *= 5
        lines = mac.body.apdl(0)
        assert any("A*5" in line for line in lines)


class TestNumberParameterDiv:
    """Test cases for division (/)."""

    def test_div_two_parameters(self):
        """Test parameter / parameter."""
        mac = Mac()
        A = NumberParameter(mac, "A")
        B = NumberParameter(mac, "B")
        result = A / B
        assert isinstance(result, DivNode)
        assert result.apdl(0) == "A/B"

    def test_div_with_literal(self):
        """Test parameter / number."""
        mac = Mac()
        A = NumberParameter(mac, "A")
        result = A / 5
        assert result.apdl(0) == "A/5"

    def test_rdiv_with_literal(self):
        """Test number / parameter (reflected)."""
        mac = Mac()
        A = NumberParameter(mac, "A")
        result = 5 / A
        assert result.apdl(0) == "5/A"

    def test_itruediv(self):
        """Test /= operator."""
        mac = Mac()
        A = NumberParameter(mac, "A")
        A /= 5
        lines = mac.body.apdl(0)
        assert any("A/5" in line for line in lines)


class TestNumberParameterPow:
    """Test cases for power (**)."""

    def test_pow_two_parameters(self):
        """Test parameter ** parameter."""
        mac = Mac()
        A = NumberParameter(mac, "A")
        B = NumberParameter(mac, "B")
        result = A ** B
        assert isinstance(result, PowNode)
        assert result.apdl(0) == "A**B"

    def test_pow_with_literal(self):
        """Test parameter ** number."""
        mac = Mac()
        A = NumberParameter(mac, "A")
        result = A ** 2
        assert result.apdl(0) == "A**2"

    def test_rpow_with_literal(self):
        """Test number ** parameter (reflected)."""
        mac = Mac()
        A = NumberParameter(mac, "A")
        result = 2 ** A
        assert result.apdl(0) == "2**A"

    def test_ipow(self):
        """Test **= operator."""
        mac = Mac()
        A = NumberParameter(mac, "A")
        A **= 2
        lines = mac.body.apdl(0)
        assert any("A**2" in line for line in lines)


class TestNumberParameterChained:
    """Test cases for chained operations."""

    def test_chained_arithmetic(self):
        """Test chained arithmetic operations.

        Note: Due to operator precedence, A + B * C is parsed as A + (B * C).
        """
        mac = Mac()
        A = NumberParameter(mac, "A")
        B = NumberParameter(mac, "B")
        C = NumberParameter(mac, "C")
        result = A + B * C
        assert result.apdl(0) == "A+B*C"

    def test_complex_expression(self):
        """Test complex expression with multiple operations on nodes."""
        mac = Mac()
        A = NumberParameter(mac, "A")
        B = NumberParameter(mac, "B")
        result = (A + B) * (A - B)
        # (A+B)*(A-B) - parentheses needed due to equal priority
        assert result.apdl(0) == "(A+B)*(A-B)"

    def test_node_chained_operations(self):
        """Test that arithmetic nodes support further operations."""
        mac = Mac()
        A = NumberParameter(mac, "A")
        B = NumberParameter(mac, "B")
        # A + B is an AddNode, which should support further operations
        sum_ab = A + B
        result = sum_ab * 2
        assert result.apdl(0) == "(A+B)*2"


class TestNumberParameterComparison:
    """Test cases for comparison operations."""

    def test_eq(self):
        """Test == operator."""
        mac = Mac()
        A = NumberParameter(mac, "A")
        B = NumberParameter(mac, "B")
        result = A == B
        assert isinstance(result, EQNode)
        assert result.apdl(0) == "A,EQ,B"

    def test_eq_with_literal(self):
        """Test == with literal."""
        mac = Mac()
        A = NumberParameter(mac, "A")
        result = A == 5
        assert result.apdl(0) == "A,EQ,5"

    def test_req(self):
        """Test reflected == (5 == A).

        Note: Python falls back to A.__eq__(5), so result is A,EQ,5.
        """
        mac = Mac()
        A = NumberParameter(mac, "A")
        result = 5 == A
        assert result.apdl(0) == "A,EQ,5"

    def test_ne(self):
        """Test != operator."""
        mac = Mac()
        A = NumberParameter(mac, "A")
        B = NumberParameter(mac, "B")
        result = A != B
        assert isinstance(result, NENode)
        assert result.apdl(0) == "A,NE,B"

    def test_lt(self):
        """Test < operator."""
        mac = Mac()
        A = NumberParameter(mac, "A")
        B = NumberParameter(mac, "B")
        result = A < B
        assert isinstance(result, LTNode)
        assert result.apdl(0) == "A,LT,B"

    def test_rlt(self):
        """Test reflected < (5 < A).

        Python falls back to A.__gt__(5), so result is A,GT,5.
        """
        mac = Mac()
        A = NumberParameter(mac, "A")
        result = 5 < A
        assert isinstance(result, GTNode)
        assert result.apdl(0) == "A,GT,5"

    def test_le(self):
        """Test <= operator."""
        mac = Mac()
        A = NumberParameter(mac, "A")
        B = NumberParameter(mac, "B")
        result = A <= B
        assert isinstance(result, LENode)
        assert result.apdl(0) == "A,LE,B"

    def test_rle(self):
        """Test reflected <= (5 <= A).

        Python falls back to A.__ge__(5), so result is A,GE,5.
        """
        mac = Mac()
        A = NumberParameter(mac, "A")
        result = 5 <= A
        assert isinstance(result, GENode)
        assert result.apdl(0) == "A,GE,5"

    def test_gt(self):
        """Test > operator."""
        mac = Mac()
        A = NumberParameter(mac, "A")
        B = NumberParameter(mac, "B")
        result = A > B
        assert isinstance(result, GTNode)
        assert result.apdl(0) == "A,GT,B"

    def test_rgt(self):
        """Test reflected > (5 > A).

        Python falls back to A.__lt__(5), so result is A,LT,5.
        """
        mac = Mac()
        A = NumberParameter(mac, "A")
        result = 5 > A
        assert isinstance(result, LTNode)
        assert result.apdl(0) == "A,LT,5"

    def test_ge(self):
        """Test >= operator."""
        mac = Mac()
        A = NumberParameter(mac, "A")
        B = NumberParameter(mac, "B")
        result = A >= B
        assert isinstance(result, GENode)
        assert result.apdl(0) == "A,GE,B"

    def test_rge(self):
        """Test reflected >= (5 >= A).

        Python falls back to A.__le__(5), so result is A,LE,5.
        """
        mac = Mac()
        A = NumberParameter(mac, "A")
        result = 5 >= A
        assert isinstance(result, LENode)
        assert result.apdl(0) == "A,LE,5"


class TestComparisonNodeChained:
    """Test cases for chained comparison operations."""

    def test_comparison_with_literal(self):
        """Test comparison with literal value."""
        mac = Mac()
        A = NumberParameter(mac, "A")
        result = A > 10
        assert result.apdl(0) == "A,GT,10"

    def test_comparison_chained_with_and(self):
        """Test comparison can be combined (e.g., for IF conditions)."""
        mac = Mac()
        A = NumberParameter(mac, "A")
        B = NumberParameter(mac, "B")
        gt_node = A > B
        lt_node = A < 100
        assert gt_node.apdl(0) == "A,GT,B"
        assert lt_node.apdl(0) == "A,LT,100"
