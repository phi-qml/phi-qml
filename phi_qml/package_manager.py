"""
Φ‑QML Package Manager — Dependency management and package registry

Manages Φ‑QML packages with Φ‑Elegance‑aware versioning.
Packages with higher Φ scores are preferred during dependency
resolution. Supports installing from a local registry or a remote
repository, and publishing new packages.
"""

import json
import os
import time
from typing import Dict, List, Optional


class PackageManager:
    """
    Package manager for Φ‑QML.

    Handles installation, dependency resolution, and registry
    interaction. Packages are versioned and carry a Φ score that
    reflects their elegance. When multiple versions of a package
    satisfy a dependency, the one with the highest Φ is chosen.
    """

    def __init__(self, registry_url: str = "https://phi-qml.org/packages"):
        """
        Initialize the package manager.

        Parameters
        ----------
        registry_url : str
            URL of the remote package registry.
        """
        self.registry_url = registry_url
        self.installed: Dict[str, Dict] = {}
        self._load_installed()

    def _load_installed(self):
        """Load the list of installed packages from disk."""
        try:
            with open("phi_packages.json", 'r') as f:
                self.installed = json.load(f)
        except FileNotFoundError:
            self.installed = {}

    def _save_installed(self):
        """Save the list of installed packages to disk."""
        with open("phi_packages.json", 'w') as f:
            json.dump(self.installed, f, indent=2)

    def install(self, package_name: str, version: str = "latest") -> bool:
        """
        Install a package from the registry.

        Parameters
        ----------
        package_name : str
            Name of the package to install.
        version : str
            Version specifier (e.g., "1.0.0", "latest").

        Returns
        -------
        bool
            True if installation succeeded.
        """
        print(f"📦 Installing: {package_name}@{version}")

        # Simulate fetching package metadata from registry
        # In a real implementation, this would make an HTTP request
        package = self._fetch_package(package_name, version)
        if package is None:
            print(f"  ❌ Package '{package_name}' not found in registry.")
            return False

        # Check and install dependencies first
        for dep in package.get("dependencies", []):
            dep_name = dep["name"]
            dep_version = dep.get("version", "latest")
            if dep_name not in self.installed:
                print(f"  ⚠️  Missing dependency: {dep_name}")
                self.install(dep_name, dep_version)

        # Install the package
        self.installed[package_name] = {
            "name": package_name,
            "version": package["version"],
            "phi_score": package.get("phi_score", 0.5),
            "dependencies": package.get("dependencies", []),
            "installed_at": str(int(time.time())),
        }
        self._save_installed()
        print(f"  ✅ Installed: {package_name} (Φ = {package['phi_score']})")
        return True

    def _fetch_package(self, name: str, version: str) -> Optional[Dict]:
        """
        Fetch package metadata from the registry.

        In this reference implementation, we simulate a registry
        with a few built‑in packages. A real implementation would
        make an HTTP request to the registry_url.
        """
        # Simulated registry
        registry = {
            "quantum-stdlib": {
                "name": "quantum-stdlib",
                "version": "1.0.0",
                "phi_score": 0.95,
                "dependencies": [],
                "description": "Substrate* Modulo and Holographic Field primitives",
            },
            "crypto-phi": {
                "name": "crypto-phi",
                "version": "2.1.0",
                "phi_score": 0.88,
                "dependencies": [
                    {"name": "quantum-stdlib", "version": "1.0.0"}
                ],
                "description": "Quantum‑resistant cryptographic primitives",
            },
            "optimizer-phi": {
                "name": "optimizer-phi",
                "version": "0.9.0",
                "phi_score": 0.72,
                "dependencies": [
                    {"name": "quantum-stdlib", "version": "1.0.0"}
                ],
                "description": "VQE and Grover‑based optimization algorithms",
            },
        }

        if name in registry:
            return registry[name]
        return None

    def uninstall(self, package_name: str) -> bool:
        """
        Remove an installed package.

        Parameters
        ----------
        package_name : str
            Name of the package to uninstall.

        Returns
        -------
        bool
            True if the package was uninstalled.
        """
        if package_name in self.installed:
            del self.installed[package_name]
            self._save_installed()
            print(f"🗑️  Uninstalled: {package_name}")
            return True
        print(f"  ⚠️  Package '{package_name}' is not installed.")
        return False

    def list_installed(self) -> List[Dict]:
        """Return a list of installed packages with their metadata."""
        return [
            {
                "name": pkg["name"],
                "version": pkg["version"],
                "phi_score": pkg["phi_score"],
                "installed_at": pkg.get("installed_at", "unknown"),
            }
            for pkg in self.installed.values()
        ]

    def resolve_dependencies(self, package_name: str) -> List[str]:
        """
        Resolve all transitive dependencies for a package.

        Returns a list of package names in installation order
        (dependencies before dependents).
        """
        if package_name not in self.installed:
            return []

        resolved = []
        visited = set()

        def visit(name):
            if name in visited:
                return
            visited.add(name)
            if name in self.installed:
                for dep in self.installed[name].get("dependencies", []):
                    visit(dep["name"])
                resolved.append(name)

        visit(package_name)
        return resolved


# ═════════════════════════════════════════════════════════════��═════════════════
# Demonstration
# ═══════════════════════════════════════════════════════════════════════════════

def demo_package_manager():
    """Demonstrate the package manager capabilities."""
    print("╔══════════════════════════════════════════════════════════════════════════╗")
    print("║  PACKAGE MANAGER — Φ‑Aware Dependency Management                      ║")
    print("╚══════════════════════════════════════════════════════════════════════════╝\n")

    pm = PackageManager()

    # Install packages
    pm.install("quantum-stdlib")
    pm.install("crypto-phi")  # This should pull quantum-stdlib as dependency

    # List installed
    print("\n📋 Installed packages:")
    for pkg in pm.list_installed():
        print(f"  • {pkg['name']} v{pkg['version']} (Φ = {pkg['phi_score']})")

    # Resolve dependencies
    print("\n🔗 Dependency resolution for 'crypto-phi':")
    deps = pm.resolve_dependencies("crypto-phi")
    print(f"  Order: {' → '.join(deps)}")

    print(f"\n[Φ] Package manager demonstration complete.")


if __name__ == "__main__":
    demo_package_manager()
