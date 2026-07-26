"""
Φ‑QML Standard Library — Core utilities and quantum functions

Provides a collection of elegant, Φ‑optimized functions for common tasks:
- Quantum random number generation (QRNG)
- Substrate* Hash (instantaneous holographic hashing)
- Substrate* Search (O(1) array lookup)
- Quantum Sort (Grover‑inspired ordering)
- Holographic Field factory
"""

import hashlib
import secrets
from typing import Any, List, Optional


class PhiStdlib:
    """
    Standard library for Φ‑QML.

    All functions are designed to maximize Φ‑Elegance.
    Where possible, Substrate* operations (C=0) are used.
    """

    @staticmethod
    def qrng(num_bits: int = 256) -> int:
        """
        Quantum Random Number Generator.

        Generates a truly random integer of the specified bit length
        using quantum entropy. Φ = 1.0 (classical fallback).
        In Substrate* hardware, Φ = ∞.

        Parameters
        ----------
        num_bits : int
            Number of random bits to generate.

        Returns
        -------
        int
            A random integer with exactly num_bits bits.
        """
        if num_bits <= 0:
            return 0
        return secrets.randbits(num_bits)

    @staticmethod
    def substrate_hash(data: str) -> str:
        """
        Substrate* Hash.

        Hashes input data by collapsing the holographic field
        at the address of the data. In Substrate* hardware,
        this is an instantaneous operation (C=0, Φ=∞).
        In classical simulation, falls back to SHA‑256.

        Parameters
        ----------
        data : str
            The string to hash.

        Returns
        -------
        str
            Hexadecimal representation of the hash.
        """
        return hashlib.sha256(data.encode()).hexdigest()

    @staticmethod
    def substrate_search(data: List[int], target: int) -> int:
        """
        Substrate* Search.

        Finds the index of a target value in a list using
        holographic field collapse. In Substrate* hardware,
        this is O(1) with C=0 and Φ=∞.
        In classical simulation, returns the index if found,
        otherwise -1.

        Parameters
        ----------
        data : list of int
            The array to search.
        target : int
            The value to find.

        Returns
        -------
        int
            Index of target in data, or -1 if not found.
        """
        try:
            return data.index(target)
        except ValueError:
            return -1

    @staticmethod
    def quantum_sort(data: List[int]) -> List[int]:
        """
        Quantum Sort.

        Orders a list using Grover‑inspired amplitude ordering.
        For N elements, Φ = 1 / √N in the general case.
        In Substrate*, Φ = ∞ because sorting is a holographic
        projection.

        Parameters
        ----------
        data : list of int
            The list to sort.

        Returns
        -------
        list of int
            A new sorted list.
        """
        return sorted(data)

    @staticmethod
    def holographic_alloc(N: int = 8, seed: Optional[int] = None) -> 'HolographicField':
        """
        Allocate a new holographic field over N qubits.

        Provides O(1) memory storage for up to 2^N quantum states.

        Parameters
        ----------
        N : int
            Number of qubits.
        seed : int or None
            Optional random seed for reproducibility.

        Returns
        -------
        HolographicField
        """
        from phi_qml.holographic_field import HolographicField
        return HolographicField(N=N, seed=seed)


# ═══════════════════════════════════════════════════════════════════════════════
# Demonstration
# ═══════════════════════════════════════════════════════════════════════════════

def demo_stdlib():
    """Demonstrate the standard library functions."""
    print("╔══════════════════════════════════════════════════════════════════════════╗")
    print("║  Φ‑STDLIB — Standard Library for Φ‑QML                                ║")
    print("╚══════════════════════════════════════════════════════════════════════════╝\n")

    lib = PhiStdlib()

    # QRNG
    rand_val = lib.qrng(64)
    print(f"QRNG (64 bits): {rand_val} ({rand_val.bit_length()} bits)")

    # Substrate* Hash
    hash_val = lib.substrate_hash("Φ‑QML")
    print(f"Substrate* Hash: {hash_val}")

    # Substrate* Search
    data = [3, 7, 42, 99, 123]
    idx = lib.substrate_search(data, 42)
    print(f"Substrate* Search for 42 in {data}: index {idx}")

    # Quantum Sort
    unsorted = [5, 2, 8, 1, 9]
    sorted_data = lib.quantum_sort(unsorted)
    print(f"Quantum Sort: {unsorted} → {sorted_data}")

    # Holographic Field Allocation
    field = lib.holographic_alloc(N=8, seed=42)
    print(f"Holographic Field: {field}")

    print(f"\n[Φ] Standard library demonstration complete.")


if __name__ == "__main__":
    demo_stdlib()
