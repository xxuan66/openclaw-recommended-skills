# 🔒 GitHub 内容发布安全规则

> 保护敏感信息，安全发布内容

**最后更新:** 2026-03-10  
**适用范围:** 所有 GitHub 项目更新

---

## 🚫 禁止发布的内容

### 1️⃣ 模型配置信息 ❌

**绝对禁止发布：**

```diff
- 模型名称：mimo/mimo-claw-0301
- 模型 API 地址：https://api.xiaomimimo.com/v1
- 模型 API Key: sk-c4h73yssf547yzc7ixesji634nhvcn4y8gw60kxe3x8i3cbv
- 模型配置详情：openclaw.json 中的 models.providers.mimo 部分
```

**正确做法：**
```markdown
✅ 使用通用描述：
- "备用模型"
- "fallback 模型"
- "Provider B"
- "<provider>/<model-name>"
```

---

### 2️⃣ API Keys 和凭证 ❌

**绝对禁止发布：**

```diff
- 任何 API Key (sk-xxx, ghp_xxx 等)
- Access Token
- Password/密码
- Secret/密钥
- Private Key/私钥
```

**正确做法：**
```markdown
✅ 使用占位符：
- `sk-xxx` 或 `YOUR_API_KEY`
- `<your-token>`
- `[已配置]`
- `[已隐藏]`
```

---

### 3️⃣ 个人/公司敏感信息 ❌

**绝对禁止发布：**

```diff
- 真实姓名（除非公开）
- 身份证号/护照号
- 手机号/个人邮箱
- 家庭地址
- 公司内部 IP 地址
- 服务器配置详情
- 数据库连接字符串
```

**正确做法：**
```markdown
✅ 使用通用描述：
- "用户 @xxuan66" (GitHub 用户名可公开)
- "某云服务器"
- "本地环境"
- "生产环境"
```

---

### 4️⃣ 配置文件原文 ❌

**禁止直接发布：**

```diff
- openclaw.json 完整内容
- 包含敏感信息的配置文件
- 环境变量文件 (.env)
- 数据库配置文件
```

**正确做法：**
```markdown
✅ 发布脱敏版本：
- 只展示结构，不展示值
- 用 `***` 或 `xxx` 替换敏感部分
- 提供配置模板（不含真实值）
```

**示例：**
```json
{
  "models": {
    "providers": {
      "bailian": {
        "apiKey": "***",
        "baseUrl": "https://***"
      },
      "mimo": {
        "apiKey": "***",
        "baseUrl": "***"
      }
    }
  }
}
```

---

## ✅ 可以发布的内容

### 安全内容清单

| 类型 | 示例 | 状态 |
|------|------|------|
| 项目 README | 功能介绍、使用说明 | ✅ 安全 |
| 使用技巧 | 命令示例、最佳实践 | ✅ 安全 |
| 工作流示例 | 配置步骤（不含密钥） | ✅ 安全 |
| 更新日志 | Day XXX 更新内容 | ✅ 安全 |
| 统计数据 | Stars/Forks/Issues 数量 | ✅ 安全 |
| 场景配置说明 | 配置用途说明 | ✅ 安全 |
| 脚本代码 | 不含密钥的自动化脚本 | ✅ 安全 |

---

## 📝 发布前检查清单

### 每次发布前必查

**文件内容检查：**

- [ ] 没有 API Keys
- [ ] 没有模型具体名称（用通用名）
- [ ] 没有个人敏感信息
- [ ] 没有配置文件原文
- [ ] 没有服务器/数据库配置
- [ ] 没有内部网络信息

**Git 提交检查：**

- [ ] `.gitignore` 已配置
- [ ] 没有误提交敏感文件
- [ ] 提交信息不包含敏感内容

**GitHub 设置检查：**

- [ ] 仓库是 Public（除非特殊要求）
- [ ] 没有启用不必要的集成
- [ ] Webhook 配置安全

---

## 🔧 技术防护措施

### 1. .gitignore 配置

```gitignore
# 敏感配置文件
openclaw.json
*.env
*.local.json
*.secret
*.key

# 日志文件
*.log

# 临时文件
tmp/
temp/
```

### 2. 使用环境变量

**错误做法：**
```bash
# ❌ 硬编码 API Key
API_KEY="sk-xxx"
```

**正确做法：**
```bash
# ✅ 使用环境变量
API_KEY="${API_KEY:-}"
```

### 3. 配置检查脚本

```bash
#!/bin/bash
# check-secrets.sh

echo "🔍 检查敏感信息..."

# 检查 API Keys
if grep -r "sk-[a-zA-Z0-9]" . --exclude="*.md"; then
  echo "❌ 发现 API Key!"
  exit 1
fi

# 检查模型名称
if grep -r "mimo-claw-0301" . --exclude="*.md"; then
  echo "❌ 发现敏感模型名称!"
  exit 1
fi

echo "✅ 检查通过"
```

---

## 📋 违规处理流程

### 如果发现敏感信息已发布

**立即执行：**

1. **删除敏感内容**
   ```bash
   git reset --hard HEAD~1  # 撤销提交
   ```

2. **从 Git 历史中彻底删除**
   ```bash
   git filter-branch --force --index-filter \
     'git rm --cached --ignore-unmatch path/to/sensitive/file' \
     --prune-empty --tag-name-filter cat -- --all
   ```

3. **通知 GitHub 删除缓存**
   - 联系 GitHub Support
   - 请求删除 cached views

4. **更换泄露的凭证**
   - 立即更换 API Key
   - 更新所有使用处

---

## 🎯 发布流程规范

### 标准发布流程

```
1. 准备内容
   ↓
2. 自我审查（检查清单）
   ↓
3. 技术检查（脚本扫描）
   ↓
4. 提交到本地 Git
   ↓
5. 再次检查 diff
   ↓
6. Push 到 GitHub
   ↓
7. 确认发布内容
```

### 审查要点

| 审查项 | 检查内容 | 负责人 |
|--------|---------|--------|
| 内容审查 | 无敏感信息 | 发布者 |
| 技术审查 | 脚本扫描通过 | 自动化 |
| 最终审查 | GitHub 预览确认 | 发布者 |

---

## 📚 相关文档

- [GitHub 更新计划](./GITHUB_UPDATE_SCHEDULE.md)
- [每日更新日志](https://github.com/xxuan66/openclaw-recommended-skills/blob/main/DAILY_UPDATES.md)
- [内容安全最佳实践](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure)

---

## ⚠️ 违规后果

**可能导致的后果：**

1. **安全风险** - API 被盗用，产生费用
2. **隐私泄露** - 个人信息暴露
3. **账号风险** - GitHub 账号被封
4. **法律风险** - 违反服务条款

**请务必遵守！**

---

## 📞 如有疑问

**不确定是否能发布？**

1. 问自己：这个信息泄露会有风险吗？
2. 如果有疑问，就不要发布
3. 可以私下讨论，不要公开

---

**安全第一，发布第二！** 🔒
