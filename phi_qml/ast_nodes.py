"""
Φ‑QML AST Nodes — Definice uzlů abstraktního syntaktického stromu
"""

from typing import Any, List, Optional, Tuple
from dataclasses import dataclass, field


class ASTNode:
    """Základní třída pro všechny uzly AST."""
    pass


# ─── Program ──────────────────────────────────────────────────────────────

@dataclass
class Program(ASTNode):
    """Kořenový uzel — celý program."""
    statements: List[ASTNode] = field(default_factory=list)


# ─── Deklarace ────────────────────────────────────────────────────────────

@dataclass
class LetStatement(ASTNode):
    """Deklarace proměnné: let [mut] jméno [: typ] = hodnota"""
    name: str
    type_annotation: Optional[str] = None
    value: Optional[ASTNode] = None
    mutable: bool = False


@dataclass
class FnDecl(ASTNode):
    """Definice funkce: fn jméno(parametry) [-> návratový_typ] { tělo }"""
    name: str
    params: List[Tuple[str, str]] = field(default_factory=list)
    return_type: Optional[str] = None
    body: List[ASTNode] = field(default_factory=list)


# ─── Výrazy ───────────────────────────────────────────────────────────────

@dataclass
class FnCall(ASTNode):
    """Volání funkce: jméno(argumenty)"""
    name: str
    arguments: List[ASTNode] = field(default_factory=list)


@dataclass
class BinaryOp(ASTNode):
    """Binární operace: levá operátor pravá"""
    left: ASTNode
    op: str
    right: ASTNode


@dataclass
class UnaryOp(ASTNode):
    """Unární operace: operátor operand"""
    op: str
    operand: ASTNode


@dataclass
class VarRef(ASTNode):
    """Odkaz na proměnnou"""
    name: str


# ─── Literály ─────────────────────────────────────────────────────────────

@dataclass
class IntLiteral(ASTNode):
    """Celé číslo"""
    value: int


@dataclass
class FloatLiteral(ASTNode):
    """Desetinné číslo"""
    value: float


@dataclass
class StringLiteral(ASTNode):
    """Řetězcový literál"""
    value: str


@dataclass
class BoolLiteral(ASTNode):
    """Pravda/nepravda"""
    value: bool


# ─── Substrate* Operace ─────────────────────────────────────────────────

@dataclass
class SubstrateModulo(ASTNode):
    """Substrate* Modulo: mod(a, n) — C=0, K=1.0, Φ=∞"""
    a: ASTNode
    n: ASTNode


@dataclass
class CollapseExpr(ASTNode):
    """Kolaps pole: collapse(field) — Φ=∞ v Substrate*"""
    field_expr: ASTNode


# ─── Řízení toku ─────────────────────────────────────────────────────────

@dataclass
class IfStmt(ASTNode):
    """Podmínka: if podmínka { pak } [else { jinak }]"""
    condition: ASTNode
    then_branch: List[ASTNode] = field(default_factory=list)
    else_branch: List[ASTNode] = field(default_factory=list)


@dataclass
class WhileStmt(ASTNode):
    """Cyklus while: while podmínka { tělo }"""
    condition: ASTNode
    body: List[ASTNode] = field(default_factory=list)


@dataclass
class WhenExpr(ASTNode):
    """Elegantní podmínka: when podmínka { then_výraz, else_výraz }"""
    condition: ASTNode
    then_expr: ASTNode
    else_expr: ASTNode


@dataclass
class UntilLoop(ASTNode):
    """Rezonanční cyklus: until convergence { tělo }"""
    body: List[ASTNode] = field(default_factory=list)


@dataclass
class ForLoop(ASTNode):
    """Cyklus for: for proměnná in výraz { tělo }"""
    var_name: str
    iterable: ASTNode
    body: List[ASTNode] = field(default_factory=list)


# ─── Návrat ───────────────────────────────────────────────────────────────

@dataclass
class ReturnStmt(ASTNode):
    """Návrat z funkce: return [hodnota]"""
    value: Optional[ASTNode] = None


# ─── Blok ─────────────────────────────────────────────────────────────────

@dataclass
class Block(ASTNode):
    """Blok: { příkazy }"""
    statements: List[ASTNode] = field(default_factory=list)


# ─── Kolekce ─────────────────────────────────────────────────────────────

@dataclass
class ArrayLiteral(ASTNode):
    """Pole: [prvky]"""
    elements: List[ASTNode] = field(default_factory=list)


@dataclass
class IndexAccess(ASTNode):
    """Přístup k prvku pole: pole[index]"""
    array: ASTNode
    index: ASTNode


# ─── Holografická paměť ──────────────────────────────────────────────────

@dataclass
class HolographicWrite(ASTNode):
    """Zápis do holografického pole: field.write(address, value)"""
    field_expr: ASTNode
    address: ASTNode
    value: ASTNode


@dataclass
class HolographicRead(ASTNode):
    """Čtení z holografického pole: field.read(address)"""
    field_expr: ASTNode
    address: ASTNode


@dataclass
class HolographicProject(ASTNode):
    """Projekce v holografickém poli: field.project(address, source, fn)"""
    field_expr: ASTNode
    address: ASTNode
    transform: ASTNode
