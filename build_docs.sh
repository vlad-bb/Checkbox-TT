#!/bin/bash
# Documentation build script

set -e

echo "Building Sphinx documentation..."

# Ensure we're in the docs directory
cd "$(dirname "$0")/docs"

# Clean previous build
make clean

# Build HTML documentation
make html

echo "Documentation built successfully!"
echo "Open docs/_build/html/index.html to view the documentation"