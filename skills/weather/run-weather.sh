#!/bin/sh
# 天气查询技能启动脚本

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/.."

# 天气查询无需 API 密钥，直接使用 wttr.in 和 Open-Meteo 免费服务
echo "🌤️  天气查询技能 - 无需 API 密钥"
echo "   数据源：wttr.in + Open-Meteo"
echo ""

uv run scripts/weather.py "$@"
