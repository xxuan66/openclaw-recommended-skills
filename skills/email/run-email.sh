#!/bin/sh
# 邮件管理技能启动脚本

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/.."

# 检查配置
if [ -z "$EMAIL_ADDRESS" ] || [ -z "$EMAIL_PASSWORD" ]; then
    echo "⚠️  警告：未配置邮箱凭证"
    echo "   请设置 EMAIL_ADDRESS 和 EMAIL_PASSWORD 环境变量"
    echo "   或使用飞书邮件 API"
    echo ""
fi

uv run scripts/email.py "$@"
