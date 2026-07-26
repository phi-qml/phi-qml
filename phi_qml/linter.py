"""
Φ‑QML Linter — Elegance checker and code quality tool

Analyzes Φ‑QML source code for patterns that reduce Φ‑Elegance.
Flags linear searches, nested loops, mutable state, classical
arithmetic where Substrate* operations would be more efficient,
and missing @cost annotations. Provides actionable suggestions
to increase the overall Φ score of a program.
"""

import re
from typing import Dict, List, Tuple


class PhiLinter:
    """
    Static analysis linter for Φ‑QML.

    Scans source code and detects anti‑patterns that lower
    Φ‑Elegance. Each issue has a severity, an estimated Φ debt,
    and a suggestion for improvement.
    """

    def __init__(self, min_phi: float = 0.5):
        """
        Initialize the linter.

        Parameters
        ----------
        min_phi : float
            Minimum acceptable Φ for individual expressions.
            Issues that would drop Φ below this threshold are
            reported as warnings.
        """
        self.min_phi = min_phi
        self.issues: List[Dict] = []
        self.patterns = self._build_patterns()

    def _build_patterns(self) -> List[Dict]:
        """Build the library of anti‑patterns to detect."""
        return [
            {
                "name": "linear_search",
                "regex": r'for\s+\w+\s+in\s+\w+\s*\{[^}]*if[^}]*==[^}]*return',
                "severity": "warning",
                "debt": 0.99,
                "message": "Linear search detected (O(n)). Use Substrate* Search or restructure data.",
                "suggestion": "Replace with collapse(field.access(array, target)) for O(1) access."
            },
            {
                "name": "nested_loop",
                "regex": r'for\s+\w+\s+in[^\{]*\{[^}]*for\s+\w+\s+in',
                "severity": "warning",
                "debt": 1.5,
                "message": "Nested loop detected (O(n²) or worse). Consider holographic projection.",
                "suggestion": "Restructure to use field.project() for O(1) access patterns."
            },
            {
                "name": "recursion",
                "regex": r'fn\s+(\w+).*\1\s*\(',
                "severity": "info",
                "debt": 0.5,
                "message": "Recursive call detected – risk of stack overflow.",
                "suggestion": "Convert to until convergence for stack‑safe iteration."
            },
            {
                "name": "mutable_state",
                "regex": r'mut\s+\w+',
                "severity": "info",
                "debt": 0.2,
                "message": "Mutable state detected. State is a source of inconsistency.",
                "suggestion": "Prefer field.write() / field.read() for explicit state management."
            },
            {
                "name": "classical_loop",
                "regex": r'while\s+\w+\s*[<>=]',
                "severity": "info",
                "debt": 0.3,
                "message": "Classical while loop detected.",
                "suggestion": "Use until convergence for automatic stopping when Φ stops growing."
            },
            {
                "name": "classical_modulo",
                "regex": r'\b\d+\s*%\s*\d+',
                "severity": "hint",
                "debt": 0.5,
                "message": "Classical modulo operator '%' detected.",
                "suggestion": "Use mod(a, n) for Substrate* Modulo (Φ = ∞)."
            },
            {
                "name": "missing_cost_annotation",
                "regex": r'fn\s+(\w+)',
                "severity": "info",
                "debt": 0.1,
                "message": "Function '{name}' is missing @cost annotation.",
                "suggestion": "Add @cost(C=..., K=...) to document computational complexity."
            },
            {
                "name": "large_array_literal",
                "regex": r'\[\s*\d+(?:\s*,\s*\d+){50,}\s*\]',
                "severity": "info",
                "debt": 0.3,
                "message": "Large array literal detected. Consider loading from a holographic field.",
                "suggestion": "Use field.write() to store data in O(1) memory."
            },
        ]

    def lint(self, source: str) -> List[Dict]:
        """
        Scan the source code and return a list of issues.

        Parameters
        ----------
        source : str
            Φ‑QML source code.

        Returns
        -------
        list of dicts
            Each dict describes one issue: line, severity, message,
            suggestion, estimated Φ debt.
        """
        self.issues = []
        lines = source.split('\n')

        for pattern in self.patterns:
            for match in re.finditer(pattern["regex"], source, re.DOTALL):
                line_no = source[:match.start()].count('\n') + 1

                issue = {
                    "line": line_no,
                    "severity": pattern["severity"],
                    "name": pattern["name"],
                    "message": pattern["message"],
                    "suggestion": pattern["suggestion"],
                    "debt": pattern["debt"],
                }

                # For the missing_cost_annotation, insert the function name
                if pattern["name"] == "missing_cost_annotation":
                    fn_name = match.group(1)
                    issue["message"] = issue["message"].format(name=fn_name)

                self.issues.append(issue)

        # Sort by line number
        self.issues.sort(key=lambda i: i["line"])
        return self.issues

    def get_total_debt(self) -> float:
        """Return the total estimated Φ debt for the scanned code."""
        return sum(issue["debt"] for issue in self.issues)

    def report(self):
        """Print a formatted linter report to the console."""
        print("\n" + "═" * 70)
        print("Φ‑LINTER REPORT")
        print("═" * 70)

        if not self.issues:
            print("  ✅ No issues found – code is elegant!")
            print("═" * 70)
            return

        severity_order = {"error": 0, "warning": 1, "info": 2, "hint": 3}
        sorted_issues = sorted(self.issues, key=lambda i: severity_order.get(i["severity"], 99))

        for issue in sorted_issues:
            icon = {"error": "❌", "warning": "⚠️ ", "info": "ℹ️ ", "hint": "💡"}.get(issue["severity"], "  ")
            print(f"  {icon} Line {issue['line']:3d}: {issue['message']}")
            print(f"     → {issue['suggestion']}")
            print(f"     (Φ debt: {issue['debt']:.2f})")

        print("─" * 70)
        print(f"  Total issues: {len(self.issues)}")
        print(f"  Total Φ debt: {self.get_total_debt():.2f}")
        print(f"  Estimated Φ after fixes: {1.0 / (1.0 + self.get_total_debt()):.3f}")
        print("═" * 70)


# ═══════════════════════════════════════════════════════════════════════════════
# Demonstration
# ═══════════════════════════════��═══════════════════════════════════════════════

def demo_linter():
    """Demonstrate the linter with sample Φ‑QML code."""
    print("╔══════════════════════════════════════════════════════════════════════════╗")
    print("║  Φ‑LINTER — Code Quality & Elegance Checker                           ║")
    print("╚══════════════════════════════════════════════════════════════════════════╝\n")

    # Sample Φ‑QML code with several anti‑patterns
    sample_code = """
fn find(array, target) {
    for item in array {
        if item == target {
            return item;
        }
    }
    return -1;
}

fn process_data(data) {
    let mut counter = 0;
    while counter < 100 {
        let x = data[counter];
        counter = counter + 1;
    }
    return counter % 997;
}

fn fib(n) {
    if n <= 1 {
        return n;
    }
    return fib(n-1) + fib(n-2);
}
"""

    print("📝 Analyzing sample code:")
    print("─" * 60)
    for i, line in enumerate(sample_code.strip().split('\n'), 1):
        print(f"  {i:2d}: {line}")
    print("─" * 60)

    linter = PhiLinter()
    issues = linter.lint(sample_code)
    linter.report()

    print(f"\n[Φ] Linter demonstration complete.")


if __name__ == "__main__":
    demo_linter()
