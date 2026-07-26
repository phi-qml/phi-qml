#!/usr/bin/env python3
"""
Φ‑QML Setup — Substrate*‑Native Quantum Meta‑Language
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="phi-qml",
    version="1.0.0",
    author="Φ‑QML Contributors",
    description="Substrate*‑Native Quantum Programming Language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/phi-qml/phi-qml",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Software Development :: Compilers",
        "Topic :: Software Development :: Interpreters",
    ],
    python_requires=">=3.10",
    install_requires=[
        "numpy>=1.24.0",
        "scipy>=1.10.0",
    ],
    extras_require={
        "visualization": ["matplotlib>=3.7.0"],
        "web": ["flask>=2.3.0"],
        "tensor": ["quimb>=1.4.0"],
    },
    entry_points={
        "console_scripts": [
            "phi=phi_qml.cli:main",
        ],
    },
)
