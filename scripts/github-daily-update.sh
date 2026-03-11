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

# 更新 openclaw-recommended-skills
echo "  - openclaw-recommended-skills"
openclaw agent \
  --session-id github-$(date +%Y%m%d) \
  --message "执行 $(date +%Y-%m-%d) GitHub 更新：更新 DAILY_UPDATES.md，添加今日技巧。注意：只写公开内容，不要添加本地数据追踪（如 Stars/Forks/Issues/Commits 统计、本周目标等）" \
  --thinking minimal

# 更新 openclaw-starter
echo "  - openclaw-starter"
openclaw agent \
  --session-id github-$(date +%Y%m%d) \
  --message "更新 starter 配置指南或使用技巧" \
  --thinking minimal

# 更新 openclaw-workflows
echo "  - openclaw-workflows"
openclaw agent \
  --session-id github-$(date +%Y%m%d) \
  --message "更新 workflows 索引或添加新工作流示例" \
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
