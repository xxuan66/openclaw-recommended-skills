#!/bin/bash

# GitHub 每日更新脚本
# 执行时间：每天早上 6:00
# 使用模型：mimo/mimo-claw-0301

set -e

echo "🦞 OpenClaw GitHub 每日更新 - $(date)"
echo "=========================================="

# 1. 确认当前模型（应该是 mimo，晚上 22 点已自动切换）
echo "📱 检查当前模型..."
CURRENT_MODEL=$(openclaw config get agents.defaults.model.primary 2>/dev/null | grep -o '"[^"]*"' | tail -1)
echo "当前模型：$CURRENT_MODEL"
if echo "$CURRENT_MODEL" | grep -q "mimo"; then
  echo "✅ 已是 mimo 模型"
else
  echo "⚠️  切换到 mimo 模型..."
  openclaw models set mimo/mimo-claw-0301
  echo "✅ 模型切换完成"
fi

# 2. 执行 GitHub 更新任务
echo ""
echo "🔄 开始更新 GitHub 项目..."

# 更新 openclaw-recommended-skills（主仓库，小步迭代）
echo "  - openclaw-recommended-skills（主仓库）"
openclaw agent \
  --session-id github-$(date +%Y%m%d) \
  --message "执行 $(date +%Y-%m-%d) GitHub 更新：在原有内容基础上小步迭代，完善现有章节或添加新技巧。改动不要太大，保持内容质量。注意：只写公开内容，不要添加本地数据追踪" \
  --thinking minimal

# 更新 openclaw-starter（每日更新）
echo "  - openclaw-starter（每日）"
openclaw agent \
  --session-id github-$(date +%Y%m%d) \
  --message "执行 $(date +%Y-%m-%d) GitHub 更新：添加或优化场景配置，小步迭代。注意：只写公开内容，不要添加本地数据追踪" \
  --thinking minimal

# 更新 openclaw-workflows（每日更新）
echo "  - openclaw-workflows（每日）"
openclaw agent \
  --session-id github-$(date +%Y%m%d) \
  --message "执行 $(date +%Y-%m-%d) GitHub 更新：添加或优化工作流示例，小步迭代。注意：只写公开内容，不要添加本地数据追踪" \
  --thinking minimal

# 更新 agent-learning-path（每日小幅度迭代）
echo "  - agent-learning-path（每日小幅度优化）"
openclaw agent \
  --session-id github-$(date +%Y%m%d) \
  --message "执行 $(date +%Y-%m-%d) GitHub 更新：小幅度迭代优化 agent-learning-path 仓库，修复错误、补充内容、优化表达。改动不要太大，保持内容质量。" \
  --thinking minimal

echo "✅ GitHub 更新完成"

# 3. 切回 qwen 模型（默认）
echo ""
echo "📱 切回 qwen3.5-plus 模型..."
openclaw models set bailian/qwen3.5-plus
echo "✅ 模型切回完成"

# 4. 发送完成通知（可选）
echo ""
echo "📊 更新日志："
echo "  - 日期：$(date +%Y-%m-%d)"
echo "  - 模型：mimo → qwen"
echo "  - 项目：3 个"
echo "  - 状态：✅ 完成"

echo ""
echo "=========================================="
echo "🎉 GitHub 每日更新完成！"
echo "=========================================="
