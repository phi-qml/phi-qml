"""
Φ‑QML Interpreter — Tree‑walk execution engine

Walks the AST produced by the parser and executes Φ‑QML programs.
Supports classical simulation, holographic field operations,
Substrate* Modulo, Φ‑Elegance scoring, and the extended primitives
(when, until, holographic memory).
"""

import math
from typing import Any, Dict, List, Optional, Tuple

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
from phi_qml.holographic_field import HolographicField
from phi_qml.substrate_modulo import SubstrateModuloEngine
from phi_qml.elegance_tracker import EleganceTracker


class Environment:
    """
    A lexical scope for variable and function bindings.
    Supports nested scopes through a parent chain.
    """

    def __init__(self, parent: Optional['Environment'] = None):
        self.variables: Dict[str, Any] = {}
        self.functions: Dict[str, FnDecl] = {}
        self.parent = parent
        self.return_value: Optional[Any] = None
        self.should_return = False

    def define(self, name: str, value: Any):
        """Bind a variable in the current scope."""
        self.variables[name] = value

    def assign(self, name: str, value: Any):
        """Assign to an existing variable (searching parent scopes)."""
        if name in self.variables:
            self.variables[name] = value
        elif self.parent:
            self.parent.assign(name, value)
        else:
            raise NameError(f"Undefined variable: {name}")

    def get(self, name: str) -> Any:
        """Look up a variable (searching parent scopes)."""
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.get(name)
        raise NameError(f"Undefined variable: {name}")

    def define_function(self, name: str, fn: FnDecl):
        """Register a function declaration."""
        self.functions[name] = fn

    def get_function(self, name: str) -> Optional[FnDecl]:
        """Look up a function (searching parent scopes)."""
        if name in self.functions:
            return self.functions[name]
        if self.parent:
            return self.parent.get_function(name)
        return None


class Interpreter:
    """
    Tree‑walk interpreter for Φ‑QML.

    Executes Φ‑QML programs by walking the AST and performing
    operations. Integrates with HolographicField for quantum
    simulation, SubstrateModuloEngine for zero‑cost modulo,
    and EleganceTracker for Φ scoring.
    """

    def __init__(self, field: Optional[HolographicField] = None):
        """
        Initialize the interpreter.

        Parameters
        ----------
        field : HolographicField or None
            Optional holographic field for quantum operations.
            If None, quantum operations will use classical fallbacks.
        """
        self.global_env = Environment()
        self.modulo_engine = SubstrateModuloEngine(field)
        self.field = field
        self.tracker = EleganceTracker(min_phi=0.5)
        self.operation_count = 0
        self._register_builtins()

    def _register_builtins(self):
        """Register built‑in functions available to all Φ‑QML programs."""
        def phi_score(expr_result: Any, operations: int = 0) -> float:
            """Built‑in: phi_score(expr, operations) → Φ = K / C."""
            return self.tracker.track("phi_score()", expr_result, operations)

        def println(*args):
            """Built‑in: println(...) – print arguments to console."""
            print(*(str(a) for a in args))

        def holographic_alloc(size: int = 8) -> HolographicField:
            """Built‑in: holographic_alloc(N) – create a new holographic field."""
            return HolographicField(N=size)

        self.global_env.define("phi_score", phi_score)
        self.global_env.define("println", println)
        self.global_env.define("holographic_alloc", holographic_alloc)
        self.global_env.define("PI", math.pi)
        self.global_env.define("PHI", 1.61803398874989484820458683436563811772030917980576)
        self.global_env.define("true", True)
        self.global_env.define("false", False)

    def interpret(self, node, env: Optional[Environment] = None) -> Any:
        """
        Execute a node of the AST.

        Parameters
        ----------
        node : ASTNode
            The AST node to execute.
        env : Environment or None
            The current lexical environment (defaults to global).

        Returns the result of evaluating the node.
        """
        if env is None:
            env = self.global_env

        # ─── Program ────────────────────────────────────────────────
        if isinstance(node, Program):
            result = None
            for stmt in node.statements:
                result = self.interpret(stmt, env)
                if env.should_return:
                    break
            return result

        # ─── Let Statement ─────────────────────────────────────────
        if isinstance(node, LetStatement):
            value = self.interpret(node.value, env) if node.value else None
            env.define(node.name, value)
            self.tracker.track(f"let {node.name}", value, operations=0)
            return value

        # ─── Function Declaration ──────────────────────────────────
        if isinstance(node, FnDecl):
            env.define_function(node.name, node)
            return None

        # ─── Function Call ─────────────────────────────────────────
        if isinstance(node, FnCall):
            # Try built‑in first
            func = env.get(node.name) if node.name in env.variables else None
            if callable(func):
                args = [self.interpret(a, env) for a in node.arguments]
                self.operation_count += 1
                return func(*args)

            # Try user‑defined function
            fn_decl = env.get_function(node.name)
            if fn_decl:
                call_env = Environment(parent=env)
                for (pname, _), arg in zip(fn_decl.params, node.arguments):
                    call_env.define(pname, self.interpret(arg, env))
                result = None
                for stmt in fn_decl.body:
                    result = self.interpret(stmt, call_env)
                    if call_env.should_return:
                        call_env.should_return = False
                        return call_env.return_value
                return result

            raise RuntimeError(f"{node.name} is not callable")

        # ─── Binary Operations ─────────────────────────────────────
        if isinstance(node, BinaryOp):
            left = self.interpret(node.left, env)
            right = self.interpret(node.right, env)
            self.operation_count += 1

            ops = {
                "+": lambda a, b: a + b,
                "-": lambda a, b: a - b,
                "*": lambda a, b: a * b,
                "/": lambda a, b: a / b if b != 0 else float('inf'),
                "%": lambda a, b: a % b,
                "eq": lambda a, b: a == b,
                "neq": lambda a, b: a != b,
                "lt": lambda a, b: a < b,
                "gt": lambda a, b: a > b,
                "lte": lambda a, b: a <= b,
                "gte": lambda a, b: a >= b,
            }
            if node.op in ops:
                result = ops[node.op](left, right)
                self.tracker.track(f"binary_op({node.op})", result, operations=1)
                return result
            raise RuntimeError(f"Unknown operator: {node.op}")

        # ─── Unary Operations ──────────────────────────────────────
        if isinstance(node, UnaryOp):
            operand = self.interpret(node.operand, env)
            self.operation_count += 1
            if node.op == "-":
                result = -operand
            elif node.op == "!":
                result = not operand
            else:
                raise RuntimeError(f"Unknown unary operator: {node.op}")
            self.tracker.track(f"unary_op({node.op})", result, operations=1)
            return result

        # ─── Substrate* Modulo ─────────────────────────────────────
        if isinstance(node, SubstrateModulo):
            a = self.interpret(node.a, env)
            n = self.interpret(node.n, env)
            result, K, C = self.modulo_engine.modulo(a, n)
            self.tracker.track(f"mod({a}, {n})", result, operations=C, K=K)
            return result

        # ─── Collapse ──────────────────────────────────────────────
        if isinstance(node, CollapseExpr):
            if self.field is None:
                raise RuntimeError("No holographic field attached for collapse")
            result = self.field.collapse()
            self.tracker.track("collapse(field)", result, operations=0)
            return result

        # ─── If Statement ──────────────────────────────────────────
        if isinstance(node, IfStmt):
            cond = self.interpret(node.condition, env)
            if cond:
                for stmt in node.then_branch:
                    result = self.interpret(stmt, env)
                    if env.should_return:
                        return result
            else:
                for stmt in node.else_branch:
                    result = self.interpret(stmt, env)
                    if env.should_return:
                        return result
            return None

        # ─── While Statement ───────────────────────────────────────
        if isinstance(node, WhileStmt):
            while self.interpret(node.condition, env):
                for stmt in node.body:
                    result = self.interpret(stmt, env)
                    if env.should_return:
                        return result
            return None

        # ─── When Expression ───────────────────────────────────────
        if isinstance(node, WhenExpr):
            condition = self.interpret(node.condition, env)

            # Evaluate both branches and compute their Φ
            saved_ops = self.operation_count
            then_val = self.interpret(node.then_expr, env)
            then_ops = self.operation_count - saved_ops

            self.operation_count = saved_ops
            else_val = self.interpret(node.else_expr, env)
            else_ops = self.operation_count - saved_ops

            then_phi = 1.0 / max(then_ops, 1) if then_val is not None else 0.0
            else_phi = 1.0 / max(else_ops, 1) if else_val is not None else 0.0

            if condition:
                result = then_val if then_phi >= else_phi else else_val
                chosen = "then" if then_phi >= else_phi else "else"
            else:
                result = else_val
                chosen = "else"

            self.tracker.track(
                f"when(condition={condition}, chosen={chosen})",
                result,
                operations=then_ops if chosen == "then" else else_ops
            )
            return result

        # ─── Until Loop ────────────────────────────────────────────
        if isinstance(node, UntilLoop):
            max_iterations = 1000
            prev_phi = -1.0
            iteration = 0
            last_result = None

            while iteration < max_iterations:
                saved_ops = self.operation_count
                for stmt in node.body:
                    last_result = self.interpret(stmt, env)
                current_ops = self.operation_count - saved_ops
                current_phi = 1.0 / max(current_ops, 1) if last_result is not None else 0.0

                if current_phi <= prev_phi:
                    break

                prev_phi = current_phi
                iteration += 1

            self.tracker.track(
                f"until_convergence({iteration} iters)",
                last_result,
                operations=iteration
            )
            return last_result

        # ─── For Loop ──────────────────────────────────────────────
        if isinstance(node, ForLoop):
            iterable = self.interpret(node.iterable, env)
            result = None
            for item in iterable:
                env.define(node.var_name, item)
                for stmt in node.body:
                    result = self.interpret(stmt, env)
                    if env.should_return:
                        return result
            self.tracker.track(f"for_loop", result, operations=len(iterable))
            return result

        # ─── Return Statement ──────────────────────────────────────
        if isinstance(node, ReturnStmt):
            value = self.interpret(node.value, env) if node.value else None
            env.return_value = value
            env.should_return = True
            return value

        # ─── Block ─────────────────────────────────────────────────
        if isinstance(node, Block):
            block_env = Environment(parent=env)
            result = None
            for stmt in node.statements:
                result = self.interpret(stmt, block_env)
                if block_env.should_return:
                    env.return_value = block_env.return_value
                    env.should_return = True
                    return result
            return result

        # ─── Literals ──────────────────────────────────────────────
        if isinstance(node, (IntLiteral, FloatLiteral, StringLiteral, BoolLiteral)):
            return node.value

        # ─── Variable Reference ────────────────────────────────────
        if isinstance(node, VarRef):
            return env.get(node.name)

        # ─── Array Literal ─────────────────────────────────────────
        if isinstance(node, ArrayLiteral):
            return [self.interpret(e, env) for e in node.elements]

        # ─── Index Access ──────────────────────────────────────────
        if isinstance(node, IndexAccess):
            arr = self.interpret(node.array, env)
            idx = self.interpret(node.index, env)
            return arr[idx]

        # ─── Holographic Write ─────────────────────────────────────
        if isinstance(node, HolographicWrite):
            field_obj = self.interpret(node.field_expr, env)
            address = self.interpret(node.address, env)
            value = self.interpret(node.value, env)
            field_obj.write(int(address), value)
            self.tracker.track(f"write({address})", value, operations=1)
            return value

        # ─── Holographic Read ──────────────────────────────────────
        if isinstance(node, HolographicRead):
            field_obj = self.interpret(node.field_expr, env)
            address = self.interpret(node.address, env)
            value = field_obj.read(int(address))
            self.tracker.track(f"read({address})", value, operations=1)
            return value

        # ─── Holographic Project ───────────────────────────────────
        if isinstance(node, HolographicProject):
            field_obj = self.interpret(node.field_expr, env)
            address = self.interpret(node.address, env)
            # Transform is a function node – execute it later lazily
            self.tracker.track(f"project({address})", None, operations=1)
            return None

        raise RuntimeError(f"Unknown AST node type: {type(node).__name__}")


# ═══════════════════════════════════════════════════════════════════════════════
# Demonstration
# ═══════════════════════════════════════════════════════════════════════════════

def demo_interpreter():
    """Demonstrate the interpreter with a sample program."""
    print("╔══════════════════════════════════════════════════════════════════════════╗")
    print("║  INTERPRETER — Φ‑QML Execution Engine                                  ║")
    print("╚══════════════════════════════════════════════════════════════════════════╝\n")

    # Build a simple AST manually (in real use, the parser produces this)
    from phi_qml.ast_nodes import Program, LetStatement, FnDecl, FnCall, VarRef, IntLiteral, SubstrateModulo

    # Program: let result = mod(42, 13); return result;
    program = Program([
        LetStatement("result", value=SubstrateModulo(IntLiteral(42), IntLiteral(13))),
        FnCall("println", [VarRef("result")]),
    ])

    # Create interpreter and run
    interpreter = Interpreter()
    result = interpreter.interpret(program)
    print(f"\nProgram result: {result}")

    # Show elegance report
    interpreter.tracker.report()

    print(f"\n[Φ] Interpreter demonstration complete.")


if __name__ == "__main__":
    demo_interpreter()
