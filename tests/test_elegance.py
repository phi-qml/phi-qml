"""
Tests for Φ‑QML Elegance Tracker
"""

import unittest
from phi_qml.elegance_tracker import EleganceTracker


class TestEleganceTracker(unittest.TestCase):
    """Test cases for the Φ‑Elegance tracker."""

    def setUp(self):
        """Create a fresh tracker for each test."""
        self.tracker = EleganceTracker(min_phi=0.5)

    def test_basic_tracking(self):
        """Tracking an expression returns its Φ score."""
        phi = self.tracker.track("add", 8, operations=1, K=1.0)
        self.assertAlmostEqual(phi, 1.0)

    def test_phi_score_builtin(self):
        """The phi_score function matches the language specification."""
        phi = self.tracker.phi_score(42, operations=0)
        self.assertEqual(phi, float('inf'))

    def test_substrate_operation_has_infinite_phi(self):
        """Substrate* operation (C=0) has Φ = ∞."""
        phi = self.tracker.track("mod", 3, operations=0, K=1.0)
        self.assertEqual(phi, float('inf'))

    def test_failed_operation_has_zero_phi(self):
        """Failed operation (result=None) has K=0, Φ=0."""
        phi = self.tracker.track("fail", None, operations=5)
        self.assertAlmostEqual(phi, 0.0)

    def test_high_cost_lowers_phi(self):
        """Higher operation count reduces Φ."""
        phi = self.tracker.track("slow", 42, operations=100, K=1.0)
        self.assertAlmostEqual(phi, 0.01)

    def test_reduced_consistency_lowers_phi(self):
        """Lower K reduces Φ."""
        phi = self.tracker.track("unreliable", "ok", operations=1, K=0.8)
        self.assertAlmostEqual(phi, 0.8)

    def test_warning_below_minimum(self):
        """Expression below min_phi generates a warning."""
        self.tracker.track("slow", 42, operations=100, K=1.0)
        self.assertTrue(len(self.tracker.warnings) > 0)

    def test_no_warning_above_minimum(self):
        """Expression above min_phi generates no warning."""
        self.tracker.track("fast", 42, operations=1, K=1.0)
        self.assertTrue(len(self.tracker.warnings) == 0)

    def test_hint_generation(self):
        """Hints are generated for suboptimal expressions."""
        self.tracker.track("slow", 42, operations=101, K=1.0)
        self.assertTrue(len(self.tracker.hints) > 0)

    def test_average_phi(self):
        """Average Φ excludes infinite values."""
        self.tracker.track("a", 1, operations=1, K=1.0)   # Φ=1.0
        self.tracker.track("b", 2, operations=2, K=1.0)   # Φ=0.5
        self.tracker.track("c", 3, operations=0, K=1.0)   # Φ=∞ (excluded)
        avg = self.tracker.get_average_phi()
        self.assertAlmostEqual(avg, 0.75)

    def test_elegance_debt(self):
        """Elegance Debt sums Φ_max − Φ_actual for finite expressions."""
        self.tracker.track("a", 1, operations=2, K=1.0)   # Φ=0.5, debt=0.5
        self.tracker.track("b", 2, operations=0, K=1.0)   # Φ=∞, debt=0
        debt = self.tracker.get_elegance_debt()
        self.assertAlmostEqual(debt, 0.5)

    def test_clear_resets_state(self):
        """Clear removes all history, warnings, and hints."""
        self.tracker.track("slow", 42, operations=100)
        self.tracker.clear()
        self.assertEqual(len(self.tracker.history), 0)
        self.assertEqual(len(self.tracker.warnings), 0)
        self.assertEqual(len(self.tracker.hints), 0)

    def test_report_runs_without_error(self):
        """Report method runs without exceptions."""
        self.tracker.track("test", 42, operations=1)
        self.tracker.report()


if __name__ == "__main__":
    unittest.main()
