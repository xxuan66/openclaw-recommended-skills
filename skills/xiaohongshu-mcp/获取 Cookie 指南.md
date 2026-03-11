# 🔐 如何获取小红书 Cookie

## 方法 1：浏览器获取（推荐）

### 步骤

1. **打开小红书网页版**
   ```
   https://www.xiaohongshu.com
   ```

2. **登录账号**
   - 使用手机号/微信扫码登录

3. **打开开发者工具**
   - 按 `F12` 或右键 → 检查
   - 切换到 **Network** 标签

4. **刷新页面**
   - 按 `F5` 刷新
   - 查看 Network 中的请求

5. **复制 Cookie**
   - 点击任意请求（如 `api/sns/web/v1/homefeed`）
   - 查看 **Request Headers**
   - 找到 `cookie` 字段
   - 复制完整值

6. **更新配置**
   ```bash
   vim /home/admin/.openclaw/workspace/skills/xhs-note-creator/.env
   ```
   
   替换 `XHS_COOKIE=...` 后面的内容

---

## 方法 2：使用浏览器插件

### Chrome/Edge 插件

1. 安装 **EditThisCookie** 或 **Cookie Editor**
2. 打开小红书网页版
3. 点击插件图标
4. 点击 **Export** → **JSON**
5. 复制 cookie 字段

---

## Cookie 格式示例

```
XHS_COOKIE=acw_tc=0a00d8df...; a1=19cbbbf171...; web_session=040069...; sec_poison_id=...; ...
```

**必要字段：**
- ✅ `acw_tc` - 访问令牌
- ✅ `a1` - 用户标识（搜索必需）
- ✅ `web_session` - 会话 ID
- ✅ `sec_poison_id` - 安全标识

---

## 更新 Cookie

```bash
# 编辑配置文件
vim /home/admin/.openclaw/workspace/skills/xhs-note-creator/.env

# 或直接用命令替换
echo 'XHS_COOKIE=你的新_cookie' > /home/admin/.openclaw/workspace/skills/xhs-note-creator/.env
```

---

## 测试 Cookie

```bash
cd /home/admin/.openclaw/workspace/skills/xiaohongshu-mcp
source ../xhs-note-creator/.venv/bin/activate

# 测试登录状态
python scripts/xhs_api.py status

# 测试搜索
python scripts/xhs_api.py search "AI 工具"
```

---

## 注意事项

1. **Cookie 有效期** - 通常 7-30 天
2. **不要分享** - Cookie 包含登录凭证
3. **及时更新** - 失效后重新获取
4. **账号安全** - 不要在多个地方同时登录

---

**获取到新 Cookie 后，运行测试命令验证！**
