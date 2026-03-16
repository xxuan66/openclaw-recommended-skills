# 🦞 OpenClaw 推荐 Skill 清单

> 精选优质 OpenClaw Skill，持续更新中...

[![Updated](https://img.shields.io/badge/updated-2026--03--13-blue)](https://github.com/xxuan66/openclaw-recommended-skills)
[![Skills](https://img.shields.io/badge/skills-14-green)](https://github.com/xxuan66/openclaw-recommended-skills)
[![Top Picks](https://img.shields.io/badge/top%20picks-5-orange)](https://github.com/xxuan66/openclaw-recommended-skills/blob/main/top-picks/2026-03.md)
[![Daily](https://img.shields.io/badge/daily-updated-yellow)](https://github.com/xxuan66/openclaw-recommended-skills/tree/main/daily)
[![Weekly](https://img.shields.io/badge/weekly-top10-blue)](https://github.com/xxuan66/openclaw-recommended-skills/tree/main/weekly)
[![Monthly](https://img.shields.io/badge/monthly-top10-purple)](https://github.com/xxuan66/openclaw-recommended-skills/tree/main/monthly)
[![License](https://img.shields.io/badge/license-MIT-blue)](https://github.com/xxuan66/openclaw-recommended-skills/blob/main/LICENSE)

---

## 📋 目录

- [🏆 本月 Top 5](#-本月-top-5)
- [🌟 全部推荐](#-全部推荐)
- [📂 分类索引](#-分类索引)
- [📦 快速安装](#-快速安装)
- [📚 使用案例](#-使用案例)
- [🔄 更新日志](#-更新日志)

---

## 🏆 本月 Top 5

> 🆕 全新栏目！每月精选 5 个必装 Skill，新手闭眼装不踩坑

| 排名 | Skill | 一句话理由 | 安装 |
|------|-------|-----------|------|
| 🥇 | **self-improving-agent** | 让 Agent 越用越聪明，唯一带"复利效应"的 Skill | `clawhub install self-improving-agent` |
| 🥈 | **searxng** | 隐私搜索刚需，无需 API Key，日常使用频率最高 | `clawhub install searxng` |
| 🥉 | **github** | GitHub 重度用户必备，CLI 集成效率翻倍 | `clawhub install github` |
| 🏅 | **skill-vetter** | 安装 Skill 前的安全检查员，避免踩坑 | `clawhub install skill-vetter` |
| 🏅 | **tavily-search** | AI 优化的搜索，结果更精准，适合研究场景 | `clawhub install tavily-search` |

**📖 详细评测：** [查看 3 月 Top 5 完整介绍](./top-picks/2026-03.md)  
**📊 使用报告：** [self-improving-agent 30 天实测](./examples/self-improving-agent-30days.md)

---

## 📅 精选栏目

> 🆕 全新内容矩阵！日/周/月 + 分类，满足不同需求

| 栏目 | 更新频率 | 内容 | 最新 |
|------|---------|------|------|
| 📅 **[每日精选](./daily/)** | 每日 08:00 | 每天发现一个最佳 Skill | [2026-03-16: searxng](./daily/2026-03-16.md) |
| 📆 **[每周热门](./weekly/)** | 周一 08:00 | 本周最火的 Top 10 | [2026-W12](./weekly/2026-W12.md) |
| 📊 **[每月精选](./monthly/)** | 每月 1 日 08:00 | 深度评测 Top 10 | [2026-03](./monthly/2026-03.md) |
| 🎯 **[分类必备](./essentials/)** | 按需更新 | 按场景找 Skill | [搜索类](./essentials/search.md) |

---

## 🌟 全部推荐

| # | Skill | 版本 | 类别 | 简介 |
|---|-------|------|------|------|
| 1 | **searxng** | 1.0.3 | 🔍 搜索 | 隐私保护的本地元搜索引擎 |
| 2 | **self-improving-agent** | 3.0.0 | 🧠 学习 | 自我反思 + 持续学习 + 记忆管理 |
| 3 | **tavily-search** | 1.0.0 | 🔍 搜索 | AI 优化的实时网络搜索 |
| 4 | **github** | 1.0.0 | 💻 开发 | GitHub CLI 集成，管理 PR/Issue/CI |
| 5 | **summarize** | 1.0.0 | 📄 文档 | 多格式文档/URL/图片/音频摘要 |
| 6 | **skill-vetter** | 1.0.0 | 🛡️ 安全 | Skill 安全审查，检查权限和风险 |
| 7 | **gog** | 1.0.0 | 📧 办公 | Google Workspace 全套集成 |
| 8 | **find-skills** | 0.1.0 | 🔎 发现 | 帮你发现和安装新 Skill |
| 9 | **baidu-search** | 1.1.1 | 🔍 搜索 | 百度 AI 搜索引擎集成 |
| 10 | **starmemo** | 2.0.0 | 🧠 记忆 | 结构化记忆 + 知识库 + AI 优化 |
| 11 | **github-trending** | 1.0.0 | 🔎 发现 | GitHub Trending 热门项目追踪 |
| 12 | **xiaohongshu-mcp** | 1.0.0 | 📱 社交 | 小红书内容发布与分析 |
| 13 | **douyin-hot-trend** | 1.0.0 | 📱 社交 | 抖音热榜/热搜数据获取 |

---

## ⚡ 快速技巧

> 每日精选一个实用小技巧，帮助你更好地使用 OpenClaw。

### 今日技巧：天气查询

使用 `weather` Skill 可以快速查询天气信息，无需 API Key：

```bash
# 直接对话查询
openclaw agent -m "北京今天天气怎么样？"

# 设置每日天气提醒（配合 cron）
# 在 HEARTBEAT.md 或 cron 配置中添加
```

**安装：** `clawhub install weather`

更多技巧请查看 [DAILY_UPDATES.md](./DAILY_UPDATES.md)

---

## 📂 分类索引

### 🔍 搜索类

| Skill | 版本 | 描述 | 安装命令 |
|-------|------|------|---------|
| searxng | 1.0.3 | 隐私保护的本地元搜索引擎 | `clawhub install searxng` |
| tavily-search | 1.0.0 | AI 优化的实时网络搜索 | `clawhub install tavily-search` |
| baidu-search | 1.1.1 | 百度 AI 搜索引擎集成 | `clawhub install baidu-search` |

### 🧠 学习/记忆类

| Skill | 版本 | 描述 | 安装命令 |
|-------|------|------|---------|
| self-improving-agent | 3.0.0 | 自我反思 + 持续学习 + 记忆管理 | `clawhub install self-improving-agent` |
| starmemo | 2.0.0 | 结构化记忆 + 知识库 + AI 优化 | `clawhub install starmemo` |

### 💻 开发类

| Skill | 版本 | 描述 | 安装命令 |
|-------|------|------|---------|
| github | 1.0.0 | GitHub CLI 集成，管理 PR/Issue/CI | `clawhub install github` |
| skill-vetter | 1.0.0 | Skill 安全审查工具 | `clawhub install skill-vetter` |

### 📄 文档/内容类

| Skill | 版本 | 描述 | 安装命令 |
|-------|------|------|---------|
| summarize | 1.0.0 | 多格式文档摘要 (PDF/图片/音频/URL) | `clawhub install summarize` |

### 📧 办公/效率类

| Skill | 版本 | 描述 | 安装命令 |
|-------|------|------|---------|
| gog | 1.0.0 | Google Workspace 全套 (Gmail/Calendar/Drive) | `clawhub install gog` |
| find-skills | 0.1.0 | 发现和安装新 Skill | `clawhub install find-skills` |

### 🔎 发现/趋势类

| Skill | 版本 | 描述 | 安装命令 |
|-------|------|------|---------|
| github-trending | 1.0.0 | GitHub Trending 热门项目追踪 | `clawhub install github-trending` |

### 📱 社交/内容类

| Skill | 版本 | 描述 | 安装命令 |
|-------|------|------|---------|
| xiaohongshu-mcp | 1.0.0 | 小红书内容发布与分析 | `clawhub install xiaohongshu-mcp` |
| douyin-hot-trend | 1.0.0 | 抖音热榜/热搜数据获取 | `clawhub install douyin-hot-trend` |

---

## 📦 快速安装

### 批量安装推荐 Skill

```bash
# 安装全部推荐 Skill（clawhub）
for skill in searxng self-improving-agent tavily-search github summarize skill-vetter gog find-skills baidu-search starmemo github-trending xiaohongshu-mcp douyin-hot-trend; do
  clawhub install $skill
done

# 或者使用 ClawHub 登录后的 token
clawhub login --token <your-token>
clawhub install searxng
```

### 验证安装

```bash
# 查看已安装 Skill
clawhub list

# 查看 Skill 详情
clawhub inspect <skill-name>
```

---

## 📊 Skill 评分标准

我们根据以下维度评估 Skill：

| 维度 | 权重 | 说明 |
|------|------|------|
| **实用性** | ⭐⭐⭐⭐⭐ | 日常使用频率高 |
| **稳定性** | ⭐⭐⭐⭐ | 运行稳定，少 bug |
| **安全性** | ⭐⭐⭐⭐⭐ | 权限合理，无风险 |
| **文档质量** | ⭐⭐⭐⭐ | 文档完善，示例清晰 |
| **维护活跃度** | ⭐⭐⭐⭐ | 持续更新，响应 issue |

---

## 📚 使用案例

> 真实记录 Skill 的使用效果和成长历程

### 📈 self-improving-agent 30 天使用报告

**核心数据：**
- 运行 30 天，积累 152 条经验教训
- 重复错误减少 83%
- 任务效率提升 42%
- 累计节省 36 小时

**用户评价：**
> "唯一值得'投资'的 Skill，Agent 像换了一个'人'"

**📖 完整报告：** [查看 30 天详细记录](./examples/self-improving-agent-30days.md)

---

## 🔄 更新日志

### 2026-03-13 - 版本 1.1.1

- ✅ README 日期更新至 2026-03-13
- ✅ 新增「快速技巧」栏目
- ✅ skills-index.json 版本升级至 v1.1.1
- ✅ DAILY_UPDATES.md 添加 Day 004

### 2026-03-12 - 版本 1.1.0

- ✅ 索引从 10 扩展至 13 个 Skill
- ✅ 新增发现/趋势类：github-trending
- ✅ 新增社交/内容类：xiaohongshu-mcp、douyin-hot-trend
- ✅ 分类索引新增 2 个分类
- ✅ README 技能表格更新

### 2026-03-10 - 初始版本

- ✅ 创建仓库
- ✅ 精选 10 个热门 Skill
- ✅ 分类索引
- ✅ 快速安装指南

---

## 📝 贡献指南

欢迎推荐更多优质 Skill！

1. Fork 本仓库
2. 在 `recommendations/` 目录下添加 Skill 信息
3. 提交 PR

### 推荐格式

```markdown
### Skill 名称

- **Slug:** `skill-slug`
- **版本:** 1.0.0
- **类别:** 搜索/学习/开发/...
- **简介:** 一句话描述
- **推荐理由:** 为什么值得安装
- **安装命令:** `clawhub install skill-slug`
```

---

## 🔗 相关链接

- [OpenClaw 官方文档](https://docs.openclaw.ai)
- [OpenClaw GitHub](https://github.com/openclaw/openclaw)
- [ClawHub 技能市场](https://clawhub.ai)
- [Discord 社区](https://discord.com/invite/clawd)

---

**维护者:** @xxuan66  
**最后更新:** 2026-03-13
