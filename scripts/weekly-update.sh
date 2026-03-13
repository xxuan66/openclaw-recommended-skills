#!/bin/bash
# 每周热门自动更新脚本
# 运行时间：每周一 08:00

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
WEEKLY_DIR="$REPO_DIR/weekly"
WEEK_NUM=$(date +%Y-W%W)
PREV_WEEK=$(date -d "last week" +%Y-W%W)

echo "========================================"
echo "📆 每周热门自动更新"
echo "========================================"
echo "周次：$WEEK_NUM"
echo ""

cd "$REPO_DIR"

# 检查是否已存在本周文件
if [ -f "$WEEKLY_DIR/$WEEK_NUM.md" ]; then
    echo "⚠️  本周文件已存在：$WEEK_NUM.md"
    echo "跳过更新"
    exit 0
fi

# 获取本周日期范围
WEEK_START=$(date -d "monday this week" +%Y-%m-%d)
WEEK_END=$(date -d "sunday this week" +%Y-%m-%d)

echo "📅 统计周期：$WEEK_START ~ $WEEK_END"
echo ""

# 创建每周热门文件
cat > "$WEEKLY_DIR/$WEEK_NUM.md" << EOF
# $WEEK_NUM 每周热门 Top 10

> 📅 统计周期：$WEEK_START ~ $WEEK_END

---

## 📊 本周数据

| 指标 | 数值 | 环比 |
|------|------|------|
| **总安装量** | 待统计 | - |
| **页面访问** | 待统计 | - |
| **独立访客** | 待统计 | - |
| **新增 Skill** | - | - |

---

## 🏆 Top 10 榜单

| 排名 | Skill | 热度 | 一周理由 | 安装 |
|------|-------|------|---------|------|
| 1 | **self-improving-agent** | 🔥🔥🔥 | 复利效应，越用越聪明 | \`clawhub install self-improving-agent\` |
| 2 | **searxng** | 🔥🔥🔥 | 隐私搜索刚需 | \`clawhub install searxng\` |
| 3 | **github** | 🔥🔥 | GitHub 用户必备 | \`clawhub install github\` |
| 4 | **skill-vetter** | 🔥🔥 | 安全检查员 | \`clawhub install skill-vetter\` |
| 5 | **tavily-search** | 🔥🔥 | AI 优化搜索 | \`clawhub install tavily-search\` |
| 6 | **summarize** | 🔥 | 多格式文档摘要 | \`clawhub install summarize\` |
| 7 | **starmemo** | 🔥 | 结构化记忆 | \`clawhub install starmemo\` |
| 8 | **gog** | 🔥 | Google Workspace | \`clawhub install gog\` |
| 9 | **find-skills** | 🔥 | Skill 发现工具 | \`clawhub install find-skills\` |
| 10 | **baidu-search** | 🔥 | 中文搜索 | \`clawhub install baidu-search\` |

---

## 📈 新上榜

> 暂无新上榜

---

## 📉 下降

> 暂无下降

---

## 💡 本周洞察

1. **学习类 Skill 最受欢迎** - self-improving-agent 持续领先
2. **搜索类需求稳定** - 多个搜索 Skill 上榜
3. **安全意识提升** - skill-vetter 进入前 5

---

## 🎯 下周预告

**${WEEK_NUM}**（待计算）

- 📊 更新环比数据
- 📈 追踪增长趋势
- 🔥 发现新热门

---

## 📖 深度阅读

- [每日精选](../daily/) - 每天了解一个 Skill
- [每月精选](../monthly/) - 深度评测 Top 10
- [分类必备](../essentials/) - 按场景找 Skill

---

**统计周期：** $WEEK_START ~ $WEEK_END  
**发布日期：** $(date +%Y-%m-%d) 08:00  
**维护者：** @xxuan66  
**下期：** 下周一 08:00
EOF

echo "✅ 创建成功：$WEEKLY_DIR/$WEEK_NUM.md"
echo ""

# 更新 weekly/README.md
echo "📝 更新 weekly/README.md..."
sed -i "s/\*\*最新榜单：\*\.*/\*\*最新榜单：\*\* [$WEEK_NUM](./$WEEK_NUM.md)/" "$WEEKLY_DIR/README.md"

# 添加并提交
git add "$WEEKLY_DIR/$WEEK_NUM.md" "$WEEKLY_DIR/README.md"
git commit -m "chore(weekly): $WEEK_NUM 每周热门 Top 10" || echo "⚠️  没有变化需要提交"

echo ""
echo "========================================"
echo "✅ 每周更新完成"
echo "========================================"
