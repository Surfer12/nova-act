#!/bin/bash

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

# Print location of coverage reports
echo "Coverage HTML report generated in htmlcov/index.html"
echo "Coverage XML report generated in coverage.xml"