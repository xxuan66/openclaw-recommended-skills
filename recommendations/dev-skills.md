# 💻 开发类 Skill 推荐

## 1. github

**版本:** 1.0.0  
**Slug:** `github`  
**类别:** 开发  

### 简介
使用 `gh` CLI 与 GitHub 交互。支持 issue、PR、CI runs 和高级 API 查询。

### 推荐理由
- ✅ 完整的 GitHub 功能
- ✅ 官方 CLI 支持
- ✅ 适合自动化工作流
- ✅ 免费使用

### 安装命令
```bash
clawhub install github
```

### 配置要求
- 需要安装 gh CLI
- 需要 GitHub Token (可选，用于认证)

### 使用示例
```bash
# 查看 PR 的 CI 状态
gh pr checks 55 --repo owner/repo

# 列出 workflow runs
gh run list --repo owner/repo --limit 10

# 查看失败日志
gh run view <run-id> --repo owner/repo --log-failed
```

---

## 2. skill-vetter

**版本:** 1.0.0  
**Slug:** `skill-vetter`  
**类别:** 开发/安全  

### 简介
安全优先的 Skill 审查工具。在安装任何 Skill 前检查红旗、权限范围、可疑模式。

### 推荐理由
- ✅ 安全检查
- ✅ 权限审查
- ✅ 风险识别
- ✅ 保护隐私

### 安装命令
```bash
clawhub install skill-vetter
```

### 配置要求
- 无需额外配置

### 使用场景
1. 安装新 Skill 前
2. 审查 Skill 权限
3. 识别潜在风险
4. 安全审计

---

## 对比总结

| Skill | 开发效率 | 安全性 | 必需性 |
|-------|----------|--------|--------|
| github | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| skill-vetter | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

**推荐:** 两者都是必备，github 提效，skill-vetter 保安全
