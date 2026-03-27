# 🎯 按场景找 Skills

> 不要问"这个 Skill 有什么用"，要问"我想解决这个问题，该用什么 Skill"

---

## 📌 三大核心场景

### 💰 搞钱/变现

**适合人群：** 自媒体运营、副业探索、个人品牌打造

**核心需求：**
- ✅ 自动化内容创作与发布
- ✅ 多平台账号管理
- ✅ 数据分析和涨粉
- ✅ 副业机会监控

**推荐 Skills：**

| Skill | 来源 | 用途 | 安装命令 |
|-------|------|------|----------|
| `wechat-operator` | 自研 | 公众号一体化运营 | 已安装 |
| `xiaohongshu-mcp` | 自研 | 小红书自动化发布 | 已安装 |
| `social-pack` | ClawHub | 多平台内容生成 | `clawhub install social-pack` |
| `auto-social-post` | ClawHub | 自动发布到社交媒体 | `clawhub install auto-social-post` |
| `ecommerce-price-scraper` | 自研 | 电商价格监控（副业） | 已安装 |

**实战指南：**
- [公众号自动化发布完整流程](https://github.com/xxuan66/openclaw-workflows/blob/main/scenarios/money-making/wechat-auto-publish.md)
- 小红书矩阵运营（待更新）
- 多平台一键分发（待更新）

**时间节省：** 每天 2-3 小时 → 30 分钟

---

### ⏰ 省时间

**适合人群：** 职场人士、效率追求者、自动化爱好者

**核心需求：**
- ✅ 自动化重复工作
- ✅ 智能提醒和待办
- ✅ 信息快速处理
- ✅ 文件自动整理

**推荐 Skills：**

| Skill | 来源 | 用途 | 安装命令 |
|-------|------|------|----------|
| `qqbot-cron` | 自研 | 定时任务/提醒 | 已安装 |
| `feishu-bitable` | 自研 | 多维表格自动化 | 已安装 |
| `feishu-doc-manager` | 自研 | 飞书文档批量管理 | 已安装 |
| `automation-workflows` | ClawHub | 自动化工作流 | `clawhub install automation-workflows` |
| `productivity-automation-kit` | ClawHub | 效率工具包 | `clawhub install productivity-automation-kit` |
| `weather` | ClawHub | 天气查询 | `clawhub install weather` |

**实战指南：**
- [每日简报自动化](https://github.com/xxuan66/openclaw-workflows/blob/main/scenarios/time-saving/daily-brief.md)
- 待办事项自动追踪（待更新）
- 文件自动归档（待更新）

**时间节省：** 每天 30 分钟

---

### 📰 获取信息

**适合人群：** 研究者、数据分析师、内容运营

**核心需求：**
- ✅ 热点趋势追踪
- ✅ 新闻聚合与摘要
- ✅ 数据收集与分析
- ✅ 竞品监控

**推荐 Skills：**

| Skill | 来源 | 用途 | 安装命令 |
|-------|------|------|----------|
| `github-trending` | 自研 | GitHub 热门项目 | 已安装 |
| `douyin-hot-trend` | 自研 | 抖音热榜数据 | 已安装 |
| `tavily-search` | ClawHub | AI 优化搜索 | `clawhub install tavily-search` |
| `news-aggregator` | ClawHub | 新闻聚合 | `clawhub install news-aggregator` |
| `hot-news-aggregator` | ClawHub | 热点新闻聚合 | `clawhub install hot-news-aggregator` |
| `new-akshare-stock` | 自研 | A 股数据分析 | 已安装 |

**实战指南：**
- [每日热点简报](https://github.com/xxuan66/openclaw-workflows/blob/main/scenarios/information/daily-hot-brief.md)
- A 股数据监控（待更新）
- 竞品自动追踪（待更新）

**时间节省：** 每天 1-2 小时

---

## 🚀 快速开始

### 新手入门（3 分钟）

1. **选择一个场景** - 从最需要的开始
2. **安装推荐 Skills** - 复制上面的安装命令
3. **运行测试脚本** - 确保正常工作
4. **设置定时任务** - 让自动化跑起来

### 示例：每日热点简报

```bash
# 1. 确认已安装 Skills
clawhub list | grep -E "github-trending|douyin-hot-trend"

# 2. 测试运行
python3 /home/admin/.openclaw/workspace/scripts/daily_brief_run.py

# 3. 设置定时任务（每天 8:00）
qqbot-cron set --time "0 8 * * *" --task "python3 /home/admin/.openclaw/workspace/scripts/daily_brief_run.py"
```

---

## 📊 效果对比

| 场景 | 传统方式 | 自动化后 | 节省时间 | 年化收益 |
|------|----------|----------|----------|----------|
| 搞钱/变现 | 2-3 小时/天 | 30 分钟/天 | 2 小时/天 | 730 小时/年 |
| 省时间 | 30 分钟/天 | 2 分钟/天 | 28 分钟/天 | 170 小时/年 |
| 获取信息 | 1-2 小时/天 | 10 分钟/天 | 1 小时/天 | 365 小时/年 |

**总计：** 每年节省 **1265 小时** = 52 天不眠不休

---

## 💡 进阶技巧

### 1. 组合使用

```bash
# 天气 + 新闻 + 待办 = 每日简报
weather + tavily-search + feishu-bitable + qqbot-cron

# 热点 + 创作 + 发布 = 自媒体自动化
github-trending + skill-creator + wechat-operator
```

### 2. 条件触发

```bash
# 如果下雨 → 发送带伞提醒
# 如果待办逾期 → 发送紧急提醒
# 如果新闻重要 → 立即推送
```

### 3. 批量处理

```bash
# 一次性处理 100 个 URL 摘要
# 批量更新飞书文档
# 自动整理 1000+ 文件
```

---

## 📚 相关资源

- [场景化方案总览](https://github.com/xxuan66/openclaw-workflows/blob/main/scenarios/README.md)
- [快速开始指南](https://github.com/xxuan66/openclaw-workflows/blob/main/scenarios/QUICKSTART.md)
- [实现总结](https://github.com/xxuan66/openclaw-workflows/blob/main/scenarios/IMPLEMENTATION-SUMMARY.md)
- [ClawHub Skills 搜索](https://clawhub.com/search)

---

## ❓ 常见问题

### Q: 我是新手，从哪个场景开始？
A: 推荐从**获取信息**场景的"每日热点简报"开始，最简单，立即见效。

### Q: Skills 安装失败怎么办？
A: 检查以下几点：
1. 网络连接是否正常
2. ClawHub CLI 是否安装（`npm i -g clawhub`）
3. 查看错误信息，通常是依赖问题

### Q: 可以自定义推送时间吗？
A: 可以！修改 `qqbot-cron` 的 cron 表达式：
- `0 8 * * *` = 每天 8:00
- `0 9 * * 1-5` = 工作日 9:00
- `0 */2 * * *` = 每 2 小时

### Q: 能推送到多个渠道吗？
A: 可以，修改脚本同时调用多个 message 工具，支持飞书、微信、钉钉等。

---

*持续更新中... 想看什么场景可以提需求*
