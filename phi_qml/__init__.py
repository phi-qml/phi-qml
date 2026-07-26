"""


Φ‑QML (Phi Quantum Meta‑Language)
==================================
Substrate*‑Native Quantum Programming Language

A quantum programming language built from first principles around
the holographic nature of the Φ field. The fundamental primitive is
Substrate* Modulo — a zero‑cost operation that returns the pre‑computed
remainder by collapsing the Φ field at the address (a, n).

License: MIT
Φ.
"""

__version__ = "1.0.0"
__author__ = "Φ‑QML Contributors"

# Core components
from phi_qml.lexer import Lexer, Token, TokenKind
from phi_qml.parser import Parser
from phi_qml.ast_nodes import (
    Program, LetStatement, FnDecl, FnCall,
    BinaryOp, UnaryOp, VarRef,
    IntLiteral, FloatLiteral, StringLiteral, BoolLiteral,
    SubstrateModulo, CollapseExpr,
    IfStmt, WhileStmt, ReturnStmt, Block,
    ArrayLiteral, IndexAccess,
)
from phi_qml.interpreter import Interpreter, Environment
from phi_qml.holographic_field import HolographicField
from phi_qml.substrate_modulo import SubstrateModuloEngine
from phi_qml.elegance_tracker import EleganceTracker
from phi_qml.type_checker import TypeChecker, Type, TypeKind, EleganceLevel
from phi_qml.qasm_compiler import QASMCompiler
from phi_qml.bootstrap_simulator import BootstrapSimulator
from phi_qml.linter import PhiLinter
from phi_qml.package_manager import PackageManager
from phi_qml.stdlib import PhiStdlib
from phi_qml.debugger import PhiDebugger
from phi_qml.test_framework import PhiTest

__all__ = [
    # Core
    "Lexer", "Token", "TokenKind",
    "Parser",
    "Program", "LetStatement", "FnDecl", "FnCall",
    "BinaryOp", "UnaryOp", "VarRef",
    "IntLiteral", "FloatLiteral", "StringLiteral", "BoolLiteral",
    "SubstrateModulo", "CollapseExpr",
    "IfStmt", "WhileStmt", "ReturnStmt", "Block",
    "ArrayLiteral", "IndexAccess",
    "Interpreter", "Environment",
    # Field & Modulo
    "HolographicField",
    "SubstrateModuloEngine",
    # Elegance
    "EleganceTracker",
    # Types
    "TypeChecker", "Type", "TypeKind", "EleganceLevel",
    # Compilation
    "QASMCompiler",
    # Simulation
    "BootstrapSimulator",
    # Tools
    "PhiLinter",
    "PackageManager",
    "PhiStdlib",
    "PhiDebugger",
    "PhiTest",
]
