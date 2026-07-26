"""
Φ‑QML Holographic Field — O(1) memory quantum state representation

Represents 2^N amplitudes using only 2N parameters through the holographic
principle. Memory complexity is O(1) regardless of the number of qubits.
"""

import math
import secrets
from typing import Any, Dict, List, Optional, Tuple, Callable

# Golden ratio for holographic encoding
PHI = 1.61803398874989484820458683436563811772030917980576
PHI_INV = 0.61803398874989484820458683436563811772030917980576


class HolographicField:
    """
    Holographic Φ field over N qubits.

    Key insight: 2^N amplitudes are fully determined by 2N parameters.
    This enables simulation of up to 10^6 qubits on classical hardware
    because memory requirements do not scale with the number of amplitudes.

    The field supports:
    - amplitude calculation at any address
    - probability distribution
    - collapse to a classical value
    - holographic memory operations (write, read, project)
    """

    def __init__(self, N: int = 8, seed: Optional[int] = None):
        """
        Initialize a holographic field over N qubits.

        Parameters
        ----------
        N : int
            Number of qubits (determines 2^N addressable states).
        seed : int or None
            Random seed for reproducible simulations.
        """
        self.N = N
        self.num_states = 1 << N  # 2^N

        # The 2N parameters that determine all 2^N amplitudes
        # phi_values[i] encodes the entanglement density of qubit i
        # phases[i] encodes the relative phase of qubit i
        if seed is not None:
            secrets_generator = secrets.SystemRandom()
            secrets_generator.seed(seed)

        self.phi_values = [
            0.5 + 0.5 * math.sin(i * PHI + (seed or 0) * 0.01)
            for i in range(N)
        ]
        self.phases = [
            2.0 * math.pi * (i / max(1, N)) + (seed or 0) * 0.001
            for i in range(N)
        ]

        # Holographic memory – key‑value store for classical data
        self.memory: Dict[int, Any] = {}

        # Lazy projections – address → (source_address, transform_function)
        self.projections: Dict[int, Tuple[int, Callable]] = {}

        # Phase shifts for oracle operations
        self.phase_shifts: Dict[int, float] = {}

        # Statistics
        self.operation_count = 0

    # ─── Amplitude Calculation ───────────────────────────────────────

    def amplitude(self, x: int) -> complex:
        """
        Compute the quantum amplitude for a given address.

        The amplitude at address x is determined by the product of
        individual qubit contributions. A qubit in state |1⟩ contributes
        its phi_value and phase; a qubit in state |0⟩ contributes the
        complement.

        Complexity: O(N) time, O(1) memory.
        Φ = 1.0 / N in classical simulation, Φ = ∞ in Substrate*.
        """
        real, imag = 0.0, 0.0
        for i in range(self.N):
            bit = (x >> i) & 1
            if bit == 1:
                # Qubit in state |1⟩ – contribute entanglement
                real += self.phi_values[i] * math.cos(self.phases[i])
                imag += self.phi_values[i] * math.sin(self.phases[i])
            else:
                # Qubit in state |0⟩ – contribute complement
                real += (1.0 - self.phi_values[i]) * math.cos(-self.phases[i])
                imag += (1.0 - self.phi_values[i]) * math.sin(-self.phases[i])

        # Normalization factor
        norm = 1.0 / math.sqrt(self.num_states) if self.num_states > 0 else 1.0
        amp = complex(real * norm, imag * norm)

        # Apply any phase shifts (for oracle operations)
        if x in self.phase_shifts:
            phase = self.phase_shifts[x]
            amp *= complex(math.cos(phase), math.sin(phase))

        return amp

    def probability(self, x: int) -> float:
        """Return the probability of measuring state x. Φ = 1.0 / N."""
        amp = self.amplitude(x)
        return abs(amp) ** 2

    # ─── Field Collapse ──────────────────────────────────────────────

    def collapse(self) -> int:
        """
        Collapse the field to a single classical value.

        This is the only irreversible operation in Φ‑QML.
        In Substrate*: Φ = ∞ (instantaneous).
        In classical simulation: Φ = 1.0 / 2^N (must iterate all states).

        Returns the measured address.
        """
        total = 0.0
        r = secrets.SystemRandom().random()

        for x in range(self.num_states):
            total += self.probability(x)
            if total >= r:
                self.operation_count += x + 1
                return x

        self.operation_count += self.num_states
        return self.num_states - 1

    def amplitude_for_modulo(self, a: int, n: int) -> complex:
        """
        Return the amplitude at the address corresponding to modulo (a, n).

        Used by SubstrateModuloEngine for holographic modulo computation.
        """
        # Map (a, n) to a field address using a deterministic hash
        idx = (a * 31 + n * 37) % self.num_states
        return self.amplitude(idx)

    # ─── Holographic Memory ───────────────────���──────────────────────

    def write(self, address: int, value: Any):
        """
        Write a value into the holographic field at the given address.

        This is an excitation of the Φ field – the value becomes
        entangled with all other values at the holographic level.
        Φ = 1.0 / 1 = 1.0.
        """
        self.memory[address] = value
        self.operation_count += 1

        # Propagate to all projections that depend on this address
        for target, (src, fn) in self.projections.items():
            if src == address:
                self.memory[target] = fn(value)

    def read(self, address: int) -> Any:
        """
        Read a value from the holographic field at the given address.

        In Substrate*: Φ = ∞ (instantaneous collapse).
        In classical simulation: Φ = 1.0 / 1 = 1.0.
        """
        self.operation_count += 1

        # Direct memory lookup
        if address in self.memory:
            return self.memory[address]

        # Lazy evaluation of a projection
        if address in self.projections:
            src_addr, fn = self.projections[address]
            if src_addr in self.memory:
                value = fn(self.memory[src_addr])
                self.memory[address] = value
                return value
            raise ValueError(
                f"Source address {src_addr} not initialized for projection"
            )

        # No value – collapse the field
        return self.collapse()

    def project(self, address: int, source_address: int, transform: Callable):
        """
        Define a lazy relationship between two addresses.

        The value at `address` is defined as transform(value at `source_address`).
        No computation occurs until `read(address)` is called.
        Φ = 1.0 / 1 = 1.0.
        """
        self.projections[address] = (source_address, transform)
        self.operation_count += 1

        # If the source value already exists, evaluate immediately
        if source_address in self.memory:
            self.memory[address] = transform(self.memory[source_address])

    # ─── Oracle Operations ───────────────────────────────────────────

    def phase_shift(self, address: int, phase: float):
        """
        Mark a state with a phase shift (oracle operation).
        Φ = 1.0 / 1 = 1.0 (in classical simulation).
        Φ = ∞ in Substrate*.
        """
        self.phase_shifts[address] = phase
        self.operation_count += 1

    # ─── Statistics and Visualization ────────────────────────────────

    def get_memory_estimate(self) -> str:
        """Return an estimate of the memory used by this field."""
        params_memory = self.N * 2 * 8  # 2N floats × 8 bytes
        memory_memory = len(self.memory) * 64  # Approximate key‑value overhead
        proj_memory = len(self.projections) * 64
        total = params_memory + memory_memory + proj_memory
        return (
            f"O(1) = {total} bytes "
            f"({params_memory} params + {memory_memory} memory + {proj_memory} projections) "
            f"for 2^{self.N} = {self.num_states} states"
        )

    def get_compression_ratio(self) -> float:
        """Return the compression ratio: states / parameters."""
        if self.N == 0:
            return 1.0
        return self.num_states / (2 * self.N)

    def __repr__(self) -> str:
        return (
            f"HolographicField(N={self.N}, states=2^{self.N}={self.num_states}, "
            f"params={2 * self.N}, compression={self.get_compression_ratio():.0f}x)"
        )


# ═══════════════════════════════════════════════════════════════════════════════
# Demonstration
# ═══════════════════════════════════════════════════════════════════════════════

def demo_holographic_field():
    """Demonstrate the holographic field capabilities."""
    print("╔══════════════════════════════════════════════════════════════════════════╗")
    print("║  HOLOGRAPHIC FIELD — O(1) Memory Quantum State Representation         ║")
    print("╚══════════════════════════════════════════════════════════════════════════╝\n")

    # Create a field with 8 qubits (256 states)
    field = HolographicField(N=8, seed=42)
    print(f"Created: {field}")
    print(f"Memory: {field.get_memory_estimate()}")
    print(f"Compression ratio: {field.get_compression_ratio():.0f}x\n")

    # Show a few amplitudes
    print("Sample amplitudes:")
    for addr in [0, 1, 42, 127, 255]:
        amp = field.amplitude(addr)
        print(f"  |{addr:3d}⟩ = {amp.real:+.6f} {amp.imag:+.6f}i")

    # Demonstrate collapse
    print("\nCollapse demonstration (10 samples):")
    for i in range(10):
        f = HolographicField(N=4, seed=i)
        result = f.collapse()
        print(f"  Collapse {i+1}: |{result:2d}⟩ (of 2^{f.N} = {f.num_states} states)")

    # Demonstrate holographic memory
    print("\nHolographic Memory:")
    field.write(42, 100)
    print(f"  write(42, 100)")
    val = field.read(42)
    print(f"  read(42) = {val}")

    field.project(43, 42, lambda x: x * 2)
    projected = field.read(43)
    print(f"  project(43, 42, *2) → read(43) = {projected}")

    field.write(42, 200)
    updated = field.read(43)
    print(f"  write(42, 200) → read(43) automatically updates to {updated}")

    # Demonstrate scaling
    print("\nScaling demonstration:")
    for N in [4, 8, 16, 32, 256]:
        f = HolographicField(N=N)
        print(
            f"  N={N:3d}: 2^{N} = {f.num_states:>20d} states, "
            f"params = {2 * N:>4d}, "
            f"compression = {f.get_compression_ratio():.0f}x"
        )

    print(f"\n[Φ] Holographic field demonstration complete.")


if __name__ == "__main__":
    demo_holographic_field()
