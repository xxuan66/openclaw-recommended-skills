#!/bin/bash

# 微信公众号自动化发布脚本
# 功能：获取 Token、发布文章、管理草稿

set -e

# ==================== 配置区域 ====================
# 申请公众号后，在这里填写你的 AppID 和 AppSecret
APPID="wx8f5bee5bd870d904"
APPSECRET="7d40436cc2e5766f82c54741be73bb89"

# Token 缓存文件
TOKEN_FILE="/tmp/wechat_token.json"

# ==================== 颜色定义 ====================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# ==================== 函数定义 ====================

# 获取 Access Token
get_access_token() {
    echo "🔑 获取 Access Token..."
    
    # 检查缓存是否有效
    if [ -f "$TOKEN_FILE" ]; then
        EXPIRES_AT=$(jq -r '.expires_at' "$TOKEN_FILE")
        NOW=$(date +%s)
        if [ "$NOW" -lt "$EXPIRES_AT" ]; then
            echo -e "${GREEN}✅ 使用缓存的 Token${NC}"
            jq -r '.access_token' "$TOKEN_FILE"
            return 0
        fi
    fi
    
    # 请求新 Token
    RESPONSE=$(curl -s "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=$APPID&secret=$APPSECRET")
    
    # 检查是否成功
    if echo "$RESPONSE" | jq -e '.errcode' > /dev/null 2>&1; then
        echo -e "${RED}❌ 获取 Token 失败：$(echo "$RESPONSE" | jq -r '.errmsg')${NC}"
        exit 1
    fi
    
    # 提取 Token
    ACCESS_TOKEN=$(echo "$RESPONSE" | jq -r '.access_token')
    EXPIRES_IN=$(echo "$RESPONSE" | jq -r '.expires_in')
    
    # 计算过期时间（提前 5 分钟过期）
    EXPIRES_AT=$(($(date +%s) + EXPIRES_IN - 300))
    
    # 保存缓存
    jq -n \
        --arg token "$ACCESS_TOKEN" \
        --argjson expires "$EXPIRES_AT" \
        '{access_token: $token, expires_at: $expires}' > "$TOKEN_FILE"
    
    echo -e "${GREEN}✅ Token 获取成功，有效期 $(($EXPIRES_IN / 60)) 分钟${NC}"
    echo "$ACCESS_TOKEN"
}

# 上传临时素材（封面图片）
upload_temp_material() {
    local IMAGE_FILE="$1"
    local TYPE="${2:-image}"
    
    echo "📷 上传封面图片：$IMAGE_FILE"
    
    ACCESS_TOKEN=$(get_access_token)
    
    RESPONSE=$(curl -s -F "media=@$IMAGE_FILE" \
        -F "type=$TYPE" \
        "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=$ACCESS_TOKEN&type=$TYPE")
    
    if echo "$RESPONSE" | jq -e '.errcode' > /dev/null 2>&1; then
        echo -e "${RED}❌ 上传失败：$(echo "$RESPONSE" | jq -r '.errmsg')${NC}"
        exit 1
    fi
    
    MEDIA_ID=$(echo "$RESPONSE" | jq -r '.media_id')
    echo -e "${GREEN}✅ 上传成功，MEDIA_ID: $MEDIA_ID${NC}"
    echo "$MEDIA_ID"
}

# 创建草稿
create_draft() {
    local TITLE="$1"
    local CONTENT="$2"
    local THUMB_MEDIA_ID="$3"
    local AUTHOR="${4:-}"
    local DIGEST="${5:-}"
    
    echo "📝 创建草稿：$TITLE"
    
    ACCESS_TOKEN=$(get_access_token)
    
    # 构建 JSON
    if [ -z "$AUTHOR" ]; then
        AUTHOR="xuan"
    fi
    
    if [ -z "$DIGEST" ]; then
        DIGEST=$(echo "$CONTENT" | head -c 100 | sed 's/<[^>]*>//g')
    fi
    
    # 如果没有封面 ID，使用空值
    if [ -z "$THUMB_MEDIA_ID" ]; then
        JSON_DATA=$(jq -n \
            --arg title "$TITLE" \
            --arg author "$AUTHOR" \
            --arg digest "$DIGEST" \
            --arg content "$CONTENT" \
            '{
                articles: [{
                    title: $title,
                    author: $author,
                    digest: $digest,
                    content: $content,
                    thumb_media_id: "",
                    show_cover_pic: 0,
                    need_open_comment: 0,
                    only_fans_can_comment: false
                }]
            }')
    else
        JSON_DATA=$(jq -n \
            --arg title "$TITLE" \
            --arg author "$AUTHOR" \
            --arg digest "$DIGEST" \
            --arg content "$CONTENT" \
            --arg thumb "$THUMB_MEDIA_ID" \
            '{
                articles: [{
                    title: $title,
                    author: $author,
                    digest: $digest,
                    content: $content,
                    thumb_media_id: $thumb,
                    show_cover_pic: 1,
                    need_open_comment: 0,
                    only_fans_can_comment: false
                }]
            }')
    fi
    
    RESPONSE=$(curl -s -X POST \
        -H "Content-Type: application/json" \
        -d "$JSON_DATA" \
        "https://api.weixin.qq.com/cgi-bin/draft/add?access_token=$ACCESS_TOKEN")
    
    if echo "$RESPONSE" | jq -e '.errcode' > /dev/null 2>&1; then
        echo -e "${RED}❌ 创建草稿失败：$(echo "$RESPONSE" | jq -r '.errmsg')${NC}"
        exit 1
    fi
    
    MEDIA_ID=$(echo "$RESPONSE" | jq -r '.media_id')
    echo -e "${GREEN}✅ 草稿创建成功，MEDIA_ID: $MEDIA_ID${NC}"
    echo "$MEDIA_ID"
}

# 发布文章（从草稿）
publish_article() {
    local MEDIA_ID="$1"
    local IS_REPRINT="${2:-0}"
    
    echo "🚀 发布文章：$MEDIA_ID"
    
    ACCESS_TOKEN=$(get_access_token)
    
    JSON_DATA=$(jq -n \
        --arg media_id "$MEDIA_ID" \
        --argjson is_reprint "$IS_REPRINT" \
        '{
            media_id: $media_id,
            is_reprint: $is_reprint
        }')
    
    RESPONSE=$(curl -s -X POST \
        -H "Content-Type: application/json" \
        -d "$JSON_DATA" \
        "https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token=$ACCESS_TOKEN")
    
    if echo "$RESPONSE" | jq -e '.errcode' > /dev/null 2>&1; then
        echo -e "${RED}❌ 发布失败：$(echo "$RESPONSE" | jq -r '.errmsg')${NC}"
        exit 1
    fi
    
    PUBLISH_ID=$(echo "$RESPONSE" | jq -r '.publish_id')
    echo -e "${GREEN}✅ 发布成功，PUBLISH_ID: $PUBLISH_ID${NC}"
    echo "$PUBLISH_ID"
}

# 删除草稿
delete_draft() {
    local MEDIA_ID="$1"
    
    echo "🗑️  删除草稿：$MEDIA_ID"
    
    ACCESS_TOKEN=$(get_access_token)
    
    JSON_DATA=$(jq -n --arg media_id "$MEDIA_ID" '{media_id: $media_id}')
    
    RESPONSE=$(curl -s -X POST \
        -H "Content-Type: application/json" \
        -d "$JSON_DATA" \
        "https://api.weixin.qq.com/cgi-bin/draft/delete?access_token=$ACCESS_TOKEN")
    
    if echo "$RESPONSE" | jq -e '.errcode' > /dev/null 2>&1; then
        echo -e "${RED}❌ 删除失败：$(echo "$RESPONSE" | jq -r '.errmsg')${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ 删除成功${NC}"
}

# 获取草稿列表
list_drafts() {
    echo "📋 获取草稿列表..."
    
    ACCESS_TOKEN=$(get_access_token)
    
    JSON_DATA='{"offset":0,"count":20,"no_content":0}'
    
    RESPONSE=$(curl -s -X POST \
        -H "Content-Type: application/json" \
        -d "$JSON_DATA" \
        "https://api.weixin.qq.com/cgi-bin/draft/batchget?access_token=$ACCESS_TOKEN")
    
    if echo "$RESPONSE" | jq -e '.errcode' > /dev/null 2>&1; then
        echo -e "${RED}❌ 获取失败：$(echo "$RESPONSE" | jq -r '.errmsg')${NC}"
        exit 1
    fi
    
    echo "$RESPONSE" | jq '.item_count'
    echo "$RESPONSE" | jq '.item'
}

# 检查发布状态
check_publish_status() {
    local PUBLISH_ID="$1"
    
    echo "📊 检查发布状态：$PUBLISH_ID"
    
    ACCESS_TOKEN=$(get_access_token)
    
    JSON_DATA=$(jq -n --arg publish_id "$PUBLISH_ID" '{publish_id: $publish_id}')
    
    RESPONSE=$(curl -s -X POST \
        -H "Content-Type: application/json" \
        -d "$JSON_DATA" \
        "https://api.weixin.qq.com/cgi-bin/freepublish/get?access_token=$ACCESS_TOKEN")
    
    if echo "$RESPONSE" | jq -e '.errcode' > /dev/null 2>&1; then
        echo -e "${RED}❌ 查询失败：$(echo "$RESPONSE" | jq -r '.errmsg')${NC}"
        exit 1
    fi
    
    echo "$RESPONSE" | jq '.'
}

# 显示帮助
show_help() {
    echo "微信公众号自动化发布脚本"
    echo ""
    echo "用法：$0 <命令> [参数]"
    echo ""
    echo "命令:"
    echo "  token              获取 Access Token"
    echo "  upload <图片>      上传封面图片"
    echo "  draft <标题> <内容> [封面 ID] [作者] [摘要]  创建草稿"
    echo "  publish <草稿 ID> [是否转载]  发布文章"
    echo "  delete <草稿 ID>   删除草稿"
    echo "  list               获取草稿列表"
    echo "  status <发布 ID>   检查发布状态"
    echo "  help               显示帮助"
    echo ""
    echo "示例:"
    echo "  $0 token"
    echo "  $0 upload cover.jpg"
    echo "  $0 draft \"我的文章\" \"<p>内容</p>\" <封面 ID>"
    echo "  $0 publish <草稿 ID>"
    echo ""
}

# ==================== 主程序 ====================

case "${1:-help}" in
    token)
        get_access_token
        ;;
    upload)
        if [ -z "$2" ]; then
            echo -e "${RED}❌ 请提供图片文件路径${NC}"
            exit 1
        fi
        upload_temp_material "$2" "${3:-image}"
        ;;
    draft)
        if [ -z "$2" ] || [ -z "$3" ]; then
            echo -e "${RED}❌ 请提供标题和内容${NC}"
            exit 1
        fi
        create_draft "$2" "$3" "${4:-}" "${5:-}" "${6:-}"
        ;;
    publish)
        if [ -z "$2" ]; then
            echo -e "${RED}❌ 请提供草稿 ID${NC}"
            exit 1
        fi
        publish_article "$2" "${3:-0}"
        ;;
    delete)
        if [ -z "$2" ]; then
            echo -e "${RED}❌ 请提供草稿 ID${NC}"
            exit 1
        fi
        delete_draft "$2"
        ;;
    list)
        list_drafts
        ;;
    status)
        if [ -z "$2" ]; then
            echo -e "${RED}❌ 请提供发布 ID${NC}"
            exit 1
        fi
        check_publish_status "$2"
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}❌ 未知命令：$1${NC}"
        show_help
        exit 1
        ;;
esac
