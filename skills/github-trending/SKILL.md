---
name: github-trending
description: 获取 GitHub Trending 热门项目信息，支持按时间范围筛选（今日/每周/每月）。自动抓取 GitHub 官方趋势页面，无需 API Key。
---

# GitHub Trending 技能

自动获取 GitHub Trending 热门项目信息，支持按时间范围筛选。

## 使用场景

- 发现热门开源项目
- 跟踪技术趋势
- 寻找优质项目参考
- 了解社区动态

## 使用方法

### 基础用法

```bash
# 获取今日热门（默认）
python scripts/github_trending.py

# 获取本周热门
python scripts/github_trending.py --period weekly

# 获取本月热门
python scripts/github_trending.py --period monthly
```

### 高级选项

```bash
# 指定获取数量（默认 10）
python scripts/github_trending.py --limit 20

# 指定编程语言过滤
python scripts/github_trending.py --language Python

# 输出为 JSON 格式
python scripts/github_trending.py --json

# 保存到文件
python scripts/github_trending.py --output trending.md
```

## 输出格式

### 默认输出（终端）

```
🔥 GitHub Trending - 今日热门 🔥
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🥇 1. owner/project-name
   📝 项目简介...
   💻 Python | ⭐ 1,234 today | 📊 12,345 total
   🔗 https://github.com/owner/project-name

🥈 2. owner/project-name
   ...
```

### JSON 输出

```json
{
  "period": "daily",
  "fetched_at": "2026-03-06T14:30:00Z",
  "projects": [
    {
      "rank": 1,
      "name": "owner/project-name",
      "language": "Python",
      "stars_today": 1234,
      "stars_total": 12345,
      "description": "项目简介",
      "url": "https://github.com/owner/project-name"
    }
  ]
}
```

## 配置信息

- **数据源**: `https://github.com/trending`
- **更新频率**: 实时（每次调用重新获取）
- **无需认证**: 使用公开页面抓取，无需 API Key
- **超时设置**: 30 秒

## 依赖安装

```bash
# 需要 Python 3.6+
pip install requests beautifulsoup4

# 或使用系统包
apt install python3-requests python3-bs4  # Debian/Ubuntu
yum install python3-requests python3-beautifulsoup4  # CentOS/RHEL
```

## 示例工作流

### 1. 每日早报自动推送

```bash
# 添加到 crontab，每天早上 9 点推送
0 9 * * * cd /path/to/github-trending && python scripts/github_trending.py --output /tmp/trending.md
```

### 2. 监控特定语言

```bash
# 只关注 Python 项目
python scripts/github_trending.py --language Python --limit 5
```

### 3. 生成 Markdown 报告

```bash
# 生成完整的 Markdown 报告
python scripts/github_trending.py --period weekly --output weekly-report.md
```

## 注意事项

1. **网络访问**: 需要能访问 github.com
2. **频率限制**: 建议不要频繁调用（GitHub 可能限制）
3. **HTML 结构变化**: 如果 GitHub 页面结构变化，可能需要更新解析逻辑
4. **代理设置**: 如需代理，设置环境变量 `HTTP_PROXY` 和 `HTTPS_PROXY`

## 故障排查

### 无法访问 GitHub

```bash
# 检查网络连接
curl -I https://github.com/trending

# 使用代理
export HTTPS_PROXY=http://proxy:port
python scripts/github_trending.py
```

### 解析失败

```bash
# 查看原始 HTML
python scripts/github_trending.py --debug

# 检查 Python 版本
python3 --version  # 需要 3.6+
```

## API 参考

### 命令行参数

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--period` | `-p` | 时间范围 (daily/weekly/monthly) | daily |
| `--limit` | `-l` | 获取数量 | 10 |
| `--language` | `-L` | 编程语言过滤 | 全部 |
| `--json` | `-j` | 输出 JSON 格式 | false |
| `--output` | `-o` | 输出文件路径 | 终端 |
| `--debug` | `-d` | 调试模式 | false |

### 返回值

- `0`: 成功
- `1`: 网络错误
- `2`: 解析错误
- `3`: 参数错误
