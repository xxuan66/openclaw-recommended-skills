#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "rich", "markdown"]
# ///
"""微信公众号技能 - 选题、写作、排版、发布全流程"""

import argparse
import os
import sys
import json
import httpx
from rich.console import Console
from rich.table import Table
from rich import print as rprint
import markdown

console = Console()

# 配置
WECHAT_APP_ID = os.getenv("WECHAT_APP_ID", "")
WECHAT_APP_SECRET = os.getenv("WECHAT_APP_SECRET", "")
WECHAT_BASE_URL = "https://api.weixin.qq.com/cgi-bin"


def get_access_token() -> str:
    """获取微信公众号 access token"""
    if not WECHAT_APP_ID or not WECHAT_APP_SECRET:
        console.print("[red]错误：请配置 WECHAT_APP_ID 和 WECHAT_APP_SECRET[/red]")
        return ""
    
    try:
        response = httpx.get(
            f"{WECHAT_BASE_URL}/token",
            params={
                "grant_type": "client_credential",
                "appid": WECHAT_APP_ID,
                "secret": WECHAT_APP_SECRET
            },
            timeout=30
        )
        data = response.json()
        if "access_token" in data:
            return data["access_token"]
        else:
            console.print(f"[red]获取 token 失败：{data}[/red]")
            return ""
    except Exception as e:
        console.print(f"[red]请求失败：{e}[/red]")
        return ""


def generate_topics(keyword: str, limit: int = 5) -> list:
    """生成公众号选题建议"""
    topics = [
        f"{keyword} 的 5 个关键趋势",
        f"为什么{keyword}如此重要？深度解析",
        f"{keyword}新手入门指南",
        f"{keyword}常见误区及解决方案",
        f"2026 年{keyword}行业展望"
    ]
    return topics[:limit]


def write_article(topic: str, style: str = "professional") -> str:
    """撰写公众号文章"""
    # 这里调用 AI 模型生成文章内容
    # 简化版本：返回模板
    article = f"""# {topic}

## 引言

在当今快速发展的时代，{topic}成为了越来越多人关注的话题...

## 核心观点

1. **第一个关键点**：详细说明...
2. **第二个关键点**：深入分析...
3. **第三个关键点**：实践建议...

## 案例分析

让我们通过一个实际案例来说明...

## 总结

{topic}是一个值得深入探索的领域，希望本文能为你提供一些有价值的见解。

---
*欢迎关注我们的公众号，获取更多优质内容*"""
    return article


def markdown_to_wechat_html(md_content: str) -> str:
    """将 Markdown 转换为微信公众号 HTML 格式"""
    # 基础 Markdown 转 HTML
    html = markdown.markdown(md_content, extensions=['extra', 'codehilite'])
    
    # 添加微信公众号样式
    styled_html = f"""
<section style="font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei UI', 'Microsoft YaHei', Arial, sans-serif; line-height: 1.75; letter-spacing: 0.5px; word-spacing: 2px; font-size: 16px; color: #333;">
{html}
</section>
"""
    return styled_html


def create_draft(title: str, content: str, access_token: str) -> dict:
    """创建公众号草稿"""
    if not access_token:
        return {"error": "缺少 access token"}
    
    try:
        response = httpx.post(
            f"{WECHAT_BASE_URL}/draft/add?access_token={access_token}",
            json={
                "articles": [{
                    "title": title,
                    "content": content,
                    "thumb_media_id": "",  # 需要上传图片获取
                    "author": "",
                    "digest": content[:100] + "..."
                }]
            },
            timeout=60
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}


def cmd_topics(args):
    """生成选题命令"""
    topics = generate_topics(args.keyword, args.limit)
    
    table = Table(title=f"📝 公众号选题建议：{args.keyword}")
    table.add_column("#", style="dim", width=3)
    table.add_column("选题", style="bold")
    
    for i, topic in enumerate(topics, 1):
        table.add_row(str(i), topic)
    
    console.print(table)


def cmd_write(args):
    """撰写文章命令"""
    rprint(f"\n[bold]正在撰写文章：{args.topic}[/bold]\n")
    article = write_article(args.topic, args.style)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(article)
        rprint(f"[green]文章已保存到：{args.output}[/green]")
    else:
        rprint(article)


def cmd_draft(args):
    """创建草稿命令"""
    # 读取文章
    if os.path.exists(args.file):
        with open(args.file, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        content = args.file
    
    # 转换格式
    html_content = markdown_to_wechat_html(content)
    
    # 获取 token
    access_token = get_access_token()
    
    if access_token:
        # 提取标题
        title = args.title or "未命名文章"
        
        # 创建草稿
        result = create_draft(title, html_content, access_token)
        
        if "media_id" in result:
            rprint(f"[green]✓ 草稿创建成功！[/green]")
            rprint(f"草稿 ID: {result['media_id']}")
        else:
            rprint(f"[red]✗ 草稿创建失败：{result}[/red]")
    else:
        rprint("[yellow]未配置微信公众号凭证，仅生成 HTML 预览[/yellow]")
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(html_content)
            rprint(f"[green]HTML 已保存到：{args.output}[/green]")


def main():
    parser = argparse.ArgumentParser(
        description="微信公众号技能 - 选题、写作、排版、发布",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # topics 命令
    topics_parser = subparsers.add_parser("topics", help="生成选题建议")
    topics_parser.add_argument("keyword", help="关键词")
    topics_parser.add_argument("-n", "--limit", type=int, default=5, help="生成数量")
    topics_parser.set_defaults(func=cmd_topics)
    
    # write 命令
    write_parser = subparsers.add_parser("write", help="撰写文章")
    write_parser.add_argument("topic", help="文章主题")
    write_parser.add_argument("-s", "--style", default="professional", 
                             choices=["professional", "casual", "storytelling"],
                             help="写作风格")
    write_parser.add_argument("-o", "--output", help="输出文件路径")
    write_parser.set_defaults(func=cmd_write)
    
    # draft 命令
    draft_parser = subparsers.add_parser("draft", help="创建草稿")
    draft_parser.add_argument("file", help="文章文件路径或内容")
    draft_parser.add_argument("-t", "--title", help="文章标题")
    draft_parser.add_argument("-o", "--output", help="输出 HTML 文件路径")
    draft_parser.set_defaults(func=cmd_draft)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    args.func(args)


if __name__ == "__main__":
    main()
