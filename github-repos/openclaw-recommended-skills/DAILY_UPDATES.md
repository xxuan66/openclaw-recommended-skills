# 📅 每日更新日志

> 每日记录三个项目的更新、新 Skill 推荐、使用技巧

**项目矩阵：**
- [openclaw-recommended-skills](https://github.com/xxuan66/openclaw-recommended-skills) - Skill 推荐
- [openclaw-starter](https://github.com/xxuan66/openclaw-starter) - 场景配置
- [openclaw-workflows](https://github.com/xxuan66/openclaw-workflows) - 自动化工作流

**🔒 安全规则：** [查看发布规则](../../GITHUB_PUBLISHING_RULES.md)

---

## 2026-03-10

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

## 2026-03-11

**主题：** Cron 自动化 + Session 隔离 + 模型切换

### ✅ 今日完成

#### openclaw-recommended-skills
- ✅ DAILY_UPDATES.md 更新
- ✅ 添加 Cron 自动化最佳实践
- ✅ 添加 Session 隔离最佳实践
- ✅ 添加模型切换最佳实践

#### openclaw-starter
- ✅ 添加 cron 场景配置模板
- ✅ CONFIG_GUIDE.md 更新（cron/automation）
- ✅ README.md 更新

#### openclaw-workflows
- ✅ 添加 cron-automation 工作流示例

---

### 💡 今日技巧 1：Cron 自动化最佳实践

**技能名称：** cron-automation  
**版本：** 1.0  
**类别：** ⏰ 自动化

**核心用法：**
```bash
# 添加定时任务
openclaw cron add --name "每日提醒" --cron "0 9 * * *" \
  --message "早上好！今天有什么计划？"

# 查看任务列表
openclaw cron list

# 运行任务（测试用）
openclaw cron run <task-id>

# 禁用/启用任务
openclaw cron disable <task-id>
openclaw cron enable <task-id>
```

**💡 技巧说明：**
1. **isolated session** - cron 任务默认使用 isolated session，避免干扰主对话
2. **announce 模式** - 使用 `--announce` 可以将结果发送到聊天
3. **测试先行** - 添加 cron 前先用 `cron run` 测试
4. **时间格式** - 支持标准 cron 表达式和 ISO 时间

**推荐场景：**
- ⏰ 每日提醒（起床、休息、发布）
- 📊 定时数据同步
- 🔄 模型自动切换
- 📝 内容自动生成

**相关配置：** [openclaw-starter/configs/cron-scenario.json](https://github.com/xxuan66/openclaw-starter/blob/main/configs/cron-scenario.json)

---

### 💡 今日技巧 2：Session 隔离最佳实践

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
1. **命名规范** - 使用 `search-时间戳 `、`task-日期` 等清晰命名
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

### 💡 今日技巧 3：模型切换最佳实践

**技能名称：** model-switching  
**版本：** 1.0  
**类别：** 🔄 效率优化

**核心用法：**
```bash
# 切换模型
openclaw models set <model-name>

# 查看当前模型
openclaw config get agents.defaults.model.primary

# 定时切换（cron）
openclaw cron add --name "切换到备用模型" --cron "0 22 * * *" \
  --message "openclaw models set <provider>/<model-name>"
```

**💡 技巧说明：**
1. **场景分离** - 夜间任务用备用模型（批量处理），日常对话用默认模型（响应快）
2. **自动切换** - 用 cron 定时切换，避免手动操作
3. **成本优化** - 批量任务用低成本模型，交互用高质量模型
4. **session 隔离** - 切换模型时用不同 session，避免上下文混乱

**推荐配置：**
```bash
# 晚上 22:00 切换到备用模型（夜间任务）
openclaw cron add --name "切换到备用模型" --cron "0 22 * * *" \
  --message "openclaw models set <provider>/<model-name>"

# 早上 9:00 切回默认模型（日常使用）
openclaw cron add --name "恢复默认模型" --cron "0 9 * * *" \
  --message "openclaw models set <default-model>"
```

---

### 🔗 今日提交

**openclaw-recommended-skills:**
- [x] DAILY_UPDATES.md 更新
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

### 📝 明日预告 (2026-03-12)

**主题：** 模型切换使用指南

**计划更新：**
- 📖 模型切换完整使用指南
- 🔧 starter 添加模型切换配置示例
- ⚡ workflows 添加自动切换工作流

---
