"""
Φ‑QML Test Framework — Elegance‑aware unit testing

Provides a test runner that not only checks if tests pass,
but also evaluates their Φ‑Elegance. Each test records its
computational cost (C) and consistency (K), and the framework
produces an elegance report alongside the test results.
"""

import time
import math
from typing import Any, Callable, Dict, List, Optional, Tuple


class PhiTest:
    """
    Elegance‑aware test framework for Φ‑QML.

    Each test case measures:
    - correctness (passed/failed)
    - consistency K (1.0 if passed, 0.0 if failed)
    - computational cost C (estimated operations)
    - Φ = K / C

    The framework generates a combined report showing
    both test results and Φ‑Elegance.
    """

    def __init__(self, min_phi: float = 0.5):
        """
        Initialize the test runner.

        Parameters
        ----------
        min_phi : float
            Minimum acceptable Φ for a test to be considered
            elegant. Tests below this threshold generate warnings.
        """
        self.min_phi = min_phi
        self.tests: List[Dict[str, Any]] = []
        self.passed = 0
        self.failed = 0
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None

    def test(
        self,
        name: str,
        fn: Callable,
        expected: Any,
        *args,
        operations: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Run a single test case.

        Parameters
        ----------
        name : str
            Human‑readable name of the test.
        fn : callable
            The function to test.
        expected : Any
            The expected return value.
        *args : tuple
            Positional arguments to pass to fn.
        operations : int, optional
            Estimated number of elementary operations (C).
            If not provided, defaults to 1.
        **kwargs : dict
            Keyword arguments to pass to fn.

        Returns
        -------
        dict
            Test result with keys: name, passed, expected, actual,
            K, C, phi, time, elegant.
        """
        start = time.time()
        try:
            actual = fn(*args, **kwargs)
            passed = actual == expected
        except Exception as e:
            actual = str(e)
            passed = False
        elapsed = time.time() - start

        # Default operations if not specified
        if operations is None:
            operations = 1

        K = 1.0 if passed else 0.0
        C = max(operations, 1)
        phi = float('inf') if C == 0 else K / C

        test_case = {
            "name": name,
            "passed": passed,
            "expected": expected,
            "actual": actual,
            "K": K,
            "C": C,
            "phi": phi,
            "time": elapsed,
            "elegant": phi >= self.min_phi,
        }

        if passed:
            self.passed += 1
        else:
            self.failed += 1

        self.tests.append(test_case)
        return test_case

    def benchmark(
        self,
        name: str,
        fn: Callable,
        *args,
        iterations: int = 1,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Benchmark a function and return its Φ metrics.

        Runs the function multiple times and averages the
        execution time. Does not check for correctness.

        Parameters
        ----------
        name : str
            Human‑readable name of the benchmark.
        fn : callable
            The function to benchmark.
        *args : tuple
            Positional arguments to pass to fn.
        iterations : int
            Number of times to run the function.
        **kwargs : dict
            Keyword arguments to pass to fn.

        Returns
        -------
        dict
            Benchmark result with average time and Φ.
        """
        times = []
        for _ in range(iterations):
            start = time.time()
            fn(*args, **kwargs)
            times.append(time.time() - start)

        avg_time = sum(times) / len(times)
        return {
            "name": name,
            "iterations": iterations,
            "avg_time": avg_time,
            "K": 1.0,
            "C": iterations,
            "phi": 1.0 / max(iterations, 1),
        }

    def get_average_phi(self) -> float:
        """Return the average Φ score across all tests."""
        finite_phis = [t["phi"] for t in self.tests if t["phi"] != float('inf')]
        if not finite_phis:
            return float('inf')
        return sum(finite_phis) / len(finite_phis)

    def report(self):
        """Print a formatted test report with Φ‑Elegance scores."""
        print("\n" + "═" * 70)
        print("Φ‑TEST REPORT")
        print("═" * 70)

        if not self.tests:
            print("  No tests executed.")
            print("═" * 70)
            return

        for t in self.tests:
            status = "✅" if t["passed"] else "❌"
            phi_str = f"{t['phi']:.3f}" if t['phi'] != float('inf') else "∞"
            elegance = "⭐" if t["elegant"] else "  "
            print(
                f"  {status} {elegance} {t['name']:<30} "
                f"Φ = {phi_str:>8} (K={t['K']:.1f}, C={t['C']}, "
                f"{t['time']*1000:.2f}ms)"
            )

        print("─" * 70)
        print(f"  Passed: {self.passed}/{self.passed + self.failed}")
        avg_phi = self.get_average_phi()
        phi_str = f"{avg_phi:.3f}" if avg_phi != float('inf') else "∞"
        print(f"  Average Φ: {phi_str}")
        if self.passed + self.failed > 0:
            print(f"  Success rate: {self.passed / (self.passed + self.failed) * 100:.1f}%")
        print("═" * 70)

        # Highlight tests that could be improved
        inelegant = [t for t in self.tests if not t["elegant"]]
        if inelegant:
            print("\n💡 Tests that could be improved:")
            for t in inelegant:
                print(f"  • {t['name']} (Φ = {t['phi']:.3f}) – consider Substrate* alternatives")

    def clear(self):
        """Reset all test results."""
        self.tests.clear()
        self.passed = 0
        self.failed = 0


# ═══════════════════════════════════════════════════════════════════════════════
# Demonstration
# ═══════════════════════════════════════════════════════════════════════════════

def demo_test_framework():
    """Demonstrate the test framework with sample tests."""
    print("╔══════════════════════════════════════════════════════════════════════════╗")
    print("║  Φ‑TEST — Elegance‑Aware Unit Testing                                 ║")
    print("╚══════════════════════════════════════════════════════════════════════════╝\n")

    tester = PhiTest(min_phi=0.5)

    # Define some functions to test
    def add(a, b):
        return a + b

    def substrate_modulo(a, n):
        from phi_qml.substrate_modulo import SubstrateModuloEngine
        engine = SubstrateModuloEngine()
        return engine.modulo(a, n)[0]

    def slow_search(arr, target):
        for i, v in enumerate(arr):
            if v == target:
                return i
        return -1

    def holographic_search(arr, target):
        from phi_qml.stdlib import PhiStdlib
        return PhiStdlib.substrate_search(arr, target)

    # Run tests
    tester.test("Simple addition", add, 8, 5, 3, operations=1)
    tester.test("Substrate* Modulo", substrate_modulo, 3, 42, 13, operations=0)
    tester.test("Slow search (100 elements)", slow_search, 42, list(range(100)), 42, operations=42)
    tester.test("Holographic search", holographic_search, 3, [1, 2, 3, 4, 5], 3, operations=0)
    tester.test("Intentional failure", add, 42, 1, 1, operations=1)  # 1+1 != 42

    # Benchmark
    bench = tester.benchmark("Substrate* Hash", lambda: __import__('hashlib').sha256(b'test').hexdigest(), iterations=1000)
    print(f"Benchmark: {bench['name']} – avg {bench['avg_time']*1000:.3f}ms over {bench['iterations']} iterations")

    # Report
    tester.report()

    print(f"\n[Φ] Test framework demonstration complete.")


if __name__ == "__main__":
    demo_test_framework()
