# 📱 微信公众号自动化发布指南

> 从申请账号到自动化发布完整教程

---

## 📋 目录

1. [申请微信公众号](#申请微信公众号)
2. [成为开发者](#成为开发者)
3. [配置脚本](#配置脚本)
4. [使用示例](#使用示例)
5. [常见问题](#常见问题)

---

## 🎯 第一步：申请微信公众号

### 1. 访问官网

**网址：** https://mp.weixin.qq.com

### 2. 选择账号类型

| 类型 | 适用 | 发布次数 | 难度 |
|------|------|---------|------|
| **订阅号** | 个人/媒体 | 每天 1 次 | ⭐⭐ |
| **服务号** | 企业/组织 | 每月 4 次 | ⭐⭐⭐⭐ |
| **企业微信** | 企业内部 | 不限 | ⭐⭐⭐ |

**推荐：** 个人选择**订阅号**

### 3. 准备材料

**个人订阅号：**
- ✅ 身份证
- ✅ 手机号
- ✅ 邮箱（未注册过微信）
- ✅ 微信扫码绑定管理员

**企业服务号：**
- ✅ 营业执照
- ✅ 对公账户
- ✅ 管理员身份证
- ✅ 运营者身份证

### 4. 注册流程

```
1. 打开 mp.weixin.qq.com
2. 点击右上角"立即注册"
3. 选择账号类型（订阅号）
4. 填写邮箱、密码
5. 激活邮箱
6. 填写主体信息（个人/企业）
7. 填写公众号信息（名称、介绍）
8. 扫码绑定管理员
9. 等待审核（1-3 个工作日）
```

### 5. 费用

- **个人订阅号：** 免费
- **企业认证服务号：** 300 元/年

---

## 🔧 第二步：成为开发者

### 1. 登录公众号

使用申请的账号登录 https://mp.weixin.qq.com

### 2. 进入开发设置

```
左侧菜单 → 设置与开发 → 基本配置
```

### 3. 创建应用

**需要：**
- **AppID** (应用唯一标识)
- **AppSecret** (应用密钥)

**步骤：**
1. 在"基本配置"页面找到 AppID 和 AppSecret
2. 点击"生成"或"重置" AppSecret
3. **立即复制并保存**（只显示一次！）

### 4. 配置 IP 白名单（可选但推荐）

```
IP 白名单 → 添加你的服务器 IP
```

**作用：** 提高安全性，防止 Token 被盗用

### 5. 测试 Token

使用脚本测试：
```bash
./wechat-publish.sh token
```

---

## ⚙️ 第三步：配置脚本

### 1. 编辑配置文件

打开脚本，修改配置区域：

```bash
nano /home/admin/.openclaw/workspace/scripts/wechat-publish.sh
```

### 2. 填写 AppID 和 AppSecret

```bash
# 修改前
APPID="YOUR_APPID_HERE"
APPSECRET="YOUR_APPSECRET_HERE"

# 修改后
APPID="wx1234567890abcdef"
APPSECRET="your_actual_appsecret_here"
```

### 3. 添加执行权限

```bash
chmod +x /home/admin/.openclaw/workspace/scripts/wechat-publish.sh
```

### 4. 安装依赖

```bash
# 需要 jq 处理 JSON
sudo apt install jq  # Ubuntu/Debian
# 或
brew install jq  # macOS
```

---

## 📝 第四步：使用示例

### 快速开始

```bash
# 1. 获取 Token
./wechat-publish.sh token

# 2. 上传封面图片
./wechat-publish.sh upload cover.jpg

# 3. 创建草稿
./wechat-publish.sh draft "我的第一篇文章" "<p>这里是 HTML 内容</p>" <封面 ID>

# 4. 发布文章
./wechat-publish.sh publish <草稿 ID>
```

### 完整示例

```bash
#!/bin/bash

# 发布一篇新文章

# 1. 上传封面
MEDIA_ID=$(./wechat-publish.sh upload /path/to/cover.jpg)

# 2. 准备内容（HTML 格式）
CONTENT="<h1>标题</h1><p>这里是正文...</p>"

# 3. 创建草稿
DRAFT_ID=$(./wechat-publish.sh draft "GitHub 项目每日更新自动化" "$CONTENT" "$MEDIA_ID")

# 4. 发布
./wechat-publish.sh publish "$DRAFT_ID"

echo "✅ 发布完成！"
```

### 高级用法

```bash
# 查看草稿列表
./wechat-publish.sh list

# 删除草稿
./wechat-publish.sh delete <草稿 ID>

# 检查发布状态
./wechat-publish.sh status <发布 ID>

# 获取 Token（不缓存）
./wechat-publish.sh token
```

---

## 🎨 内容格式说明

### HTML 支持

微信公众号支持标准 HTML：

```html
<h1>标题</h1>
<h2>副标题</h2>
<p>正文段落</p>
<strong>加粗</strong>
<em>斜体</em>
<a href="链接">链接文字</a>
<img src="图片 URL" />
```

### 样式建议

```html
<!-- 居中标题 -->
<h1 style="text-align: center;">标题</h1>

<!-- 引用块 -->
<blockquote style="border-left: 3px solid #ccc; padding-left: 10px;">
  引用内容
</blockquote>

<!-- 代码块 -->
<pre style="background: #f5f5f5; padding: 10px;">
<code>代码内容</code>
</pre>
```

---

## ⚠️ 常见问题

### Q1: Token 获取失败

**错误信息：** `invalid appid`

**解决：**
- 检查 AppID 是否正确
- 确认公众号已通过审核
- 等待 5 分钟后重试

### Q2: 发布失败

**错误信息：** `invalid media_id`

**解决：**
- 确认草稿 ID 正确
- 草稿创建后需要等待几秒
- 检查 Token 是否过期

### Q3: 图片上传失败

**错误信息：** `invalid image size`

**要求：**
- 格式：JPG/PNG
- 大小：< 2MB
- 尺寸：建议 900x383 像素

### Q4: 内容审核不通过

**原因：**
- 包含敏感词
- 涉及政治/色情/暴力
- 侵权内容

**解决：**
- 修改内容后重新提交
- 避免敏感话题
- 使用原创内容

### Q5: Token 缓存位置

**位置：** `/tmp/wechat_token.json`

**清除缓存：**
```bash
rm /tmp/wechat_token.json
```

---

## 🔒 安全建议

### 1. 保护 AppSecret

```bash
# ❌ 不要提交到 Git
git add wechat-publish.sh

# ✅ 使用环境变量
export WECHAT_APPID="xxx"
export WECHAT_APPSECRET="xxx"
```

### 2. 配置 IP 白名单

在公众号后台添加服务器 IP，防止 Token 被盗用。

### 3. 定期重置 AppSecret

建议每 3-6 个月重置一次 AppSecret。

### 4. 监控 API 调用

定期查看公众号后台的 API 调用记录。

---

## 📊 API 限制

| 接口 | 限制 |
|------|------|
| Token 获取 | 2000 次/小时 |
| 上传素材 | 1000 次/天 |
| 创建草稿 | 1000 次/天 |
| 发布文章 | 1000 次/天 |

---

## 🎯 下一步

1. ✅ 申请公众号（1-3 天）
2. ✅ 配置脚本（5 分钟）
3. ✅ 测试发布（10 分钟）
4. ✅ 集成到自动化流程

---

## 📞 官方文档

- [微信公众号开发文档](https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Overview.html)
- [草稿箱接口](https://developers.weixin.qq.com/doc/offiaccount/Draft_Box/Add_Draft.html)
- [发布接口](https://developers.weixin.qq.com/doc/offiaccount/Publish/Submit_publish_job.html)

---

**祝你发布顺利！** 🚀

**最后更新:** 2026-03-10
