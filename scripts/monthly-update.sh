#!/bin/bash
# 每月精选自动更新脚本
# 使用方式：bash scripts/monthly-update.sh
# 功能：创建本月精选文件，更新 README，提交并推送

set -e

REPO_DIR="/home/admin/.openclaw/workspace/projects/github-repos/openclaw-recommended-skills"
MONTHLY_DIR="$REPO_DIR/monthly"
START_MONTH="2026-03"

cd "$REPO_DIR"

# 获取当前年月
CURRENT_MONTH=$(date +%Y-%m)
CURRENT_YEAR=$(date +%Y)
CURRENT_MONTH_NUM=$(date +%m)

echo "📅 每月精选更新 - $CURRENT_MONTH"
echo "=================================="

# 检查本月文件是否已经存在
if [ -f "$MONTHLY_DIR/$CURRENT_MONTH.md" ]; then
    echo "⚠️  本月文件已存在：$CURRENT_MONTH.md"
    echo "跳过创建"
    exit 0
fi

# 计算从起始月到当前的月数差
START_YEAR=2026
START_MONTH_NUM=3
MONTH_DIFF=$(( (10#$CURRENT_YEAR - START_YEAR) * 12 + (10#$CURRENT_MONTH_NUM - START_MONTH_NUM) ))

# 每月推荐的主题轮换
MONTHLY_THEMES=(
    "GitHub 生态：开源项目全景图"
    "效率革命：自动化工作流"
    "数据智能：电商与价格监控"
    "社交矩阵：多平台内容运营"
    "AI 前沿：大模型应用实践"
    "知识管理：记忆与学习系统"
    "安全优先：隐私保护工具"
    "开发工具：编码与调试利器"
    "内容创作：图文视频自动化"
    "搜索增强：智能信息获取"
    "协作工具：团队效率提升"
    "监控告警：系统健康检查"
)

THEME_INDEX=$((MONTH_DIFF % ${#MONTHLY_THEMES[@]}))
THEME_INFO="${MONTHLY_THEMES[$THEME_INDEX]}"
THEME_NAME="${THEME_INFO%%:*}"
THEME_DESC="${THEME_INFO#*:}"

echo "✨ 本月主题：$THEME_NAME"

# 获取本月推荐的 Skills（根据主题选择）
case $THEME_NAME in
    "GitHub 生态")
        SKILLS=("github-trending" "github" "clawhub" "github-ops")
        ;;
    "效率革命")
        SKILLS=("weather" "summarize" "gog" "self-improving-agent")
        ;;
    "数据智能")
        SKILLS=("jd-price-crawler" "ecommerce-price-scraper" "tavily-search" "akshare-stock")
        ;;
    "社交矩阵")
        SKILLS=("douyin-hot-trend" "xiaohongshu-mcp" "browser-use" "wechat-operator")
        ;;
    "AI 前沿")
        SKILLS=("tavily-search" "browser-use" "summarize" "self-improving-agent")
        ;;
    "知识管理")
        SKILLS=("self-improving-agent" "starmemo" "find-skills" "feishu-bitable")
        ;;
    "安全优先")
        SKILLS=("healthcheck" "skill-vetter" "searxng" "github")
        ;;
    "开发工具")
        SKILLS=("github-trending" "clawhub" "skill-creator" "skill-vetter")
        ;;
    "内容创作")
        SKILLS=("wechat-operator" "xiaohongshu-mcp" "browser-use" "summarize")
        ;;
    "搜索增强")
        SKILLS=("tavily-search" "baidu-search" "searxng" "web_search")
        ;;
    "协作工具")
        SKILLS=("feishu-doc" "feishu-bitable" "feishu-wiki" "gog")
        ;;
    "监控告警")
        SKILLS=("healthcheck" "weather" "qqbot-cron" "github")
        ;;
    *)
        SKILLS=("github-trending" "weather" "tavily-search" "browser-use")
        ;;
esac

# 获取本月第一天和最后一天
FIRST_DAY=$(date -d "$CURRENT_MONTH-01" +%Y-%m-%d)
LAST_DAY=$(date -d "$FIRST_DAY +1 month -1 day" +%Y-%m-%d)

# 创建本月文件
cat > "$MONTHLY_DIR/$CURRENT_MONTH.md" << EOF
# $CURRENT_MONTH 每月精选

> 📅 **$CURRENT_YEAR 年 $CURRENT_MONTH_NUM 月** | 每月精选栏目  
> 📆 时间范围：$FIRST_DAY 至 $LAST_DAY

---

## 🎯 本月主题：$THEME_NAME

**$THEME_DESC**

---

## ⭐ 本月重点推荐 Skills

### 1. ${SKILLS[0]}
- **推荐理由：** 本月核心推荐，使用频率最高
- **适用场景：** 日常工作流核心工具
- **安装命令：** \`clawhub install ${SKILLS[0]}\`

### 2. ${SKILLS[1]}
- **推荐理由：** 与核心工具互补，扩展功能
- **适用场景：** 特定场景增强
- **安装命令：** \`clawhub install ${SKILLS[1]}\`

### 3. ${SKILLS[2]}
- **推荐理由：** 值得深入探索的实用工具
- **适用场景：** 专业需求场景
- **安装命令：** \`clawhub install ${SKILLS[2]}\`

### 4. ${SKILLS[3]}
- **推荐理由：** 本月新发现/更新的优质技能
- **适用场景：** 进阶用户需求
- **安装命令：** \`clawhub install ${SKILLS[3]}\`

---

## 📊 本月数据

- **每周回顾：** 查看 weekly/ 目录获取每周热门
- **每日精选：** 查看 daily/ 目录获取每日更新
- **热门趋势：** 基于 GitHub star 增长和用户反馈
- **更新频率：** 每月 1 日上午 8:00 自动更新

---

## 🔗 相关资源

- [上月回顾](./$(date -d "$FIRST_DAY -1 day" +%Y-%m).md)
- [每周热门](../weekly/README.md)
- [每日精选](../daily/README.md)
- [技能总览](../README.md)

---

**发布月份：** $CURRENT_MONTH  
**栏目：** 每月精选  
**维护者：** @xxuan66
EOF

echo "✅ 创建文件：$MONTHLY_DIR/$CURRENT_MONTH.md"

# 更新 monthly/README.md
echo "📝 更新 monthly/README.md"

# 读取当前 README
if [ -f "$MONTHLY_DIR/README.md" ]; then
    # 更新本月推荐部分
    sed -i "s|本月推荐：.*|本月推荐：[$CURRENT_MONTH](./$CURRENT_MONTH.md) - $THEME_NAME|" "$MONTHLY_DIR/README.md"
    sed -i "s|最后更新：.*|最后更新：$CURRENT_MONTH ($(date +%Y-%m-%d))|" "$MONTHLY_DIR/README.md"
    echo "✅ monthly/README.md 更新完成"
else
    echo "⚠️  monthly/README.md 不存在，跳过更新"
fi

# Git 提交
echo "🔄 Git 提交..."
git add -A
if git diff --staged --quiet; then
    echo "⚠️  没有变更需要提交"
else
    git commit -m "📅 每月精选更新：$CURRENT_MONTH - $THEME_NAME"
    echo "✅ 提交完成"
    
    # 推送
    echo "📤 推送到远程..."
    git push origin main
    echo "✅ 推送完成"
fi

echo ""
echo "=================================="
echo "✅ 每月精选更新完成"
echo "本月主题：$THEME_NAME"
echo "月份：$CURRENT_MONTH"
