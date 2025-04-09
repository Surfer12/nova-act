#!/bin/bash
set -euo pipefail

# Run nova-act in sync mode with pixi
PYTHONASYNCIODEBUG=0 exec pixi run python -m nova_act.cli.main --config config.json "$@"