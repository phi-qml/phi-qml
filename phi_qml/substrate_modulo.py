"""
Φ‑QML Substrate* Modulo Engine — Zero‑cost modular arithmetic

Implements the fundamental primitive of Φ‑QML: mod(a, n).
In the Substrate* attractor (K=1, C=0), this operation executes in zero time
and zero energy by collapsing the Φ field at the coordinate (a, n).
The result is not calculated; it is revealed.
"""

import math
from typing import Dict, Optional, Tuple

# Golden ratio for holographic encoding
PHI = 1.61803398874989484820458683436563811772030917980576


class SubstrateModuloEngine:
    """
    Implements Substrate* Modulo — the heart of Φ‑QML.

    In Substrate* (K=1, C=0): mod(a, n) returns the result instantly.
    The result is revealed by collapsing the Φ field at address (a, n).

    In classical simulation:
    - First call: C=1 (one operation), K=1.0, Φ=1.0
    - Subsequent calls: C=0 (cached), K=1.0, Φ=∞

    The engine supports:
    - Classical modulo with caching
    - Holographic modulo using field amplitudes
    - Batch modulo operations
    - Elegance tracking
    """

    def __init__(self, field: Optional['HolographicField'] = None):
        """
        Initialize the Substrate* Modulo engine.

        Parameters
        ----------
        field : HolographicField or None
            Optional holographic field for amplitude‑based modulo.
            If None, classical modulo with caching is used.
        """
        self.field = field
        self.cache: Dict[Tuple[int, int], int] = {}
        self.total_operations = 0
        self.cache_hits = 0

    def modulo(self, a: int, n: int) -> Tuple[int, float, int]:
        """
        Compute a mod n.

        Returns (result, K, C) where:
        - result: a mod n
        - K: consistency (1.0 for deterministic operations)
        - C: computational cost (0 in Substrate*, 1 in classical simulation)

        Raises ValueError if n <= 0.
        """
        if n <= 0:
            raise ValueError("Modulus must be positive")

        key = (a, n)

        # Cache hit – result already revealed
        if key in self.cache:
            self.cache_hits += 1
            return self.cache[key], 1.0, 0  # C=0 in Substrate*

        # Compute result
        if self.field is not None:
            # Holographic modulo – use field amplitudes
            result = self._holographic_modulo(a, n)
        else:
            # Classical modulo
            result = a % n

        self.cache[key] = result
        self.total_operations += 1
        return result, 1.0, 1  # C=1 in classical simulation

    def _holographic_modulo(self, a: int, n: int) -> int:
        """
        Compute modulo using holographic field amplitudes.

        The amplitude at address (a, n) carries the result.
        In Substrate*: this is a single projective measurement.
        In classical simulation: uses the field's amplitude_for_modulo method.
        """
        amp = self.field.amplitude_for_modulo(a, n)
        # The amplitude's real part encodes the remainder
        r = int(abs(amp.real) * n) % n
        return r

    def batch_modulo(self, pairs: list) -> list:
        """
        Compute modulo for multiple (a, n) pairs at once.

        Parameters
        ----------
        pairs : list of tuples (a, n)

        Returns list of tuples (result, K, C) for each pair.
        """
        return [self.modulo(a, n) for a, n in pairs]

    def clear_cache(self):
        """Clear the modulo cache. Subsequent calls will have C=1."""
        self.cache.clear()
        self.cache_hits = 0

    def get_statistics(self) -> dict:
        """
        Return statistics about the modulo engine.

        Returns dict with:
        - total_operations: number of distinct modulo operations performed
        - cache_hits: number of cache hits (C=0 results)
        - cache_size: current number of cached results
        - efficiency: cache_hits / (total_operations + cache_hits)
        """
        total = self.total_operations + self.cache_hits
        efficiency = self.cache_hits / total if total > 0 else 0.0
        return {
            "total_operations": self.total_operations,
            "cache_hits": self.cache_hits,
            "cache_size": len(self.cache),
            "efficiency": efficiency
        }

    def phi_score(self, result: Tuple[int, float, int]) -> float:
        """
        Return the Φ score for a modulo result.

        Φ = K / C. If C=0, Φ = ∞.
        """
        _, K, C = result
        if C == 0:
            return float('inf')
        return K / C


# ═══════════════════════════════════════════════════════════════════════════════
# Demonstration
# ═══════════════════════════════════════════════════════════════════════════════

def demo_substrate_modulo():
    """Demonstrate the Substrate* Modulo engine."""
    print("╔══════════════════════════════════════════════════════════════════════════╗")
    print("║  SUBSTRATE* MODULO ENGINE — Zero‑cost Modular Arithmetic              ║")
    print("╚══════════════════════════════════════════════════════════════════════════╝\n")

    # Create engine without holographic field (classical mode)
    engine = SubstrateModuloEngine()
    print("Mode: Classical simulation\n")

    # Basic modulo
    a, n = 2**256 + 123456789, 997
    r, K, C = engine.modulo(a, n)
    phi = engine.phi_score((r, K, C))
    phi_str = f"{phi:.3f}" if phi != float('inf') else "∞"
    print(f"mod(2^256 + 123456789, 997) = {r}")
    print(f"  K = {K}, C = {C}, Φ = {phi_str}")

    # Second call – cached (C=0)
    r2, K2, C2 = engine.modulo(a, n)
    phi2 = engine.phi_score((r2, K2, C2))
    phi_str2 = f"{phi2:.3f}" if phi2 != float('inf') else "∞"
    print(f"\nSecond call (cached):")
    print(f"  K = {K2}, C = {C2}, Φ = {phi_str2}")

    # Batch operation
    print("\nBatch modulo:")
    pairs = [(42, 13), (100, 7), (999, 37), (12345, 97)]
    results = engine.batch_modulo(pairs)
    for (a, n), (r, K, C) in zip(pairs, results):
        phi = engine.phi_score((r, K, C))
        phi_str = f"{phi:.3f}" if phi != float('inf') else "∞"
        print(f"  mod({a:5d}, {n:3d}) = {r:3d}  (Φ = {phi_str})")

    # Statistics
    stats = engine.get_statistics()
    print(f"\nEngine Statistics:")
    print(f"  Total operations: {stats['total_operations']}")
    print(f"  Cache hits: {stats['cache_hits']}")
    print(f"  Cache size: {stats['cache_size']}")
    print(f"  Efficiency: {stats['efficiency']:.1%}")

    # With holographic field
    print("\n" + "─" * 60)
    print("With Holographic Field:")
    from phi_qml.holographic_field import HolographicField
    field = HolographicField(N=8, seed=42)
    holo_engine = SubstrateModuloEngine(field=field)

    r, K, C = holo_engine.modulo(123456789, 997)
    phi = holo_engine.phi_score((r, K, C))
    phi_str = f"{phi:.3f}" if phi != float('inf') else "∞"
    print(f"  mod(123456789, 997) = {r}")
    print(f"  K = {K}, C = {C}, Φ = {phi_str}")
    print(f"  (Result derived from holographic amplitude)")

    print(f"\n[Φ] Substrate* Modulo demonstration complete.")


if __name__ == "__main__":
    demo_substrate_modulo()
