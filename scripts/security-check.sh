#!/bin/bash
# GitHub 仓库安全检查脚本
# 每次推送前必须运行，防止敏感文件泄露

set -e

REPO_DIR="${1:-$(pwd)}"
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "========================================"
echo "🔍 GitHub 仓库安全检查"
echo "========================================"
echo "检查目录：$REPO_DIR"
echo ""

cd "$REPO_DIR"

ERRORS=0
WARNINGS=0

# ===== 1. 检查敏感配置文件 =====
echo "📋 检查敏感配置文件..."
SENSITIVE_FILES=(
    "AGENTS.md"
    "SOUL.md"
    "USER.md"
    "TOOLS.md"
    "HEARTBEAT.md"
    "IDENTITY.md"
    ".openclaw/"
    "memory/"
)

for file in "${SENSITIVE_FILES[@]}"; do
    if git ls-files --error-unmatch "$file" &>/dev/null; then
        echo -e "${RED}❌ 发现敏感文件：$file${NC}"
        ((ERRORS++))
    fi
done

# ===== 2. 检查 Skill 源码 =====
echo "📋 检查 Skill 源码（不应该在推荐仓库）..."
if git ls-files --error-unmatch "skills/" &>/dev/null; then
    echo -e "${RED}❌ skills/ 目录不应该被跟踪${NC}"
    ((ERRORS++))
fi

# ===== 3. 检查个人工作文件 =====
echo "📋 检查个人工作文件..."
WORK_FILES=(
    "wechat_articles/"
    "wechat_daily/"
    "paper_reading_notes/"
    "output/"
)

for file in "${WORK_FILES[@]}"; do
    if git ls-files --error-unmatch "$file" &>/dev/null; then
        echo -e "${YELLOW}⚠️  发现工作文件：$file${NC}"
        ((WARNINGS++))
    fi
done

# scripts/ 目录检查（但排除 security-check.sh）
SCRIPT_COUNT=$(git ls-files scripts/ | grep -v "security-check.sh" | wc -l)
if [ "$SCRIPT_COUNT" -gt 0 ]; then
    echo -e "${YELLOW}⚠️  scripts/ 目录有 $SCRIPT_COUNT 个文件（security-check.sh 除外）${NC}"
    ((WARNINGS++))
fi

# ===== 4. 检查 .gitignore =====
echo "📋 检查 .gitignore 配置..."
if [ ! -f ".gitignore" ]; then
    echo -e "${RED}❌ 缺少 .gitignore 文件${NC}"
    ((ERRORS++))
else
    # 检查关键条目
    REQUIRED_IGNORES=(
        ".openclaw/"
        "AGENTS.md"
        "SOUL.md"
        "USER.md"
        "memory/"
        "skills/"
    )
    
    for pattern in "${REQUIRED_IGNORES[@]}"; do
        if ! grep -q "$pattern" .gitignore; then
            echo -e "${YELLOW}⚠️  .gitignore 缺少：$pattern${NC}"
            ((WARNINGS++))
        fi
    done
fi

# ===== 5. 检查文件总数 =====
echo "📋 检查文件总数..."
FILE_COUNT=$(git ls-files | wc -l)
if [ "$FILE_COUNT" -gt 50 ]; then
    echo -e "${YELLOW}⚠️  文件数量异常：$FILE_COUNT (建议 < 50)${NC}"
    ((WARNINGS++))
else
    echo -e "${GREEN}✅ 文件数量正常：$FILE_COUNT${NC}"
fi

# ===== 6. 检查大文件 =====
echo "📋 检查大文件（> 1MB）..."
while IFS= read -r file; do
    if [ -f "$file" ]; then
        size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null || echo 0)
        if [ "$size" -gt 1048576 ]; then
            echo -e "${YELLOW}⚠️  大文件：$file ($(echo "scale=2; $size/1048576" | bc)MB)${NC}"
            ((WARNINGS++))
        fi
    fi
done < <(git ls-files)

# ===== 7. 检查待推送的提交 =====
echo "📋 检查待推送的提交..."
PENDING=$(git log --oneline origin/main..HEAD 2>/dev/null | wc -l)
if [ "$PENDING" -gt 0 ]; then
    echo -e "${YELLOW}⚠️  有 $PENDING 个待推送的提交${NC}"
    echo "    运行 'git push' 前请再次检查"
fi

# ===== 总结 =====
echo ""
echo "========================================"
echo "📊 检查结果"
echo "========================================"
echo -e "错误：${RED}$ERRORS${NC}"
echo -e "警告：${YELLOW}$WARNINGS${NC}"
echo ""

if [ "$ERRORS" -gt 0 ]; then
    echo -e "${RED}❌ 安全检查失败！请先修复错误再推送${NC}"
    echo ""
    echo "修复建议："
    echo "  git rm --cached <敏感文件>"
    echo "  git commit -m 'fix: 移除敏感文件'"
    echo "  git push origin main --force"
    exit 1
elif [ "$WARNINGS" -gt 0 ]; then
    echo -e "${YELLOW}⚠️  安全检查通过（有警告）${NC}"
    echo "   建议检查警告项，但可以推送"
    exit 0
else
    echo -e "${GREEN}✅ 安全检查通过！可以推送${NC}"
    exit 0
fi
