# 💻 开发类必备 Skill

> 开发者效率提升神器

---

## 🎯 适合人群

- ✅ 开发者/程序员
- ✅ GitHub 重度用户
- ✅ 需要代码审查
- ✅ 关注开源趋势

---

## 🏆 Top 5 推荐

### 1. github ⭐⭐⭐⭐⭐

**定位：** GitHub CLI 集成

**一句话：** GitHub 重度用户必备，CLI 集成效率翻倍

**推荐理由：**
- 📊 快速查看 Stars/Issues/PR 状态
- 🤖 CI/CD 状态监控
- 📝 Issue 管理（创建/更新/关闭）
- 🔔 重要事件通知提醒
- 🚀 PR 审查和合并

**典型场景：**
```bash
# 查看今日 Trending
openclaw agent -m "今天 GitHub trending 有哪些项目"

# 检查 PR 状态
openclaw agent -m "检查我的仓库 PR"

# 分析仓库数据
openclaw agent -m "分析我的 GitHub 项目访问数据"
```

**安装：**
```bash
clawhub install github
```

**配置：** ⭐⭐ 中等（需 GitHub Token）

---

### 2. skill-vetter ⭐⭐⭐⭐⭐

**定位：** Skill 安全审查

**一句话：** 安装 Skill 前的安全检查员

**推荐理由：**
- 🛡️ 安装前自动 vetting
- 🔍 权限范围审查
- ⚠️ 可疑代码检测
- 📋 文档完整性验证
- 🔒 依赖安全检查

**典型场景：**
```bash
# 安装新 Skill 前自动检查
clawhub install some-new-skill

# 手动检查
openclaw agent -m "检查 skill-vetter 的安全性"
```

**安装：**
```bash
clawhub install skill-vetter
```

**配置：** ⭐ 简单

---

### 3. github-trending ⭐⭐⭐⭐

**定位：** GitHub Trending 追踪

**一句话：** 发现热门开源项目，追踪技术趋势

**推荐理由：**
- 📊 发现热门开源项目
- 🔥 追踪技术趋势
- 💡 寻找优质项目参考
- ⏰ 支持今日/每周/每月筛选
- 🌍 多语言过滤

**典型场景：**
```bash
# 查看今日热门
openclaw agent -m "今天 GitHub trending 有哪些"

# 筛选 Python 项目
openclaw agent -m "Python 本周 trending 项目"

# 保存报告
openclaw agent -m "生成本周 trending 报告" --output trending.md
```

**安装：**
```bash
clawhub install github-trending
```

**配置：** ⭐ 简单（无需 API Key）

---

### 4. tavily-search ⭐⭐⭐⭐

**定位：** AI 优化搜索

**一句话：** 技术调研/竞品分析必备

**推荐理由：**
- 🤖 AI 优化，结果精准
- 📊 自动生成技术摘要
- 🔍 适合技术调研
- ⚡ 快速找到解决方案
- 📚 文档/教程搜索

**典型场景：**
```bash
# 技术调研
openclaw agent -m "调研 2026 年 AI Agent 框架"

# 查找解决方案
openclaw agent -m "Python 异步编程最佳实践"

# 竞品分析
openclaw agent -m "分析 OpenClaw 的竞争对手"
```

**安装：**
```bash
clawhub install tavily-search
```

**配置：** ⭐⭐ 中等（需 API Key）

---

### 5. self-improving-agent ⭐⭐⭐⭐⭐

**定位：** 让 Agent 持续学习

**一句话：** 开发效率提升神器

**推荐理由：**
- 🔄 记录开发经验教训
- 📈 避免重复错误
- 💡 积累最佳实践
- 🤖 代码审查建议
- 📝 自动生成文档

**安装：**
```bash
clawhub install self-improving-agent
```

**配置：** ⭐ 简单

---

## 💡 搭配建议

### 日常开发
```
github + skill-vetter + self-improving-agent
```

### 技术调研
```
github-trending + tavily-search
```

### 开源贡献
```
github + github-trending + skill-vetter
```

---

## 🔗 相关

- [每日精选](../daily/) - github 详细介绍
- [每周热门](../weekly/) - 开发类趋势
- [每月精选](../monthly/) - 深度评测

---

**更新日期：** 2026-03-13  
**维护者：** @xxuan66
