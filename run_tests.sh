#!/bin/bash
set -euo pipefail

# Install package in development mode
pip install -e .

# Install test dependencies
pip install -r requirements-test.txt

# Run tests with coverage
pytest \
    --cov=nova_act \
    --cov-report=html \
    --cov-report=term-missing \
    --cov-report=xml \
    tests/