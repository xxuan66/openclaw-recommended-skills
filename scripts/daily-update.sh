#!/bin/bash
# 每日精选自动更新脚本
# 运行时间：每日 08:00

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
DAILY_DIR="$REPO_DIR/daily"
DATE=$(date +%Y-%m-%d)
DAY_COUNT=$(ls -1 "$DAILY_DIR"/20*.md 2>/dev/null | wc -l)
DAY_NUM=$((DAY_COUNT + 1))

echo "========================================"
echo "📅 每日精选自动更新"
echo "========================================"
echo "日期：$DATE"
echo "期数：Day $(printf "%03d" $DAY_NUM)"
echo ""

cd "$REPO_DIR"

# 检查是否已存在今日文件
if [ -f "$DAILY_DIR/$DATE.md" ]; then
    echo "⚠️  今日文件已存在：$DATE.md"
    echo "跳过更新"
    exit 0
fi

# 选择今日 Skill（轮询推荐）
SKILLS=(
    "searxng:隐私保护的本地元搜索引擎"
    "self-improving-agent:让 Agent 越用越聪明"
    "github:GitHub CLI 集成"
    "skill-vetter:Skill 安全审查"
    "tavily-search:AI 优化搜索"
    "summarize:多格式文档摘要"
    "starmemo:结构化记忆"
    "gog:Google Workspace"
    "find-skills:Skill 发现工具"
    "baidu-search:中文搜索"
)

# 根据日期选择 Skill（简单轮询）
DAY_OF_YEAR=$(date +%j)
SKILL_INDEX=$(( (DAY_OF_YEAR - 1) % ${#SKILLS[@]} ))
SKILL_DATA="${SKILLS[$SKILL_INDEX]}"
SKILL_SLUG="${SKILL_DATA%%:*}"
SKILL_DESC="${SKILL_DATA##*:}"

echo "📌 今日推荐：$SKILL_SLUG"
echo "📝 简介：$SKILL_DESC"
echo ""

# 创建每日精选文件
cat > "$DAILY_DIR/$DATE.md" << EOF
# $DATE 今日精选：$SKILL_SLUG

> 📅 **Day $(printf "%03d" $DAY_NUM)** | 每日精选栏目

---

## 🎯 一句话推荐

**$SKILL_DESC**

---

## ⭐ 今日理由

为什么今天推荐 $SKILL_SLUG？

1. **实用性强** - 日常使用频率高
2. **配置简单** - 2 分钟完成安装
3. **完全免费** - 无需 API Key 或配额限制
4. **用户好评** - 社区评分高

---

## 🚀 快速安装

\`\`\`bash
clawhub install $SKILL_SLUG
\`\`\`

**配置时间：** 2 分钟  
**难度：** ⭐ 简单

---

## 💡 使用示例

\`\`\`bash
# 基础使用
openclaw agent -m "使用 $SKILL_SLUG"
\`\`\`

---

## 📖 详细评测

想看更详细的使用报告？

- [每月精选](../monthly/2026-03.md)
- [分类必备](../essentials/)

---

## 📅 明日预告

**明天推荐：** 敬请期待...

---

## 📊 栏目统计

| 指标 | 数值 |
|------|------|
| 累计更新 | Day $(printf "%03d" $DAY_NUM) |
| 本月已推荐 | $DAY_NUM 个 |
| 创刊日期 | 2026-03-13 |

---

**更新时间：** $DATE 08:00  
**维护者：** @xxuan66  
**下期：** $(date -d "tomorrow" +%Y-%m-%d) 08:00
EOF

echo "✅ 创建成功：$DAILY_DIR/$DATE.md"
echo ""

# 更新 daily/README.md 的今日推荐
echo "📝 更新 daily/README.md..."
sed -i "s/\*\*今天推荐：\*\.*/\*\*今天推荐：\*\* [$SKILL_SLUG](./$DATE.md)/" "$DAILY_DIR/README.md"

# 添加并提交
git add "$DAILY_DIR/$DATE.md" "$DAILY_DIR/README.md"
git commit -m "chore(daily): $DATE 每日精选 - $SKILL_SLUG" || echo "⚠️  没有变化需要提交"

echo ""
echo "========================================"
echo "✅ 每日更新完成"
echo "========================================"
