#!/bin/bash

# GitHub 发布前安全检查脚本
# 用法：./check-github-secrets.sh [目录]

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🔍 GitHub 发布前安全检查"
echo "=========================================="

# 检查目录
CHECK_DIR="${1:-/home/admin/.openclaw/workspace/github-repos}"
cd "$CHECK_DIR"

ERRORS=0
WARNINGS=0

# 1. 检查 API Keys
echo ""
echo "1️⃣  检查 API Keys..."
if grep -r "sk-[a-zA-Z0-9]\{20,\}" . --include="*.md" --include="*.json" --include="*.sh" 2>/dev/null | grep -v "***" | grep -v "xxx"; then
  echo -e "${RED}❌ 发现疑似 API Key!${NC}"
  ERRORS=$((ERRORS + 1))
else
  echo -e "${GREEN}✅ 未发现 API Key${NC}"
fi

# 2. 检查模型名称
echo ""
echo "2️⃣  检查敏感模型名称..."
if grep -r "mimo-claw-0301" . --include="*.md" --include="*.json" 2>/dev/null; then
  echo -e "${RED}❌ 发现敏感模型名称！${NC}"
  ERRORS=$((ERRORS + 1))
else
  echo -e "${GREEN}✅ 未发现敏感模型名称${NC}"
fi

# 3. 检查 GitHub Token
echo ""
echo "3️⃣  检查 GitHub Token..."
if grep -r "ghp_[a-zA-Z0-9]\{30,\}" . --include="*.md" --include="*.json" --include="*.sh" 2>/dev/null | grep -v "***"; then
  echo -e "${RED}❌ 发现 GitHub Token!${NC}"
  ERRORS=$((ERRORS + 1))
else
  echo -e "${GREEN}✅ 未发现 GitHub Token${NC}"
fi

# 4. 检查密码/密钥
echo ""
echo "4️⃣  检查密码/密钥..."
if grep -ri "password.*=.*['\"][^'\"]*['\"]" . --include="*.md" --include="*.json" --include="*.sh" 2>/dev/null | grep -v "***" | grep -v "xxx"; then
  echo -e "${YELLOW}⚠️  发现疑似密码配置（请确认已脱敏）${NC}"
  WARNINGS=$((WARNINGS + 1))
else
  echo -e "${GREEN}✅ 未发现明文密码${NC}"
fi

# 5. 检查 openclaw.json
echo ""
echo "5️⃣  检查 openclaw.json..."
if find . -name "openclaw.json" -type f 2>/dev/null | grep -v ".git"; then
  echo -e "${YELLOW}⚠️  发现 openclaw.json 文件（请确认已添加到.gitignore）${NC}"
  WARNINGS=$((WARNINGS + 1))
else
  echo -e "${GREEN}✅ 未发现 openclaw.json${NC}"
fi

# 6. 检查 .env 文件
echo ""
echo "6️⃣  检查 .env 文件..."
if find . -name "*.env" -type f 2>/dev/null | grep -v ".git"; then
  echo -e "${YELLOW}⚠️  发现 .env 文件（请确认已添加到.gitignore）${NC}"
  WARNINGS=$((WARNINGS + 1))
else
  echo -e "${GREEN}✅ 未发现 .env 文件${NC}"
fi

# 7. 检查 .gitignore
echo ""
echo "7️⃣  检查 .gitignore..."
if [ -f ".gitignore" ]; then
  echo -e "${GREEN}✅ 发现 .gitignore 文件${NC}"
else
  echo -e "${YELLOW}⚠️  未发现 .gitignore 文件（建议创建）${NC}"
  WARNINGS=$((WARNINGS + 1))
fi

# 总结
echo ""
echo "=========================================="
echo "📊 检查结果："
echo "  错误：$ERRORS"
echo "  警告：$WARNINGS"
echo "=========================================="

if [ $ERRORS -gt 0 ]; then
  echo -e "${RED}❌ 检查失败！发现敏感信息，不能发布！${NC}"
  exit 1
elif [ $WARNINGS -gt 0 ]; then
  echo -e "${YELLOW}⚠️  检查通过，但有警告，请确认后再发布${NC}"
  exit 0
else
  echo -e "${GREEN}✅ 检查通过，可以安全发布！${NC}"
  exit 0
fi
