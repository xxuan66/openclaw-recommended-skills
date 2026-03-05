#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "rich"]
# ///
"""Mify LLM API 技能 - OpenAI 兼容的大语言模型接口"""

import argparse
import os
import sys
import json
import httpx
from rich.console import Console
from rich import print as rprint
from rich.markdown import Markdown

console = Console()

# 配置
MIFY_API_KEY = os.getenv("MIFY_API_KEY", "")
MIFY_BASE_URL = os.getenv("MIFY_BASE_URL", "http://model.mify.ai.srv/v1")
MIFY_MODEL = os.getenv("MIFY_MODEL", "")
MIFY_MAX_TOKENS = int(os.getenv("MIFY_MAX_TOKENS", "2048"))
MIFY_TEMPERATURE = float(os.getenv("MIFY_TEMPERATURE", "0.7"))


def get_headers() -> dict:
    """获取请求头"""
    headers = {
        "Content-Type": "application/json"
    }
    if MIFY_API_KEY:
        headers["Authorization"] = f"Bearer {MIFY_API_KEY}"
    return headers


def list_models() -> list:
    """获取可用模型列表"""
    try:
        response = httpx.get(
            f"{MIFY_BASE_URL}/models",
            headers=get_headers(),
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        return data.get("data", [])
    except Exception as e:
        return [{"error": str(e)}]


def chat_completion(messages: list, model: str = None, **kwargs) -> dict:
    """对话补全"""
    try:
        payload = {
            "model": model or MIFY_MODEL or "default",
            "messages": messages,
            "max_tokens": kwargs.get("max_tokens", MIFY_MAX_TOKENS),
            "temperature": kwargs.get("temperature", MIFY_TEMPERATURE),
            "stream": False
        }
        
        response = httpx.post(
            f"{MIFY_BASE_URL}/chat/completions",
            headers=get_headers(),
            json=payload,
            timeout=120
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}


def text_completion(prompt: str, model: str = None, **kwargs) -> dict:
    """文本补全"""
    try:
        payload = {
            "model": model or MIFY_MODEL or "default",
            "prompt": prompt,
            "max_tokens": kwargs.get("max_tokens", MIFY_MAX_TOKENS),
            "temperature": kwargs.get("temperature", MIFY_TEMPERATURE),
            "stream": False
        }
        
        response = httpx.post(
            f"{MIFY_BASE_URL}/completions",
            headers=get_headers(),
            json=payload,
            timeout=120
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}


def create_embeddings(text: str, model: str = None) -> dict:
    """生成嵌入向量"""
    try:
        payload = {
            "model": model or MIFY_MODEL or "embedding",
            "input": text
        }
        
        response = httpx.post(
            f"{MIFY_BASE_URL}/embeddings",
            headers=get_headers(),
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}


def cmd_models(args):
    """列出模型命令"""
    rprint(f"\n[bold]🤖 Mify 可用模型[/bold]")
    rprint(f"API: {MIFY_BASE_URL}\n")
    
    models = list_models()
    
    if "error" in models[0]:
        rprint(f"[red]获取失败：{models[0]['error']}[/red]")
        rprint(f"\n[dim]请检查：[/dim]")
        rprint(f"  • MIFY_API_KEY 是否已配置")
        rprint(f"  • API URL 是否正确")
        rprint(f"  • 网络连接是否正常")
        return
    
    from rich.table import Table
    table = Table(title=f"可用模型 ({len(models)} 个)")
    table.add_column("ID", style="cyan")
    table.add_column("类型", width=15)
    table.add_column("描述", width=40)
    
    for model in models:
        model_id = model.get("id", "unknown")
        model_type = "LLM" if "chat" in model_id or "instruct" in model_id else "Embedding"
        description = model.get("description", "")[:38]
        
        table.add_row(model_id, model_type, description)
    
    console.print(table)


def cmd_chat(args):
    """对话命令"""
    if not MIFY_API_KEY:
        rprint("[yellow]⚠️  警告：未配置 MIFY_API_KEY[/yellow]")
        rprint("[dim]请设置环境变量：export MIFY_API_KEY='your-key'[/dim]\n")
    
    rprint(f"\n[bold]💬 对话[/bold]")
    rprint(f"模型：{args.model or MIFY_MODEL or 'default'}")
    rprint(f"问题：{args.message}\n")
    
    messages = [
        {"role": "system", "content": "你是一个有帮助的 AI 助手。"},
        {"role": "user", "content": args.message}
    ]
    
    result = chat_completion(
        messages,
        model=args.model,
        max_tokens=args.max_tokens,
        temperature=args.temperature
    )
    
    if "error" in result:
        rprint(f"[red]请求失败：{result['error']}[/red]")
        return
    
    # 提取回复
    choices = result.get("choices", [])
    if choices:
        reply = choices[0].get("message", {}).get("content", "")
        rprint(f"[bold green]AI 回复:[/bold green]\n")
        console.print(Markdown(reply))
        
        # 显示使用量
        usage = result.get("usage", {})
        if usage:
            rprint(f"\n[dim]Tokens: {usage.get('total_tokens', 'N/A')} (prompt: {usage.get('prompt_tokens', 0)}, completion: {usage.get('completion_tokens', 0)})[/dim]")
    else:
        rprint(f"[yellow]无回复内容[/yellow]")


def cmd_complete(args):
    """文本补全命令"""
    rprint(f"\n[bold]✏️ 文本补全[/bold]")
    rprint(f"模型：{args.model or MIFY_MODEL or 'default'}")
    rprint(f"提示：{args.prompt[:100]}...\n")
    
    result = text_completion(
        args.prompt,
        model=args.model,
        max_tokens=args.max_tokens,
        temperature=args.temperature
    )
    
    if "error" in result:
        rprint(f"[red]请求失败：{result['error']}[/red]")
        return
    
    choices = result.get("choices", [])
    if choices:
        completion = choices[0].get("text", "")
        rprint(f"[bold green]补全结果:[/bold green]\n")
        console.print(Markdown(completion))
    else:
        rprint(f"[yellow]无补全内容[/yellow]")


def cmd_embed(args):
    """嵌入向量命令"""
    rprint(f"\n[bold]🔢 生成嵌入向量[/bold]")
    rprint(f"文本：{args.text[:100]}...\n")
    
    result = create_embeddings(args.text, args.model)
    
    if "error" in result:
        rprint(f"[red]请求失败：{result['error']}[/red]")
        return
    
    data = result.get("data", [])
    if data:
        embedding = data[0].get("embedding", [])
        rprint(f"[green]✓ 生成成功[/green]")
        rprint(f"向量维度：{len(embedding)}")
        rprint(f"前 10 个值：{embedding[:10]}")
        
        # 保存到文件
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump({"embedding": embedding, "text": args.text}, f, ensure_ascii=False, indent=2)
            rprint(f"[green]已保存到：{args.output}[/green]")
    else:
        rprint(f"[yellow]无嵌入数据[/yellow]")


def cmd_test(args):
    """测试连接命令"""
    rprint(f"\n[bold]🔧 测试 Mify API 连接[/bold]\n")
    rprint(f"Base URL: {MIFY_BASE_URL}")
    rprint(f"API Key: {'已配置' if MIFY_API_KEY else '[red]未配置[/red]'}\n")
    
    # 测试模型列表
    rprint("[dim]测试获取模型列表...[/dim]")
    models = list_models()
    
    if "error" in models[0]:
        rprint(f"[red]✗ 连接失败：{models[0]['error']}[/red]")
        rprint(f"\n[dim]排查步骤：[/dim]")
        rprint(f"  1. 检查 MIFY_API_KEY 是否正确")
        rprint(f"  2. 检查 API URL 是否可访问")
        rprint(f"  3. 检查网络连接")
        rprint(f"  4. 确认 API 服务是否运行")
        return
    
    rprint(f"[green]✓ 连接成功！[/green]")
    rprint(f"可用模型数：{len(models)}")
    
    # 显示前 3 个模型
    if models:
        rprint(f"\n[bold]部分模型:[/bold]")
        for m in models[:3]:
            rprint(f"  • {m.get('id', 'unknown')}")


def main():
    parser = argparse.ArgumentParser(
        description="Mify LLM API 技能 - OpenAI 兼容的大语言模型接口"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # models 命令
    models_parser = subparsers.add_parser("models", help="列出可用模型")
    models_parser.set_defaults(func=cmd_models)
    
    # chat 命令
    chat_parser = subparsers.add_parser("chat", help="对话")
    chat_parser.add_argument("message", help="消息内容")
    chat_parser.add_argument("-m", "--model", help="模型名称")
    chat_parser.add_argument("--max-tokens", type=int, help="最大 token 数")
    chat_parser.add_argument("-t", "--temperature", type=float, help="温度参数")
    chat_parser.set_defaults(func=cmd_chat)
    
    # complete 命令
    complete_parser = subparsers.add_parser("complete", help="文本补全")
    complete_parser.add_argument("prompt", help="提示文本")
    complete_parser.add_argument("-m", "--model", help="模型名称")
    complete_parser.add_argument("--max-tokens", type=int, help="最大 token 数")
    complete_parser.add_argument("-t", "--temperature", type=float, help="温度参数")
    complete_parser.set_defaults(func=cmd_complete)
    
    # embed 命令
    embed_parser = subparsers.add_parser("embed", help="生成嵌入向量")
    embed_parser.add_argument("text", help="输入文本")
    embed_parser.add_argument("-m", "--model", help="模型名称")
    embed_parser.add_argument("-o", "--output", help="输出文件路径")
    embed_parser.set_defaults(func=cmd_embed)
    
    # test 命令
    test_parser = subparsers.add_parser("test", help="测试连接")
    test_parser.set_defaults(func=cmd_test)
    
    args = parser.parse_args()
    
    if not args.command:
        # 默认显示帮助
        parser.print_help()
        rprint(f"\n[dim]提示：使用 'test' 命令测试 API 连接[/dim]")
        return
    
    args.func(args)


if __name__ == "__main__":
    main()
