#!/bin/bash
PYTHONASYNCIODEBUG=0 pixi run python -m nova_act.cli.main --config config.json "$@"