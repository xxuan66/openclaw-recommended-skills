#!/bin/sh
# Mify LLM API 技能启动脚本

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/.."

# 检查配置
if [ -z "$MIFY_API_KEY" ]; then
    echo "⚠️  警告：未配置 MIFY_API_KEY"
    echo "   请设置环境变量：export MIFY_API_KEY='your-api-key'"
    echo ""
fi

echo "🤖 Mify LLM API"
echo "   Base URL: ${MIFY_BASE_URL:-http://model.mify.ai.srv/v1}"
echo ""

uv run scripts/mify-llm.py "$@"
