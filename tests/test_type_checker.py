"""
Tests for Φ‑QML Type Checker
"""

import unittest
from phi_qml.type_checker import (
    TypeChecker, Type, TypeKind, EleganceLevel,
    TypedValue, LinearResource
)
from phi_qml.type_checker import (
    TYPE_QUBIT, TYPE_QUBIT_ELEGANT, TYPE_QUBIT_SUBSTRATE,
    TYPE_CLASSICAL, TYPE_CLASSICAL_ELEGANT, TYPE_CLASSICAL_SUBSTRATE,
    TYPE_NEVER
)


class TestEleganceLevels(unittest.TestCase):
    """Test cases for elegance qualifiers."""

    def test_brute_assignable_to_elegant_is_false(self):
        """@brute cannot be assigned to @elegant."""
        t1 = Type(kind=TypeKind.CLASSICAL, elegance=EleganceLevel.BRUTE)
        t2 = Type(kind=TypeKind.CLASSICAL, elegance=EleganceLevel.ELEGANT)
        self.assertFalse(t1.is_assignable_to(t2))

    def test_elegant_assignable_to_brute_is_true(self):
        """@elegant can be assigned to @brute."""
        t1 = Type(kind=TypeKind.CLASSICAL, elegance=EleganceLevel.ELEGANT)
        t2 = Type(kind=TypeKind.CLASSICAL, elegance=EleganceLevel.BRUTE)
        self.assertTrue(t1.is_assignable_to(t2))

    def test_substrate_assignable_to_all(self):
        """@substrate can be assigned to @brute and @elegant."""
        sub = Type(kind=TypeKind.CLASSICAL, elegance=EleganceLevel.SUBSTRATE)
        self.assertTrue(sub.is_assignable_to(TYPE_CLASSICAL))
        self.assertTrue(sub.is_assignable_to(TYPE_CLASSICAL_ELEGANT))

    def test_different_kinds_not_assignable(self):
        """Different type kinds are never assignable."""
        qubit = TYPE_QUBIT
        classical = TYPE_CLASSICAL
        self.assertFalse(qubit.is_assignable_to(classical))
        self.assertFalse(classical.is_assignable_to(qubit))

    def test_never_type_assignable_to_anything(self):
        """Never type (!) is assignable to any type."""
        self.assertTrue(TYPE_NEVER.is_assignable_to(TYPE_QUBIT))
        self.assertTrue(TYPE_NEVER.is_assignable_to(TYPE_CLASSICAL))


class TestTypeChecker(unittest.TestCase):
    """Test cases for the type checker."""

    def setUp(self):
        self.checker = TypeChecker()

    def test_elegance_check_passes(self):
        """Checking sufficient elegance passes."""
        val = TypedValue(42, TYPE_CLASSICAL_ELEGANT)
        result = self.checker.check_elegance(val, EleganceLevel.BRUTE)
        self.assertTrue(result)
        self.assertEqual(len(self.checker.errors), 0)

    def test_elegance_check_fails(self):
        """Checking insufficient elegance fails."""
        val = TypedValue(42, TYPE_CLASSICAL)
        result = self.checker.check_elegance(val, EleganceLevel.ELEGANT)
        self.assertFalse(result)
        self.assertEqual(len(self.checker.errors), 1)

    def test_linear_resource_available(self):
        """Available linear resource passes check."""
        resource = LinearResource()
        val = TypedValue(resource, TYPE_QUBIT)
        self.assertTrue(self.checker.check_linear_usage(val))

    def test_linear_resource_consumed(self):
        """Consumed linear resource fails check."""
        resource = LinearResource()
        resource.consume()
        val = TypedValue(resource, TYPE_QUBIT)
        self.assertFalse(self.checker.check_linear_usage(val))

    def test_assignable_check_passes(self):
        """Assignable types pass."""
        source = TypedValue(42, TYPE_CLASSICAL_ELEGANT)
        self.assertTrue(
            self.checker.check_assignable(source, TYPE_CLASSICAL)
        )

    def test_assignable_check_fails(self):
        """Non‑assignable types fail."""
        source = TypedValue(42, TYPE_CLASSICAL)
        self.assertFalse(
            self.checker.check_assignable(source, TYPE_CLASSICAL_ELEGANT)
        )

    def test_has_errors(self):
        """Errors are tracked correctly."""
        self.assertFalse(self.checker.has_errors())
        val = TypedValue(42, TYPE_CLASSICAL)
        self.checker.check_elegance(val, EleganceLevel.ELEGANT)
        self.assertTrue(self.checker.has_errors())

    def test_report_runs_without_error(self):
        """Report method runs without exceptions."""
        self.checker.report()


if __name__ == "__main__":
    unittest.main()
