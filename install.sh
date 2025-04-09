#!/bin/bash
set -euo pipefail

echo "Setting up Nova ACT development environment..."

# Install package in development mode
python -m pip install -e .

echo "Development setup complete"