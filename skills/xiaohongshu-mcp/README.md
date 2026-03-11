# ⚠️ xiaohongshu-mcp 使用说明

## 当前状态

**已安装但无法使用** - 需要解决登录问题

---

## 问题原因

`xiaohongshu-mcp` 需要：

1. **运行本地服务器**
   ```bash
   xiaohongshu-mcp-server  # 监听 localhost:18060
   ```

2. **扫码登录**
   ```bash
   xiaohongshu-mcp-login   # 弹出二维码
   ```

3. **Linux 服务器限制**
   - ❌ 无图形界面，无法显示二维码
   - ❌ 无法使用官方登录工具
   - ❌ 服务器无法访问

---

## 解决方案

### 方案 1：本地运行服务器（推荐）

**在你的本地电脑（有浏览器）运行：**

```bash
# macOS
brew install xiaohongshu-mcp
xiaohongshu-mcp-server

# Windows
# 下载 https://github.com/xpzouying/xiaohongshu-mcp/releases
xiaohongshu-mcp-server.exe
```

**然后在服务器上通过 API 调用：**

```bash
# 修改 xhs_client.py 的 BASE_URL
# 从 localhost:18060 改为你的电脑 IP:18060
```

### 方案 2：使用网页版 Cookie（当前方案）

**继续使用 `xhs-note-creator` 的发布功能：**

```bash
cd xhs-note-creator/
python scripts/publish_xhs.py -t "标题" -i cover.png card_*.png
```

**市场调研手动完成：**
1. 浏览器打开小红书网页版
2. 手动搜索热门笔记
3. 复制内容给 AI 分析

### 方案 3：使用其他 API 服务

寻找提供 HTTP API 的小红书数据服务，无需本地服务器。

---

## 当前可用功能

| 功能 | 状态 | 替代方案 |
|------|------|---------|
| **发布笔记** | ✅ xhs-note-creator | 正常使用 |
| **图片渲染** | ✅ xhs-note-creator | 正常使用 |
| **文案生成** | ✅ xhs-note-creator | 正常使用 |
| **搜索热门** | ❌ 需要服务器 | 手动网页搜索 |
| **数据分析** | ❌ 需要服务器 | 手动查看 |
| **获取详情** | ❌ 需要服务器 | 手动查看 |

---

## 建议

**暂时只用 `xhs-note-creator`**，等有机会在本地电脑运行服务器时再启用 `xiaohongshu-mcp` 的数据功能。

**市场调研替代方案：**
1. 浏览器访问 https://www.xiaohongshu.com
2. 搜索关键词
3. 记录热门笔记的标题、点赞、收藏
4. 让 AI 分析爆款特点

---

**最后更新：** 2026-03-06
