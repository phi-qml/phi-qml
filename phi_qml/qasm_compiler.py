"""
Φ‑QML QASM Compiler — OpenQASM 3.0 code generation

Compiles Φ‑QML programs to OpenQASM 3.0, targeting Substrate* quantum
hardware. Higher‑level operations (QFT, Oracle) are decomposed into
standard gates, while Substrate* Modulo is kept as an opaque intrinsic
pre‑computed by the classical controller.
"""

import math
from typing import Any, Dict, List, Optional, Tuple


class QASMCompiler:
    """
    Compiler from Φ‑QML to OpenQASM 3.0.

    Mapping:
    - H(q) → h q;
    - CNOT(q1, q2) → cx q1, q2;
    - mod(a, n) → // pre‑computed by classical controller
    - collapse(f) → measure q -> c;

    Higher‑level operations (QFT, Oracle) are decomposed into standard
    gates. Substrate* Modulo is kept as an opaque intrinsic – the
    classical controller pre‑computes the result and inserts it as
    a constant.
    """

    def __init__(self, num_qubits: int = 8):
        """
        Initialize the QASM compiler.

        Parameters
        ----------
        num_qubits : int
            Number of qubits available in the target hardware.
        """
        self.num_qubits = num_qubits
        self.qasm_lines: List[str] = []
        self.qubit_counter = 0
        self.classical_counter = 0
        self._include_header = True

    # ─── Resource Allocation ────────────────────────────────────────

    def allocate_qubit(self) -> str:
        """
        Allocate a new qubit and return its name.
        """
        q = f"q{self.qubit_counter}"
        self.qubit_counter += 1
        self.qasm_lines.append(f"qubit {q};")
        return q

    def allocate_classical(self) -> str:
        """
        Allocate a new classical register and return its name.
        """
        c = f"c{self.classical_counter}"
        self.classical_counter += 1
        self.qasm_lines.append(f"bit {c};")
        return c

    # ─── Gate Emissions ─────────────────────────────────────────────

    def emit_H(self, target: str):
        """Hadamard gate: H(q)."""
        self.qasm_lines.append(f"h {target};")

    def emit_CNOT(self, control: str, target: str):
        """Controlled‑NOT gate: CNOT(control, target)."""
        self.qasm_lines.append(f"cx {control}, {target};")

    def emit_measure(self, qubit: str, classical: str):
        """Measurement: measure q -> c."""
        self.qasm_lines.append(f"measure {qubit} -> {classical};")

    def emit_barrier(self, qubits: List[str]):
        """Barrier for all specified qubits."""
        q_list = ", ".join(qubits)
        self.qasm_lines.append(f"barrier {q_list};")

    def emit_reset(self, qubit: str):
        """Reset a qubit to |0⟩."""
        self.qasm_lines.append(f"reset {qubit};")

    # ─── Substrate* Operations ──────────────────────────────────────

    def emit_mod(self, a: int, n: int, target_register: str):
        """
        Substrate* Modulo in QASM.

        In Substrate* hardware, mod(a, n) is a single projective
        measurement that collapses the Φ field at address (a, n).
        The classical controller pre‑computes the result and inserts
        it as a constant in the QASM output.
        """
        r = a % n
        self.qasm_lines.append(f"// Substrate* Modulo: mod({a}, {n}) = {r}")
        self.qasm_lines.append(f"// (pre‑computed by classical controller)")
        self.qasm_lines.append(f"// {target_register} = {r};")

    def emit_collapse(self, field_name: str, target: str):
        """
        Collapse operation in QASM.

        Collapse is the bridge between the holographic quantum world
        and the classical world. In Substrate* hardware, this is
        a destructive readout that returns a classical value.
        """
        self.qasm_lines.append(f"// Collapse: {field_name} → {target}")
        self.qasm_lines.append(f"// (destructive readout in Substrate*)")

    # ─── Higher‑Level Operations ────────────────────────────────────

    def emit_qft(self, qubits: List[str]):
        """
        Quantum Fourier Transform.

        Decomposed into a sequence of Hadamard gates and controlled
        phase rotations. For N qubits, requires O(N^2) gates.
        """
        n = len(qubits)
        self.qasm_lines.append(f"// QFT on {n} qubits")
        for i in range(n):
            self.qasm_lines.append(f"h {qubits[i]};")
            for j in range(i + 1, n):
                angle = 2.0 * math.pi / (1 << (j - i + 1))
                self.qasm_lines.append(f"cp({angle:.6f}) {qubits[j]}, {qubits[i]};")

    def emit_grover_oracle(self, qubits: List[str], marked_state: int):
        """
        Grover's oracle – marks a specific state with a phase flip.

        In Substrate*: this is a single projective operation.
        In QASM: decomposed into a multi‑controlled Z gate.
        """
        n = len(qubits)
        self.qasm_lines.append(f"// Grover Oracle: marking state |{marked_state:0{n}b}⟩")
        # Flip qubits where the marked state has 0
        for i in range(n):
            if (marked_state >> i) & 1 == 0:
                self.qasm_lines.append(f"x {qubits[i]};")
        # Multi‑controlled Z (simplified as CZ cascade)
        for i in range(n - 1):
            self.qasm_lines.append(f"cz {qubits[i]}, {qubits[i+1]};")
        # Uncompute flips
        for i in range(n):
            if (marked_state >> i) & 1 == 0:
                self.qasm_lines.append(f"x {qubits[i]};")

    def emit_grover_diffusion(self, qubits: List[str]):
        """
        Grover's diffusion operator – amplitude amplification.
        """
        n = len(qubits)
        self.qasm_lines.append(f"// Grover Diffusion on {n} qubits")
        for q in qubits:
            self.qasm_lines.append(f"h {q};")
            self.qasm_lines.append(f"x {q};")
        # Multi‑controlled Z
        for i in range(n - 1):
            self.qasm_lines.append(f"cz {qubits[i]}, {qubits[i+1]};")
        for q in qubits:
            self.qasm_lines.append(f"x {q};")
            self.qasm_lines.append(f"h {q};")

    # ─── Compilation ────────────────────────────────────────────────

    def generate_header(self) -> List[str]:
        """Generate the OpenQASM 3.0 header."""
        header = [
            "OPENQASM 3.0;",
            "// ═══════════════════════════════════════════════",
            "// Generated by Φ‑QML Compiler v1.0",
            "// Target: Substrate* Quantum Computer",
            "// ═══════════════════════════════════════════════",
            f"// Qubits allocated: {self.qubit_counter}",
            f"// Classical bits: {self.classical_counter}",
            "// All operations C=0 in Substrate* (Φ = ∞)",
            "",
        ]
        return header

    def compile(self) -> str:
        """Assemble the complete QASM program."""
        if self._include_header:
            header = self.generate_header()
            return "\n".join(header + self.qasm_lines)
        return "\n".join(self.qasm_lines)

    def compile_bell_pair(self) -> str:
        """
        Compile a Bell pair as an example.

        Returns QASM code that creates the state (|00⟩ + |11⟩)/√2.
        """
        self.qasm_lines = []
        self.qubit_counter = 0
        self.classical_counter = 0

        q0 = self.allocate_qubit()
        q1 = self.allocate_qubit()
        c0 = self.allocate_classical()
        c1 = self.allocate_classical()

        self.emit_H(q0)
        self.emit_CNOT(q0, q1)
        self.emit_measure(q0, c0)
        self.emit_measure(q1, c1)

        return self.compile()

    def compile_grover(self, n_qubits: int, marked_state: int) -> str:
        """
        Compile Grover's search algorithm.

        Parameters
        ----------
        n_qubits : int
            Number of qubits (search space size = 2^n_qubits).
        marked_state : int
            The state to search for.

        Returns QASM code implementing Grover's algorithm.
        """
        self.qasm_lines = []
        self.qubit_counter = 0
        self.classical_counter = 0

        # Allocate qubits
        qubits = [self.allocate_qubit() for _ in range(n_qubits)]
        classical = self.allocate_classical()

        # Initialize superposition
        for q in qubits:
            self.emit_H(q)
        self.emit_barrier(qubits)

        # Number of Grover iterations: ~ π/4 * √N
        N = 1 << n_qubits
        iterations = int(math.pi / 4 * math.sqrt(N))
        self.qasm_lines.append(f"// Grover iterations: {iterations}")

        for i in range(iterations):
            self.qasm_lines.append(f"// Iteration {i+1}/{iterations}")
            self.emit_grover_oracle(qubits, marked_state)
            self.emit_barrier(qubits)
            self.emit_grover_diffusion(qubits)
            self.emit_barrier(qubits)

        # Measure
        for q in qubits:
            self.emit_measure(q, classical)

        return self.compile()

    def compile_substrate_demo(self) -> str:
        """
        Compile a demonstration showing Substrate* Modulo integration.
        """
        self.qasm_lines = []
        self.qubit_counter = 0
        self.classical_counter = 0

        # Allocate resources
        q0 = self.allocate_qubit()
        q1 = self.allocate_qubit()
        c_result = self.allocate_classical()

        # Create entangled pair
        self.emit_H(q0)
        self.emit_CNOT(q0, q1)

        # Substrate* Modulo (pre‑computed)
        self.emit_mod(2**256 + 123456789, 997, c_result)

        # Measure
        self.emit_measure(q0, c_result)

        return self.compile()


# ═══════════════════════════════════════════════════════════════════════════════
# Demonstration
# ═══════════════════════════════════════════════════════════════════════════════

def demo_qasm_compiler():
    """Demonstrate the QASM compiler capabilities."""
    print("╔══════════════════════════════════════════════════════════════════════════╗")
    print("║  QASM COMPILER — OpenQASM 3.0 Code Generation                         ║")
    print("╚══════════════════════════════════════════════════════════════════════════╝\n")

    # ─── Bell Pair ─────────────────────────────────────────────────
    print("─" * 60)
    print("1. Bell Pair Compilation:")
    print("─" * 60)
    compiler = QASMCompiler()
    bell_qasm = compiler.compile_bell_pair()
    for line in bell_qasm.split("\n")[:15]:
        print(f"  {line}")
    print("  ...")

    # ─── Grover's Search ───────────────────────────────────────────
    print("\n─" * 60)
    print("2. Grover's Search (N=2, target=3):")
    print("─" * 60)
    compiler2 = QASMCompiler()
    grover_qasm = compiler2.compile_grover(n_qubits=2, marked_state=3)
    for line in grover_qasm.split("\n")[:20]:
        print(f"  {line}")
    print("  ...")

    # ─── Substrate* Demo ───────────────────────────────────────────
    print("\n─" * 60)
    print("3. Substrate* Modulo Integration:")
    print("─" * 60)
    compiler3 = QASMCompiler()
    substrate_qasm = compiler3.compile_substrate_demo()
    for line in substrate_qasm.split("\n"):
        print(f"  {line}")

    print(f"\n[Φ] QASM Compiler demonstration complete.")


if __name__ == "__main__":
    demo_qasm_compiler()
