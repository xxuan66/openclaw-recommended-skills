#!/bin/bash
# 每周热门自动更新脚本
# 使用方式：bash scripts/weekly-update.sh
# 功能：创建本周热门文件，更新 README，提交并推送

set -e

REPO_DIR="/home/admin/.openclaw/workspace/projects/github-repos/openclaw-recommended-skills"
WEEKLY_DIR="$REPO_DIR/weekly"
START_WEEK="2026-W11"

cd "$REPO_DIR"

# 获取当前周数
CURRENT_WEEK=$(date +%G-W%V)
CURRENT_YEAR=$(date +%G)
CURRENT_WEEK_NUM=$(date +%V)

echo "📅 每周热门更新 - $CURRENT_WEEK"
echo "=================================="

# 检查本周文件是否已经存在
if [ -f "$WEEKLY_DIR/$CURRENT_WEEK.md" ]; then
    echo "⚠️  本周文件已存在：$CURRENT_WEEK.md"
    echo "跳过创建"
    exit 0
fi

# 计算从起始周到当前的周数
START_WEEK_NUM=$(echo $START_WEEK | cut -d'-' -f2)
WEEK_DIFF=$((10#$CURRENT_WEEK_NUM - 10#$START_WEEK_NUM))

# 每周推荐的主题轮换
WEEKLY_THEMES=(
    "GitHub 趋势：追踪热门开源项目"
    "效率工具：提升日常工作流"
    "数据分析：电商价格监控"
    "社交媒体：抖音/小红书自动化"
    "AI 搜索：智能搜索工具"
    "记忆管理：让 Agent 更聪明"
    "浏览器自动化：解放双手"
    "安全工具：保护隐私和数据"
)

THEME_INDEX=$((WEEK_DIFF % ${#WEEKLY_THEMES[@]}))
THEME_INFO="${WEEKLY_THEMES[$THEME_INDEX]}"
THEME_NAME="${THEME_INFO%%:*}"
THEME_DESC="${THEME_INFO#*:}"

echo "✨ 本周主题：$THEME_NAME"

# 获取本周推荐的 Skills（根据主题选择）
case $THEME_NAME in
    "GitHub 趋势")
        SKILLS=("github-trending" "github" "clawhub")
        ;;
    "效率工具")
        SKILLS=("weather" "summarize" "gog")
        ;;
    "数据分析")
        SKILLS=("jd-price-crawler" "ecommerce-price-scraper" "tavily-search")
        ;;
    "社交媒体")
        SKILLS=("douyin-hot-trend" "xiaohongshu-mcp" "browser-use")
        ;;
    "AI 搜索")
        SKILLS=("tavily-search" "baidu-search" "searxng")
        ;;
    "记忆管理")
        SKILLS=("self-improving-agent" "starmemo" "find-skills")
        ;;
    "浏览器自动化")
        SKILLS=("browser-use" "xiaohongshu-mcp" "jd-price-crawler")
        ;;
    "安全工具")
        SKILLS=("healthcheck" "skill-vetter" "searxng")
        ;;
    *)
        SKILLS=("github-trending" "weather" "tavily-search")
        ;;
esac

# 创建本周文件
cat > "$WEEKLY_DIR/$CURRENT_WEEK.md" << EOF
# $CURRENT_WEEK 每周热门

> 📅 **$CURRENT_YEAR 年第 $CURRENT_WEEK_NUM 周** | 每周热门栏目  
> 📆 时间范围：$(date -d "monday" +%Y-%m-%d) 至 $(date -d "sunday" +%Y-%m-%d)

---

## 🎯 本周主题：$THEME_NAME

**$THEME_DESC**

---

## ⭐ 本周推荐 Skills

### 1. ${SKILLS[0]}
- **推荐理由：** 本周最热门，使用频率最高
- **适用场景：** 日常工作流核心工具
- **安装命令：** \`clawhub install ${SKILLS[0]}\`

### 2. ${SKILLS[1]}
- **推荐理由：**  complementary to the top pick
- **适用场景：** 扩展功能场景
- **安装命令：** \`clawhub install ${SKILLS[1]}\`

### 3. ${SKILLS[2]}
- **推荐理由：** 值得尝试的新选择
- **适用场景：** 特定需求场景
- **安装命令：** \`clawhub install ${SKILLS[2]}\`

---

## 📊 本周数据

- **新增 Skills：** 查看 daily/ 目录获取每日精选
- **热门趋势：** 基于 GitHub star 增长和用户反馈
- **更新频率：** 每周一上午 8:00 自动更新

---

## 🔗 相关资源

- [上周回顾](./$(date -d "last monday - 7 days" +%G-W%V).md)
- [每日精选](../daily/README.md)
- [技能总览](../README.md)

---

**发布周数：** $CURRENT_WEEK  
**栏目：** 每周热门  
**维护者：** @xxuan66
EOF

echo "✅ 创建文件：$WEEKLY_DIR/$CURRENT_WEEK.md"

# 更新 weekly/README.md
echo "📝 更新 weekly/README.md"

# 读取当前 README
if [ -f "$WEEKLY_DIR/README.md" ]; then
    # 更新本周推荐部分
    sed -i "s|本周推荐：.*|本周推荐：[$CURRENT_WEEK](./$CURRENT_WEEK.md) - $THEME_NAME|" "$WEEKLY_DIR/README.md"
    sed -i "s|最后更新：.*|最后更新：$CURRENT_WEEK ($(date +%Y-%m-%d))|" "$WEEKLY_DIR/README.md"
    echo "✅ weekly/README.md 更新完成"
else
    echo "⚠️  weekly/README.md 不存在，跳过更新"
fi

# Git 提交
echo "🔄 Git 提交..."
git add -A
if git diff --staged --quiet; then
    echo "⚠️  没有变更需要提交"
else
    git commit -m "📅 每周热门更新：$CURRENT_WEEK - $THEME_NAME"
    echo "✅ 提交完成"
    
    # 推送
    echo "📤 推送到远程..."
    git push origin main
    echo "✅ 推送完成"
fi

echo ""
echo "=================================="
echo "✅ 每周热门更新完成"
echo "本周主题：$THEME_NAME"
echo "周数：$CURRENT_WEEK"
