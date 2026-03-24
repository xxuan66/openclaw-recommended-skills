#!/bin/bash
# 每日精选栏目自动更新脚本
# 使用方式：bash update-daily-readme.sh "skill_name" "一句话描述"

set -e

DAILY_DIR="/home/admin/.openclaw/workspace/projects/github-repos/openclaw-recommended-skills/daily"
TODAY=$(date +%Y-%m-%d)
DAY_NUM=$(($(date -d "$TODAY" +%j) - $(date -d "2026-03-13" +%j) + 1))

SKILL_NAME="${1:-searxng}"
SKILL_DESC="${2:-隐私保护的本地元搜索引擎}"

echo "📅 更新每日精选 README - $TODAY (Day $DAY_NUM)"

# 更新 daily/README.md 中的今日精选部分
cd "$DAILY_DIR"

# 备份原文件
cp README.md README.md.bak

# 更新"今日精选"部分
sed -i "s/\*\*今天推荐：\*\* .*/\*\*今天推荐：\*\* [$SKILL_NAME](./$TODAY.md)/" README.md

# 更新描述（在"> "开头的行）
sed -i "s/^> .*/> $SKILL_DESC/" README.md

# 更新累计更新天数
sed -i "s/\*\*累计更新：\*\* Day .*/\*\*累计更新：\*\* Day $DAY_NUM/" README.md

# 更新最后更新日期
sed -i "s/\*\*最后更新：\*\* .*/\*\*最后更新：\*\* $TODAY 08:00/" README.md

echo "✅ daily/README.md 更新完成"
echo ""
echo "今日推荐：$SKILL_NAME"
echo "描述：$SKILL_DESC"
echo "天数：Day $DAY_NUM"
