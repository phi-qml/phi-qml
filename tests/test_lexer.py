"""
Tests for Φ‑QML Lexer
"""

import unittest
from phi_qml.lexer import Lexer, TokenKind


class TestLexer(unittest.TestCase):
    """Test cases for the Φ‑QML lexer."""

    def _tokenize(self, source: str) -> list:
        """Helper: tokenize source and return list of token kinds."""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        return [t.kind for t in tokens if t.kind != TokenKind.EOF]

    def _tokenize_with_values(self, source: str) -> list:
        """Helper: tokenize source and return list of (kind, value)."""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        return [(t.kind, t.value) for t in tokens if t.kind != TokenKind.EOF]

    def test_keywords(self):
        """All keywords are recognized."""
        for word, kind in Lexer.KEYWORDS.items():
            kinds = self._tokenize(word)
            self.assertEqual(len(kinds), 1, f"Keyword '{word}' not recognized")
            self.assertEqual(kinds[0], kind, f"Wrong kind for '{word}'")

    def test_identifiers(self):
        """Identifiers are tokenized correctly."""
        tokens = self._tokenize_with_values("x y123 _private")
        self.assertEqual(len(tokens), 3)
        for (kind, val) in tokens:
            self.assertEqual(kind, TokenKind.IDENT)
        self.assertEqual(tokens[0][1], "x")
        self.assertEqual(tokens[1][1], "y123")
        self.assertEqual(tokens[2][1], "_private")

    def test_integers(self):
        """Integer literals are parsed."""
        tokens = self._tokenize_with_values("0 42 999")
        self.assertEqual(len(tokens), 3)
        for kind, _ in tokens:
            self.assertEqual(kind, TokenKind.INT)
        self.assertEqual(tokens[0][1], 0)
        self.assertEqual(tokens[1][1], 42)
        self.assertEqual(tokens[2][1], 999)

    def test_floats(self):
        """Float literals are parsed."""
        tokens = self._tokenize_with_values("3.14 0.001 2.0")
        self.assertEqual(len(tokens), 3)
        for kind, _ in tokens:
            self.assertEqual(kind, TokenKind.FLOAT)
        self.assertAlmostEqual(tokens[0][1], 3.14)
        self.assertAlmostEqual(tokens[1][1], 0.001)
        self.assertAlmostEqual(tokens[2][1], 2.0)

    def test_strings(self):
        """String literals are parsed correctly."""
        tokens = self._tokenize_with_values('"hello" "Φ‑QML" ""')
        self.assertEqual(len(tokens), 3)
        for kind, _ in tokens:
            self.assertEqual(kind, TokenKind.STRING)
        self.assertEqual(tokens[0][1], "hello")
        self.assertEqual(tokens[1][1], "Φ‑QML")
        self.assertEqual(tokens[2][1], "")

    def test_operators(self):
        """All operator tokens are recognized."""
        operator_map = {
            "+": TokenKind.PLUS,
            "-": TokenKind.MINUS,
            "*": TokenKind.STAR,
            "/": TokenKind.SLASH,
            "%": TokenKind.PERCENT,
            "=": TokenKind.ASSIGN,
            "==": TokenKind.EQ,
            "!=": TokenKind.NEQ,
            "<": TokenKind.LT,
            ">": TokenKind.GT,
            "<=": TokenKind.LTE,
            ">=": TokenKind.GTE,
            "&&": TokenKind.AND,
            "||": TokenKind.OR,
            "!": TokenKind.BANG,
            "+=": TokenKind.PLUS_ASSIGN,
            "-=": TokenKind.MINUS_ASSIGN,
            "*=": TokenKind.STAR_ASSIGN,
            "/=": TokenKind.SLASH_ASSIGN,
            "%=": TokenKind.PERCENT_ASSIGN,
            "->": TokenKind.ARROW,
            "|>": TokenKind.PIPE,
        }
        for op, expected_kind in operator_map.items():
            kinds = self._tokenize(op)
            self.assertEqual(len(kinds), 1, f"Operator '{op}' not recognized")
            self.assertEqual(kinds[0], expected_kind, f"Wrong kind for '{op}'")

    def test_delimiters(self):
        """Delimiter tokens are recognized."""
        delim_map = {
            "(": TokenKind.LPAREN,
            ")": TokenKind.RPAREN,
            "{": TokenKind.LBRACE,
            "}": TokenKind.RBRACE,
            "[": TokenKind.LBRACKET,
            "]": TokenKind.RBRACKET,
            ";": TokenKind.SEMICOLON,
            ":": TokenKind.COLON,
            ",": TokenKind.COMMA,
            ".": TokenKind.DOT,
        }
        for delim, expected_kind in delim_map.items():
            kinds = self._tokenize(delim)
            self.assertEqual(len(kinds), 1, f"Delimiter '{delim}' not recognized")
            self.assertEqual(kinds[0], expected_kind, f"Wrong kind for '{delim}'")

    def test_comments(self):
        """Line and block comments are ignored."""
        source = "// this is a comment\nlet x = 42;"
        tokens = self._tokenize(source)
        self.assertEqual(len(tokens), 4)  # let, IDENT, ASSIGN, INT
        self.assertEqual(tokens[0], TokenKind.LET)

        source2 = "/* block\ncomment */ let y = 10;"
        tokens2 = self._tokenize(source2)
        self.assertEqual(len(tokens2), 4)

    def test_substrate_modulo(self):
        """mod keyword is recognized and call syntax parsed."""
        source = "mod(42, 13)"
        tokens = self._tokenize_with_values(source)
        expected = [
            (TokenKind.MOD, None),
            (TokenKind.LPAREN, None),
            (TokenKind.INT, 42),
            (TokenKind.COMMA, None),
            (TokenKind.INT, 13),
            (TokenKind.RPAREN, None),
        ]
        self.assertEqual(len(tokens), len(expected))
        for (actual, exp) in zip(tokens, expected):
            self.assertEqual(actual[0], exp[0])
            if exp[1] is not None:
                self.assertEqual(actual[1], exp[1])

    def test_full_program(self):
        """Tokenization of a small program."""
        source = """
        fn main() {
            let a = 42;
            let r = mod(a, 13);
            println(r);
        }
        """
        kinds = self._tokenize(source)
        expected = [
            TokenKind.FN, TokenKind.IDENT, TokenKind.LPAREN, TokenKind.RPAREN, TokenKind.LBRACE,
            TokenKind.LET, TokenKind.IDENT, TokenKind.ASSIGN, TokenKind.INT, TokenKind.SEMICOLON,
            TokenKind.LET, TokenKind.IDENT, TokenKind.ASSIGN, TokenKind.MOD, TokenKind.LPAREN,
            TokenKind.IDENT, TokenKind.COMMA, TokenKind.INT, TokenKind.RPAREN, TokenKind.SEMICOLON,
            TokenKind.IDENT, TokenKind.LPAREN, TokenKind.IDENT, TokenKind.RPAREN, TokenKind.SEMICOLON,
            TokenKind.RBRACE,
        ]
        self.assertEqual(len(kinds), len(expected))
        for actual, exp in zip(kinds, expected):
            self.assertEqual(actual, exp, f"Expected {exp}, got {actual}")


if __name__ == "__main__":
    unittest.main()
