#!/bin/sh
# 博客写手技能启动脚本

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/.."

# 检查配置
if [ -z "$BLOG_API_URL" ] || [ -z "$BLOG_API_KEY" ]; then
    echo "⚠️  警告：未配置博客平台凭证"
    echo "   请设置 BLOG_API_URL 和 BLOG_API_KEY 环境变量"
    echo ""
fi

uv run scripts/blog-writer.py "$@"
