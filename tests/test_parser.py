"""
Tests for Φ‑QML Parser
"""

import unittest
from phi_qml.lexer import Lexer
from phi_qml.parser import Parser, ParseError
from phi_qml.ast_nodes import (
    Program, LetStatement, FnDecl, FnCall,
    BinaryOp, UnaryOp, VarRef,
    IntLiteral, FloatLiteral, StringLiteral, BoolLiteral,
    SubstrateModulo, CollapseExpr,
    IfStmt, WhileStmt, WhenExpr, UntilLoop, ForLoop,
    ReturnStmt, Block,
    ArrayLiteral, IndexAccess,
    HolographicWrite, HolographicRead, HolographicProject,
)


class TestParser(unittest.TestCase):
    """Test cases for the Φ‑QML parser."""

    def _parse(self, source: str) -> Program:
        """Helper: tokenize and parse source, return the AST Program."""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        return parser.parse()

    def test_empty_program(self):
        """An empty source produces an empty Program."""
        program = self._parse("")
        self.assertIsInstance(program, Program)
        self.assertEqual(len(program.statements), 0)

    def test_integer_literal(self):
        """Single integer literal is parsed."""
        program = self._parse("42")
        self.assertEqual(len(program.statements), 1)
        expr = program.statements[0]
        self.assertIsInstance(expr, IntLiteral)
        self.assertEqual(expr.value, 42)

    def test_float_literal(self):
        """Single float literal is parsed."""
        program = self._parse("3.14")
        self.assertEqual(len(program.statements), 1)
        expr = program.statements[0]
        self.assertIsInstance(expr, FloatLiteral)
        self.assertAlmostEqual(expr.value, 3.14)

    def test_string_literal(self):
        """Single string literal is parsed."""
        program = self._parse('"hello"')
        self.assertEqual(len(program.statements), 1)
        expr = program.statements[0]
        self.assertIsInstance(expr, StringLiteral)
        self.assertEqual(expr.value, "hello")

    def test_bool_literals(self):
        """True and false are parsed."""
        for val, expected in [("true", True), ("false", False)]:
            program = self._parse(val)
            expr = program.statements[0]
            self.assertIsInstance(expr, BoolLiteral)
            self.assertEqual(expr.value, expected)

    def test_variable_reference(self):
        """A single identifier is parsed as a variable reference."""
        program = self._parse("x")
        expr = program.statements[0]
        self.assertIsInstance(expr, VarRef)
        self.assertEqual(expr.name, "x")

    def test_let_statement(self):
        """Basic let statement with integer value."""
        program = self._parse("let x = 42;")
        self.assertEqual(len(program.statements), 1)
        stmt = program.statements[0]
        self.assertIsInstance(stmt, LetStatement)
        self.assertEqual(stmt.name, "x")
        self.assertIsNone(stmt.type_annotation)
        self.assertFalse(stmt.mutable)
        self.assertIsInstance(stmt.value, IntLiteral)
        self.assertEqual(stmt.value.value, 42)

    def test_let_mutable(self):
        """Mutable let statement."""
        program = self._parse("let mut counter = 0;")
        stmt = program.statements[0]
        self.assertTrue(stmt.mutable)
        self.assertEqual(stmt.name, "counter")

    def test_let_with_type_annotation(self):
        """Let statement with type annotation."""
        program = self._parse("let x: qubit = |0>;")
        stmt = program.statements[0]
        self.assertEqual(stmt.name, "x")
        self.assertEqual(stmt.type_annotation, "qubit")

    def test_substrate_modulo(self):
        """Substrate* Modulo expression."""
        program = self._parse("mod(42, 13)")
        expr = program.statements[0]
        self.assertIsInstance(expr, SubstrateModulo)
        self.assertIsInstance(expr.a, IntLiteral)
        self.assertIsInstance(expr.n, IntLiteral)
        self.assertEqual(expr.a.value, 42)
        self.assertEqual(expr.n.value, 13)

    def test_collapse(self):
        """Collapse expression."""
        program = self._parse("collapse(field)")
        expr = program.statements[0]
        self.assertIsInstance(expr, CollapseExpr)
        self.assertIsInstance(expr.field_expr, VarRef)
        self.assertEqual(expr.field_expr.name, "field")

    def test_binary_operations(self):
        """Binary operations with correct precedence."""
        # Addition
        program = self._parse("1 + 2")
        expr = program.statements[0]
        self.assertIsInstance(expr, BinaryOp)
        self.assertEqual(expr.op, "+")

        # Multiplication over addition
        program = self._parse("1 + 2 * 3")
        expr = program.statements[0]
        self.assertIsInstance(expr, BinaryOp)
        self.assertEqual(expr.op, "+")
        self.assertIsInstance(expr.right, BinaryOp)
        self.assertEqual(expr.right.op, "*")

    def test_unary_operations(self):
        """Unary minus and negation."""
        program = self._parse("-5")
        expr = program.statements[0]
        self.assertIsInstance(expr, UnaryOp)
        self.assertEqual(expr.op, "-")
        self.assertIsInstance(expr.operand, IntLiteral)

        program = self._parse("!true")
        expr = program.statements[0]
        self.assertIsInstance(expr, UnaryOp)
        self.assertEqual(expr.op, "!")

    def test_comparisons(self):
        """Comparison operators."""
        for op, op_name in [(
            "==", "eq"), ("!=", "neq"), ("<", "lt"), (">", "gt"), ("<=", "lte"), (">=", "gte")
        ]:
            program = self._parse(f"a {op} b")
            expr = program.statements[0]
            self.assertIsInstance(expr, BinaryOp)
            self.assertEqual(expr.op, op_name)

    def test_function_call(self):
        """Function call with arguments."""
        program = self._parse("println(42)")
        expr = program.statements[0]
        self.assertIsInstance(expr, FnCall)
        self.assertEqual(expr.name, "println")
        self.assertEqual(len(expr.arguments), 1)
        self.assertIsInstance(expr.arguments[0], IntLiteral)

    def test_function_call_no_args(self):
        """Function call without arguments."""
        program = self._parse("f()")
        expr = program.statements[0]
        self.assertIsInstance(expr, FnCall)
        self.assertEqual(expr.name, "f")
        self.assertEqual(len(expr.arguments), 0)

    def test_function_declaration(self):
        """Simple function declaration."""
        program = self._parse("fn add(a: Int, b: Int) -> Int { return a + b; }")
        self.assertEqual(len(program.statements), 1)
        decl = program.statements[0]
        self.assertIsInstance(decl, FnDecl)
        self.assertEqual(decl.name, "add")
        self.assertEqual(len(decl.params), 2)
        self.assertEqual(decl.params[0], ("a", "Int"))
        self.assertEqual(decl.params[1], ("b", "Int"))
        self.assertEqual(decl.return_type, "Int")
        self.assertEqual(len(decl.body), 1)
        self.assertIsInstance(decl.body[0], ReturnStmt)

    def test_if_statement(self):
        """If statement with else."""
        program = self._parse("if x { 1 } else { 2 }")
        stmt = program.statements[0]
        self.assertIsInstance(stmt, IfStmt)
        self.assertIsInstance(stmt.condition, VarRef)
        self.assertEqual(len(stmt.then_branch), 1)
        self.assertEqual(len(stmt.else_branch), 1)

    def test_while_statement(self):
        """While loop."""
        program = self._parse("while x > 0 { x = x - 1; }")
        stmt = program.statements[0]
        self.assertIsInstance(stmt, WhileStmt)
        self.assertIsInstance(stmt.condition, BinaryOp)

    def test_when_expression(self):
        """When expression with two branches."""
        program = self._parse("when condition { 1, 2 }")
        expr = program.statements[0]
        self.assertIsInstance(expr, WhenExpr)
        self.assertIsInstance(expr.condition, VarRef)
        self.assertIsInstance(expr.then_expr, IntLiteral)
        self.assertIsInstance(expr.else_expr, IntLiteral)

    def test_until_loop(self):
        """Until convergence loop."""
        program = self._parse("until convergence { x = x / 2; }")
        stmt = program.statements[0]
        self.assertIsInstance(stmt, UntilLoop)
        self.assertEqual(len(stmt.body), 1)

    def test_for_loop(self):
        """For loop over a range."""
        program = self._parse("for i in 0..10 { println(i); }")
        stmt = program.statements[0]
        self.assertIsInstance(stmt, ForLoop)
        self.assertEqual(stmt.var_name, "i")
        self.assertEqual(len(stmt.body), 1)

    def test_array_literal(self):
        """Array literal."""
        program = self._parse("[1, 2, 3]")
        expr = program.statements[0]
        self.assertIsInstance(expr, ArrayLiteral)
        self.assertEqual(len(expr.elements), 3)

    def test_index_access(self):
        """Array index access."""
        program = self._parse("arr[0]")
        expr = program.statements[0]
        self.assertIsInstance(expr, IndexAccess)
        self.assertIsInstance(expr.array, VarRef)
        self.assertEqual(expr.array.name, "arr")
        self.assertIsInstance(expr.index, IntLiteral)
        self.assertEqual(expr.index.value, 0)

    def test_holographic_write(self):
        """Holographic write method."""
        program = self._parse("f.write(42, 100)")
        expr = program.statements[0]
        self.assertIsInstance(expr, HolographicWrite)
        self.assertIsInstance(expr.field_expr, VarRef)

    def test_holographic_read(self):
        """Holographic read method."""
        program = self._parse("f.read(42)")
        expr = program.statements[0]
        self.assertIsInstance(expr, HolographicRead)

    def test_holographic_project(self):
        """Holographic project method."""
        program = self._parse("f.project(43, 42, fn(x) { x * 2 })")
        expr = program.statements[0]
        self.assertIsInstance(expr, HolographicProject)

    def test_parse_error(self):
        """Invalid syntax raises ParseError."""
        with self.assertRaises(ParseError):
            self._parse("fn missing_paren {")

    def test_full_program(self):
        """A complete program parses successfully."""
        source = """
        fn main() {
            let a = 42;
            let r = mod(a, 13);
            println(r);
        }
        """
        program = self._parse(source)
        self.assertIsInstance(program, Program)
        self.assertEqual(len(program.statements), 1)
        fn_decl = program.statements[0]
        self.assertIsInstance(fn_decl, FnDecl)
        self.assertEqual(fn_decl.name, "main")
        self.assertEqual(len(fn_decl.body), 3)
        self.assertIsInstance(fn_decl.body[0], LetStatement)
        self.assertIsInstance(fn_decl.body[1], LetStatement)
        self.assertIsInstance(fn_decl.body[2], FnCall)


if __name__ == "__main__":
    unittest.main()
