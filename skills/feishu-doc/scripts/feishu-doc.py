#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "rich", "markdown"]
# ///
"""飞书文档技能 - 读写编辑飞书文档，知识库管理

此技能封装 OpenClaw 内置的 feishu_doc 工具，提供 CLI 接口。
"""

import argparse
import os
import sys
import json
import subprocess
from rich.console import Console
from rich import print as rprint

console = Console()

# 配置
FEISHU_APP_ID = os.getenv("FEISHU_APP_ID", "")
FEISHU_APP_SECRET = os.getenv("FEISHU_APP_SECRET", "")
DEFAULT_FOLDER_TOKEN = os.getenv("DEFAULT_FOLDER_TOKEN", "")


def run_feishu_command(action: str, **kwargs) -> dict:
    """执行飞书文档命令（通过 openclaw 工具）"""
    # 构建命令
    cmd = ["openclaw", "feishu", "doc", action]
    
    for key, value in kwargs.items():
        if value:
            cmd.append(f"--{key.replace('_', '-')}")
            cmd.append(str(value))
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            return {"success": True, "output": result.stdout}
        return {"error": result.stderr or result.stdout}
    except Exception as e:
        return {"error": str(e)}


def cmd_read(args):
    """读取文档命令"""
    rprint(f"\n[bold]📖 读取飞书文档[/bold]")
    rprint(f"文档：{args.doc}\n")
    
    # 提取 doc token
    doc_token = args.doc
    if "/docx/" in args.doc:
        doc_token = args.doc.split("/docx/")[-1].split("?")[0].split("/")[0]
    
    result = run_feishu_command("read", doc_token=doc_token)
    
    if result.get("success"):
        rprint(result["output"])
    else:
        rprint(f"[red]读取失败：{result.get('error')}[/red]")


def cmd_create(args):
    """创建文档命令"""
    rprint(f"\n[bold]➕ 创建飞书文档[/bold]")
    rprint(f"标题：{args.title}\n")
    
    content = args.content
    if args.file and os.path.exists(args.file):
        with open(args.file, 'r', encoding='utf-8') as f:
            content = f.read()
    
    result = run_feishu_command(
        "create",
        title=args.title,
        content=content,
        folder_token=args.folder or DEFAULT_FOLDER_TOKEN
    )
    
    if result.get("success"):
        rprint(f"[green]✓ 文档创建成功！[/green]")
        rprint(result["output"])
    else:
        rprint(f"[red]创建失败：{result.get('error')}[/red]")


def cmd_update(args):
    """更新文档命令"""
    rprint(f"\n[bold]✏️ 更新飞书文档[/bold]")
    rprint(f"文档：{args.doc}\n")
    
    content = args.content
    if args.file and os.path.exists(args.file):
        with open(args.file, 'r', encoding='utf-8') as f:
            content = f.read()
    
    doc_token = args.doc
    if "/docx/" in args.doc:
        doc_token = args.doc.split("/docx/")[-1].split("?")[0].split("/")[0]
    
    result = run_feishu_command("write", doc_token=doc_token, content=content)
    
    if result.get("success"):
        rprint(f"[green]✓ 文档更新成功！[/green]")
    else:
        rprint(f"[red]更新失败：{result.get('error')}[/red]")


def cmd_list(args):
    """列出文档命令"""
    rprint(f"\n[bold]📋 列出飞书文档[/bold]\n")
    
    folder_token = args.folder or DEFAULT_FOLDER_TOKEN
    
    result = run_feishu_command("list", folder_token=folder_token)
    
    if result.get("success"):
        rprint(result["output"])
    else:
        rprint(f"[red]获取失败：{result.get('error')}[/red]")


def cmd_summary(args):
    """生成文档摘要命令"""
    rprint(f"\n[bold]📝 生成文档摘要[/bold]")
    rprint(f"文档：{args.doc}\n")
    
    # 先读取文档
    doc_token = args.doc
    if "/docx/" in args.doc:
        doc_token = args.doc.split("/docx/")[-1].split("?")[0].split("/")[0]
    
    result = run_feishu_command("read", doc_token=doc_token)
    
    if result.get("success"):
        content = result["output"]
        # 简单摘要：取前 500 字
        summary = content[:500] + "..." if len(content) > 500 else content
        rprint(f"[bold]摘要:[/bold]\n{summary}")
    else:
        rprint(f"[red]读取失败：{result.get('error')}[/red]")


def main():
    parser = argparse.ArgumentParser(
        description="飞书文档技能 - 读写编辑飞书文档，知识库管理"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # read 命令
    read_parser = subparsers.add_parser("read", help="读取文档")
    read_parser.add_argument("doc", help="文档链接或 ID")
    read_parser.set_defaults(func=cmd_read)
    
    # create 命令
    create_parser = subparsers.add_parser("create", help="创建文档")
    create_parser.add_argument("title", help="文档标题")
    create_parser.add_argument("-c", "--content", help="文档内容")
    create_parser.add_argument("-f", "--file", help="从文件读取内容")
    create_parser.add_argument("--folder", help="目标文件夹 Token")
    create_parser.set_defaults(func=cmd_create)
    
    # update 命令
    update_parser = subparsers.add_parser("update", help="更新文档")
    update_parser.add_argument("doc", help="文档链接或 ID")
    update_parser.add_argument("-c", "--content", help="新内容")
    update_parser.add_argument("-f", "--file", help="从文件读取内容")
    update_parser.set_defaults(func=cmd_update)
    
    # list 命令
    list_parser = subparsers.add_parser("list", help="列出文档")
    list_parser.add_argument("--folder", help="文件夹 Token")
    list_parser.set_defaults(func=cmd_list)
    
    # summary 命令
    summary_parser = subparsers.add_parser("summary", help="生成摘要")
    summary_parser.add_argument("doc", help="文档链接或 ID")
    summary_parser.set_defaults(func=cmd_summary)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    args.func(args)


if __name__ == "__main__":
    main()
