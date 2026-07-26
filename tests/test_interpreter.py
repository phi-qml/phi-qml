"""
Tests for Φ‑QML Interpreter
"""

import unittest
from phi_qml.lexer import Lexer
from phi_qml.parser import Parser
from phi_qml.interpreter import Interpreter
from phi_qml.ast_nodes import (
    Program, LetStatement, FnDecl, FnCall, VarRef,
    IntLiteral, SubstrateModulo, BinaryOp, ReturnStmt, Block
)


class TestInterpreter(unittest.TestCase):
    """Test cases for the Φ‑QML interpreter."""

    def _interpret(self, source: str):
        """Helper: tokenize, parse, and interpret source."""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        return interpreter.interpret(ast)

    def test_integer_literal(self):
        """Integer literals evaluate to themselves."""
        result = self._interpret("42")
        self.assertEqual(result, 42)

    def test_float_literal(self):
        """Float literals evaluate to themselves."""
        result = self._interpret("3.14")
        self.assertAlmostEqual(result, 3.14)

    def test_string_literal(self):
        """String literals evaluate to themselves."""
        result = self._interpret('"hello"')
        self.assertEqual(result, "hello")

    def test_bool_literal(self):
        """Boolean literals evaluate to themselves."""
        self.assertTrue(self._interpret("true"))
        self.assertFalse(self._interpret("false"))

    def test_binary_addition(self):
        """Addition of two integers."""
        result = self._interpret("5 + 3")
        self.assertEqual(result, 8)

    def test_binary_subtraction(self):
        """Subtraction of two integers."""
        result = self._interpret("10 - 3")
        self.assertEqual(result, 7)

    def test_binary_multiplication(self):
        """Multiplication of two integers."""
        result = self._interpret("4 * 3")
        self.assertEqual(result, 12)

    def test_binary_division(self):
        """Division of two integers."""
        result = self._interpret("10 / 2")
        self.assertEqual(result, 5)

    def test_binary_modulo_classical(self):
        """Classical modulo operator."""
        result = self._interpret("42 % 13")
        self.assertEqual(result, 3)

    def test_unary_minus(self):
        """Unary minus."""
        result = self._interpret("-5")
        self.assertEqual(result, -5)

    def test_unary_not(self):
        """Logical not."""
        self.assertFalse(self._interpret("!true"))
        self.assertTrue(self._interpret("!false"))

    def test_comparisons(self):
        """All comparison operators."""
        for op, a, b, expected in [
            ("==", 5, 5, True), ("==", 5, 3, False),
            ("!=", 5, 3, True), ("!=", 5, 5, False),
            ("<", 5, 10, True), ("<", 10, 5, False),
            (">", 10, 5, True), (">", 5, 10, False),
            ("<=", 5, 5, True), ("<=", 6, 5, False),
            (">=", 5, 5, True), (">=", 4, 5, False),
        ]:
            result = self._interpret(f"{a} {op} {b}")
            self.assertEqual(result, expected, f"Failed: {a} {op} {b}")

    def test_substrate_modulo(self):
        """Substrate* Modulo operation."""
        result = self._interpret("mod(42, 13)")
        self.assertEqual(result, 3)

    def test_substrate_modulo_large(self):
        """Substrate* Modulo with large numbers."""
        result = self._interpret("mod(2^256 + 123456789, 997)")
        self.assertEqual(result, 394)

    def test_let_statement(self):
        """Variable binding and reference."""
        source = """
        let x = 42;
        x
        """
        result = self._interpret(source)
        self.assertEqual(result, 42)

    def test_let_with_expression(self):
        """Let with an expression value."""
        source = """
        let x = 5 + 3;
        x
        """
        result = self._interpret(source)
        self.assertEqual(result, 8)

    def test_if_true(self):
        """If statement with true condition."""
        source = """
        let x = 0;
        if true { x = 1; }
        x
        """
        result = self._interpret(source)
        self.assertEqual(result, 1)

    def test_if_false(self):
        """If statement with false condition."""
        source = """
        let x = 0;
        if false { x = 1; } else { x = 2; }
        x
        """
        result = self._interpret(source)
        self.assertEqual(result, 2)

    def test_while_loop(self):
        """While loop with a counter."""
        source = """
        let x = 0;
        while x < 5 { x = x + 1; }
        x
        """
        result = self._interpret(source)
        self.assertEqual(result, 5)

    def test_function_definition_and_call(self):
        """Define and call a simple function."""
        source = """
        fn add(a, b) { return a + b; }
        add(5, 3)
        """
        result = self._interpret(source)
        self.assertEqual(result, 8)

    def test_builtin_phi_score(self):
        """Built‑in phi_score function."""
        result = self._interpret("phi_score(42, 1)")
        self.assertAlmostEqual(result, 1.0)

    def test_builtin_pi(self):
        """Built‑in PI constant."""
        import math
        result = self._interpret("PI")
        self.assertAlmostEqual(result, math.pi)

    def test_builtin_phi(self):
        """Built‑in PHI constant (golden ratio)."""
        result = self._interpret("PHI")
        self.assertAlmostEqual(result, 1.618033988749895)

    def test_array_literal(self):
        """Array literal evaluation."""
        result = self._interpret("[1, 2, 3]")
        self.assertEqual(result, [1, 2, 3])

    def test_index_access(self):
        """Array index access."""
        source = """
        let arr = [10, 20, 30];
        arr[1]
        """
        result = self._interpret(source)
        self.assertEqual(result, 20)

    def test_nested_blocks(self):
        """Nested block scopes."""
        source = """
        let x = 1;
        {
            let x = 2;
        }
        x
        """
        result = self._interpret(source)
        self.assertEqual(result, 1)

    def test_return_statement(self):
        """Return from a function."""
        source = """
        fn f() { return 42; }
        f()
        """
        result = self._interpret(source)
        self.assertEqual(result, 42)


if __name__ == "__main__":
    unittest.main()
