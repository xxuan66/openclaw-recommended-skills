#!/bin/bash
# 安装 tavily-search 技能
# 计划执行时间：2026-03-09 01:38 (1 小时后)

LOG_FILE="/home/admin/.openclaw/workspace/logs/tavily_install.log"
mkdir -p /home/admin/.openclaw/workspace/logs

echo "=== 开始安装 tavily-search ===" >> $LOG_FILE
echo "时间：$(date)" >> $LOG_FILE

cd /home/admin/.openclaw/workspace

# 第一次尝试
echo "第一次尝试安装..." >> $LOG_FILE
npx clawhub install tavily-search >> $LOG_FILE 2>&1

if [ $? -eq 0 ]; then
  echo "✅ 安装成功" >> $LOG_FILE
  echo "=== tavily-search 安装完成 ===" >> $LOG_FILE
  exit 0
else
  echo "❌ 第一次失败，等待 1 小时后重试..." >> $LOG_FILE
  sleep 3600
  
  # 第二次尝试
  echo "第二次尝试安装..." >> $LOG_FILE
  npx clawhub install tavily-search >> $LOG_FILE 2>&1
  
  if [ $? -eq 0 ]; then
    echo "✅ 安装成功" >> $LOG_FILE
  else
    echo "❌ 两次都失败，请手动安装" >> $LOG_FILE
  fi
fi

echo "=== 安装流程结束 ===" >> $LOG_FILE
