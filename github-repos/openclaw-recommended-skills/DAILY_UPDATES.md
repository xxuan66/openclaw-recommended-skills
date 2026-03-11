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
- ✅ DAILY_UPDATES.md 更新（Day 070，3 次更新）
- ✅ 今日技巧 1：Cron 自动化最佳实践（06:00）
- ✅ 今日技巧 2：Session 隔离最佳实践（08:25）
- ✅ 今日技巧 3：模型切换最佳实践（08:41）
- ✅ 安全规则更新（模型名称脱敏）

#### openclaw-starter
- ✅ 新增 cron 场景配置模板
- ✅ 更新定时任务使用指南
- ✅ CONFIG_GUIDE.md 更新（添加 cron/automation 配置指南）
- ✅ README.md 更新（添加 cron-scenario.json 文档）

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
| recommended-skills | 0 | 0 | 0 | 9 |
| starter | 0 | 0 | 0 | 5 |
| workflows | 0 | 0 | 0 | 5 |

**累计目标：** 70 天持续更新 ✅

---

### 🔗 今日提交

**openclaw-recommended-skills:**
- [x] DAILY_UPDATES.md 更新 x3（06:00 / 08:25 / 08:41）
- [x] 技巧 1：Cron 自动化最佳实践
- [x] 技巧 2：Session 隔离最佳实践
- [x] 技巧 3：模型切换最佳实践

**openclaw-starter:**
- [x] cron 场景配置模板
- [x] CONFIG_GUIDE.md 更新（cron/automation）
- [x] README.md 更新（cron-scenario 文档）

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

---

### 💡 补充技巧：Session 隔离最佳实践

**技能名称：** session-management  
**版本：** 1.0  
**类别：** 🔧 效率

**核心用法：**
```bash
# 独立搜索会话（避免上下文污染）
openclaw agent -m "搜索内容" --session-id search-$(date +%s)

# 独立任务会话
openclaw agent -m "执行任务" --session-id task-$(date +%Y%m%d)

# 批量操作使用 isolated session
openclaw cron add --sessionTarget isolated ...
```

**💡 技巧说明：**
1. **命名规范** - 使用 `search-时间戳`、`task-日期` 等清晰命名
2. **自动清理** - 定期清理过期 session，避免内存占用
3. **上下文隔离** - 每个独立任务使用独立 session，避免干扰主对话
4. **批量操作** - cron job 统一使用 isolated session 模式

**推荐场景：**
- 🔍 搜索操作：每次搜索独立 session
- 📊 数据分析：大批量数据处理用独立 session
- ⏰ 定时任务：cron 统一用 isolated 模式
- 🔄 模型切换：切换前后用不同 session

**相关配置：**
```bash
# 查看活跃 session
openclaw sessions list --active

# 清理过期 session
openclaw sessions cleanup --older-than 24h
```

---

### 💡 补充技巧 2：模型切换最佳实践

**技能名称：** model-switching  
**版本：** 1.0  
**类别：** 🔄 效率优化

**核心用法：**
```bash
# 查看当前模型
openclaw config get agents.defaults.model.primary

# 手动切换模型
openclaw models set <provider>/<model-name>

# 配置定时切换（cron）
openclaw cron add \
  --name "switch-to-night" \
  --schedule "0 22 * * *" \
  --message "切换到夜间低成本模型" \
  --sessionTarget main
```

**💡 技巧说明：**
1. **成本优化** - 夜间切到低成本模型，日间恢复高性能模型
2. **自动切换** - 使用 cron 实现全自动，无需手动操作
3. **快速回滚** - 配置好默认模型，切换失败自动回退
4. **日志追踪** - 记录每次切换时间，便于排查问题

**推荐配置：**
```json
{
  "schedule": { "kind": "cron", "expr": "0 22 * * *" },
  "payload": { "kind": "systemEvent", "text": "已切换到夜间模型" },
  "sessionTarget": "main"
}
```

**最佳实践：**
- 夜间（22:00）：切换到低成本模型执行后台任务
- 白天（09:00）：切换回默认模型用于日常交互
- 使用 `systemEvent` 类型提醒，主会话可见
- 定期检查切换日志确保正常执行

**相关资源：**
- [openclaw-starter/cron-scenario.json](https://github.com/xxuan66/openclaw-starter/blob/main/configs/cron-scenario.json)
- [openclaw-workflows/cron-automation.md](https://github.com/xxuan66/openclaw-workflows/blob/main/productivity/cron-automation.md)

---

**更新日期：** 2026-03-11 08:41  
**维护者：** [@xxuan66](https://github.com/xxuan66)  
**下次更新：** 2026-03-12 09:00 (Day 071)
