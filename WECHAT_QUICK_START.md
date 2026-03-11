# 🚀 微信公众号自动化 - 快速入门

> 10 分钟上手指南

---

## 📋 准备工作

### 你需要

- [ ] 微信公众号账号（订阅号/服务号）
- [ ] AppID 和 AppSecret
- [ ] Linux/macOS 环境
- [ ] jq 工具

### 安装 jq

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install -y jq

# CentOS/RHEL
sudo yum install -y jq

# macOS
brew install jq
```

---

## ⚡ 三步配置

### 1️⃣ 编辑脚本

```bash
nano /home/admin/.openclaw/workspace/scripts/wechat-publish.sh
```

### 2️⃣ 填写配置

找到这两行（约第 10-11 行）：

```bash
APPID="YOUR_APPID_HERE"
APPSECRET="YOUR_APPSECRET_HERE"
```

改成你的：

```bash
APPID="wx1234567890abcdef"
APPSECRET="your_actual_secret_here"
```

### 3️⃣ 测试 Token

```bash
/home/admin/.openclaw/workspace/scripts/wechat-publish.sh token
```

**成功输出：**
```
🔑 获取 Access Token...
✅ Token 获取成功，有效期 120 分钟
f8d3a2b1c4e5...
```

---

## 📝 发布第一篇文章

### 方法一：命令行快速发布

```bash
# 1. 上传封面（可选）
./wechat-publish.sh upload /path/to/cover.jpg

# 2. 创建草稿
./wechat-publish.sh draft "标题" "<p>HTML 内容</p>" <封面 ID>

# 3. 发布
./wechat-publish.sh publish <草稿 ID>
```

### 方法二：使用示例脚本

```bash
# 创建发布脚本
cat > publish_my_article.sh << 'EOF'
#!/bin/bash

SCRIPT="/home/admin/.openclaw/workspace/scripts/wechat-publish.sh"

# 上传封面
COVER_ID=$($SCRIPT upload /path/to/cover.jpg)

# 内容（HTML 格式）
CONTENT="<h1>我的第一篇文章</h1><p>这里是正文...</p>"

# 创建草稿
DRAFT_ID=$($SCRIPT draft "GitHub 项目每日更新" "$CONTENT" "$COVER_ID")

# 发布
$SCRIPT publish "$DRAFT_ID"

echo "✅ 发布成功！"
EOF

chmod +x publish_my_article.sh
./publish_my_article.sh
```

---

## 🎯 完整工作流

### 每日自动发布

结合 GitHub 更新，实现自动发布：

```bash
# 早上 6 点
# 1. 更新 GitHub 项目
# 2. 生成更新日志
# 3. 发布到微信公众号

# 示例内容
CONTENT=$(cat << 'EOF'
<h2>🦞 OpenClaw 每日更新</h2>
<p>日期：2026-03-10</p>
<h3>今日完成：</h3>
<ul>
  <li>✅ openclaw-recommended-skills 更新</li>
  <li>✅ openclaw-starter 配置优化</li>
  <li>✅ openclaw-workflows 新增工作流</li>
</ul>
<p>欢迎访问：<a href="https://github.com/xxuan66">GitHub</a></p>
EOF
)

./wechat-publish.sh draft "OpenClaw 每日更新" "$CONTENT"
```

---

## 📊 常用命令速查

| 命令 | 说明 |
|------|------|
| `./wechat-publish.sh token` | 获取 Token |
| `./wechat-publish.sh upload cover.jpg` | 上传封面 |
| `./wechat-publish.sh draft "标题" "内容"` | 创建草稿 |
| `./wechat-publish.sh publish <ID>` | 发布文章 |
| `./wechat-publish.sh list` | 查看草稿 |
| `./wechat-publish.sh delete <ID>` | 删除草稿 |
| `./wechat-publish.sh help` | 显示帮助 |

---

## ⚠️ 注意事项

### 发布限制

- **订阅号：** 每天 1 次
- **服务号：** 每月 4 次

### 内容要求

- ✅ HTML 格式
- ✅ 图片需要上传获取 media_id
- ✅ 不能有敏感词
- ✅ 遵守微信公众平台规范

### Token 管理

- 自动缓存到 `/tmp/wechat_token.json`
- 有效期 120 分钟
- 提前 5 分钟自动刷新

---

## 🆘 遇到问题？

### 查看完整文档

```bash
cat /home/admin/.openclaw/workspace/WECHAT_OFFICIAL_ACCOUNT_GUIDE.md
```

### 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| `invalid appid` | AppID 错误 | 检查配置 |
| `invalid appsecret` | AppSecret 错误 | 重新生成 |
| `invalid media_id` | ID 不存在 | 重新上传 |
| `token expired` | Token 过期 | 删除缓存重试 |

---

## 🎉 下一步

1. ✅ 申请公众号 → [查看指南](./WECHAT_OFFICIAL_ACCOUNT_GUIDE.md)
2. ✅ 配置脚本
3. ✅ 测试发布
4. ✅ 集成自动化

---

**祝你使用愉快！** 🚀
