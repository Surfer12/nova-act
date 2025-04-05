#!/usr/bin/env python3
"""Test script to verify Nova Act package requirements."""

import os
import sys

print("\n=====================================================")
print("             NOVA ACT COMPATIBILITY CHECK             ")
print("=====================================================\n")

print(f"Python version: {sys.version}")
print(f"Python version info: {sys.version_info}")

if sys.version_info < (3, 10):
    print("\n⚠️ WARNING: INCOMPATIBLE PYTHON VERSION ⚠️")
    print("Nova Act requires Python 3.10 or higher.")
    print("This is because the package uses the union type operator (|) extensively,")
    print("which was introduced in Python 3.10.")
    print("\nTo use Nova Act, you need to:")
    print("1. Install Python 3.10 or higher")
    print("2. Create a virtual environment with that Python version")
    print("3. Install the package in that environment with 'pip install -e .'")
    print("\nAlternatively, you could modify all type annotations in the codebase")
    print("to use Union from typing instead of the | operator, but this would be")
    print("a significant undertaking.")
else:
    print("\n✅ Python version is compatible with Nova Act.")
    print("You can install the package with 'pip install -e .'")

print("\n=====================================================\n") 