#!/bin/sh
# 基础智能包技能启动脚本

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/.."

echo "🤖 基础智能包技能"
echo "   功能：对话、翻译、摘要、改写、提醒"
echo ""

uv run scripts/basic-ai.py "$@"
