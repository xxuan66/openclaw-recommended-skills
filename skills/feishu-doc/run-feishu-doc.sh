#!/bin/sh
# 飞书文档技能启动脚本

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/.."

# 检查配置
if [ -z "$FEISHU_APP_ID" ] || [ -z "$FEISHU_APP_SECRET" ]; then
    echo "⚠️  警告：未配置飞书开放平台凭证"
    echo "   请设置 FEISHU_APP_ID 和 FEISHU_APP_SECRET 环境变量"
    echo ""
fi

uv run scripts/feishu-doc.py "$@"
