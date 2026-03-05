# 🔑 配置 Mify LLM API 指南

## 快速开始

### 1. 设置环境变量

**临时设置（当前终端会话）**：
```bash
export MIFY_API_KEY="your-api-key-here"
export MIFY_BASE_URL="http://model.mify.ai.srv/v1"
```

**永久设置（推荐）**：
```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
echo 'export MIFY_API_KEY="your-api-key-here"' >> ~/.bashrc
echo 'export MIFY_BASE_URL="http://model.mify.ai.srv/v1"' >> ~/.bashrc
source ~/.bashrc
```

### 2. 测试连接

```bash
cd ~/.openclaw/workspace/skills/mify-llm
./run-mify-llm.sh test
```

### 3. 使用示例

```bash
# 列出可用模型
./run-mify-llm.sh models

# 对话
./run-mify-llm.sh chat "你好，请介绍一下自己"

# 文本补全
./run-mify-llm.sh complete "写一首关于春天的诗"

# 生成嵌入向量
./run-mify-llm.sh embed "这是一段测试文本" -o embedding.json
```

---

## 配置选项

| 变量 | 说明 | 默认值 | 必需 |
|------|------|--------|------|
| `MIFY_API_KEY` | API 密钥 | - | ✅ |
| `MIFY_BASE_URL` | API 基础 URL | `http://model.mify.ai.srv/v1` | ❌ |
| `MIFY_MODEL` | 默认模型名称 | - | ❌ |
| `MIFY_MAX_TOKENS` | 最大生成 token 数 | `2048` | ❌ |
| `MIFY_TEMPERATURE` | 温度参数（创造性） | `0.7` | ❌ |

---

## 在 OpenClaw 中集成

### 方法 1：Gateway 环境变量

编辑 OpenClaw Gateway 配置，添加环境变量：

```bash
# 重启 Gateway 后生效
openclaw gateway restart
```

### 方法 2：技能配置文件

在技能的 `config/settings.json` 中配置：

```json
{
  "env": {
    "MIFY_API_KEY": "your-api-key",
    "MIFY_BASE_URL": "http://model.mify.ai.srv/v1"
  }
}
```

### 方法 3： workspace 全局配置

创建 `~/.openclaw/workspace/.env` 文件：

```bash
MIFY_API_KEY=your-api-key
MIFY_BASE_URL=http://model.mify.ai.srv/v1
```

---

## API 端点参考

Mify API 兼容 OpenAI 格式，支持以下端点：

| 端点 | 方法 | 说明 |
|------|------|------|
| `/v1/models` | GET | 获取可用模型列表 |
| `/v1/chat/completions` | POST | 对话补全 |
| `/v1/completions` | POST | 文本补全 |
| `/v1/embeddings` | POST | 生成嵌入向量 |

---

## 安全建议

1. **不要硬编码 API Key**
   - ✅ 使用环境变量
   - ✅ 使用配置文件（加入 `.gitignore`）
   - ❌ 不要提交到版本控制

2. **限制访问**
   - 如果 API 在内网，确保网络隔离
   - 使用防火墙限制访问来源

3. **监控使用**
   - 定期检查 API 调用日志
   - 设置使用配额告警

---

## 故障排查

### 问题：`401 Unauthorized`
**原因**: API Key 无效或未配置
**解决**: 检查 `MIFY_API_KEY` 是否正确

### 问题：`Connection refused`
**原因**: API 服务不可达
**解决**: 
- 检查网络连接
- 确认 API 服务是否运行
- 检查 URL 是否正确

### 问题：`404 Not Found`
**原因**: 模型名称错误或端点不存在
**解决**: 
- 使用 `./run-mify-llm.sh models` 查看可用模型
- 检查 API 文档确认端点

---

## 下一步

配置完成后，你可以：

1. ✅ 测试 API 连接
2. ✅ 在技能中使用 Mify 模型
3. ✅ 集成到其他 OpenClaw 技能
4. ✅ 设置监控和告警

有任何问题，查看 `SKILL.md` 或运行 `./run-mify-llm.sh --help`
