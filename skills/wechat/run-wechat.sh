#!/bin/sh
# 微信公众号技能启动脚本

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/.."

# 检查配置
if [ -z "$WECHAT_APP_ID" ] || [ -z "$WECHAT_APP_SECRET" ]; then
    echo "⚠️  警告：未配置微信公众号凭证"
    echo "   请设置 WECHAT_APP_ID 和 WECHAT_APP_SECRET 环境变量"
    echo ""
fi

# 运行脚本
uv run scripts/wechat.py "$@"
