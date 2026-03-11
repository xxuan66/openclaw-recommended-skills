#!/bin/bash

# 微信公众号每日内容生成脚本
# 功能：生成当日文章内容 + 封面图片 prompt

set -e

# ==================== 配置区域 ====================
CONTENT_DIR="/home/admin/.openclaw/workspace/wechat_articles"
OUTPUT_DIR="/home/admin/.openclaw/workspace/wechat_daily"
DATE=$(date +%Y-%m-%d)
DAY_OF_WEEK=$(date +%u)  # 1=Monday, 7=Sunday

# ==================== 内容规划 ====================
# 星期几对应主题
declare -A WEEKLY_THEMES=(
  [1]="Skill 推荐"
  [2]="使用技巧"
  [3]="场景案例"
  [4]="开发工具"
  [5]="本周总结"
  [6]="用户问答"
  [7]="精选合集"
)

# ==================== 函数定义 ====================

# 生成封面 prompt
generate_cover_prompt() {
  local theme="$1"
  local title="$2"
  
  cat << EOF
请帮我生成一张微信公众号封面图片

【尺寸要求】
- 宽度：900 像素
- 高度：383 像素
- 比例：2.35:1（横版长图）

【设计风格】
- 现代科技感
- 渐变色背景
- 简洁大气
- 适合技术类文章

【背景】
- 使用紫色到蓝色的渐变色
- 从左上角 #667eea 渐变到右下角 #764ba2
- 或者类似的科技蓝/紫色渐变

【文字内容】
主标题：$title
副标题：OpenClaw 每日分享
日期：$DATE

【文字样式】
- 主标题：白色，粗体，字号大，居中显示
- 副标题：白色或浅色，字号中等，在主标题下方
- 日期：浅灰色或白色半透明，字号小，放在底部

【装饰元素】
- 可以添加一些科技感的线条或光点
- 或者简单的几何图形装饰
- 保持简洁，不要过于复杂

【整体感觉】
- 专业
- 科技感
- 清晰易读
- 适合技术博客/教程类文章

【输出格式】
- JPG 或 PNG
- 质量高
- 文件大小 < 2MB
EOF
}

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 获取今日主题
THEME="${WEEKLY_THEMES[$DAY_OF_WEEK]}"

echo "📅 日期：$DATE"
echo "🎯 主题：$THEME"
echo ""

# 根据主题生成内容
case $DAY_OF_WEEK in
  1)  # 周一 - Skill 推荐
    TITLE="本周推荐 Skill"
    echo "📝 生成 Skill 推荐内容..."
    ;;
  2)  # 周二 - 使用技巧
    TITLE="OpenClaw 使用技巧"
    echo "📝 生成使用技巧内容..."
    ;;
  3)  # 周三 - 场景案例
    TITLE="自动化实战案例"
    echo "📝 生成场景案例内容..."
    ;;
  4)  # 周四 - 开发工具
    TITLE="开发者工具推荐"
    echo "📝 生成开发工具内容..."
    ;;
  5)  # 周五 - 本周总结
    TITLE="本周更新总结"
    echo "📝 生成本周总结内容..."
    ;;
  6)  # 周六 - 用户问答
    TITLE="常见问题解答"
    echo "📝 生成用户问答内容..."
    ;;
  7)  # 周日 - 精选合集
    TITLE="本周精选合集"
    echo "📝 生成精选合集内容..."
    ;;
esac

# 生成封面 prompt 文件
generate_cover_prompt "$TITLE" > "$OUTPUT_DIR/cover_prompt_${DATE}.txt"
echo "✅ 封面 prompt 已生成：$OUTPUT_DIR/cover_prompt_${DATE}.txt"

# 显示 prompt
echo ""
echo "🎨 封面图片生成提示词："
echo "================================"
cat "$OUTPUT_DIR/cover_prompt_${DATE}.txt"
echo "================================"
echo ""
echo "📌 下一步："
echo "1. 复制上面的 prompt 给豆包生成封面"
echo "2. 上传封面到公众号素材库"
echo "3. 获取 media_id"
echo "4. 运行发布脚本"
