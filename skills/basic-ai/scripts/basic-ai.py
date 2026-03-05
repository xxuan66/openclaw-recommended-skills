#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "rich", "python-dateutil"]
# ///
"""基础智能包技能 - 对话理解、文本处理、任务自动化、提醒设置"""

import argparse
import os
import sys
import json
import subprocess
from rich.console import Console
from rich import print as rprint
from datetime import datetime, timedelta
from dateutil import parser as date_parser

console = Console()

# 配置
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "qwen3.5-plus")
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "zh")
MEMORY_ENABLED = os.getenv("MEMORY_ENABLED", "true").lower() == "true"
WORKSPACE_DIR = os.getenv("WORKSPACE_DIR", os.path.expanduser("~/.openclaw/workspace"))


def ask_ai(question: str, context: str = "") -> str:
    """调用 AI 模型回答问题"""
    # 使用 openclaw 内置能力
    # 这里简化为返回提示
    return f"""
[AI 回答 - 使用模型：{DEFAULT_MODEL}]

问题：{question}

{f"上下文：{context}" if context else ""}

---
这是一个基础 AI 问答功能。
实际实现需要调用 DashScope 或其他 LLM API。
"""


def translate_text(text: str, target_lang: str = "en") -> str:
    """翻译文本"""
    # 简化版本：返回提示
    translations = {
        "en": "English",
        "zh": "中文",
        "ja": "日本語",
        "ko": "한국어",
        "fr": "Français",
        "de": "Deutsch",
        "es": "Español"
    }
    
    return f"""
[翻译结果 - {translations.get(target_lang, target_lang)}]

原文：{text[:200]}...

---
实际翻译功能需要调用翻译 API。
推荐使用：DeepL、Google Translate、或通义翻译。
"""


def summarize_text(text: str, length: str = "short") -> str:
    """生成文本摘要"""
    # 简单摘要：提取关键句
    sentences = text.replace('。', '\n').replace('.', '\n').split('\n')
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
    
    if length == "short":
        limit = 3
    elif length == "medium":
        limit = 5
    else:
        limit = 10
    
    summary = sentences[:limit]
    
    return f"""
[摘要 - {length}]

{'\n'.join(summary)}

---
原文长度：{len(text)} 字符
摘要长度：{len(''.join(summary))} 字符
"""


def rewrite_text(text: str, style: str = "professional") -> str:
    """改写文本"""
    styles = {
        "professional": "专业风格",
        "casual": "休闲风格",
        "formal": "正式风格",
        "concise": "简洁风格",
        "detailed": "详细风格"
    }
    
    return f"""
[改写 - {styles.get(style, style)}]

原文：{text[:100]}...

改写后：{text[:100]}...

---
实际改写功能需要调用 LLM API 进行风格转换。
"""


def create_reminder(time_str: str, content: str, repeat: str = None) -> dict:
    """创建提醒"""
    try:
        # 解析时间
        reminder_time = date_parser.parse(time_str)
        
        # 如果时间是过去，假设是明天
        if reminder_time < datetime.now():
            reminder_time = reminder_time + timedelta(days=1)
        
        reminder = {
            "id": f"reminder_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "time": reminder_time.isoformat(),
            "content": content,
            "repeat": repeat,
            "created_at": datetime.now().isoformat(),
            "status": "pending"
        }
        
        # 保存到文件
        reminders_file = os.path.join(WORKSPACE_DIR, "memory", "reminders.json")
        os.makedirs(os.path.dirname(reminders_file), exist_ok=True)
        
        reminders = []
        if os.path.exists(reminders_file):
            with open(reminders_file, 'r', encoding='utf-8') as f:
                reminders = json.load(f)
        
        reminders.append(reminder)
        
        with open(reminders_file, 'w', encoding='utf-8') as f:
            json.dump(reminders, f, ensure_ascii=False, indent=2)
        
        return {"success": True, "reminder": reminder}
        
    except Exception as e:
        return {"error": str(e)}


def list_reminders() -> list:
    """列出提醒"""
    reminders_file = os.path.join(WORKSPACE_DIR, "memory", "reminders.json")
    
    if not os.path.exists(reminders_file):
        return []
    
    with open(reminders_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def cmd_ask(args):
    """提问命令"""
    rprint(f"\n[bold]🤖 AI 问答[/bold]")
    rprint(f"模型：{DEFAULT_MODEL}\n")
    
    question = args.question
    if args.file and os.path.exists(args.file):
        with open(args.file, 'r', encoding='utf-8') as f:
            question = f.read()
    
    answer = ask_ai(question, args.context)
    rprint(answer)


def cmd_translate(args):
    """翻译命令"""
    rprint(f"\n[bold]🌐 翻译[/bold]")
    rprint(f"目标语言：{args.lang}\n")
    
    text = args.text
    if args.file and os.path.exists(args.file):
        with open(args.file, 'r', encoding='utf-8') as f:
            text = f.read()
    
    result = translate_text(text, args.lang)
    rprint(result)


def cmd_summarize(args):
    """摘要命令"""
    rprint(f"\n[bold]📝 生成摘要[/bold]")
    rprint(f"长度：{args.length}\n")
    
    text = args.text
    if args.file and os.path.exists(args.file):
        with open(args.file, 'r', encoding='utf-8') as f:
            text = f.read()
    
    result = summarize_text(text, args.length)
    rprint(result)


def cmd_rewrite(args):
    """改写命令"""
    rprint(f"\n[bold]✏️ 改写文本[/bold]")
    rprint(f"风格：{args.style}\n")
    
    text = args.text
    if args.file and os.path.exists(args.file):
        with open(args.file, 'r', encoding='utf-8') as f:
            text = f.read()
    
    result = rewrite_text(text, args.style)
    rprint(result)


def cmd_remind(args):
    """创建提醒命令"""
    rprint(f"\n[bold]⏰ 创建提醒[/bold]")
    rprint(f"时间：{args.time}")
    rprint(f"内容：{args.content}\n")
    
    result = create_reminder(args.time, args.content, args.repeat)
    
    if result.get("success"):
        reminder = result["reminder"]
        rprint(f"[green]✓ 提醒创建成功！[/green]")
        rprint(f"ID: {reminder['id']}")
        rprint(f"时间：{reminder['time']}")
    else:
        rprint(f"[red]✗ 创建失败：{result.get('error')}[/red]")


def cmd_reminders(args):
    """列出提醒命令"""
    rprint(f"\n[bold]📋 提醒列表[/bold]\n")
    
    reminders = list_reminders()
    
    if not reminders:
        rprint("[green]✓ 没有待处理的提醒[/green]")
        return
    
    for r in reminders:
        status = "⏰" if r.get("status") == "pending" else "✅"
        rprint(f"{status} {r['time'][:16]} - {r['content']}")
        if r.get("repeat"):
            rprint(f"   重复：{r['repeat']}")


def cmd_process(args):
    """处理文件命令"""
    rprint(f"\n[bold]📄 处理文件[/bold]")
    rprint(f"文件：{args.file}\n")
    
    if not os.path.exists(args.file):
        rprint(f"[red]文件不存在：{args.file}[/red]")
        return
    
    # 根据文件类型处理
    ext = os.path.splitext(args.file)[1].lower()
    
    rprint(f"文件类型：{ext}")
    rprint(f"文件大小：{os.path.getsize(args.file)} 字节")
    
    # 读取并显示前几行
    with open(args.file, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()[:20]
    
    rprint(f"\n[bold]预览（前 20 行）:[/bold]")
    for i, line in enumerate(lines, 1):
        rprint(f"[dim]{i:3}[/dim] {line.rstrip()}")


def main():
    parser = argparse.ArgumentParser(
        description="基础智能包技能 - 对话理解、文本处理、任务自动化、提醒设置"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # ask 命令
    ask_parser = subparsers.add_parser("ask", help="提问")
    ask_parser.add_argument("question", nargs="?", help="问题")
    ask_parser.add_argument("-f", "--file", help="从文件读取问题")
    ask_parser.add_argument("-c", "--context", help="上下文")
    ask_parser.set_defaults(func=cmd_ask)
    
    # translate 命令
    translate_parser = subparsers.add_parser("translate", help="翻译")
    translate_parser.add_argument("text", nargs="?", help="要翻译的文本")
    translate_parser.add_argument("-f", "--file", help="从文件读取")
    translate_parser.add_argument("-l", "--lang", default="en", help="目标语言")
    translate_parser.set_defaults(func=cmd_translate)
    
    # summarize 命令
    summarize_parser = subparsers.add_parser("summarize", help="生成摘要")
    summarize_parser.add_argument("text", nargs="?", help="要摘要的文本")
    summarize_parser.add_argument("-f", "--file", help="从文件读取")
    summarize_parser.add_argument("-l", "--length", default="short",
                                 choices=["short", "medium", "long"],
                                 help="摘要长度")
    summarize_parser.set_defaults(func=cmd_summarize)
    
    # rewrite 命令
    rewrite_parser = subparsers.add_parser("rewrite", help="改写文本")
    rewrite_parser.add_argument("text", nargs="?", help="要改写的文本")
    rewrite_parser.add_argument("-f", "--file", help="从文件读取")
    rewrite_parser.add_argument("-s", "--style", default="professional",
                               choices=["professional", "casual", "formal", "concise", "detailed"],
                               help="改写风格")
    rewrite_parser.set_defaults(func=cmd_rewrite)
    
    # remind 命令
    remind_parser = subparsers.add_parser("remind", help="创建提醒")
    remind_parser.add_argument("time", help="提醒时间")
    remind_parser.add_argument("content", help="提醒内容")
    remind_parser.add_argument("-r", "--repeat", help="重复规则 (daily/weekly/monthly)")
    remind_parser.set_defaults(func=cmd_remind)
    
    # reminders 命令
    reminders_parser = subparsers.add_parser("reminders", help="列出提醒")
    reminders_parser.set_defaults(func=cmd_reminders)
    
    # process 命令
    process_parser = subparsers.add_parser("process", help="处理文件")
    process_parser.add_argument("file", help="文件路径")
    process_parser.set_defaults(func=cmd_process)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    args.func(args)


if __name__ == "__main__":
    main()
