#!/bin/sh
# AI 文本人性化技能启动脚本

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/.."

uv run scripts/humanizer.py "$@"
