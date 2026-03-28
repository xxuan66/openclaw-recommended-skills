#!/bin/bash
# 每日精选自动更新脚本
# 使用方式：bash scripts/daily-update.sh
# 功能：创建今日精选文件，更新 README，提交并推送

set -e

REPO_DIR="/home/admin/.openclaw/workspace/projects/github-repos/openclaw-recommended-skills"
DAILY_DIR="$REPO_DIR/daily"
START_DATE="2026-03-13"

cd "$REPO_DIR"

# 获取今天日期和天数
TODAY=$(date +%Y-%m-%d)
DAY_NUM=$((10#$(date -d "$TODAY" +%j) - 10#$(date -d "$START_DATE" +%j) + 1))

echo "📅 每日精选更新 - $TODAY (Day $DAY_NUM)"
echo "=================================="

# 检查今天是否已经更新
if [ -f "$DAILY_DIR/$TODAY.md" ]; then
    echo "⚠️  今日文件已存在：$TODAY.md"
    echo "跳过创建，仅更新 README"
else
    # 选择今日推荐的 Skill（按天数轮换）
    SKILL_INDEX=$((DAY_NUM % 20))
    
    # Skill 列表（可根据实际情况调整）
    SKILLS=(
        "searxng:隐私保护的本地元搜索引擎"
        "self-improving-agent:让 Agent 越用越聪明"
        "github-trending:零配置追踪 GitHub 热门项目"
        "weather:无需 API 的天气查询"
        "tavily-search:AI 优化的精准搜索"
        "github:GitHub 用户必备工具"
        "summarize:多格式文档摘要"
        "gog:Google Workspace 全套"
        "baidu-search:百度搜索集成"
        "find-skills:发现新技能助手"
        "skill-vetter:安装前的安全检查员"
        "starmemo:结构化记忆管理"
        "jd-price-crawler:京东价格监控"
        "ecommerce-price-scraper:电商比价工具"
        "douyin-hot-trend:抖音热榜数据"
        "xiaohongshu-mcp:小红书内容自动化"
        "xiaomi-recruitment:小米校招岗位监控"
        "browser-use:浏览器自动化"
        "healthcheck:主机安全检查"
        "clawhub:Skill 管理工具"
    )
    
    SKILL_INFO="${SKILLS[$SKILL_INDEX]}"
    SKILL_NAME="${SKILL_INFO%%:*}"
    SKILL_DESC="${SKILL_INFO#*:}"
    
    echo "✨ 创建今日精选：$SKILL_NAME"
    
    # 创建今日文件
    cat > "$DAILY_DIR/$TODAY.md" << EOF
# $TODAY 今日精选：$SKILL_NAME

> 📅 **Day $DAY_NUM** | 每日精选栏目

---

## 🎯 一句话推荐

**$SKILL_DESC**

---

## ⭐ 今日理由

为什么今天推荐 $SKILL_NAME？

1. **实用性强** — 日常使用频率高，解决实际问题
2. **配置简单** — 安装即用，无需复杂设置
3. **稳定可靠** — 经过验证的成熟 Skill

---

## 🚀 快速安装

\`\`\`bash
clawhub install $SKILL_NAME
\`\`\`

**配置时间：** 2 分钟  
**难度：** ⭐⭐ 较简单

---

## 💡 使用建议

- 适合日常使用场景
- 可配合 cron 定时任务自动化
- 查看技能文档了解更多高级用法

---

## 🔗 相关资源

- [技能文档](../skills/$SKILL_NAME/SKILL.md)
- [昨日精选](./$(date -d "$TODAY - 1 day" +%Y-%m-%d).md)

---

**发布日期：** $TODAY  
**栏目：** 每日精选  
**维护者：** @xxuan66
EOF
    
    echo "✅ 创建文件：$DAILY_DIR/$TODAY.md"
fi

# 更新 daily/README.md
echo "📝 更新 daily/README.md"

YESTERDAY=$(date -d "$TODAY - 1 day" +%Y-%m-%d)

# 备份原文件
cp "$DAILY_DIR/README.md" "$DAILY_DIR/README.md.bak"

# 更新今日精选部分
sed -i "s#\\*\\*今天推荐：\\*\\* \\[.*\\](.*)#\\*\\*今天推荐：\\*\\* [$SKILL_NAME](./$TODAY.md)#" "$DAILY_DIR/README.md"
sed -i "s#^> .*$#> $SKILL_DESC#" "$DAILY_DIR/README.md"

# 更新累计更新天数
sed -i "s#\\*\\*累计更新：\\*\\* Day.*#\\*\\*累计更新：\\*\\* Day $DAY_NUM#" "$DAILY_DIR/README.md"

# 更新最后更新时间
sed -i "s#\\*\\*最后更新：\\*\\*.*#\\*\\*最后更新：\\*\\* $TODAY 08:00#" "$DAILY_DIR/README.md"

# 更新历史表格（在表格开头添加今日记录）
DAY_OF_MONTH=$(date +%d)
TABLE_LINE="| $DAY_OF_MONTH 日 | [$SKILL_NAME](./$TODAY.md) | $SKILL_DESC"
sed -i "/^| 27 日 |/i\\$TABLE_LINE" "$DAILY_DIR/README.md"

echo "✅ daily/README.md 更新完成"

# Git 提交
echo "🔄 Git 提交..."
git add -A
if git diff --staged --quiet; then
    echo "⚠️  没有变更需要提交"
else
    git commit -m "📅 每日精选更新：$TODAY (Day $DAY_NUM) - $SKILL_NAME"
    echo "✅ 提交完成"
    
    # 推送
    echo "📤 推送到远程..."
    git push origin main
    echo "✅ 推送完成"
fi

echo ""
echo "=================================="
echo "✅ 每日精选更新完成"
echo "今日推荐：$SKILL_NAME"
echo "描述：$SKILL_DESC"
echo "天数：Day $DAY_NUM"
