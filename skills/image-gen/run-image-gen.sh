#!/bin/sh
# AI 图片生成技能启动脚本

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/.."

# 检查配置
if [ -z "$IMAGE_GEN_API_KEY" ]; then
    echo "⚠️  警告：未配置 AI 绘图 API 密钥"
    echo "   请设置 IMAGE_GEN_API_KEY 环境变量"
    echo "   支持：通义万相、Stable Diffusion、DALL-E 等"
    echo ""
fi

uv run scripts/image-gen.py "$@"
