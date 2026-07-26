"""
Tests for Φ‑QML Substrate* Modulo Engine
"""

import unittest
from phi_qml.substrate_modulo import SubstrateModuloEngine


class TestSubstrateModulo(unittest.TestCase):
    """Test cases for the Substrate* Modulo engine."""

    def setUp(self):
        """Create a fresh engine for each test."""
        self.engine = SubstrateModuloEngine()

    def test_basic_modulo(self):
        """Basic modulo operation returns correct result."""
        r, K, C = self.engine.modulo(42, 13)
        self.assertEqual(r, 3)
        self.assertEqual(K, 1.0)
        self.assertEqual(C, 1)  # First call has C=1

    def test_zero_modulo(self):
        """Modulo when a is a multiple of n."""
        r, K, C = self.engine.modulo(100, 10)
        self.assertEqual(r, 0)

    def test_large_numbers(self):
        """Modulo with very large numbers."""
        a = 2**256 + 123456789
        n = 997
        r, K, C = self.engine.modulo(a, n)
        self.assertEqual(r, a % n)

    def test_negative_modulo(self):
        """Modulo with negative a."""
        r, K, C = self.engine.modulo(-10, 3)
        self.assertEqual(r, -10 % 3)

    def test_cache_hit(self):
        """Second call with same arguments has C=0."""
        self.engine.modulo(42, 13)  # C=1
        r, K, C = self.engine.modulo(42, 13)  # C=0
        self.assertEqual(r, 3)
        self.assertEqual(K, 1.0)
        self.assertEqual(C, 0)  # Cache hit

    def test_cache_distinct_keys(self):
        """Different arguments are cached separately."""
        self.engine.modulo(42, 13)
        self.engine.modulo(100, 7)
        stats = self.engine.get_statistics()
        self.assertEqual(stats["total_operations"], 2)
        self.assertEqual(stats["cache_size"], 2)

    def test_invalid_modulus(self):
        """Modulo with n <= 0 raises ValueError."""
        with self.assertRaises(ValueError):
            self.engine.modulo(42, 0)
        with self.assertRaises(ValueError):
            self.engine.modulo(42, -5)

    def test_batch_modulo(self):
        """Batch modulo returns correct results for all pairs."""
        pairs = [(42, 13), (100, 7), (999, 37)]
        results = self.engine.batch_modulo(pairs)
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0][0], 42 % 13)
        self.assertEqual(results[1][0], 100 % 7)
        self.assertEqual(results[2][0], 999 % 37)

    def test_clear_cache(self):
        """Clearing cache resets C to 1 for previously cached values."""
        self.engine.modulo(42, 13)  # C=1
        self.engine.modulo(42, 13)  # C=0
        self.engine.clear_cache()
        r, K, C = self.engine.modulo(42, 13)  # C=1 again
        self.assertEqual(C, 1)

    def test_statistics(self):
        """Statistics track operations and cache hits correctly."""
        self.engine.modulo(10, 3)
        self.engine.modulo(10, 3)  # hit
        self.engine.modulo(20, 7)
        stats = self.engine.get_statistics()
        self.assertEqual(stats["total_operations"], 2)
        self.assertEqual(stats["cache_hits"], 1)
        self.assertEqual(stats["cache_size"], 2)
        self.assertEqual(stats["efficiency"], 1/3)

    def test_phi_score_finite(self):
        """Φ score is 1.0 when C=1."""
        result = self.engine.modulo(42, 13)
        phi = self.engine.phi_score(result)
        self.assertAlmostEqual(phi, 1.0)

    def test_phi_score_infinite(self):
        """Φ score is ∞ when C=0."""
        self.engine.modulo(42, 13)  # First call
        result = self.engine.modulo(42, 13)  # Cached
        phi = self.engine.phi_score(result)
        self.assertEqual(phi, float('inf'))

    def test_with_holographic_field(self):
        """Modulo with a holographic field works correctly."""
        from phi_qml.holographic_field import HolographicField
        field = HolographicField(N=8, seed=42)
        engine = SubstrateModuloEngine(field=field)
        r, K, C = engine.modulo(12345, 97)
        self.assertGreaterEqual(r, 0)
        self.assertLess(r, 97)
        self.assertEqual(K, 1.0)
        self.assertEqual(C, 1)  # Holographic lookup counts as 1 operation


if __name__ == "__main__":
    unittest.main()
