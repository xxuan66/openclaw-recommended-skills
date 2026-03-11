# 🦞 OpenClaw 推荐 Skill 清单

> 精选优质 OpenClaw Skill，持续更新中...

[![Updated](https://img.shields.io/badge/updated-2026--03--10-blue)](https://github.com/xxuan66/openclaw-recommended-skills)
[![Skills](https://img.shields.io/badge/skills-10-green)](https://github.com/xxuan66/openclaw-recommended-skills)
[![License](https://img.shields.io/badge/license-MIT-blue)](https://github.com/xxuan66/openclaw-recommended-skills/blob/main/LICENSE)

---

## 📋 目录

- [🌟 本月推荐](#-本月推荐)
- [📂 分类索引](#-分类索引)
- [📦 快速安装](#-快速安装)
- [🔄 更新日志](#-更新日志)

---

## 🌟 本月推荐

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

---

## 📦 快速安装

### 批量安装推荐 Skill

```bash
# 安装全部推荐 Skill
for skill in searxng self-improving-agent tavily-search github summarize skill-vetter gog find-skills baidu-search starmemo; do
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

## 🔄 更新日志

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
**最后更新:** 2026-03-10

---

## 📢 关注我们

### 🌐 多平台更新

| 平台 | 链接 |
|------|------|
| **GitHub** | https://github.com/xxuan66/openclaw-recommended-skills |
| **微信公众号** | 搜索 "OpenClaw" |
| **知乎** | @xuan |
| **掘金** | @xuan |

### 📰 每日更新

- **06:00** - GitHub 每日更新（4 个仓库）
- **09:30** - 公众号内容生成
- **11:00** - 公众号发布

### 🎯 项目矩阵

| 仓库 | 内容 | 更新频率 |
|------|------|---------|
| [openclaw-recommended-skills](https://github.com/xxuan66/openclaw-recommended-skills) | Skill 推荐 | 每日 |
| [openclaw-starter](https://github.com/xxuan66/openclaw-starter) | 场景配置 | 每日 |
| [openclaw-workflows](https://github.com/xxuan66/openclaw-workflows) | 工作流示例 | 每日 |
| [agent-learning-path](https://github.com/xxuan66/agent-learning-path) | 学习教程 | 每日 |

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

**Star⭐ 支持：** 如果这个项目对你有帮助，请给个 Star！

---

**最后更新：** 2026-03-11  
**维护者：** xuan  
**许可证：** MIT
