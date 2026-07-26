"""
Φ‑QML Debugger — Interactive debugging with Φ‑Elegance insight

Provides a command‑line debugger for Φ‑QML programs. Supports:
- Setting breakpoints on specific lines
- Stepping through code (step into, step over)
- Inspecting variables and their Φ scores
- Examining the state of holographic fields
- Measuring Φ‑Elegance at each executed line
- Displaying the call stack
"""

import re
from typing import Any, Dict, List, Optional, Tuple


class PhiDebugger:
    """
    Interactive debugger for Φ‑QML.

    Allows a developer to pause execution, inspect the quantum
    and classical state of a Φ‑QML program, and observe how
    Φ‑Elegance evolves line by line.
    """

    def __init__(self):
        self.breakpoints: List[int] = []
        self.current_line = 0
        self.variables: Dict[str, Any] = {}
        self.field_states: Dict[int, Dict] = {}  # field_id → state snapshot
        self.call_stack: List[str] = []
        self.phi_history: List[Dict] = []  # (line, phi) per step
        self.watch_expressions: Dict[str, Any] = {}

    # ─── Breakpoint Management ─────────────────────────────────────

    def set_breakpoint(self, line: int):
        """Set a breakpoint at the given line number."""
        if line not in self.breakpoints:
            self.breakpoints.append(line)
            self.breakpoints.sort()
            print(f"🔴 Breakpoint set at line {line}")

    def clear_breakpoint(self, line: int):
        """Remove a breakpoint from the given line number."""
        if line in self.breakpoints:
            self.breakpoints.remove(line)
            print(f"⭕ Breakpoint cleared at line {line}")

    def list_breakpoints(self) -> List[int]:
        """Return all currently set breakpoints."""
        return self.breakpoints

    # ─── Execution Control ────────────────────────────────────────

    def step_into(self):
        """Advance execution by one line (entering function calls)."""
        self.current_line += 1

    def step_over(self):
        """Advance execution by one line (skipping over function calls)."""
        self.current_line += 1

    def continue_execution(self) -> int:
        """
        Run until the next breakpoint or program end.
        Returns the line number where execution stopped.
        """
        # Simulated: find next breakpoint after current line
        for bp in self.breakpoints:
            if bp > self.current_line:
                self.current_line = bp
                return bp
        return -1  # No more breakpoints

    # ─── State Inspection ─────────────────────────────────────────

    def inspect_variable(self, name: str) -> Any:
        """
        Return the current value of a variable.
        Returns a message if the variable is not defined.
        """
        if name in self.variables:
            return self.variables[name]
        return f"Variable '{name}' is not defined"

    def inspect_all_variables(self) -> Dict[str, Any]:
        """Return all currently defined variables."""
        return self.variables

    def inspect_field(self, field_id: int) -> Dict:
        """
        Return the state snapshot of a holographic field.
        """
        if field_id in self.field_states:
            return self.field_states[field_id]
        return {"error": f"Field {field_id} not found"}

    def add_watch(self, expression: str):
        """
        Add a watch expression. The expression is evaluated
        after each step and its value displayed.
        """
        self.watch_expressions[expression] = None

    # ─── Φ‑Elegance at Runtime ────────────────────────────────────

    def get_phi_at_line(self, line: int) -> float:
        """
        Estimate Φ‑Elegance for a specific line.
        In a real implementation, this would be derived from
        the parsed AST; here we simulate with a heuristic
        based on the golden ratio.
        """
        # Simulated: lines with 'mod' or 'collapse' have high Φ
        # Lines with 'for' or 'while' have lower Φ
        import math
        base = 0.5
        if any(kw in str(self.variables) for kw in ['mod', 'collapse']):
            base = 0.95
        phi = base + 0.1 * math.sin(line * 1.618033988749895)
        return min(1.0, max(0.01, phi))

    def record_phi(self, line: int, phi: float):
        """Record the Φ score for a line of code."""
        self.phi_history.append({"line": line, "phi": phi})

    def get_phi_report(self) -> List[Dict]:
        """Return the Φ history for the current session."""
        return self.phi_history

    # ─── Call Stack ───────────────────────────────────────────────

    def push_call(self, function_name: str):
        """Push a function call onto the stack."""
        self.call_stack.append(function_name)

    def pop_call(self):
        """Pop the top function from the stack."""
        if self.call_stack:
            return self.call_stack.pop()
        return None

    def get_call_stack(self) -> List[str]:
        """Return the current call stack."""
        return self.call_stack

    # ─── Debug Session ────────────────────────────────────────────

    def debug_session(self, program: str):
        """
        Run a simulated debugging session on the given source code.

        Parameters
        ----------
        program : str
            Φ‑QML source code to debug.
        """
        print("─" * 60)
        print("Φ‑DEBUG – Interactive Debugging Session")
        print("─" * 60)

        lines = [line.strip() for line in program.strip().split('\n')]
        self.current_line = 1

        for i, line in enumerate(lines, 1):
            # Update variables based on simple pattern matching
            self._simulate_execution(line, i)

            # Check breakpoints
            if i in self.breakpoints:
                phi = self.get_phi_at_line(i)
                self.record_phi(i, phi)
                print(f"\n🔴 Breakpoint at line {i}: {line}")
                print(f"   Φ‑score: {phi:.3f}")
                print(f"   Call stack: {self.call_stack}")
                print(f"   Variables: {self.variables}")
                print(f"   Field states: {list(self.field_states.keys())}")

                # Evaluate watch expressions
                for expr in self.watch_expressions:
                    try:
                        val = eval(expr, {}, self.variables)
                        print(f"   Watch '{expr}': {val}")
                    except Exception:
                        print(f"   Watch '{expr}': <error>")

                user_input = input("   [Enter] step over, 's' step into, 'c' continue, 'q' quit: ").strip().lower()
                if user_input == 'q':
                    print("   ⛔ Debug session terminated.")
                    break
                elif user_input == 'c':
                    next_bp = self.continue_execution()
                    if next_bp < 0:
                        print("   No more breakpoints. Running to end.")
                elif user_input == 's':
                    self.step_into()
                else:
                    self.step_over()

        print("\n✅ Program execution completed.")
        self._print_session_summary()

    def _simulate_execution(self, line: str, line_number: int):
        """
        Simulate executing one line of Φ‑QML code.
        Updates variables and field states based on patterns.
        """
        # let x = value;
        let_match = re.match(r'let\s+(\w+)\s*=\s*(.+);?', line)
        if let_match:
            name = let_match.group(1)
            value_expr = let_match.group(2).rstrip(';')
            # Try to evaluate simple expressions
            try:
                if value_expr.startswith('mod('):
                    # Extract a and n from mod(a, n)
                    args = value_expr[4:-1].split(',')
                    if len(args) == 2:
                        a = int(args[0].strip())
                        n = int(args[1].strip())
                        self.variables[name] = a % n
                elif value_expr.isdigit():
                    self.variables[name] = int(value_expr)
                else:
                    self.variables[name] = value_expr
            except Exception:
                self.variables[name] = value_expr

        # fn name(...) { – push to call stack
        fn_match = re.match(r'fn\s+(\w+)', line)
        if fn_match:
            self.push_call(fn_match.group(1))

        # } – pop from call stack
        if line == '}':
            self.pop_call()

    def _print_session_summary(self):
        """Print a summary of the debugging session."""
        print("\n" + "─" * 60)
        print("DEBUG SESSION SUMMARY")
        print("─" * 60)
        if self.phi_history:
            avg_phi = sum(e["phi"] for e in self.phi_history) / len(self.phi_history)
            print(f"  Lines executed with Φ tracking: {len(self.phi_history)}")
            print(f"  Average Φ: {avg_phi:.3f}")
            best = max(self.phi_history, key=lambda e: e["phi"])
            worst = min(self.phi_history, key=lambda e: e["phi"])
            print(f"  Best line: {best['line']} (Φ = {best['phi']:.3f})")
            print(f"  Worst line: {worst['line']} (Φ = {worst['phi']:.3f})")
        print("─" * 60)


# ═══════════════════════════════════════════════════════════════════════════════
# Demonstration
# ═══════════════════════════════════════════════════════════════════════════════

def demo_debugger():
    """Demonstrate the debugger with a sample program."""
    print("╔══════════════════════════════════════════════════════════════════════════╗")
    print("║  Φ‑DEBUGGER — Interactive Debugging with Φ‑Elegance                  ║")
    print("╚══════════════════════════════════════════════════════════════════════════╝\n")

    debugger = PhiDebugger()
    debugger.set_breakpoint(3)
    debugger.set_breakpoint(6)

    sample_program = """
fn main() {
    let a = 42;
    let r = mod(a, 13);
    println(r);
    let found = false;
    while !found {
        found = true;
    }
}
"""
    debugger.debug_session(sample_program)

    print(f"\n[Φ] Debugger demonstration complete.")


if __name__ == "__main__":
    demo_debugger()
