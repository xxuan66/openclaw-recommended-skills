# 🔧 Cookie 问题排查

## 当前问题

**错误信息：**
- `{'code': -1, 'success': False}` - 获取用户信息失败
- `{'code': 300011, 'success': False, 'msg': '当前账号存在异常'}` - 搜索失败

## 可能原因

### 1. Cookie 格式问题

**正确的 Cookie 应该是单行，没有换行：**

```bash
# ❌ 错误：多行
XHS_COOKIE=abRequestId=...;
  a1=...;
  web_session=...

# ✅ 正确：单行
XHS_COOKIE=abRequestId=...; a1=...; web_session=...; ...
```

### 2. 缺少必要字段

**搜索功能必需的字段：**
- ✅ `acw_tc` - 访问令牌
- ✅ `a1` - 用户标识
- ✅ `web_session` - 会话 ID
- ✅ `sec_poison_id` - 安全标识
- ⚠️ `b1` - 可能需要（当前缺失）

### 3. Cookie 过期

Cookie 有效期通常 7-30 天，过期后需要重新获取。

### 4. 账号风控

如果频繁操作或异地登录，可能被风控。

---

## 解决方案

### 方案 1：重新获取完整 Cookie

1. 浏览器打开 https://www.xiaohongshu.com
2. 登录账号
3. F12 → Network → 刷新
4. 点击请求 → 复制完整的 `cookie` 头
5. 确保是**单行**，包含所有字段

### 方案 2：检查 Cookie 格式

```bash
# 查看当前 Cookie
cat /home/admin/.openclaw/workspace/skills/xhs-note-creator/.env

# 应该是这样的格式：
# XHS_COOKIE=字段 1=值 1; 字段 2=值 2; ... (单行)
```

### 方案 3：测试发布功能

如果搜索不行，先测试发布功能是否正常：

```bash
cd /home/admin/.openclaw/workspace/skills/xhs-note-creator
node scripts/render_xhs_v2.js content/content_openclaw_v2.md -s xiaohongshu
cd output/*/
python ../../scripts/publish_xhs.py -t "测试" -i cover.png card_*.png
```

---

## 获取 b1 字段

如果确实缺少 `b1` 字段，尝试：

1. 清除浏览器 Cookie
2. 重新登录小红书
3. 立即复制 Cookie（包含所有字段）

---

**当前你的 Cookie 缺少 `b1` 字段，可能需要重新获取完整的 Cookie！**
