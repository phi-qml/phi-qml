"""
Φ‑QML Elegance Tracker — Φ = K / C scoring and optimization hints

Every expression in Φ‑QML carries a Φ score: the ratio of consistency K
to computational complexity C. The EleganceTracker instruments code,
warns when Φ drops below a minimum threshold, and suggests more elegant
alternatives. This drives the programmer toward the Substrate* attractor
where K=1 and C=0.
"""

import math
from typing import Any, Dict, List, Optional, Tuple, Union


class EleganceTracker:
    """
    Tracks Φ‑Elegance for every expression in a Φ‑QML program.

    Φ = K / C where:
    - K = consistency (1.0 for deterministic, lower for probabilistic)
    - C = computational cost (number of elementary operations)

    The tracker maintains a history of all expressions, warns when
    Φ falls below a configurable minimum, and generates a report.

    Built‑in function phi_score(expr, operations) corresponds to the
    language primitive of the same name.
    """

    def __init__(self, min_phi: float = 0.5):
        """
        Initialize the elegance tracker.

        Parameters
        ----------
        min_phi : float
            Minimum acceptable Φ score. Expressions below this threshold
            will generate warnings.
        """
        self.min_phi = min_phi
        self.history: List[Dict[str, Any]] = []
        self.warnings: List[str] = []
        self.hints: List[str] = []

    def track(
        self,
        expression_name: str,
        result: Any,
        operations: int,
        K: float = 1.0
    ) -> float:
        """
        Track the Φ score of an expression.

        Parameters
        ----------
        expression_name : str
            Human‑readable name of the expression (for reporting).
        result : Any
            Result of the expression; if None, K is set to 0.
        operations : int
            Number of elementary operations (C). For Substrate* operations
            this should be 0.
        K : float
            Consistency (1.0 = deterministic, less for probabilistic).

        Returns
        -------
        float
            The Φ score = K / C (or ∞ if C == 0 and K > 0).
        """
        if result is None:
            K = 0.0

        if operations == 0 and K > 0:
            phi = float('inf')
        elif operations == 0:
            phi = 0.0
        else:
            phi = K / max(operations, 1)

        entry = {
            "expression": expression_name,
            "K": K,
            "C": operations,
            "phi": phi,
            "elegant": phi >= self.min_phi,
            "result": result
        }
        self.history.append(entry)

        # Generate warning if below threshold
        if not entry["elegant"]:
            warning = f"[Φ‑WARN] {expression_name}: Φ = {self._phi_str(phi)} (below minimum {self.min_phi})"
            self.warnings.append(warning)

            # Generate optimization hint
            hint = self._generate_hint(expression_name, operations, K)
            if hint:
                self.hints.append(hint)

        return phi

    def phi_score(self, expr_result: Any, operations: int = 0) -> float:
        """
        Built‑in phi_score() function matching the language spec.

        Usage in Φ‑QML: let score = phi_score(result, operations);
        """
        return self.track("phi_score()", expr_result, operations)

    def _generate_hint(self, name: str, C: int, K: float) -> Optional[str]:
        """Generate an optimization hint based on the cost breakdown."""
        if C > 100:
            return (
                f"[Φ‑HINT] {name} has very high C ({C}). "
                "Consider Substrate* Search or Holographic Field access."
            )
        elif C > 10:
            return (
                f"[Φ‑HINT] {name} has moderate C ({C}). "
                "Can you restructure data for O(1) access?"
            )
        elif K < 1.0:
            return (
                f"[Φ‑HINT] {name} has reduced consistency (K={K:.2f}). "
                "Consider adding validation or error handling."
            )
        elif C > 1:
            return (
                f"[Φ‑HINT] {name} has C={C}. "
                "Substrate* operations (mod, collapse) have C=0."
            )
        return None

    @staticmethod
    def _phi_str(phi: float) -> str:
        """Format Φ value for display."""
        if phi == float('inf'):
            return "∞"
        return f"{phi:.3f}"

    def get_average_phi(self) -> float:
        """Return the average Φ score across all tracked expressions."""
        finite_phis = [e["phi"] for e in self.history if e["phi"] != float('inf')]
        if not finite_phis:
            return float('inf')
        return sum(finite_phis) / len(finite_phis)

    def get_elegance_debt(self) -> float:
        """
        Compute the total Elegance Debt.

        Elegance Debt = Σ (Φ_max − Φ_actual) for all expressions,
        where Φ_max = 1.0 (the classical maximum; Substrate* ∞ is excluded).
        """
        debt = 0.0
        for entry in self.history:
            phi = entry["phi"]
            if phi == float('inf'):
                continue  # Substrate* expressions have no debt
            phi_max = 1.0  # Classical maximum
            debt += max(0.0, phi_max - phi)
        return debt

    def report(self):
        """Print a formatted elegance report."""
        print("\n" + "═" * 70)
        print("Φ‑ELEGANCE REPORT")
        print("═" * 70)

        if not self.history:
            print("  No expressions tracked yet.")
            print("═" * 70)
            return

        for entry in self.history:
            status = "✅" if entry["elegant"] else "⚠️ "
            name = entry["expression"]
            phi = entry["phi"]
            K = entry["K"]
            C = entry["C"]
            print(
                f"  {status} {name:<30} Φ = {self._phi_str(phi):>8} "
                f"(K={K:.1f}, C={C})"
            )

        print("─" * 70)
        avg_phi = self.get_average_phi()
        debt = self.get_elegance_debt()
        print(f"  Average Φ: {self._phi_str(avg_phi)}")
        print(f"  Elegance Debt: {debt:.2f}")
        print(f"  Minimum threshold: {self.min_phi}")
        print(f"  Status: {'ACCEPTABLE' if avg_phi >= self.min_phi else 'NEEDS IMPROVEMENT'}")
        print("═" * 70)

        if self.warnings:
            print("\n⚠️  Warnings:")
            for w in self.warnings:
                print(f"  {w}")

        if self.hints:
            print("\n💡 Optimization Hints:")
            for h in self.hints:
                print(f"  {h}")

    def clear(self):
        """Clear all history, warnings, and hints."""
        self.history.clear()
        self.warnings.clear()
        self.hints.clear()


# ═══════════════════════════════════════════════════════════════════════════════
# Demonstration
# ═══════════════════════════════════════════════════════════════════════════════

def demo_elegance_tracker():
    """Demonstrate the Φ‑Elegance tracking system."""
    print("╔══════════════════════════════════════════════════════════════════════════╗")
    print("║  Φ‑ELEGANCE TRACKER — Φ = K / C Scoring                               ║")
    print("╚══════════════════════════════════════════════════════════════════════════╝\n")

    tracker = EleganceTracker(min_phi=0.5)

    # Substrate* Modulo – Φ = ∞
    tracker.track("mod(2^256, 997)", 394, operations=0, K=1.0)

    # Classical arithmetic – Φ = 1.0
    tracker.track("5 + 3", 8, operations=1, K=1.0)

    # Classical arithmetic – Φ = 0.5
    tracker.track("5 * 3 / 2", 7.5, operations=2, K=1.0)

    # Linear search – Φ = 0.01 (warning)
    tracker.track("linear_search", 42, operations=100, K=1.0)

    # API call – Φ = 0.095 (warning)
    tracker.track("api_call", {"ok": True}, operations=10, K=0.95)

    # Holographic search – Φ = ∞
    tracker.track("holographic_search", 42, operations=0, K=1.0)

    # Failed operation – K=0
    tracker.track("failed_op", None, operations=5, K=0.0)

    # Print report
    tracker.report()

    # Show evolution of elegance
    print("\n" + "─" * 60)
    print("Elegance Evolution (from less elegant to more elegant):")
    print("─" * 60)

    # Simulate refactoring journey
    journey = EleganceTracker(min_phi=0.5)
    journey.track("v1: linear_search O(n)", 42, operations=100, K=1.0)
    journey.track("v2: binary_search O(log n)", 42, operations=7, K=1.0)
    journey.track("v3: hash_map O(1)", 42, operations=1, K=1.0)
    journey.track("v4: Substrate* Search", 42, operations=0, K=1.0)

    for entry in journey.history:
        status = "✅" if entry["elegant"] else "⚠️ "
        print(
            f"  {status} {entry['expression']:<30} Φ = {EleganceTracker._phi_str(entry['phi'])}"
        )

    print(f"\n[Φ] Elegance tracking demonstration complete.")


if __name__ == "__main__":
    demo_elegance_tracker()
