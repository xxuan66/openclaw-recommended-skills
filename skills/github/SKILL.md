---
name: github
description: "GitHub 运营和自动化工具。支持每日内容更新、多仓库管理、PR/CI 操作、安全发布。专为 OpenClaw GitHub 运营设计。"
---

# GitHub Skill - 增强版

> 针对 GitHub 运营优化，支持每日更新、多仓库管理、安全发布。

## 📋 核心概念

### 仓库结构
当前维护的 4 个核心仓库（全部每日更新）：
- **openclaw-recommended-skills** - Skill 推荐（⭐ 主仓库）
- **openclaw-starter** - 场景配置
- **openclaw-workflows** - 自动化工作流
- **agent-learning-path** - Agent 学习教程

### 更新策略
| 仓库 | 频率 | 策略 |
|------|------|------|
| openclaw-recommended-skills | 每日 | 小步迭代，完善现有内容 |
| openclaw-starter | 每日 | 添加/优化场景配置 |
| openclaw-workflows | 每日 | 添加/优化工作流示例 |
| agent-learning-path | 每日 | 小幅度迭代优化，修复错误，补充内容 |

### 认证方式
使用 Token 认证，URL 格式：
```bash
https://x-access-token:ghp_xxx@github.com/owner/repo.git
```

### 命名规范
- **日期格式：** yyyy-mm-dd（不用 Day XXX）
- **提交信息：** 简洁明了，中文为主
- **分支：** main 分支

---

## 🔄 每日更新操作

### 标准流程
每天 06:00 自动执行（通过 cron），流程：
```
1. 切换到备用模型（夜间任务）
2. 更新 4 个仓库内容
3. 切回默认模型
4. 发送完成通知
```

### 手动执行每日更新
```bash
# 执行完整的每日更新
/home/admin/.openclaw/workspace/scripts/github-daily-update.sh
```

### 单个仓库更新
```bash
# 切换到仓库目录
cd /home/admin/.openclaw/workspace/github-repos/openclaw-recommended-skills

# 拉取最新
git pull origin main

# 编辑内容（例如更新 DAILY_UPDATES.md）
# ... 编辑 ...

# 提交并推送
git add -A
git commit -m "yyyy-mm-dd: 更新内容描述"
git push origin main
```

### 批量更新所有仓库
```bash
# 更新所有 3 个仓库
for repo in openclaw-recommended-skills openclaw-starter openclaw-workflows; do
  cd /home/admin/.openclaw/workspace/github-repos/$repo
  git pull origin main
  # 执行更新操作...
  git add -A
  git commit -m "$(date +%Y-%m-%d): 每日更新"
  git push origin main
done
```

---

## 📦 仓库管理

### 克隆仓库
```bash
# 使用 Token 克隆（推荐）
git clone https://x-access-token:ghp_xxx@github.com/xxuan66/repo-name.git

# 或配置远程
cd /path/to/local/repo
git remote set-url origin https://x-access-token:ghp_xxx@github.com/xxuan66/repo-name.git
```

### 查看仓库状态
```bash
# 查看当前状态
cd /home/admin/.openclaw/workspace/github-repos/openclaw-recommended-skills
git status
git log --oneline -5

# 查看远程配置
git remote -v
```

### 创建新仓库
```bash
# 通过 GitHub CLI（如果有 gh）
gh repo create xxuan66/repo-name --public --description "描述"

# 或通过 API
curl -H "Authorization: token ghp_xxx" \
  https://api.github.com/user/repos \
  -d '{"name":"repo-name","description":"描述","public":true}'
```

### 删除仓库
```bash
# 通过 API（谨慎操作）
curl -X DELETE -H "Authorization: token ghp_xxx" \
  https://api.github.com/repos/xxuan66/repo-name
```

---

## 📝 内容发布

### 安全发布规则
**重要：** 发布前必须检查！

```bash
# 运行安全检查脚本
/home/admin/.openclaw/workspace/scripts/check-github-secrets.sh
```

**禁止发布的内容：**
- API Keys (sk-xxx, ghp_xxx)
- 模型具体名称（mimo-claw-0301）
- 个人敏感信息
- 配置文件原文（openclaw.json）
- 服务器/数据库配置

**可以发布的内容：**
- 项目 README、使用说明
- 使用技巧、最佳实践
- 工作流示例（不含密钥）
- 更新日志（用日期格式）
- 统计数据（Stars/Forks/Issues）

### 发布流程
```
1. 准备内容（检查安全规则）
2. 自我审查（检查清单）
3. 技术检查（脚本扫描）
4. 提交到本地 Git
5. 再次检查 diff
6. Push 到 GitHub
7. 确认发布内容
```

### 提交规范
```bash
# 好的提交信息
git commit -m "2026-03-11: 添加 Cron 自动化最佳实践"
git commit -m "2026-03-11: 更新框架对比（新增 LangChain 入门）"

# 避免
git commit -m "update"
git commit -m "fix"
```

---

## 🔧 常用操作

### Git 操作
```bash
# 查看提交历史
git log --oneline -10

# 查看文件变化
git diff HEAD~1

# 撤销上次提交（保留文件）
git reset --soft HEAD~1

# 强制推送（谨慎使用）
git push origin main --force
```

### Token 配置
```bash
# 配置 Token（用于 HTTPS 推送）
git remote set-url origin https://x-access-token:YOUR_TOKEN@github.com/owner/repo.git

# 查看当前配置
git remote -v
```

### 分支操作
```bash
# 创建新分支
git checkout -b feature/new-feature

# 切换分支
git checkout main

# 合并分支
git merge feature/new-feature
```

---

## 📊 统计和监控

### 查看仓库统计
```bash
# 通过 API 获取 Stars/Forks
curl -s https://api.github.com/repos/xxuan66/openclaw-recommended-skills \
  | jq '.stargazers_count, .forks_count, .open_issues_count'

# 查看最近提交
curl -s https://api.github.com/repos/xxuan66/openclaw-recommended-skills/commits \
  | jq '.[].commit.message'
```

### 监控 Issues
```bash
# 列出 Issues
curl -s https://api.github.com/repos/xxuan66/openclaw-recommended-skills/issues \
  | jq '.[] | {title, state, created_at}'

# 创建 Issue
curl -X POST -H "Authorization: token ghp_xxx" \
  https://api.github.com/repos/xxuan66/openclaw-recommended-skills/issues \
  -d '{"title":"Issue title","body":"Issue body"}'
```

### 查看 PR 状态
```bash
# 使用 gh CLI
gh pr list --repo xxuan66/openclaw-recommended-skills
gh pr checks 55 --repo xxuan66/openclaw-recommended-skills
```

---

## ⚙️ OpenClaw 集成

### Cron 任务配置
GitHub 更新已配置为 cron 任务：
- **任务 ID:** 4d7ebe29-d315-4e61-b146-004ef1b3c52a
- **执行时间:** 每天 06:00
- **模型:** 备用模型（夜间）→ 默认模型（日常）

### 查看任务状态
```bash
openclaw cron list | grep GitHub
```

### 手动触发
```bash
openclaw cron run 4d7ebe29-d315-4e61-b146-004ef1b3c52a
```

### 任务脚本
```bash
# 每日更新脚本
/home/admin/.openclaw/workspace/scripts/github-daily-update.sh

# 安全检查脚本
/home/admin/.openclaw/workspace/scripts/check-github-secrets.sh
```

---

## 🚨 故障排除

### 推送失败
```bash
# 检查 Token 是否有效
curl -H "Authorization: token ghp_xxx" https://api.github.com/user

# 重新配置远程
git remote set-url origin https://x-access-token:ghp_xxx@github.com/owner/repo.git

# 强制推送（谨慎）
git push origin main --force
```

### 认证问题
```bash
# 检查 Token 权限
curl -s -H "Authorization: token ghp_xxx" \
  https://api.github.com/repos/owner/repo \
  | jq '.permissions'
```

### 仓库冲突
```bash
# 拉取最新并合并
git pull origin main --rebase

# 解决冲突后推送
git push origin main
```

---

## 📚 相关文件

- **每日更新脚本:** `/home/admin/.openclaw/workspace/scripts/github-daily-update.sh`
- **安全检查脚本:** `/home/admin/.openclaw/workspace/scripts/check-github-secrets.sh`
- **发布规则:** `/home/admin/.openclaw/workspace/GITHUB_PUBLISHING_RULES.md`
- **更新计划:** `/home/admin/.openclaw/workspace/GITHUB_UPDATE_SCHEDULE.md`
- **仓库目录:** `/home/admin/.openclaw/workspace/github-repos/`

---

## 💡 最佳实践

1. **每日更新：** 自动执行，手动检查结果
2. **安全第一：** 发布前务必运行安全检查
3. **日期格式：** 统一使用 yyyy-mm-dd
4. **提交信息：** 简洁明了，中文为主
5. **Token 管理：** 定期轮换，权限最小化
6. **备份习惯：** 重要内容本地备份
7. **监控指标：** 关注 Stars/Forks/Issues 变化

---

**最后更新:** 2026-03-11  
**维护者:** xuan  
**适用范围:** OpenClaw GitHub 运营
