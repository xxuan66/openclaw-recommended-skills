#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "rich", "yaml"]
# ///
"""博客写手技能 - 长文写作、SEO 优化、多平台发布"""

import argparse
import os
import sys
import json
import httpx
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from datetime import datetime

console = Console()

# 配置
BLOG_PLATFORM = os.getenv("BLOG_PLATFORM", "wordpress")
BLOG_API_URL = os.getenv("BLOG_API_URL", "")
BLOG_API_KEY = os.getenv("BLOG_API_KEY", "")
BLOG_AUTHOR = os.getenv("BLOG_AUTHOR", "Author")


def generate_outline(topic: str) -> dict:
    """生成文章大纲"""
    outline = {
        "title": f"{topic}：完整指南",
        "sections": [
            {"heading": "引言", "points": ["背景介绍", "文章目的", "读者收益"]},
            {"heading": f"{topic} 的基础概念", "points": ["定义", "核心要素", "重要性"]},
            {"heading": f"{topic} 的实践方法", "points": ["步骤一", "步骤二", "步骤三", "注意事项"]},
            {"heading": "案例分析", "points": ["成功案例", "失败教训", "关键启示"]},
            {"heading": "常见问题", "points": ["Q1", "Q2", "Q3"]},
            {"heading": "总结", "points": ["核心要点回顾", "行动建议"]}
        ]
    }
    return outline


def write_content(outline: dict, style: str = "professional") -> str:
    """根据大纲撰写内容"""
    content = f"# {outline['title']}\n\n"
    content += f"*作者：{BLOG_AUTHOR} | 更新时间：{datetime.now().strftime('%Y-%m-%d')}*\n\n"
    
    for section in outline['sections']:
        content += f"## {section['heading']}\n\n"
        for point in section['points']:
            content += f"- {point}\n"
        content += "\n"
    
    return content


def generate_seo_meta(title: str, content: str) -> dict:
    """生成 SEO 元数据"""
    # 提取关键词（简化版）
    keywords = [title.split()[0], "指南", "教程", "2026"]
    
    # 生成描述
    description = content[:150].replace('\n', ' ') + "..."
    
    return {
        "title": title,
        "description": description,
        "keywords": ", ".join(keywords),
        "slug": title.lower().replace(" ", "-").replace(":", ""),
        "meta_robots": "index, follow"
    }


def publish_to_wordpress(title: str, content: str, status: str = "draft") -> dict:
    """发布到 WordPress"""
    if not BLOG_API_URL or not BLOG_API_KEY:
        return {"error": "请配置 BLOG_API_URL 和 BLOG_API_KEY"}
    
    try:
        response = httpx.post(
            f"{BLOG_API_URL}/wp-json/wp/v2/posts",
            headers={
                "Authorization": f"Bearer {BLOG_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "title": title,
                "content": content,
                "status": status,
                "excerpt": content[:200]
            },
            timeout=60
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}


def cmd_outline(args):
    """生成大纲命令"""
    rprint(f"\n[bold]生成文章大纲：{args.topic}[/bold]\n")
    outline = generate_outline(args.topic)
    
    rprint(f"[bold cyan]标题：[/bold cyan] {outline['title']}\n")
    rprint("[bold cyan]章节：[/bold cyan]")
    
    for i, section in enumerate(outline['sections'], 1):
        rprint(f"\n  [bold]{i}. {section['heading']}[/bold]")
        for point in section['points']:
            rprint(f"     • {point}")
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(outline, f, ensure_ascii=False, indent=2)
        rprint(f"\n[green]大纲已保存到：{args.output}[/green]")


def cmd_write(args):
    """撰写文章命令"""
    rprint(f"\n[bold]撰写文章：{args.topic}[/bold]\n")
    
    # 生成大纲
    outline = generate_outline(args.topic)
    # 撰写内容
    content = write_content(outline, args.style)
    # 生成 SEO
    seo = generate_seo_meta(outline['title'], content)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(content)
        rprint(f"[green]文章已保存到：{args.output}[/green]")
        
        # 保存 SEO 元数据
        seo_file = args.output.replace('.md', '_seo.json')
        with open(seo_file, 'w', encoding='utf-8') as f:
            json.dump(seo, f, ensure_ascii=False, indent=2)
        rprint(f"[green]SEO 元数据已保存到：{seo_file}[/green]")
    else:
        rprint(content)
        rprint(f"\n[bold]SEO 元数据:[/bold]")
        rprint(f"  Title: {seo['title']}")
        rprint(f"  Description: {seo['description']}")
        rprint(f"  Keywords: {seo['keywords']}")


def cmd_publish(args):
    """发布文章命令"""
    if not os.path.exists(args.file):
        rprint(f"[red]文件不存在：{args.file}[/red]")
        return
    
    with open(args.file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取标题
    title = args.title or "未命名文章"
    if content.startswith('#'):
        title = content.split('\n')[0].replace('#', '').strip()
    
    rprint(f"[bold]发布到 {BLOG_PLATFORM}...[/bold]")
    
    status = "draft" if args.draft else "publish"
    result = publish_to_wordpress(title, content, status)
    
    if "id" in result:
        rprint(f"[green]✓ 发布成功！[/green]")
        rprint(f"文章 ID: {result['id']}")
        if "link" in result:
            rprint(f"链接：{result['link']}")
    else:
        rprint(f"[red]✗ 发布失败：{result.get('error', result)}[/red]")


def main():
    parser = argparse.ArgumentParser(
        description="博客写手技能 - 长文写作、SEO 优化、多平台发布"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # outline 命令
    outline_parser = subparsers.add_parser("outline", help="生成文章大纲")
    outline_parser.add_argument("topic", help="文章主题")
    outline_parser.add_argument("-o", "--output", help="输出文件路径")
    outline_parser.set_defaults(func=cmd_outline)
    
    # write 命令
    write_parser = subparsers.add_parser("write", help="撰写文章")
    write_parser.add_argument("topic", help="文章主题")
    write_parser.add_argument("-s", "--style", default="professional",
                             choices=["professional", "casual", "technical", "storytelling"],
                             help="写作风格")
    write_parser.add_argument("-o", "--output", help="输出文件路径")
    write_parser.set_defaults(func=cmd_write)
    
    # publish 命令
    publish_parser = subparsers.add_parser("publish", help="发布文章")
    publish_parser.add_argument("file", help="文章文件路径")
    publish_parser.add_argument("-t", "--title", help="文章标题")
    publish_parser.add_argument("--draft", action="store_true", help="发布为草稿")
    publish_parser.set_defaults(func=cmd_publish)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    args.func(args)


if __name__ == "__main__":
    main()
