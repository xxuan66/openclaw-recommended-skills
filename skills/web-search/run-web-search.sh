#!/bin/sh
# 网页搜索 & 分析技能启动脚本

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/.."

# 检查 SearXNG 配置
if [ -z "$SEARXNG_URL" ]; then
    echo "⚠️  提示：未设置 SEARXNG_URL"
    echo "   将使用默认值：http://localhost:8080"
    echo "   确保 SearXNG 服务已启动"
    echo ""
fi

uv run scripts/web-search.py "$@"
