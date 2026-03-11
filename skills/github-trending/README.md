# 🚀 快速开始

## 安装依赖

```bash
pip3 install --user requests beautifulsoup4
```

## 基本用法

### 获取今日热门

```bash
cd /home/admin/.openclaw/workspace/skills/github-trending
python3 scripts/github_trending.py
```

### 获取本周热门

```bash
python3 scripts/github_trending.py --period weekly
```

### 获取本月热门

```bash
python3 scripts/github_trending.py --period monthly
```

## 高级用法

### 指定数量

```bash
# 获取 Top 20
python3 scripts/github_trending.py --limit 20
```

### 过滤语言

```bash
# 只看 Python 项目
python3 scripts/github_trending.py --language Python

# 只看 JavaScript 项目
python3 scripts/github_trending.py --language JavaScript
```

### 输出格式

```bash
# JSON 格式（适合程序处理）
python3 scripts/github_trending.py --format json > trending.json

# Markdown 格式（适合分享）
python3 scripts/github_trending.py --format markdown > trending.md

# 文本格式（默认，适合终端查看）
python3 scripts/github_trending.py --format text
```

### 保存到文件

```bash
# 保存为文本
python3 scripts/github_trending.py --output today.txt

# 保存为 Markdown
python3 scripts/github_trending.py --format markdown --output report.md
```

## 自动化示例

### 每日早报（Cron）

```bash
# 编辑 crontab
crontab -e

# 添加：每天早上 9 点生成报告
0 9 * * * cd /home/admin/.openclaw/workspace/skills/github-trending && python3 scripts/github_trending.py --format markdown --output /tmp/github-trending-$(date +\%Y\%m\%d).md
```

### 监控特定项目

```bash
# 创建一个监控脚本
cat > monitor.sh << 'EOF'
#!/bin/bash
cd /home/admin/.openclaw/workspace/skills/github-trending
python3 scripts/github_trending.py --language Python --limit 10 --format markdown
EOF

chmod +x monitor.sh
```

### 发送到 QQ/微信

```bash
# 结合 QQ Bot 发送
python3 scripts/github_trending.py --format text | while read line; do
    echo "$line"
done | openclaw message send --channel qqbot --target "your-qq" --message "$(cat)"
```

## 输出示例

### 文本格式

```
🔥 GitHub Trending - 今日 🔥
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🥇 1. owner/project
   📝 项目简介...
   💻 Python | ⭐ +123 today | 📊 12,345 total
   🔗 https://github.com/owner/project
```

### Markdown 格式

```markdown
# 🔥 GitHub Trending - 今日

**更新时间**: 2026-03-06 14:30:00

| 排名 | 项目 | 语言 | 今日 Stars | 总 Stars |
|------|------|------|------------|----------|
| 🥇 | [owner/project](url) | Python | +123 | 12,345 |
```

### JSON 格式

```json
{
  "period": "daily",
  "period_name": "今日",
  "fetched_at": "2026-03-06T14:30:00",
  "count": 10,
  "projects": [
    {
      "rank": 1,
      "name": "owner/project",
      "url": "https://github.com/owner/project",
      "language": "Python",
      "stars_today": "123",
      "stars_total": "12345",
      "description": "项目简介"
    }
  ]
}
```

---

**更多帮助：**
```bash
python3 scripts/github_trending.py --help
```
