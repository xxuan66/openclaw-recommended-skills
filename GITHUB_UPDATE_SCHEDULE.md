# 📅 GitHub 每日更新计划

> 自动化模型切换 + GitHub 更新

---

## ⏰ 更新时间表

| 时间 | 任务 | 模型 | 说明 |
|------|------|------|------|
| **06:00** | GitHub 每日更新 | mimo | 切换模型 → 执行更新 → 记录日志 |
| **09:00** | 恢复默认模型 | qwen | 切回 qwen3.5-plus，供日常使用 |

**更新窗口：** 3 小时（06:00-09:00）

---

## 📋 已配置的定时任务

### 1️⃣ GitHub 每日更新

- **Cron:** `0 6 * * *` (每天早上 6 点)
- **模型:** mimo/mimo-claw-0301
- **脚本:** `/home/admin/.openclaw/workspace/scripts/github-daily-update.sh`
- **任务 ID:** `4d7ebe29-d315-4e61-b146-004ef1b3c52a`

**执行内容：**
1. 切换到 mimo 模型
2. 更新 openclaw-recommended-skills
3. 更新 openclaw-starter
4. 更新 openclaw-workflows
5. 更新 DAILY_UPDATES.md
6. 切回 qwen 模型

---

### 2️⃣ 恢复默认模型

- **Cron:** `0 9 * * *` (每天早上 9 点)
- **模型:** bailian/qwen3.5-plus
- **脚本:** `/home/admin/.openclaw/workspace/scripts/restore-default-model.sh`
- **任务 ID:** `d1c590bd-010a-4ddf-933a-e4d4d50cf32c`

**执行内容：**
1. 切换到 qwen3.5-plus 模型
2. 确认切换成功

---

## 📁 相关脚本

### github-daily-update.sh

**位置:** `/home/admin/.openclaw/workspace/scripts/github-daily-update.sh`

**功能:**
- 切换到 mimo 模型
- 执行三个 GitHub 项目的每日更新
- 切回 qwen 模型
- 输出更新日志

### restore-default-model.sh

**位置:** `/home/admin/.openclaw/workspace/scripts/restore-default-model.sh`

**功能:**
- 切换到 qwen3.5-plus 模型
- 确认切换成功

---

## 📊 查看任务状态

```bash
# 查看所有 cron 任务
openclaw cron list

# 查看任务详情
openclaw cron get --id <task-id>

# 手动触发 GitHub 更新（测试用）
openclaw cron trigger --id 4d7ebe29-d315-4e61-b146-004ef1b3c52a
```

---

## 🔧 管理任务

### 暂停任务

```bash
# 暂停 GitHub 更新
openclaw cron disable --id 4d7ebe29-d315-4e61-b146-004ef1b3c52a

# 暂停恢复模型
openclaw cron disable --id d1c590bd-010a-4ddf-933a-e4d4d50cf32c
```

### 恢复任务

```bash
# 恢复 GitHub 更新
openclaw cron enable --id 4d7ebe29-d315-4e61-b146-004ef1b3c52a

# 恢复恢复模型
openclaw cron enable --id d1c590bd-010a-4ddf-933a-e4d4d50cf32c
```

### 删除任务

```bash
# 删除 GitHub 更新
openclaw cron remove --id 4d7ebe29-d315-4e61-b146-004ef1b3c52a

# 删除恢复模型
openclaw cron remove --id d1c590bd-010a-4ddf-933a-e4d4d50cf32c
```

---

## 📝 更新日志

每日更新记录在：
- [DAILY_UPDATES.md](https://github.com/xxuan66/openclaw-recommended-skills/blob/main/DAILY_UPDATES.md)

---

## ⚠️ 注意事项

1. **确保 Gateway 运行:** cron 任务需要 Gateway 运行
2. **检查执行日志:** 定期查看 cron 任务执行状态
3. **模型切换:** 切换无需重启 Gateway
4. **失败处理:** 如果任务失败，可以手动触发

---

## 🎯 下次执行时间

| 任务 | 下次执行 |
|------|---------|
| GitHub 每日更新 | 明日 06:00 |
| 恢复默认模型 | 明日 09:00 |

---

**创建日期:** 2026-03-10  
**维护者:** @xxuan66
