# 🔒 GitHub 安全规则

> ⚠️ **重要：** 每次操作 GitHub 后必须执行安全检查

---

## 📋 安全检查清单

### 每次推送前必查

- [ ] **敏感配置文件** - 确保没有 AGENTS.md, SOUL.md, USER.md, TOOLS.md 等
- [ ] **记忆文件** - 确保 memory/ 目录没有被跟踪
- [ ] **工作状态** - 确保 .openclaw/ 目录没有被跟踪
- [ ] **Skill 源码** - 确保 skills/ 目录没有被跟踪（应该在 ClawHub）
- [ ] **个人脚本** - 确保 scripts/ 目录没有被跟踪
- [ ] **微信运营** - 确保 wechat_articles/, wechat_daily/ 没有被跟踪
- [ ] **文件总数** - 确认文件数量合理（< 50）
- [ ] **大文件** - 确认没有 > 1MB 的文件

---

## 🛠️ 自动化工具

### 本地检查脚本

```bash
# 运行安全检查
cd /home/admin/.openclaw/workspace/github-repos/openclaw-recommended-skills
bash scripts/security-check.sh
```

### GitHub Actions 自动检查

每次 push/PR 会自动运行 `.github/workflows/security-check.yml`

---

## 📦 仓库定位

**应该包含：**
- ✅ README.md - 推荐清单
- ✅ skills-index.json - 机器可读索引
- ✅ top-picks/ - 月度精选
- ✅ examples/ - 使用案例
- ✅ recommendations/ - 分类推荐
- ✅ .github/ - Issue 模板和 Actions
- ✅ DAILY_UPDATES.md - 更新日志
- ✅ CONTRIBUTING.md - 贡献指南

**不应该包含：**
- ❌ AGENTS.md, SOUL.md, USER.md, TOOLS.md（私人配置）
- ❌ memory/（记忆文件）
- ❌ .openclaw/（工作状态）
- ❌ skills/（Skill 源码）
- ❌ scripts/（个人脚本）
- ❌ wechat_articles/, wechat_daily/（微信运营）
- ❌ paper_reading_notes/（论文笔记）
- ❌ 其他项目目录

---

## 🚨 泄露修复流程

如果发现敏感文件被推送：

### 1. 立即停止
```bash
# 不要继续任何操作
```

### 2. 从 Git 历史中移除
```bash
# 从跟踪中移除（不删除本地文件）
git rm --cached <敏感文件>

# 提交修复
git commit -m "fix: 移除敏感文件"

# 强制推送（会重写历史）
git push origin main --force
```

### 3. 更新 .gitignore
```bash
# 确保敏感文件在 .gitignore 中
echo "<敏感文件>" >> .gitignore
git add .gitignore
git commit -m "chore: 更新 .gitignore"
git push
```

### 4. 通知相关人员
- 如果有团队成员，立即通知
- 如果泄露了 API Key 等，立即撤销并重新生成

---

## 📊 检查记录

| 日期 | 操作 | 检查结果 | 操作人 |
|------|------|---------|--------|
| 2026-03-13 | 清理敏感文件 | ✅ 通过 | OpenClaw |
| 2026-03-13 | 创建安全检查机制 | ✅ 通过 | OpenClaw |

---

## 🔗 相关文档

- [CONTRIBUTING.md](./CONTRIBUTING.md) - 贡献指南
- [.gitignore](./.gitignore) - Git 忽略规则
- [scripts/security-check.sh](./scripts/security-check.sh) - 检查脚本

---

**最后更新：** 2026-03-13  
**维护者：** @xxuan66
