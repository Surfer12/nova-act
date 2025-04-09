#!/bin/bash
set -euo pipefail

# Check if pixi is installed
if ! command -v pixi &>/dev/null; then
    echo "Error: pixi is not installed. Please install pixi first."
    exit 1
fi

# Check if config file exists
if [ ! -f "config.json" ]; then
    echo "Error: config.json not found"
    exit 1
fi

# Run nova-act in async mode with pixi
PYTHONASYNCIODEBUG=1 exec pixi run python -m nova_act.cli.main --config config.json --async "$@"