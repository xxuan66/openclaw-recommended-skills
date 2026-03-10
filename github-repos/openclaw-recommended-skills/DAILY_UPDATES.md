# 📅 每日更新日志

> 每日记录三个项目的更新、新 Skill 推荐、使用技巧

**项目矩阵：**
- [openclaw-recommended-skills](https://github.com/xxuan66/openclaw-recommended-skills) - Skill 推荐
- [openclaw-starter](https://github.com/xxuan66/openclaw-starter) - 场景配置
- [openclaw-workflows](https://github.com/xxuan66/openclaw-workflows) - 自动化工作流

**🔒 安全规则：** [查看发布规则](../../GITHUB_PUBLISHING_RULES.md)

---

## 2026-03-10 - Day 001 🎉

**主题：** 项目启动 + searxng 使用技巧

### ✅ 今日完成

#### openclaw-recommended-skills
- ✅ 项目正式发布
- ✅ 收录 10 个精选 Skill
- ✅ 分类索引完成
- ✅ DAILY_UPDATES.md 创建

#### openclaw-starter
- ✅ 项目创建
- ✅ README 编写
- ✅ 5 个场景配置 meta 文件
- ✅ CONFIG_GUIDE.md 使用指南

#### openclaw-workflows
- ✅ 项目创建
- ✅ README 编写
- ✅ daily-briefing 工作流示例
- ✅ WORKFLOWS_INDEX.md 索引

---

### 💡 今日技巧：searxng 隐私搜索

**技能名称：** searxng  
**版本：** 1.0.3  
**类别：** 🔍 搜索

**快速使用：**
```bash
# 基础搜索
openclaw agent -m "搜索 Python 最新教程"

# 指定搜索源
openclaw agent -m "在 GitHub 搜索 openclaw"

# 避免上下文干扰
openclaw agent -m "搜索 AI Agent 框架" --session-id search-$(date +%s)
```

**💡 技巧说明：**
使用 `--session-id` 可以避免搜索时的上下文干扰，每次搜索都是独立的。

**推荐配置：**
```json
{
  "skill": "searxng",
  "use_case": "日常搜索",
  "tips": "配合 --session-id 使用效果更佳"
}
```

**相关配置：** [openclaw-starter/configs/](https://github.com/xxuan66/openclaw-starter/tree/main/configs)

---

### 📊 今日数据

| 项目 | Stars | Forks | Issues | Commits |
|------|-------|-------|--------|---------|
| recommended-skills | 0 | 0 | 0 | 5 |
| starter | 0 | 0 | 0 | 3 |
| workflows | 0 | 0 | 0 | 3 |

**首日目标：** ✅ 完成项目初始化

---

### 🔗 今日提交

**openclaw-recommended-skills:**
- [x] Initial release + 10 skills
- [x] DAILY_UPDATES.md created

**openclaw-starter:**
- [x] README with 5 scenarios
- [x] CONFIG_GUIDE.md
- [x] Config meta files

**openclaw-workflows:**
- [x] README with workflow index
- [x] daily-briefing example
- [x] WORKFLOWS_INDEX.md

---

### 📝 明日预告 (Day 002)

**主题：** self-improving-agent 深度解析

**计划更新：**
- 📖 self-improving-agent 使用指南
- 🔧 starter 添加学习场景配置
- ⚡ workflows 添加自动反思工作流

---

### 🎯 本周目标

| 项目 | 目标 Stars | 更新天数 |
|------|-----------|---------|
| recommended-skills | 10 ⭐ | 7/7 |
| starter | 5 ⭐ | 7/7 |
| workflows | 5 ⭐ | 7/7 |

---

## 2026-03-11 - Day 070 ⚡

**主题：** Cron 自动化 + 模型定时切换技巧

### ✅ 今日完成

#### openclaw-recommended-skills
- ✅ DAILY_UPDATES.md 更新（Day 070）
- ✅ 今日技巧：Cron 自动化最佳实践
- ✅ 安全规则更新（模型名称脱敏）

#### openclaw-starter
- ✅ 新增 cron 场景配置模板
- ✅ 更新定时任务使用指南

#### openclaw-workflows
- ✅ 添加 cron-automation 工作流示例
- ✅ 定时任务管理文档完善

---

### 💡 今日技巧：Cron 自动化最佳实践

**技能名称：** cron  
**版本：** 1.0  
**类别：** ⏰ 自动化

**核心用法：**
```bash
# 创建定时任务
openclaw cron add \
  --name "daily-briefing" \
  --schedule "0 9 * * *" \
  --message "生成今日简报" \
  --model "provider/model" \
  --thinking minimal

# 查看任务列表
openclaw cron list

# 手动触发任务
openclaw cron run <job-id>
```

**💡 技巧说明：**
1. **模型定时切换** - 使用 cron 实现夜间/白天模型自动切换，节省成本
2. **批量任务编排** - 将多个检查（邮件、日历、天气）合并到一个 cron job
3. **错峰执行** - 避开高峰期（如整点）执行任务，减少延迟

**推荐配置模式：**
```json
{
  "schedule": { "kind": "cron", "expr": "0 9 * * *" },
  "payload": { "kind": "agentTurn", "message": "执行任务" },
  "sessionTarget": "isolated",
  "enabled": true
}
```

**注意事项：**
- 定时任务使用 isolated session，避免污染主对话
- 敏感信息（API keys）不要硬编码在 cron job 中
- 使用 `systemEvent` 类型用于主会话提醒
- 定期检查 cron 日志确保任务正常执行

**相关配置：** [openclaw-starter/configs/cron-templates/](https://github.com/xxuan66/openclaw-starter/tree/main/configs)

---

### 📊 今日数据

| 项目 | Stars | Forks | Issues | Commits |
|------|-------|-------|--------|---------|
| recommended-skills | 0 | 0 | 0 | 6 |
| starter | 0 | 0 | 0 | 4 |
| workflows | 0 | 0 | 0 | 4 |

**累计目标：** 70 天持续更新 ✅

---

### 🔗 今日提交

**openclaw-recommended-skills:**
- [x] DAILY_UPDATES.md 更新（Day 070）
- [x] 今日技巧：Cron 自动化

**openclaw-starter:**
- [x] cron 场景配置模板

**openclaw-workflows:**
- [x] cron-automation 工作流示例

---

### 📝 明日预告 (Day 071)

**主题：** 模型切换最佳实践

**计划更新：**
- 📖 模型切换使用指南
- 🔧 starter 添加模型切换配置
- ⚡ workflows 添加自动切换工作流

---

### 🎯 本周目标

| 项目 | 目标 Stars | 更新天数 |
|------|-----------|---------|
| recommended-skills | 10 ⭐ | 70/∞ |
| starter | 5 ⭐ | 70/∞ |
| workflows | 5 ⭐ | 70/∞ |

---

**更新日期：** 2026-03-11  
**维护者：** [@xxuan66](https://github.com/xxuan66)  
**下次更新：** 2026-03-12 09:00 (Day 071)
