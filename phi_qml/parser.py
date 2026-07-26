"""
Φ‑QML Parser — Syntactic analysis and AST construction
"""

from typing import List, Optional, Tuple
from phi_qml.lexer import Token, TokenKind
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


class ParseError(Exception):
    """Exception for parsing errors."""
    def __init__(self, message: str, line: int = 0):
        self.line = line
        super().__init__(f"Parse error at line {line}: {message}")


class Parser:
    """
    Parser for Φ‑QML.
    Converts a stream of tokens into an AST according to the grammar:

    program      → statement*
    statement    → let_stmt | fn_decl | if_stmt | while_stmt
                 | until_loop | when_expr | for_loop
                 | return_stmt | block | expression
    let_stmt     → 'let' 'mut'? IDENT (':' type)? '=' expression
    fn_decl      → 'fn' IDENT '(' params? ')' ('->' type)? block
    if_stmt      → 'if' expression block ('else' (block | if_stmt))?
    while_stmt   → 'while' expression block
    until_loop   → 'until' 'convergence'? block
    when_expr    → 'when' expression '{' expression ',' expression '}'
    for_loop     → 'for' IDENT 'in' expression block
    block        → '{' statement* '}'
    return_stmt  → 'return' expression?
    expression   → comparison
    comparison   → term (('==' | '!=' | '<' | '>' | '<=' | '>=') term)*
    term         → factor (('+' | '-') factor)*
    factor       → unary (('*' | '/' | '%') unary)*
    unary        → ('-' | '!')? call
    call         → primary ('(' args? ')' | '[' expression ']' | '.' IDENT '(' args? ')')*
    primary      → INT | FLOAT | STRING | TRUE | FALSE | IDENT
                 | 'mod' '(' expression ',' expression ')'
                 | 'collapse' '(' expression ')'
                 | '(' expression ')'
                 | '[' (expression (',' expression)*)? ']'
    """

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def _current(self) -> Token:
        """Returns the current token."""
        return self.tokens[self.pos]

    def _advance(self) -> Token:
        """Advances to the next token and returns the previous one."""
        t = self.tokens[self.pos]
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return t

    def _expect(self, kind: TokenKind, msg: str = "") -> Token:
        """Expects a token of the given kind; otherwise raises an exception."""
        if self._current().kind != kind:
            raise ParseError(
                f"Expected {kind.name}, got {self._current().kind.name}. {msg}",
                self._current().line
            )
        return self._advance()

    def parse(self) -> Program:
        """Main entry point – returns the AST of the whole program."""
        stmts = []
        while self._current().kind != TokenKind.EOF:
            stmts.append(self._parse_statement())
        return Program(stmts)

    # ─── Statements ────────────────────────────────────────────────────

    def _parse_statement(self) -> 'ASTNode':
        """Parses a single statement."""
        if self._current().kind == TokenKind.LET:
            return self._parse_let()
        if self._current().kind == TokenKind.FN:
            return self._parse_fn()
        if self._current().kind == TokenKind.IF:
            return self._parse_if()
        if self._current().kind == TokenKind.WHILE:
            return self._parse_while()
        if self._current().kind == TokenKind.UNTIL:
            return self._parse_until()
        if self._current().kind == TokenKind.WHEN:
            return self._parse_when()
        if self._current().kind == TokenKind.FOR:
            return self._parse_for()
        if self._current().kind == TokenKind.RETURN:
            return self._parse_return()
        if self._current().kind == TokenKind.LBRACE:
            return self._parse_block()
        # Otherwise expression
        return self._parse_expression()

    def _parse_let(self) -> LetStatement:
        """Parses 'let' ['mut'] IDENT [':' type] '=' expression."""
        self._advance()  # let
        mutable = False
        if self._current().kind == TokenKind.MUT:
            mutable = True
            self._advance()
        name = self._expect(TokenKind.IDENT).value
        type_ann = None
        if self._current().kind == TokenKind.COLON:
            self._advance()
            type_ann = self._expect(TokenKind.IDENT).value
        value = None
        if self._current().kind == TokenKind.ASSIGN:
            self._advance()
            value = self._parse_expression()
        return LetStatement(name, type_ann, value, mutable)

    def _parse_fn(self) -> FnDecl:
        """Parses 'fn' IDENT '(' params ')' ['->' type] block."""
        self._advance()  # fn
        name = self._expect(TokenKind.IDENT).value
        self._expect(TokenKind.LPAREN)
        params = []
        if self._current().kind != TokenKind.RPAREN:
            while True:
                pname = self._expect(TokenKind.IDENT).value
                self._expect(TokenKind.COLON)
                ptype = self._expect(TokenKind.IDENT).value
                params.append((pname, ptype))
                if self._current().kind == TokenKind.COMMA:
                    self._advance()
                else:
                    break
        self._expect(TokenKind.RPAREN)
        return_type = None
        if self._current().kind == TokenKind.ARROW:
            self._advance()
            return_type = self._expect(TokenKind.IDENT).value
        body = self._parse_block().statements
        return FnDecl(name, params, return_type, body)

    def _parse_block(self) -> Block:
        """Parses '{' statement* '}'."""
        self._expect(TokenKind.LBRACE)
        stmts = []
        while self._current().kind not in (TokenKind.RBRACE, TokenKind.EOF):
            stmts.append(self._parse_statement())
        self._expect(TokenKind.RBRACE)
        return Block(stmts)

    def _parse_if(self) -> IfStmt:
        """Parses 'if' expression block ['else' (block | if_stmt)]."""
        self._advance()  # if
        cond = self._parse_expression()
        then_branch = self._parse_block().statements
        else_branch = []
        if self._current().kind == TokenKind.ELSE:
            self._advance()
            if self._current().kind == TokenKind.IF:
                else_branch = [self._parse_if()]
            else:
                else_branch = self._parse_block().statements
        return IfStmt(cond, then_branch, else_branch)

    def _parse_while(self) -> WhileStmt:
        """Parses 'while' expression block."""
        self._advance()  # while
        cond = self._parse_expression()
        body = self._parse_block().statements
        return WhileStmt(cond, body)

    def _parse_until(self) -> UntilLoop:
        """Parses 'until' ['convergence'] block."""
        self._advance()  # until
        if self._current().kind == TokenKind.CONVERGENCE:
            self._advance()  # convergence
        body = self._parse_block().statements
        return UntilLoop(body)

    def _parse_when(self) -> WhenExpr:
        """Parses 'when' expression '{' expression ',' expression '}'."""
        self._advance()  # when
        condition = self._parse_expression()
        self._expect(TokenKind.LBRACE)
        then_expr = self._parse_expression()
        if self._current().kind == TokenKind.COMMA:
            self._advance()
        else_expr = self._parse_expression()
        self._expect(TokenKind.RBRACE)
        return WhenExpr(condition, then_expr, else_expr)

    def _parse_for(self) -> ForLoop:
        """Parses 'for' IDENT 'in' expression block."""
        self._advance()  # for
        var_name = self._expect(TokenKind.IDENT).value
        self._expect(TokenKind.IN)
        iterable = self._parse_expression()
        body = self._parse_block().statements
        return ForLoop(var_name, iterable, body)

    def _parse_return(self) -> ReturnStmt:
        """Parses 'return' [expression]."""
        self._advance()  # return
        if self._current().kind in (TokenKind.RBRACE, TokenKind.EOF, TokenKind.SEMICOLON):
            return ReturnStmt()
        value = self._parse_expression()
        return ReturnStmt(value)

    # ─── Expressions ───────────────────────────────────────────────────

    def _parse_expression(self) -> 'ASTNode':
        """Parses an expression."""
        return self._parse_comparison()

    def _parse_comparison(self) -> 'ASTNode':
        """Parses comparison: term (('==' | '!=' | '<' | '>' | '<=' | '>=') term)*."""
        left = self._parse_term()
        while self._current().kind in (
            TokenKind.EQ, TokenKind.NEQ, TokenKind.LT,
            TokenKind.GT, TokenKind.LTE, TokenKind.GTE
        ):
            op_map = {
                TokenKind.EQ: "eq", TokenKind.NEQ: "neq",
                TokenKind.LT: "lt", TokenKind.GT: "gt",
                TokenKind.LTE: "lte", TokenKind.GTE: "gte"
            }
            op = op_map[self._current().kind]
            self._advance()
            right = self._parse_term()
            left = BinaryOp(left, op, right)
        return left

    def _parse_term(self) -> 'ASTNode':
        """Parses addition and subtraction: factor (('+' | '-') factor)*."""
        left = self._parse_factor()
        while self._current().kind in (TokenKind.PLUS, TokenKind.MINUS):
            op = "+" if self._current().kind == TokenKind.PLUS else "-"
            self._advance()
            right = self._parse_factor()
            left = BinaryOp(left, op, right)
        return left

    def _parse_factor(self) -> 'ASTNode':
        """Parses multiplication and division: unary (('*' | '/' | '%') unary)*."""
        left = self._parse_unary()
        while self._current().kind in (TokenKind.STAR, TokenKind.SLASH, TokenKind.PERCENT):
            op = (
                "*" if self._current().kind == TokenKind.STAR else
                "/" if self._current().kind == TokenKind.SLASH else "%"
            )
            self._advance()
            right = self._parse_unary()
            left = BinaryOp(left, op, right)
        return left

    def _parse_unary(self) -> 'ASTNode':
        """Parses unary operators: ('-' | '!')? call."""
        if self._current().kind in (TokenKind.MINUS, TokenKind.BANG):
            op = "-" if self._current().kind == TokenKind.MINUS else "!"
            self._advance()
            return UnaryOp(op, self._parse_call())
        return self._parse_call()

    def _parse_call(self) -> 'ASTNode':
        """Parses function calls, array indexing, and holographic memory methods."""
        expr = self._parse_primary()
        while True:
            if self._current().kind == TokenKind.LPAREN:
                self._advance()
                args = []
                if self._current().kind != TokenKind.RPAREN:
                    while True:
                        args.append(self._parse_expression())
                        if self._current().kind == TokenKind.COMMA:
                            self._advance()
                        else:
                            break
                self._expect(TokenKind.RPAREN)
                if isinstance(expr, VarRef):
                    expr = FnCall(expr.name, args)
                else:
                    raise ParseError(
                        f"Cannot call non‑function", self._current().line
                    )
            elif self._current().kind == TokenKind.LBRACKET:
                self._advance()
                index = self._parse_expression()
                self._expect(TokenKind.RBRACKET)
                expr = IndexAccess(expr, index)
            elif self._current().kind == TokenKind.DOT:
                self._advance()
                method = self._expect(TokenKind.IDENT).value
                self._expect(TokenKind.LPAREN)
                args = []
                if self._current().kind != TokenKind.RPAREN:
                    while True:
                        args.append(self._parse_expression())
                        if self._current().kind == TokenKind.COMMA:
                            self._advance()
                        else:
                            break
                self._expect(TokenKind.RPAREN)
                if method == "write":
                    expr = HolographicWrite(expr, args[0], args[1] if len(args) > 1 else None)
                elif method == "read":
                    expr = HolographicRead(expr, args[0])
                elif method == "project":
                    expr = HolographicProject(expr, args[0], args[1] if len(args) > 1 else None)
                else:
                    expr = FnCall(f"field_{method}", [expr] + args)
            else:
                break
        return expr

    def _parse_primary(self) -> 'ASTNode':
        """Parses primary expressions: literals, variables, mod, collapse, parentheses, arrays."""
        tok = self._current()

        if tok.kind == TokenKind.INT:
            self._advance()
            return IntLiteral(tok.value)
        if tok.kind == TokenKind.FLOAT:
            self._advance()
            return FloatLiteral(tok.value)
        if tok.kind == TokenKind.STRING:
            self._advance()
            return StringLiteral(tok.value)
        if tok.kind == TokenKind.TRUE:
            self._advance()
            return BoolLiteral(True)
        if tok.kind == TokenKind.FALSE:
            self._advance()
            return BoolLiteral(False)
        if tok.kind == TokenKind.IDENT:
            self._advance()
            return VarRef(tok.value)
        if tok.kind == TokenKind.MOD:
            self._advance()
            self._expect(TokenKind.LPAREN)
            a = self._parse_expression()
            self._expect(TokenKind.COMMA)
            n = self._parse_expression()
            self._expect(TokenKind.RPAREN)
            return SubstrateModulo(a, n)
        if tok.kind == TokenKind.COLLAPSE:
            self._advance()
            self._expect(TokenKind.LPAREN)
            field_expr = self._parse_expression()
            self._expect(TokenKind.RPAREN)
            return CollapseExpr(field_expr)
        if tok.kind == TokenKind.LPAREN:
            self._advance()
            expr = self._parse_expression()
            self._expect(TokenKind.RPAREN)
            return expr
        if tok.kind == TokenKind.LBRACKET:
            self._advance()
            elements = []
            if self._current().kind != TokenKind.RBRACKET:
                while True:
                    elements.append(self._parse_expression())
                    if self._current().kind == TokenKind.COMMA:
                        self._advance()
                    else:
                        break
            self._expect(TokenKind.RBRACKET)
            return ArrayLiteral(elements)

        raise ParseError(
            f"Unexpected token {tok.kind.name}", tok.line
        )
