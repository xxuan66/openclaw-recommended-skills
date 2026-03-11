# 技能安装计划

## 已设置的定时任务

### 1. tavily-search (网络搜索技能)
- **首次尝试**: 2026-03-09 02:00 (1 小时后)
- **重试时间**: 如果失败，脚本会自动等待 1 小时后重试
- **日志文件**: `/home/admin/.openclaw/workspace/logs/tavily_install.log`

### 2. self-improving-agent (自我改进代理)
- **安装时间**: 2026-03-09 04:00 (3 小时后)
- **说明**: ClawHub 热门榜第一，46k+ installs
- **日志文件**: `/home/admin/.openclaw/workspace/logs/self_improving_install.log`

---

## 定时任务详情

```cron
# OpenClaw 技能安装定时任务
0 2 * * * /home/admin/.openclaw/workspace/scripts/install_tavily.sh
0 4 * * * /home/admin/.openclaw/workspace/scripts/install_self_improving.sh
```

---

## 查看安装进度

```bash
# 查看 tavily-search 安装日志
tail -f /home/admin/.openclaw/workspace/logs/tavily_install.log

# 查看 self-improving-agent 安装日志
tail -f /home/admin/.openclaw/workspace/logs/self_improving_install.log

# 查看定时任务
crontab -l
```

---

## 手动安装（如果需要）

```bash
# tavily-search
cd /home/admin/.openclaw/workspace
npx clawhub install tavily-search

# self-improving-agent
npx clawhub install self-improving-agent
```

---

## 注意事项

1. **速率限制**: clawhub 有 API 速率限制，如果失败会自动重试
2. **已安装检查**: self-improving-agent 已有手动创建的简化版本
3. **日志记录**: 所有安装过程都会记录到日志文件
4. **取消定时任务**: `crontab -r`

---

**设置时间**: 2026-03-09 00:38
**状态**: ✅ 定时任务已激活
