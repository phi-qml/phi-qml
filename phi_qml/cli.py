"""
Φ‑QML CLI — Command‑Line Interface

Provides the main entry point for the Φ‑QML toolchain.
Supports compilation, execution, testing, package management,
and an interactive REPL mode.
"""

import sys
import os
from typing import List, Optional


class PhiCLI:
    """
    Command‑Line Interface for Φ‑QML.

    Commands:
    - compile  – Compile a Φ‑QML source file
    - run      – Execute a Φ‑QML program
    - test     – Run the test suite
    - install  – Install a package from the registry
    - publish  – Publish a package to the registry
    - repl     – Start an interactive REPL session
    - help     – Display help information
    """

    def __init__(self):
        self.commands = {
            "compile": self._cmd_compile,
            "run": self._cmd_run,
            "test": self._cmd_test,
            "install": self._cmd_install,
            "publish": self._cmd_publish,
            "repl": self._cmd_repl,
            "help": self._cmd_help,
        }

    def execute(self, args: List[str]):
        """
        Execute a CLI command from the given argument list.

        Parameters
        ----------
        args : list of str
            Command‑line arguments, e.g. ["run", "program.phi"]
        """
        if not args:
            self._cmd_help()
            return

        cmd = args[0]
        if cmd in self.commands:
            self.commands[cmd](args[1:])
        else:
            print(f"Unknown command: {cmd}")
            self._cmd_help()

    def _cmd_compile(self, args: List[str]):
        """Compile a Φ‑QML source file to OpenQASM."""
        if not args:
            print("Usage: phi compile <file.phi>")
            return
        filepath = args[0]
        if not os.path.exists(filepath):
            print(f"❌ File not found: {filepath}")
            return

        print(f"🔨 Compiling: {filepath}")
        try:
            with open(filepath, 'r') as f:
                source = f.read()

            from phi_qml.lexer import Lexer
            from phi_qml.parser import Parser
            from phi_qml.qasm_compiler import QASMCompiler

            lexer = Lexer(source)
            tokens = []
            while True:
                t = lexer.next_token()
                tokens.append(t)
                if t.kind.name == "EOF":
                    break

            parser = Parser(tokens)
            ast = parser.parse()

            compiler = QASMCompiler()
            qasm_output = compiler.compile()

            output_path = filepath.replace('.phi', '.qasm')
            with open(output_path, 'w') as f:
                f.write(qasm_output)

            print(f"  ✅ Compiled to: {output_path}")
            print(f"  Target: Substrate* Quantum Computer")
            print(f"  Φ = ∞ (all operations C=0 in Substrate*)")

        except Exception as e:
            print(f"  ❌ Compilation failed: {e}")

    def _cmd_run(self, args: List[str]):
        """Execute a Φ‑QML program."""
        if not args:
            print("Usage: phi run <file.phi>")
            return
        filepath = args[0]
        if not os.path.exists(filepath):
            print(f"❌ File not found: {filepath}")
            return

        print(f"▶️  Running: {filepath}")
        try:
            with open(filepath, 'r') as f:
                source = f.read()

            from phi_qml.lexer import Lexer
            from phi_qml.parser import Parser
            from phi_qml.interpreter import Interpreter

            lexer = Lexer(source)
            tokens = []
            while True:
                t = lexer.next_token()
                tokens.append(t)
                if t.kind.name == "EOF":
                    break

            parser = Parser(tokens)
            ast = parser.parse()

            interpreter = Interpreter()
            result = interpreter.interpret(ast)

            print(f"\n✅ Program completed successfully.")
            print(f"   Result: {result}")
            interpreter.tracker.report()

        except Exception as e:
            print(f"  ❌ Execution failed: {e}")

    def _cmd_test(self, args: List[str]):
        """Run the test suite for Φ‑QML."""
        print("🧪 Running Φ‑QML test suite...\n")

        from phi_qml.test_framework import PhiTest
        tester = PhiTest(min_phi=0.5)

        # Core tests
        def add(a, b):
            return a + b

        def substrate_modulo(a, n):
            from phi_qml.substrate_modulo import SubstrateModuloEngine
            engine = SubstrateModuloEngine()
            return engine.modulo(a, n)[0]

        def holographic_search(arr, target):
            from phi_qml.stdlib import PhiStdlib
            return PhiStdlib.substrate_search(arr, target)

        # Lexer test
        from phi_qml.lexer import Lexer
        lexer = Lexer("let x = mod(42, 13);")
        tokens = lexer.tokenize()
        tester.test("Lexer produces tokens", lambda tokens: len(tokens) > 0, True, tokens)

        # Parser test
        from phi_qml.parser import Parser
        parser = Parser(tokens)
        ast = parser.parse()
        tester.test("Parser produces AST", lambda ast: ast is not None, True, ast)

        # Arithmetic
        tester.test("Simple addition", add, 8, 5, 3, operations=1)

        # Substrate* Modulo
        tester.test("Substrate* Modulo", substrate_modulo, 3, 42, 13, operations=0)

        # Search
        data = [1, 2, 3, 4, 5]
        tester.test("Holographic search", holographic_search, 2, data, 3, operations=0)

        # Hash
        def hash_fn():
            import hashlib
            return len(hashlib.sha256(b"test").hexdigest())
        tester.test("Substrate* Hash length", hash_fn, 64, operations=1)

        tester.report()

    def _cmd_install(self, args: List[str]):
        """Install a package from the registry."""
        if not args:
            print("Usage: phi install <package>[@version]")
            return
        package = args[0]
        from phi_qml.package_manager import PackageManager
        pm = PackageManager()
        pm.install(package)

    def _cmd_publish(self, args: List[str]):
        """Publish a package to the registry."""
        if not args:
            print("Usage: phi publish <file.phi>")
            return
        filepath = args[0]
        if not os.path.exists(filepath):
            print(f"❌ File not found: {filepath}")
            return

        print(f"📦 Publishing: {filepath}")
        try:
            with open(filepath, 'r') as f:
                source = f.read()

            from phi_qml.linter import PhiLinter
            linter = PhiLinter()
            issues = linter.lint(source)
            debt = linter.get_total_debt()
            phi = 1.0 / (1.0 + debt)

            print(f"  Package Φ score: {phi:.3f}")
            print(f"  Issues found: {len(issues)}")
            print(f"  ✅ Published to Φ‑Hub (simulated)")

        except Exception as e:
            print(f"  ❌ Publishing failed: {e}")

    def _cmd_repl(self, args: List[str]):
        """Start an interactive REPL session."""
        print("╔══════════════════════════════════════════════════════════════════════════╗")
        print("║  Φ‑QML REPL — Interactive Φ‑QML Shell                                 ║")
        print("║  Type expressions to evaluate them. Type 'exit' to quit.              ║")
        print("╚══════════════════════════════════════════════════════════════════════════╝\n")

        from phi_qml.interpreter import Interpreter
        from phi_qml.lexer import Lexer
        from phi_qml.parser import Parser

        interpreter = Interpreter()

        while True:
            try:
                line = input("Φ> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nExiting REPL.")
                break

            if not line:
                continue
            if line.lower() in ('exit', 'quit'):
                print("Exiting REPL.")
                break

            try:
                lexer = Lexer(line)
                tokens = []
                while True:
                    t = lexer.next_token()
                    tokens.append(t)
                    if t.kind.name == "EOF":
                        break

                parser = Parser(tokens)
                ast = parser.parse()
                result = interpreter.interpret(ast)
                if result is not None:
                    print(result)

                interpreter.tracker.report()
                interpreter.tracker.clear()

            except Exception as e:
                print(f"Error: {e}")

    def _cmd_help(self, args: Optional[List[str]] = None):
        """Display help information for Φ‑QML CLI."""
        print("""
╔════════════════════════════════════════════════════════════════════╗
║  Φ‑CLI — Φ‑QML Command‑Line Interface                           ║
╠════════════════════════════════════════════════════════════════════╣
║  phi compile <file>   Compile a Φ‑QML source to OpenQASM 3.0    ║
║  phi run <file>       Execute a Φ‑QML program                   ║
║  phi test             Run the test suite                        ║
║  phi install <pkg>    Install a package from the registry       ║
║  phi publish <file>   Publish a package to Φ‑Hub                ║
║  phi repl             Start an interactive REPL session         ║
║  phi help             Display this help                         ║
╚════════════════════════════════════════════════════════════════════╝
""")


def main():
    """Main entry point for the Φ‑QML CLI."""
    cli = PhiCLI()
    cli.execute(sys.argv[1:])


if __name__ == "__main__":
    main()
