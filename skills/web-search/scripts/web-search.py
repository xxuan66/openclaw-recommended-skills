#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "rich", "beautifulsoup4", "lxml"]
# ///
"""网页搜索 & 分析技能 - 智能搜索、内容提取、深度分析

此技能封装 searxng 和 web_fetch 工具，提供增强的搜索 API。
"""

import argparse
import os
import sys
import json
import subprocess
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from urllib.parse import urlparse

console = Console()

# 配置
SEARCH_ENGINE = os.getenv("SEARCH_ENGINE", "searxng")
SEARXNG_URL = os.getenv("SEARXNG_URL", "http://localhost:8080")
MAX_RESULTS = int(os.getenv("MAX_RESULTS", "10"))


def search_searxng(query: str, category: str = "general", limit: int = 10) -> list:
    """使用 SearXNG 搜索"""
    import httpx
    
    try:
        params = {
            "q": query,
            "format": "json",
            "categories": category,
            "language": "zh-CN"
        }
        
        response = httpx.get(
            f"{SEARXNG_URL}/search",
            params=params,
            timeout=30,
            verify=False
        )
        
        data = response.json()
        results = data.get("results", [])[:limit]
        
        return [{
            "title": r.get("title", "无标题"),
            "url": r.get("url", ""),
            "content": r.get("content", "")[:200],
            "engine": ", ".join(r.get("engines", [])),
            "score": r.get("score", 0)
        } for r in results]
        
    except Exception as e:
        return [{"error": str(e)}]


def fetch_url(url: str) -> dict:
    """获取网页内容"""
    try:
        result = subprocess.run(
            ["openclaw", "web", "fetch", url, "--extract-mode", "markdown"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            return {"success": True, "content": result.stdout}
        return {"error": result.stderr}
    except Exception as e:
        return {"error": str(e)}


def analyze_content(content: str, url: str = "") -> dict:
    """分析网页内容"""
    # 简单分析
    words = content.split()
    word_count = len(words)
    
    # 提取可能的标题
    title = ""
    for line in content.split('\n')[:10]:
        if line.startswith('#'):
            title = line.replace('#', '').strip()
            break
    
    # 提取链接
    import re
    links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)[:10]
    
    return {
        "url": url,
        "title": title,
        "word_count": word_count,
        "link_count": len(links),
        "links": links,
        "summary": content[:500] + "..." if len(content) > 500 else content
    }


def cmd_search(args):
    """搜索命令"""
    rprint(f"\n[bold]🔍 搜索：{args.query}[/bold]")
    rprint(f"引擎：{SEARCH_ENGINE}")
    rprint(f"类别：{args.category}\n")
    
    results = search_searxng(args.query, args.category, args.limit)
    
    if "error" in results[0]:
        rprint(f"[red]搜索失败：{results[0]['error']}[/red]")
        return
    
    if not results:
        rprint("[yellow]未找到结果[/yellow]")
        return
    
    table = Table(title=f"搜索结果 ({len(results)} 个)")
    table.add_column("#", style="dim", width=3)
    table.add_column("标题", style="bold")
    table.add_column("来源", width=15)
    table.add_column("URL", width=50)
    
    for i, r in enumerate(results, 1):
        title = r["title"][:50]
        engine = r.get("engine", "unknown")[:13]
        url = r["url"][:45] + "..." if len(r["url"]) > 45 else r["url"]
        
        table.add_row(str(i), title, engine, url)
    
    console.print(table)
    
    # 显示前 3 个摘要
    rprint(f"\n[bold]摘要:[/bold]")
    for i, r in enumerate(results[:3], 1):
        rprint(f"\n[bold cyan]{i}. {r['title']}[/bold cyan]")
        if r.get("content"):
            rprint(f"   [dim]{r['content']}...[/dim]")


def cmd_analyze(args):
    """分析网页命令"""
    rprint(f"\n[bold]📊 分析网页[/bold]")
    rprint(f"URL: {args.url}\n")
    
    result = fetch_url(args.url)
    
    if result.get("error"):
        rprint(f"[red]获取失败：{result['error']}[/red]")
        return
    
    analysis = analyze_content(result["content"], args.url)
    
    rprint(f"[bold]标题:[/bold] {analysis['title']}")
    rprint(f"[bold]字数:[/bold] {analysis['word_count']}")
    rprint(f"[bold]链接数:[/bold] {analysis['link_count']}")
    
    rprint(f"\n[bold]摘要:[/bold]")
    rprint(analysis['summary'])
    
    if analysis['links']:
        rprint(f"\n[bold]相关链接:[/bold]")
        for text, link in analysis['links'][:5]:
            rprint(f"  • {text}: {link}")


def cmd_compare(args):
    """对比多个网页命令"""
    rprint(f"\n[bold]⚖️ 对比网页[/bold]\n")
    
    results = []
    for url in args.urls:
        rprint(f"[dim]获取：{url}[/dim]")
        result = fetch_url(url)
        if result.get("success"):
            analysis = analyze_content(result["content"], url)
            results.append(analysis)
    
    if not results:
        rprint("[red]无法获取任何网页内容[/red]")
        return
    
    table = Table(title="网页对比")
    table.add_column("URL", width=40)
    table.add_column("标题", width=30)
    table.add_column("字数", justify="right")
    table.add_column("链接数", justify="right")
    
    for r in results:
        url_short = r['url'][:35] + "..." if len(r['url']) > 35 else r['url']
        table.add_row(
            url_short,
            r['title'][:28],
            str(r['word_count']),
            str(r['link_count'])
        )
    
    console.print(table)


def cmd_summarize(args):
    """生成网页摘要命令"""
    rprint(f"\n[bold]📝 生成摘要[/bold]")
    rprint(f"URL: {args.url}\n")
    
    result = fetch_url(args.url)
    
    if result.get("error"):
        rprint(f"[red]获取失败：{result['error']}[/red]")
        return
    
    analysis = analyze_content(result["content"], args.url)
    
    rprint(f"[bold]{analysis['title']}[/bold]\n")
    rprint(analysis['summary'])


def main():
    parser = argparse.ArgumentParser(
        description="网页搜索 & 分析技能 - 智能搜索、内容提取、深度分析"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # search 命令
    search_parser = subparsers.add_parser("search", help="搜索网页")
    search_parser.add_argument("query", help="搜索关键词")
    search_parser.add_argument("-n", "--limit", type=int, default=MAX_RESULTS, help="结果数量")
    search_parser.add_argument("-c", "--category", default="general",
                              choices=["general", "news", "images", "videos", "science"],
                              help="搜索类别")
    search_parser.set_defaults(func=cmd_search)
    
    # analyze 命令
    analyze_parser = subparsers.add_parser("analyze", help="分析网页")
    analyze_parser.add_argument("url", help="网页 URL")
    analyze_parser.set_defaults(func=cmd_analyze)
    
    # compare 命令
    compare_parser = subparsers.add_parser("compare", help="对比多个网页")
    compare_parser.add_argument("urls", nargs="+", help="网页 URL 列表")
    compare_parser.set_defaults(func=cmd_compare)
    
    # summarize 命令
    summarize_parser = subparsers.add_parser("summarize", help="生成网页摘要")
    summarize_parser.add_argument("url", help="网页 URL")
    summarize_parser.set_defaults(func=cmd_summarize)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    args.func(args)


if __name__ == "__main__":
    main()
