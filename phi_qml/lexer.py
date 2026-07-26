"""
Φ‑QML Lexer — Tokenizace zdrojového kódu
"""

from enum import Enum, auto
from typing import Any, Optional
from dataclasses import dataclass


class TokenKind(Enum):
    """Všechny druhy tokenů rozpoznávané lexerem Φ‑QML."""
    # Klíčová slova
    FN = auto(); LET = auto(); MUT = auto(); IF = auto(); ELSE = auto()
    WHILE = auto(); FOR = auto(); IN = auto(); RETURN = auto()
    MOD = auto(); COLLAPSE = auto(); FIELD = auto(); QUBIT = auto()
    CLASSICAL = auto(); H = auto(); CNOT = auto(); MEASURE = auto()
    TRUE = auto(); FALSE = auto(); AMPLITUDE = auto()
    WHEN = auto(); UNTIL = auto(); CONVERGENCE = auto()
    WRITE = auto(); READ = auto(); PROJECT = auto()
    # Literály
    IDENT = auto(); INT = auto(); FLOAT = auto(); STRING = auto()
    # Operátory
    PLUS = auto(); MINUS = auto(); STAR = auto(); SLASH = auto(); PERCENT = auto()
    EQ = auto(); NEQ = auto(); LT = auto(); GT = auto(); LTE = auto(); GTE = auto()
    AND = auto(); OR = auto(); NOT = auto(); BANG = auto()
    ASSIGN = auto(); PLUS_ASSIGN = auto(); MINUS_ASSIGN = auto()
    STAR_ASSIGN = auto(); SLASH_ASSIGN = auto(); PERCENT_ASSIGN = auto()
    # Oddělovače
    LPAREN = auto(); RPAREN = auto(); LBRACE = auto(); RBRACE = auto()
    LBRACKET = auto(); RBRACKET = auto(); SEMICOLON = auto(); COLON = auto()
    COMMA = auto(); ARROW = auto(); DOT = auto(); PIPE = auto()
    # Speciální
    EOF = auto(); NEWLINE = auto()


@dataclass
class Token:
    """Jeden token s druhem, hodnotou a pozicí ve zdrojovém kódu."""
    kind: TokenKind
    value: Any = None
    line: int = 0
    col: int = 0

    def __repr__(self):
        val_str = f"'{self.value}'" if self.value is not None else ""
        return f"Token({self.kind.name}, {val_str}, line={self.line})"


class Lexer:
    """Lexer pro Φ‑QML — převádí zdrojový kód na proud tokenů."""

    KEYWORDS = {
        "fn": TokenKind.FN, "let": TokenKind.LET, "mut": TokenKind.MUT,
        "if": TokenKind.IF, "else": TokenKind.ELSE, "while": TokenKind.WHILE,
        "for": TokenKind.FOR, "in": TokenKind.IN, "return": TokenKind.RETURN,
        "mod": TokenKind.MOD, "collapse": TokenKind.COLLAPSE,
        "field": TokenKind.FIELD, "qubit": TokenKind.QUBIT,
        "classical": TokenKind.CLASSICAL, "H": TokenKind.H,
        "CNOT": TokenKind.CNOT, "measure": TokenKind.MEASURE,
        "true": TokenKind.TRUE, "false": TokenKind.FALSE,
        "amplitude": TokenKind.AMPLITUDE,
        "when": TokenKind.WHEN, "until": TokenKind.UNTIL,
        "convergence": TokenKind.CONVERGENCE,
        "write": TokenKind.WRITE, "read": TokenKind.READ, "project": TokenKind.PROJECT,
    }

    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.col = 1

    def _advance(self) -> str:
        if self.pos >= len(self.source):
            return '\0'
        ch = self.source[self.pos]
        self.pos += 1
        if ch == '\n':
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return ch

    def _peek(self) -> str:
        return self.source[self.pos] if self.pos < len(self.source) else '\0'

    def _skip_whitespace_and_comments(self):
        while self.pos < len(self.source):
            ch = self._peek()
            if ch in ' \t\r':
                self._advance()
            elif ch == '/' and self.pos + 1 < len(self.source) and self.source[self.pos + 1] == '/':
                while self._peek() not in ('\n', '\0'):
                    self._advance()
            elif ch == '/' and self.pos + 1 < len(self.source) and self.source[self.pos + 1] == '*':
                self._advance()
                self._advance()
                while self.pos < len(self.source):
                    if self._peek() == '*' and self.pos + 1 < len(self.source) and self.source[self.pos + 1] == '/':
                        self._advance()
                        self._advance()
                        break
                    self._advance()
            else:
                break

    def _read_number(self, first: str) -> Token:
        num_str = first
        is_float = False
        while self._peek().isdigit():
            num_str += self._advance()
        if self._peek() == '.' and self.pos + 1 < len(self.source) and self.source[self.pos + 1].isdigit():
            is_float = True
            num_str += self._advance()
            while self._peek().isdigit():
                num_str += self._advance()
        return Token(
            TokenKind.FLOAT if is_float else TokenKind.INT,
            float(num_str) if is_float else int(num_str),
            self.line, self.col
        )

    def _read_string(self) -> Token:
        s = ""
        while True:
            ch = self._advance()
            if ch == '"':
                return Token(TokenKind.STRING, s, self.line, self.col)
            if ch == '\\':
                s += self._advance()
            elif ch == '\0':
                raise SyntaxError(f"Unterminated string at line {self.line}")
            else:
                s += ch

    def _read_ident(self, first: str) -> Token:
        ident = first
        while self._peek().isalnum() or self._peek() == '_':
            ident += self._advance()
        kind = self.KEYWORDS.get(ident, TokenKind.IDENT)
        if kind == TokenKind.TRUE:
            return Token(kind, True, self.line, self.col)
        if kind == TokenKind.FALSE:
            return Token(kind, False, self.line, self.col)
        return Token(kind, ident if kind == TokenKind.IDENT else None, self.line, self.col)

    def next_token(self) -> Token:
        self._skip_whitespace_and_comments()
        if self.pos >= len(self.source):
            return Token(TokenKind.EOF, None, self.line, self.col)

        ch = self._advance()

        # Operátory
        if ch == '+':
            if self._peek() == '=':
                self._advance()
                return Token(TokenKind.PLUS_ASSIGN)
            return Token(TokenKind.PLUS)
        if ch == '-':
            if self._peek() == '>':
                self._advance()
                return Token(TokenKind.ARROW)
            if self._peek() == '=':
                self._advance()
                return Token(TokenKind.MINUS_ASSIGN)
            return Token(TokenKind.MINUS)
        if ch == '*':
            if self._peek() == '=':
                self._advance()
                return Token(TokenKind.STAR_ASSIGN)
            return Token(TokenKind.STAR)
        if ch == '/':
            if self._peek() == '=':
                self._advance()
                return Token(TokenKind.SLASH_ASSIGN)
            return Token(TokenKind.SLASH)
        if ch == '%':
            if self._peek() == '=':
                self._advance()
                return Token(TokenKind.PERCENT_ASSIGN)
            return Token(TokenKind.PERCENT)
        if ch == '=':
            if self._peek() == '=':
                self._advance()
                return Token(TokenKind.EQ)
            return Token(TokenKind.ASSIGN)
        if ch == '!':
            if self._peek() == '=':
                self._advance()
                return Token(TokenKind.NEQ)
            return Token(TokenKind.BANG)
        if ch == '<':
            if self._peek() == '=':
                self._advance()
                return Token(TokenKind.LTE)
            return Token(TokenKind.LT)
        if ch == '>':
            if self._peek() == '=':
                self._advance()
                return Token(TokenKind.GTE)
            return Token(TokenKind.GT)
        if ch == '&':
            if self._peek() == '&':
                self._advance()
                return Token(TokenKind.AND)
            return Token(TokenKind.STAR)
        if ch == '|':
            if self._peek() == '|':
                self._advance()
                return Token(TokenKind.OR)
            if self._peek() == '>':
                self._advance()
                return Token(TokenKind.PIPE)
            return Token(TokenKind.PIPE)

        # Oddělovače
        if ch == '(': return Token(TokenKind.LPAREN)
        if ch == ')': return Token(TokenKind.RPAREN)
        if ch == '{': return Token(TokenKind.LBRACE)
        if ch == '}': return Token(TokenKind.RBRACE)
        if ch == '[': return Token(TokenKind.LBRACKET)
        if ch == ']': return Token(TokenKind.RBRACKET)
        if ch == ';': return Token(TokenKind.SEMICOLON)
        if ch == ':': return Token(TokenKind.COLON)
        if ch == ',': return Token(TokenKind.COMMA)
        if ch == '.': return Token(TokenKind.DOT)

        # Řetězec
        if ch == '"': return self._read_string()

        # Číslo
        if ch.isdigit(): return self._read_number(ch)

        # Identifikátor nebo klíčové slovo
        if ch.isalpha() or ch == '_': return self._read_ident(ch)

        raise SyntaxError(f"Unexpected character '{ch}' at line {self.line}, col {self.col}")

    def tokenize(self) -> list:
        """Vrátí všechny tokeny jako seznam (vhodné pro testování)."""
        tokens = []
        while True:
            t = self.next_token()
            tokens.append(t)
            if t.kind == TokenKind.EOF:
                break
        return tokens
