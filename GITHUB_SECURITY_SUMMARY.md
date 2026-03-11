# 🔒 GitHub 内容安全总结

> 保护敏感信息，安全发布内容

---

## 📋 已创建的安全文档

| 文档 | 位置 | 用途 |
|------|------|------|
| **发布规则** | `GITHUB_PUBLISHING_RULES.md` | 详细的安全规则 |
| **检查脚本** | `scripts/check-github-secrets.sh` | 发布前自动检查 |
| **.gitignore** | 各项目的 `.gitignore` | 防止敏感文件被提交 |

---

## 🚫 禁止发布的内容

### 绝对禁止

1. **模型配置信息**
   - ❌ mimo 模型名称
   - ❌ API 地址
   - ❌ API Keys

2. **凭证信息**
   - ❌ API Keys (sk-xxx, ghp_xxx)
   - ❌ Access Tokens
   - ❌ Passwords
   - ❌ Secrets

3. **个人信息**
   - ❌ 真实姓名（除非公开）
   - ❌ 手机号/个人邮箱
   - ❌ 身份证号

4. **配置文件原文**
   - ❌ openclaw.json
   - ❌ .env 文件
   - ❌ 包含敏感信息的配置

---

## ✅ 安全发布流程

### 发布前必做

```bash
# 1. 运行安全检查
./scripts/check-github-secrets.sh ./github-repos

# 2. 检查输出
# ✅ 通过 → 可以发布
# ❌ 失败 → 修复问题

# 3. 再次确认
git diff  # 查看将要提交的内容
```

### 发布后检查

- 在 GitHub 上预览文件
- 确认没有敏感信息
- 检查 .gitignore 是否生效

---

## 🛡️ 技术防护

### .gitignore 已配置

**所有项目已添加：**
```gitignore
# 敏感配置
openclaw.json
*.env
*.local.json
*.secret
*.key

# 凭证
credentials.json
token.json
auth.json
```

### 检查脚本

**功能：**
- ✅ 扫描 API Keys
- ✅ 检测敏感模型名称
- ✅ 查找 GitHub Tokens
- ✅ 检查密码配置
- ✅ 验证 .gitignore

**用法：**
```bash
./scripts/check-github-secrets.sh [目录]
```

---

## 📝 正确做法示例

### 提到模型

```diff
- 错误：使用 mimo/mimo-claw-0301 模型
+ 正确：使用备用模型
+ 更好：使用 Provider B
```

### 提到配置

```diff
- 错误：apiKey: sk-c4h73yssf547yzc7
+ 正确：apiKey: "***"
+ 更好：apiKey: <your-api-key>
```

### 提到 API

```diff
- 错误：https://api.xiaomimimo.com/v1
+ 正确：https://api.example.com/v1
+ 更好：API 地址（已配置）
```

---

## ⚠️ 违规处理

### 如果不小心发布了敏感信息

1. **立即删除**
   ```bash
   git reset --hard HEAD~1
   ```

2. **从历史中清除**
   ```bash
   git filter-branch --force --index-filter \
     'git rm --cached --ignore-unmatch sensitive-file' \
     --prune-empty --tag-name-filter cat -- --all
   ```

3. **更换凭证**
   - 立即更换 API Key
   - 更新所有使用处

4. **通知 GitHub**
   - 联系 GitHub Support
   - 请求删除缓存

---

## 🎯 日常检查

### 每日更新前

- [ ] 运行检查脚本
- [ ] 确认无敏感信息
- [ ] 检查 .gitignore
- [ ] 预览 git diff

### 每周审查

- [ ] 检查已发布内容
- [ ] 更新安全规则
- [ ] 审查 .gitignore
- [ ] 检查脚本更新

---

## 📚 相关文档

- [发布规则详情](./GITHUB_PUBLISHING_RULES.md)
- [更新计划](./GITHUB_UPDATE_SCHEDULE.md)
- [每日更新日志](https://github.com/xxuan66/openclaw-recommended-skills/blob/main/DAILY_UPDATES.md)

---

## 💡 最佳实践

1. **有疑问就不发** - 不确定是否安全，就不要发布
2. **脱敏处理** - 用 `***` 或 `<xxx>` 替换敏感内容
3. **最小化原则** - 只发布必要的内容
4. **双重检查** - 发布前至少检查两次
5. **自动化检查** - 使用脚本辅助检查

---

**安全第一，发布第二！** 🔒

**最后更新:** 2026-03-10  
**维护者:** @xxuan66
