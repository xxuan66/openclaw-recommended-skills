#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "rich"]
# ///
"""AI 文本人性化技能 - 去除 AI 痕迹，风格变换"""

import argparse
import os
import sys
import json
import httpx
from rich.console import Console
from rich import print as rprint

console = Console()

# 配置
HUMANIZER_MODEL = os.getenv("HUMANIZER_MODEL", "qwen-max")
HUMANIZER_STYLE = os.getenv("HUMANIZER_STYLE", "casual")
HUMANIZER_STRENGTH = int(os.getenv("HUMANIZER_STRENGTH", "5"))

# 风格定义
STYLES = {
    "casual": "自然对话风格，像朋友聊天一样轻松",
    "professional": "商务专业风格，正式但不生硬",
    "creative": "富有创意的表达，生动有趣",
    "academic": "学术论文风格，严谨规范",
    "humorous": "轻松幽默风格，带点俏皮",
    "concise": "简洁明了风格，直击要点"
}


def humanize_text(text: str, style: str = "casual", strength: int = 5) -> str:
    """人性化改写文本"""
    # 风格提示词
    style_prompts = {
        "casual": "请用自然、口语化的方式改写，像朋友聊天一样，避免过于正式的表达。",
        "professional": "请用专业但自然的商务风格改写，保持专业性但避免 AI 腔调。",
        "creative": "请用富有创意和想象力的方式改写，让文字更生动有趣。",
        "academic": "请用严谨的学术风格改写，保持专业术语但更自然流畅。",
        "humorous": "请用轻松幽默的方式改写，适当加入俏皮的表达。",
        "concise": "请用简洁明了的方式改写，去除冗余，直击要点。"
    }
    
    # 模拟人性化改写（实际应调用 AI 模型）
    # 这里做一些简单的文本优化
    modified = text
    
    # 替换常见的 AI 表达
    ai_phrases = {
        "首先，": "咱们先",
        "其次，": "然后，",
        "最后，": "最后说说",
        "总之，": "总的来说",
        "值得注意的是，": "有个事儿挺重要，",
        "综上所述，": "这么一看，",
        "可以帮助您": "能帮你",
        "我们建议": "我觉得可以",
        "需要注意的是": "得注意",
        "总而言之": "一句话"
    }
    
    for ai_phrase, human_phrase in ai_phrases.items():
        modified = modified.replace(ai_phrase, human_phrase)
    
    # 根据强度调整改写程度
    if strength >= 7:
        # 高强度：更多口语化
        modified = modified.replace("的", "哒")
        modified = modified.replace("吗？", "不？")
    
    return modified


def detect_ai_score(text: str) -> dict:
    """检测 AI 痕迹分数（简化版）"""
    # 检测常见 AI 特征
    ai_indicators = [
        "首先", "其次", "最后", "总之", "综上所述",
        "值得注意的是", "需要强调的是", "总而言之",
        "希望本文能够", "本文旨在", "笔者"
    ]
    
    score = 0
    found = []
    
    for indicator in ai_indicators:
        if indicator in text:
            score += 10
            found.append(indicator)
    
    # 句子长度分析
    sentences = text.split('。')
    avg_length = sum(len(s) for s in sentences) / max(len(sentences), 1)
    if avg_length > 50:
        score += 20
        found.append("句子过长")
    
    return {
        "ai_score": min(score, 100),
        "indicators": found,
        "avg_sentence_length": round(avg_length, 1),
        "recommendation": "建议改写" if score > 30 else "较为自然"
    }


def cmd_humanize(args):
    """人性化改写命令"""
    # 读取文本
    if os.path.exists(args.text):
        with open(args.text, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        text = args.text
    
    style = args.style or HUMANIZER_STYLE
    strength = args.strength or HUMANIZER_STRENGTH
    
    rprint(f"\n[bold]🧑 文本人性化[/bold]")
    rprint(f"风格：{style} ({STYLES.get(style, '自定义')})")
    rprint(f"强度：{strength}/10\n")
    
    # 检测原始 AI 分数
    original_score = detect_ai_score(text)
    rprint(f"[dim]原始 AI 分数：{original_score['ai_score']} - {original_score['recommendation']}[/dim]\n")
    
    # 人性化改写
    result = humanize_text(text, style, strength)
    
    rprint(f"[bold green]改写后：[/bold green]\n")
    rprint(result)
    
    # 检测改写后 AI 分数
    new_score = detect_ai_score(result)
    rprint(f"\n[dim]改写后 AI 分数：{new_score['ai_score']}[/dim]")
    
    # 保存结果
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(result)
        rprint(f"\n[green]结果已保存到：{args.output}[/green]")


def cmd_check(args):
    """检测 AI 痕迹命令"""
    # 读取文本
    if os.path.exists(args.text):
        with open(args.text, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        text = args.text
    
    rprint(f"\n[bold]🔍 AI 痕迹检测[/bold]\n")
    
    result = detect_ai_score(text)
    
    # 显示结果
    score = result['ai_score']
    
    if score >= 70:
        color = "red"
        verdict = "⚠️  AI 痕迹明显"
    elif score >= 40:
        color = "yellow"
        verdict = "⚡ 有一定 AI 特征"
    else:
        color = "green"
        verdict = "✅ 较为自然"
    
    rprint(f"[{color}]{verdict}[/]")
    rprint(f"AI 分数：{score}/100")
    rprint(f"\n检测到的特征：")
    
    for indicator in result['indicators']:
        rprint(f"  • {indicator}")
    
    rprint(f"\n平均句长：{result['avg_sentence_length']} 字")
    rprint(f"建议：{result['recommendation']}")


def cmd_style(args):
    """风格变换命令"""
    # 读取文本
    if os.path.exists(args.text):
        with open(args.text, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        text = args.text
    
    style = args.style
    
    if style not in STYLES:
        rprint(f"[red]未知风格：{style}[/red]")
        rprint(f"可用风格：{', '.join(STYLES.keys())}")
        return
    
    rprint(f"\n[bold]🎨 风格变换：{style}[/bold]")
    rprint(f"说明：{STYLES[style]}\n")
    
    result = humanize_text(text, style, 5)
    rprint(result)


def main():
    parser = argparse.ArgumentParser(
        description="AI 文本人性化技能 - 去除 AI 痕迹，风格变换"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # humanize 命令
    humanize_parser = subparsers.add_parser("humanize", help="人性化改写")
    humanize_parser.add_argument("text", help="要改写的文本或文件路径")
    humanize_parser.add_argument("-s", "--style", help=f"风格：{', '.join(STYLES.keys())}")
    humanize_parser.add_argument("-t", "--strength", type=int, help="改写强度 1-10")
    humanize_parser.add_argument("-o", "--output", help="输出文件路径")
    humanize_parser.set_defaults(func=cmd_humanize)
    
    # check 命令
    check_parser = subparsers.add_parser("check", help="检测 AI 痕迹")
    check_parser.add_argument("text", help="要检测的文本或文件路径")
    check_parser.set_defaults(func=cmd_check)
    
    # style 命令
    style_parser = subparsers.add_parser("style", help="风格变换")
    style_parser.add_argument("text", help="要变换的文本或文件路径")
    style_parser.add_argument("style", help=f"目标风格：{', '.join(STYLES.keys())}")
    style_parser.set_defaults(func=cmd_style)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    args.func(args)


if __name__ == "__main__":
    main()
