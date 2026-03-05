# 🤖 Mify LLM API 技能

## 描述
Mify 大语言模型 API 调用技能，兼容 OpenAI 格式，支持对话、补全、嵌入等功能。

## API 信息
- **Base URL**: `http://model.mify.ai.srv/v1`
- **认证方式**: Bearer Token (API KEY)
- **格式**: OpenAI 兼容

## 使用方法
```bash
./run-mify-llm.sh chat "你好"
./run-mify-llm.sh complete "写一首诗"
./run-mify-llm.sh models           # 列出可用模型
./run-mify-llm.sh embed "文本"     # 生成嵌入向量
```

## 配置项
- `MIFY_API_KEY`: Mify API 密钥（必需）
- `MIFY_BASE_URL`: API 基础 URL（默认：http://model.mify.ai.srv/v1）
- `MIFY_MODEL`: 默认模型名称（可选）
- `MIFY_MAX_TOKENS`: 最大生成 token 数（默认：2048）
- `MIFY_TEMPERATURE`: 温度参数（默认：0.7）

## 环境变量设置
```bash
export MIFY_API_KEY="your-api-key-here"
export MIFY_BASE_URL="http://model.mify.ai.srv/v1"
export MIFY_MODEL="mify-chat-v1"
```

## 安全提示
- API KEY 请妥善保管，不要提交到版本控制
- 建议使用环境变量或配置文件存储密钥
- 生产环境请使用 HTTPS
