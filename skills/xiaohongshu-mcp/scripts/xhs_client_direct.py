#!/usr/bin/env python3
"""
Xiaohongshu API Client - 直接使用 Cookie 认证，无需本地服务器

基于 xhs 库和 requests 实现搜索、详情、发布等功能
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List

try:
    import requests
    from dotenv import load_dotenv
except ImportError:
    print("❌ 缺少依赖：pip install requests python-dotenv")
    sys.exit(1)

# 小红书 API 端点
API_BASE = "https://edith.xiaohongshu.com"
MOBILE_BASE = "https://www.xiaohongshu.com"

# 默认请求头
DEFAULT_HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "content-type": "application/json;charset=UTF-8",
    "referer": "https://www.xiaohongshu.com/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}


def load_cookie() -> str:
    """从 .env 文件加载 Cookie"""
    env_paths = [
        Path(__file__).parent.parent / '.env',
        Path.cwd() / '.env',
    ]
    
    for env_path in env_paths:
        if env_path.exists():
            load_dotenv(env_path)
            break
    
    cookie = os.getenv('XHS_COOKIE')
    if not cookie:
        print("❌ 错误：未找到 XHS_COOKIE 环境变量")
        print("\n请创建 .env 文件，添加：")
        print("XHS_COOKIE=acw_tc=...; a1=...; web_session=...")
        sys.exit(1)
    
    return cookie


def get_headers() -> Dict[str, str]:
    """获取带 Cookie 的请求头"""
    headers = DEFAULT_HEADERS.copy()
    headers["cookie"] = load_cookie()
    return headers


def search_notes(keyword: str, page: int = 1, page_size: int = 20) -> Optional[Dict[str, Any]]:
    """搜索笔记"""
    print(f"\n🔍 搜索：{keyword}")
    print(f"📄 页码：{page}, 每页：{page_size} 条\n")
    
    url = f"{API_BASE}/api/sns/web/v1/search/notes"
    
    payload = {
        "keyword": keyword,
        "page": page,
        "page_size": page_size,
        "sort": "popularity_descending",  # 按热度排序
        "note_type": 0,  # 不限
    }
    
    try:
        resp = requests.post(url, json=payload, headers=get_headers(), timeout=30)
        resp.raise_for_status()
        data = resp.json()
        
        if data.get("success"):
            items = data.get("data", {}).get("items", [])
            print(f"✅ 找到 {len(items)} 条笔记：\n")
            
            for i, item in enumerate(items, 1):
                model = item.get("model_type", "")
                if model != "note":
                    continue
                    
                note = item.get("note_card", {})
                interact = note.get("interact_info", {})
                user = note.get("user", {})
                
                title = note.get("title", "无标题")[:50]
                user_name = user.get("nickname", "未知")
                liked = interact.get("liked_count", "0")
                collected = interact.get("collected_count", "0")
                note_id = note.get("note_id", "")
                xsec_token = note.get("xsec_token", "")
                
                print(f"[{i}] {title}")
                print(f"    👤 {user_name}")
                print(f"    ❤️ {liked} | ⭐ {collected}")
                print(f"    📝 ID: {note_id}")
                print(f"    🔑 Token: {xsec_token}")
                print()
            
            return {"success": True, "data": items}
        else:
            print(f"❌ 搜索失败：{data.get('msg', '未知错误')}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求失败：{e}")
        return None


def get_note_detail(note_id: str, xsec_token: str) -> Optional[Dict[str, Any]]:
    """获取笔记详情"""
    print(f"\n📝 获取笔记详情：{note_id}\n")
    
    url = f"{API_BASE}/api/sns/web/v1/feed"
    
    payload = {
        "source_note_id": note_id,
        "image_formats": ["jpg", "webp", "avif"],
        "extra": {"need_body_topic": "1"},
        "xsec_token": xsec_token,
    }
    
    try:
        resp = requests.post(url, json=payload, headers=get_headers(), timeout=30)
        resp.raise_for_status()
        data = resp.json()
        
        if data.get("success"):
            items = data.get("data", {}).get("items", [])
            if not items:
                print("❌ 未找到笔记")
                return None
            
            note = items[0].get("note_card", {})
            interact = note.get("interact_info", {})
            user = note.get("user", {})
            
            print(f"📌 标题：{note.get('title', '无标题')}")
            print(f"👤 作者：{user.get('nickname', '未知')}")
            print(f"📍 IP: {note.get('ip_location', '未知')}")
            print(f"\n📄 内容：\n{note.get('desc', '无内容')}\n")
            print(f"❤️ 点赞：{interact.get('liked_count', '0')}")
            print(f"⭐ 收藏：{interact.get('collected_count', '0')}")
            print(f"💬 评论：{interact.get('comment_count', '0')}")
            
            # 图片
            images = note.get("image_list", [])
            if images:
                print(f"\n🖼️ 图片 ({len(images)} 张):")
                for img in images[:5]:
                    print(f"  - {img.get('url', '')}")
            
            return {"success": True, "data": note}
        else:
            print(f"❌ 获取失败：{data.get('msg', '未知错误')}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求失败：{e}")
        return None


def get_feeds(page: int = 1) -> Optional[Dict[str, Any]]:
    """获取推荐 Feed"""
    print(f"\n📋 获取推荐 Feed (第{page}页)\n")
    
    url = f"{MOBILE_BASE}/api/sns/web/v1/homefeed"
    
    payload = {
        "cursor_score": "",
        "num": 30,
        "refresh_type": 1,
        "note_index": page,
        "unread_begin_note_id": "",
        "unread_end_note_id": "",
        "unread_note_count": 0,
        "category": "",
    }
    
    try:
        resp = requests.post(url, json=payload, headers=get_headers(), timeout=30)
        resp.raise_for_status()
        data = resp.json()
        
        if data.get("success"):
            items = data.get("data", {}).get("items", [])
            print(f"✅ 获取到 {len(items)} 条推荐：\n")
            
            for i, item in enumerate(items[:10], 1):
                note = item.get("note_card", {})
                title = note.get("title", "无标题")[:50]
                print(f"[{i}] {title}")
            
            return {"success": True, "data": items}
        else:
            print(f"❌ 获取失败：{data.get('msg', '未知错误')}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求失败：{e}")
        return None


def check_login_status() -> bool:
    """检查登录状态"""
    print("\n🔐 检查登录状态...\n")
    
    url = f"{MOBILE_BASE}/api/sns/web/v1/user/self"
    
    try:
        resp = requests.get(url, headers=get_headers(), timeout=30)
        resp.raise_for_status()
        data = resp.json()
        
        if data.get("success"):
            user = data.get("data", {})
            nickname = user.get("nickname", "未知")
            user_id = user.get("user_id", "未知")
            print(f"✅ 已登录")
            print(f"   👤 昵称：{nickname}")
            print(f"   🆔 ID: {user_id}")
            return True
        else:
            print(f"❌ 未登录或 Cookie 已过期")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求失败：{e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="小红书 API 客户端（直接 Cookie 认证）")
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # status 命令
    status_parser = subparsers.add_parser("status", help="检查登录状态")
    
    # search 命令
    search_parser = subparsers.add_parser("search", help="搜索笔记")
    search_parser.add_argument("keyword", help="搜索关键词")
    search_parser.add_argument("--page", type=int, default=1, help="页码")
    search_parser.add_argument("--size", type=int, default=20, help="每页数量")
    
    # detail 命令
    detail_parser = subparsers.add_parser("detail", help="获取笔记详情")
    detail_parser.add_argument("note_id", help="笔记 ID")
    detail_parser.add_argument("xsec_token", help="Xsec Token")
    
    # feeds 命令
    feeds_parser = subparsers.add_parser("feeds", help="获取推荐 Feed")
    feeds_parser.add_argument("--page", type=int, default=1, help="页码")
    
    args = parser.parse_args()
    
    if args.command == "status":
        check_login_status()
    elif args.command == "search":
        search_notes(args.keyword, args.page, args.size)
    elif args.command == "detail":
        get_note_detail(args.note_id, args.xsec_token)
    elif args.command == "feeds":
        get_feeds(args.page)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
