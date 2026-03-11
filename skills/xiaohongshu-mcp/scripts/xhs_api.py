#!/usr/bin/env python3
"""
Xiaohongshu API Client - 使用 xhs 库实现搜索、详情等功能

无需本地服务器，直接使用 Cookie 认证
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

try:
    from xhs import XhsClient
    from xhs.help import sign as local_sign
    from dotenv import load_dotenv
    import os
except ImportError:
    print("❌ 缺少依赖：pip install xhs python-dotenv")
    print("   或运行：source ../xhs-note-creator/.venv/bin/activate")
    sys.exit(1)


def load_cookie() -> str:
    """从 .env 文件加载 Cookie"""
    env_paths = [
        Path(__file__).parent.parent / '.env',
        Path.cwd() / '.env',
        Path(__file__).parent.parent.parent / 'xhs-note-creator' / '.env',
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


def get_client() -> XhsClient:
    """创建 XhsClient 实例"""
    cookie = load_cookie()
    
    # 解析 a1 值
    cookies = {}
    for item in cookie.split(';'):
        item = item.strip()
        if '=' in item:
            key, value = item.split('=', 1)
            cookies[key.strip()] = value.strip()
    
    a1 = cookies.get('a1', '')
    b1 = cookies.get('b1', '')
    
    def sign_func(uri, data=None, **kwargs):
        a1_val = kwargs.get('a1', a1)
        b1_val = kwargs.get('b1', b1)
        return local_sign(uri, data, a1=a1_val, b1=b1_val)
    
    return XhsClient(cookie=cookie, sign=sign_func)


def check_status():
    """检查登录状态"""
    print("\n🔐 检查登录状态...\n")
    
    try:
        client = get_client()
        info = client.get_self_info()
        
        if info:
            print(f"✅ 已登录")
            print(f"   👤 昵称：{info.get('nickname', '未知')}")
            print(f"   🆔 ID: {info.get('user_id', '未知')}")
            return True
        else:
            print(f"❌ 未登录或 Cookie 已过期")
            return False
    except Exception as e:
        print(f"❌ 错误：{e}")
        return False


def search_notes(keyword: str, page: int = 1, page_size: int = 20):
    """搜索笔记"""
    print(f"\n🔍 搜索：{keyword}")
    print(f"📄 页码：{page}, 每页：{page_size} 条\n")
    
    try:
        client = get_client()
        
        # 使用 xhs 库的搜索功能
        result = client.get_note_by_keyword(keyword)
        
        if result and result.get("success"):
            items = result.get("data", {}).get("items", [])
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
            
            return result
        else:
            print(f"❌ 搜索失败：{result}")
            return None
            
    except Exception as e:
        print(f"❌ 错误：{e}")
        return None


def get_note_detail(note_id: str, xsec_token: str):
    """获取笔记详情"""
    print(f"\n📝 获取笔记详情：{note_id}\n")
    
    try:
        client = get_client()
        
        # 获取笔记详情
        detail = client.get_note_by_id(note_id)
        
        if detail:
            note = detail.get("data", {})
            note_card = note.get("note_card", {})
            interact = note_card.get("interact_info", {})
            user = note_card.get("user", {})
            
            print(f"📌 标题：{note_card.get('title', '无标题')}")
            print(f"👤 作者：{user.get('nickname', '未知')}")
            print(f"📍 IP: {note_card.get('ip_location', '未知')}")
            print(f"\n📄 内容：\n{note_card.get('desc', '无内容')}\n")
            print(f"❤️ 点赞：{interact.get('liked_count', '0')}")
            print(f"⭐ 收藏：{interact.get('collected_count', '0')}")
            print(f"💬 评论：{interact.get('comment_count', '0')}")
            
            # 图片
            images = note_card.get("image_list", [])
            if images:
                print(f"\n🖼️ 图片 ({len(images)} 张):")
                for img in images[:5]:
                    print(f"  - {img.get('url', '')}")
            
            return detail
        else:
            print(f"❌ 获取失败")
            return None
            
    except Exception as e:
        print(f"❌ 错误：{e}")
        return None


def get_feeds():
    """获取推荐 Feed"""
    print(f"\n📋 获取推荐 Feed\n")
    
    try:
        client = get_client()
        
        # 获取首页推荐
        result = client.get_home_feed(category="")
        
        if result and result.get("success"):
            items = result.get("data", {}).get("items", [])
            print(f"✅ 获取到 {len(items)} 条推荐：\n")
            
            for i, item in enumerate(items[:10], 1):
                note = item.get("note_card", {})
                title = note.get("title", "无标题")[:50]
                print(f"[{i}] {title}")
            
            return result
        else:
            print(f"❌ 获取失败：{result}")
            return None
            
    except Exception as e:
        print(f"❌ 错误：{e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="小红书 API 客户端（使用 xhs 库）")
    
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
    
    args = parser.parse_args()
    
    if args.command == "status":
        check_status()
    elif args.command == "search":
        search_notes(args.keyword, args.page, args.size)
    elif args.command == "detail":
        # 注意：xhs 库可以直接用 note_id 获取详情，不需要 xsec_token
        get_note_detail(args.note_id, args.xsec_token)
    elif args.command == "feeds":
        get_feeds()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
