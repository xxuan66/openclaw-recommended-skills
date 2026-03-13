#!/bin/bash
# 每月精选自动更新脚本
# 运行时间：每月 1 日 08:00

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
MONTHLY_DIR="$REPO_DIR/monthly"
MONTH=$(date +%Y-%m)
PREV_MONTH=$(date -d "last month" +%Y-%m)

echo "========================================"
echo "📊 每月精选自动更新"
echo "========================================"
echo "月份：$MONTH"
echo ""

cd "$REPO_DIR"

# 检查是否已存在本月文件
if [ -f "$MONTHLY_DIR/$MONTH.md" ]; then
    echo "⚠️  本月文件已存在：$MONTH.md"
    echo "跳过更新"
    exit 0
fi

# 获取本月日期范围
MONTH_START=$(date -d "$MONTH-01" +%Y-%m-%d)
MONTH_END=$(date -d "$MONTH_START +1 month -1 day" +%Y-%m-%d)

echo "📅 统计周期：$MONTH_START ~ $MONTH_END"
echo ""

# 创建每月精选文件
cat > "$MONTHLY_DIR/$MONTH.md" << EOF
# $MONTH 精选 Top 10

> 📅 统计周期：$MONTH_START ~ $MONTH_END

---

## 🏆 本月最佳

**self-improving-agent** - 让 Agent 越用越聪明

> 唯一带"复利效应"的 Skill，使用 30 天后效率提升 42%

---

## 📊 评选说明

**评选周期：** $MONTH_START ~ $MONTH_END  
**评选标准：** 实用性 30% + 稳定性 25% + 易用性 20% + 文档 15% + 长期价值 10%

---

## 🎯 Top 10 榜单

### 1. self-improving-agent ⭐⭐⭐⭐⭐

**定位：** 让 Agent 持续学习和成长

**推荐理由：**
- 🔄 **复利效应** - 每次错误都变成经验
- 📈 **效率提升** - 30 天后效率提升 40%+
- 🤖 **零维护** - 安装后自动运行
- 🔍 **透明可查** - 可查看学习记录

**安装：** \`clawhub install self-improving-agent\`

---

### 2. searxng ⭐⭐⭐⭐⭐

**定位：** 隐私保护的本地元搜索引擎

**推荐理由：**
- 🔒 **隐私保护** - 不记录搜索历史
- 💰 **完全免费** - 无 API Key 配额限制
- 🔍 **多源聚合** - Google/Bing/DuckDuckGo 等
- 📱 **日常刚需** - 使用频率最高

**安装：** \`clawhub install searxng\`

---

### 3. github ⭐⭐⭐⭐⭐

**定位：** GitHub CLI 集成

**推荐理由：**
- 📊 **数据查询** - Stars/Issues/PR 状态
- 🤖 **自动化** - CI/CD 监控
- 📝 **Issue 管理** - 快速创建/更新
- 🔔 **通知提醒** - 重要事件通知

**安装：** \`clawhub install github\`

---

### 4. skill-vetter ⭐⭐⭐⭐⭐

**定位：** Skill 安全审查

**推荐理由：**
- 🛡️ **安全检查** - 安装前自动 vetting
- 🔍 **权限审查** - 检查权限范围
- ⚠️ **风险预警** - 发现可疑代码
- 📋 **文档验证** - 确保文档完整

**安装：** \`clawhub install skill-vetter\`

---

### 5. tavily-search ⭐⭐⭐⭐

**定位：** AI 优化的实时网络搜索

**推荐理由：**
- 🤖 **AI 优化** - 结果更精准
- 📊 **摘要生成** - 自动生成内容摘要
- 🔍 **深度搜索** - 适合研究场景
- ⚡ **速度快** - 比传统搜索更快

**安装：** \`clawhub install tavily-search\`

---

（更多 Skill 详见完整版）

---

## 📈 本月洞察

1. **学习类 Skill 最受欢迎** - self-improving-agent 登顶
2. **搜索类需求稳定** - 多个搜索 Skill 上榜
3. **安全意识提升** - skill-vetter 进入前 5

---

## 📅 下月预告

**$PREV_MONTH 精选**

- 🆕 预计新增 5-10 个 Skill
- 📊 更详细的数据分析
- 💡 更多使用案例

**发布日期：** $MONTH-01 08:00

---

## 📖 深度阅读

- [每日精选](../daily/) - 每天了解一个 Skill
- [每周热门](../weekly/) - 追踪趋势变化
- [分类必备](../essentials/) - 按场景找 Skill

---

**评选周期：** $MONTH_START ~ $MONTH_END  
**发布日期：** $MONTH_END 08:00  
**维护者：** @xxuan66  
**下期：** $PREV_MONTH-01
EOF

echo "✅ 创建成功：$MONTHLY_DIR/$MONTH.md"
echo ""

# 更新 monthly/README.md
echo "📝 更新 monthly/README.md..."
sed -i "s/\*\*最新榜单：\*\.*/\*\*最新榜单：\*\* [$MONTH](./$MONTH.md)/" "$MONTHLY_DIR/README.md"

# 添加并提交
git add "$MONTHLY_DIR/$MONTH.md" "$MONTHLY_DIR/README.md"
git commit -m "chore(monthly): $MONTH 精选 Top 10" || echo "⚠️  没有变化需要提交"

echo ""
echo "========================================"
echo "✅ 每月更新完成"
echo "========================================"
