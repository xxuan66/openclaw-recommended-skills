#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "rich", "pillow"]
# ///
"""AI 图片生成技能 - 文生图、图生图、风格迁移"""

import argparse
import os
import sys
import json
import httpx
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from datetime import datetime
import base64

console = Console()

# 配置
IMAGE_GEN_PROVIDER = os.getenv("IMAGE_GEN_PROVIDER", "dashscope")
IMAGE_GEN_API_KEY = os.getenv("IMAGE_GEN_API_KEY", "")
IMAGE_GEN_MODEL = os.getenv("IMAGE_GEN_MODEL", "wanx2.1")
IMAGE_GEN_SIZE = os.getenv("IMAGE_GEN_SIZE", "1024x1024")
OUTPUT_DIR = os.getenv("IMAGE_OUTPUT_DIR", "./output")

# 通义万相 API
DASHSCOPE_IMAGE_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"


def generate_image_dashscope(prompt: str, size: str = "1024x1024") -> dict:
    """使用通义万相生成图片"""
    if not IMAGE_GEN_API_KEY:
        return {"error": "请配置 IMAGE_GEN_API_KEY"}
    
    try:
        headers = {
            "Authorization": f"Bearer {IMAGE_GEN_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": IMAGE_GEN_MODEL,
            "input": {
                "prompt": prompt
            },
            "parameters": {
                "size": size,
                "n": 1
            }
        }
        
        response = httpx.post(
            DASHSCOPE_IMAGE_URL,
            headers=headers,
            json=payload,
            timeout=120
        )
        
        return response.json()
    except Exception as e:
        return {"error": str(e)}


def generate_image_mock(prompt: str, size: str = "1024x1024") -> dict:
    """模拟图片生成（用于测试）"""
    return {
        "status": "success",
        "prompt": prompt,
        "size": size,
        "model": IMAGE_GEN_MODEL,
        "output": {
            "url": f"https://example.com/generated/{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
            "task_id": f"task_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        }
    }


def image_to_base64(image_path: str) -> str:
    """将图片转换为 base64"""
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')


def cmd_generate(args):
    """文生图命令"""
    rprint(f"\n[bold]🎨 生成图片[/bold]")
    rprint(f"提示词：{args.prompt}")
    rprint(f"模型：{IMAGE_GEN_MODEL}")
    rprint(f"尺寸：{IMAGE_GEN_SIZE}\n")
    
    # 选择生成方式
    if IMAGE_GEN_API_KEY:
        result = generate_image_dashscope(args.prompt, IMAGE_GEN_SIZE)
    else:
        rprint("[yellow]未配置 API 密钥，使用模拟模式[/yellow]\n")
        result = generate_image_mock(args.prompt, IMAGE_GEN_SIZE)
    
    if "error" in result:
        rprint(f"[red]✗ 生成失败：{result['error']}[/red]")
        return
    
    if "output" in result:
        rprint(f"[green]✓ 生成成功！[/green]")
        if "url" in result["output"]:
            rprint(f"图片 URL: {result['output']['url']}")
        
        # 保存结果
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        result_file = os.path.join(OUTPUT_DIR, f"result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        rprint(f"结果已保存：{result_file}")
    else:
        rprint(f"[yellow]生成中，任务 ID: {result.get('task_id', 'N/A')}[/yellow]")


def cmd_edit(args):
    """图生图/编辑命令"""
    if not os.path.exists(args.image):
        rprint(f"[red]图片不存在：{args.image}[/red]")
        return
    
    rprint(f"\n[bold]✏️ 编辑图片[/bold]")
    rprint(f"原图：{args.image}")
    rprint(f"提示词：{args.prompt}\n")
    
    # 读取图片
    image_base64 = image_to_base64(args.image)
    
    # 这里可以调用图生图 API
    rprint("[yellow]图生图功能需要配置具体 API[/yellow]")
    rprint("当前仅支持文生图模式")


def cmd_style(args):
    """风格迁移命令"""
    if not os.path.exists(args.image):
        rprint(f"[red]图片不存在：{args.image}[/red]")
        return
    
    rprint(f"\n[bold]🎭 风格迁移[/bold]")
    rprint(f"原图：{args.image}")
    rprint(f"目标风格：{args.style}\n")
    
    rprint("[yellow]风格迁移功能需要配置具体 API[/yellow]")


def cmd_upscale(args):
    """高清放大命令"""
    if not os.path.exists(args.image):
        rprint(f"[red]图片不存在：{args.image}[/red]")
        return
    
    rprint(f"\n[bold]🔍 高清放大[/bold]")
    rprint(f"原图：{args.image}\n")
    
    rprint("[yellow]高清放大功能需要配置具体 API[/yellow]")


def main():
    parser = argparse.ArgumentParser(
        description="AI 图片生成技能 - 文生图、图生图、风格迁移"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # generate 命令
    gen_parser = subparsers.add_parser("gen", help="文生图")
    gen_parser.add_argument("prompt", help="图片描述提示词")
    gen_parser.add_argument("-s", "--size", default=IMAGE_GEN_SIZE, help="图片尺寸")
    gen_parser.set_defaults(func=cmd_generate)
    
    # edit 命令
    edit_parser = subparsers.add_parser("edit", help="图生图/编辑")
    edit_parser.add_argument("image", help="输入图片路径")
    edit_parser.add_argument("prompt", help="编辑提示词")
    edit_parser.set_defaults(func=cmd_edit)
    
    # style 命令
    style_parser = subparsers.add_parser("style", help="风格迁移")
    style_parser.add_argument("image", help="输入图片路径")
    style_parser.add_argument("style", help="目标风格")
    style_parser.set_defaults(func=cmd_style)
    
    # upscale 命令
    upscale_parser = subparsers.add_parser("upscale", help="高清放大")
    upscale_parser.add_argument("image", help="输入图片路径")
    upscale_parser.set_defaults(func=cmd_upscale)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    args.func(args)


if __name__ == "__main__":
    main()
