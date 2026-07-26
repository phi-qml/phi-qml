# Φ‑QML Language Specification v1.0

## Abstract

Φ‑QML (Phi Quantum Meta‑Language) is a quantum programming language designed
from first principles around the holographic nature of the Φ field. Unlike
existing quantum languages (Q#, Qiskit, Quipper) that treat quantum
operations as gates applied to qubits, Φ‑QML treats every quantum state
as a projection of an underlying entanglement field Φ. The fundamental
primitive is not the Hadamard gate or the CNOT, but **Substrate* Modulo** —
a zero‑cost operation that in the Substrate* attractor state (K=1, C=0)
returns the pre‑computed remainder by collapsing the Φ field at the
coordinate (a, n). The language is guided by **Φ‑Elegance**: every
construct is scored by Φ = K / C, and the programmer is encouraged to
maximize this ratio.

## 1. Design Philosophy

Φ‑QML rests on three pillars derived from the Theory of Everything.

### Pillar 1: The Φ Field is the Universal Substrate
There is no classical memory separate from quantum states. All data—classical
bits, quantum amplitudes, intermediate results—exist as excitations of a
single holographic entanglement field Φ. A qubit is not a two‑level system
in isolation; it is a localized peak of Φ that, through its entanglement
with all other qubits, implicitly defines 2^N amplitudes.

### Pillar 2: Computation is Collapse
A classical computer performs arithmetic by executing a sequence of logical
gates. A quantum computer in the Substrate* limit does not "compute" in
this sense. The result of any operation that is logically derivable from
the initial state already exists as a holographic amplitude. The act of
"computation" is the act of collapsing the Φ field to read out that
pre‑existing amplitude. Substrate* Modulo is the canonical example:
a mod n is not calculated; it is revealed.

### Pillar 3: Φ‑Elegance Governs All
Every operation has a cost C (time, energy, qubits) and a consistency K
(probability of correct result). The language provides a built‑in function
`phi_score()` that instruments any expression. The goal of the programmer
is to maximize Φ = K / C, driving code toward the Substrate* attractor
where K=1 and C=0.

## 2. Lexical Structure

### 2.1 Keywords

```
fn, let, mut, if, else, while, for, in, return,
mod, collapse, field, qubit, classical, H, CNOT, measure,
true, false, amplitude, when, until, convergence,
write, read, project
```

### 2.2 Operators

- Arithmetic: `+`, `-`, `*`, `/`, `%`
- Comparison: `==`, `!=`, `<`, `>`, `<=`, `>=`
- Logical: `&&`, `||`, `!`
- Assignment: `=`, `+=`, `-=`, `*=`, `/=`, `%=`
- Other: `->`, `|>`

### 2.3 Delimiters

`(`, `)`, `{`, `}`, `[`, `]`, `;`, `:`, `,`, `.`

### 2.4 Literals

- Integers: `42`, `0xFF`, `2^256`
- Floats: `3.14`, `0.001`
- Strings: `"hello"`, `"Φ‑QML"`
- Booleans: `true`, `false`

### 2.5 Comments

- Line: `//` to end of line
- Block: `/* ... */`

## 3. Syntax (EBNF Grammar)

```ebnf
program         ::= { statement } ;

statement       ::= let_stmt | fn_decl | if_stmt | while_stmt
                  | until_loop | when_expr | for_loop
                  | return_stmt | block | expression ;

let_stmt        ::= "let" [ "mut" ] IDENTIFIER [ ":" type ] "=" expression ;

fn_decl         ::= "fn" IDENTIFIER "(" [ parameters ] ")" [ "->" type ] block ;
parameters      ::= parameter { "," parameter } ;
parameter       ::= IDENTIFIER ":" type ;

if_stmt         ::= "if" expression block [ "else" ( block | if_stmt ) ] ;
while_stmt      ::= "while" expression block ;
until_loop      ::= "until" [ "convergence" ] block ;
when_expr       ::= "when" expression "{" expression "," expression "}" ;
for_loop        ::= "for" IDENTIFIER "in" expression block ;
return_stmt     ::= "return" [ expression ] ;
block           ::= "{" { statement } "}" ;

expression      ::= comparison ;
comparison      ::= term { ( "==" | "!=" | "<" | ">" | "<=" | ">=" ) term } ;
term            ::= factor { ( "+" | "-" ) factor } ;
factor          ::= unary { ( "*" | "/" | "%" ) unary } ;
unary           ::= ( "-" | "!" ) unary | call ;
call            ::= primary
                  { "(" [ arguments ] ")"
                  | "[" expression "]"
                  | "." IDENTIFIER "(" [ arguments ] ")" } ;
arguments       ::= expression { "," expression } ;

primary         ::= INTEGER | FLOAT | STRING | "true" | "false"
                  | IDENTIFIER
                  | "mod" "(" expression "," expression ")"
                  | "collapse" "(" expression ")"
                  | "(" expression ")"
                  | "[" [ expression { "," expression } ] "]" ;

type            ::= "qubit" | "field" "<" INTEGER ">"
                  | "classical" "<" type ">"
                  | "amplitude" | "!" ;
```

4. Type System

Φ‑QML employs a linear type system to enforce the no‑cloning theorem
and ensure that qubits are used exactly once.

4.1 Base Types

Type Description Linearity
qubit A quantum bit Linear
field<N> Holographic Φ field over N qubits Linear
classical<T> A classical value of type T Free
amplitude Complex number representing an amplitude Free
! Never type (non‑terminating functions) Free

4.2 Elegance Qualifiers

· @brute T — value obtained through classical computation (Φ < 1.0)
· @elegant T — value obtained through efficient computation (Φ > 1.0)
· @substrate T — value obtained through field collapse (Φ = ∞)

4.3 Assignability Rules

· @substrate T → @elegant T → @brute T (can assign to less elegant)
· @brute T → @elegant T (cannot assign – insufficient elegance)
· ! → any type (can assign anywhere)

5. Built‑in Primitives

Primitive C K Φ Description
mod(a, n) 0 1.0 ∞ Substrate* Modulo – instantaneous
collapse(f) 0 1.0 ∞ Field collapse
H(q) 1 1.0 1.0 Hadamard gate
CNOT(c, t) 2 1.0 0.5 Controlled‑NOT gate
measure(q) 1 1.0 1.0 Qubit measurement
phi_score(e, c) 0 1.0 ∞ Elegance scoring
println(...) 1 1.0 1.0 Console output

6. Control Flow

6.1 when — Elegant Conditional

```
when condition { then_expr, else_expr }
```

Both branches are evaluated; the one with the higher Φ is selected.

6.2 until convergence — Resonant Loop

```
until convergence { body }
```

The body repeats while Φ increases. Stops at convergence (dΦ/dt = 0).

7. Operational Modes

1. Classical Simulation — Tree‑walk interpreter with O(1) memory via
   holographic field representation.
2. Quantum Native — Direct execution on Substrate* hardware (C=0 for
   all operations).
3. QASM Compilation — Target OpenQASM 3.0 with Substrate* intrinsics.

8. Φ‑Elegance Scoring

Every expression in Φ‑QML carries a Φ score: the ratio of consistency K
to computational complexity C. The programmer is driven to maximize this
ratio.

· Built‑in function phi_score(expr, operations) returns Φ for any expression
· The linter automatically detects inelegant patterns and suggests alternatives
· The elegance path: Classical → Quantum → Substrate* (Φ → ∞)

9. License

MIT © 2024 Φ‑QML Contributors

Φ.
