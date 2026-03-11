#!/bin/bash
# 安装 self-improving-agent 技能
# 计划执行时间：2026-03-09 03:38 (3 小时后)

LOG_FILE="/home/admin/.openclaw/workspace/logs/self_improving_install.log"
mkdir -p /home/admin/.openclaw/workspace/logs

echo "=== 开始安装 self-improving-agent ===" >> $LOG_FILE
echo "时间：$(date)" >> $LOG_FILE

cd /home/admin/.openclaw/workspace

# 第一次尝试
echo "尝试安装..." >> $LOG_FILE
npx clawhub install self-improving-agent >> $LOG_FILE 2>&1

if [ $? -eq 0 ]; then
  echo "✅ 安装成功" >> $LOG_FILE
else
  echo "❌ 安装失败，可能已被手动安装或使用替代方案" >> $LOG_FILE
  echo "检查是否已存在..." >> $LOG_FILE
  if [ -d "/home/admin/.openclaw/workspace/skills/self-improving-agent" ]; then
    echo "✅ 技能目录已存在，可以使用" >> $LOG_FILE
  else
    echo "❌ 技能不存在，请手动安装" >> $LOG_FILE
  fi
fi

echo "=== 安装流程结束 ===" >> $LOG_FILE
