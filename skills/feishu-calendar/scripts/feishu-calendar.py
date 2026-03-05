#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "rich"]
# ///
"""飞书日历技能 - 日程管理、会议创建、智能提醒"""

import argparse
import os
import sys
import json
import httpx
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from datetime import datetime, timedelta

console = Console()

# 配置
FEISHU_APP_ID = os.getenv("FEISHU_APP_ID", "")
FEISHU_APP_SECRET = os.getenv("FEISHU_APP_SECRET", "")
FEISHU_ACCESS_TOKEN = os.getenv("FEISHU_ACCESS_TOKEN", "")
FEISHU_CALENDAR_ID = os.getenv("FEISHU_CALENDAR_ID", "primary")
DEFAULT_REMINDER_MINUTES = int(os.getenv("DEFAULT_REMINDER_MINUTES", "15"))

# 飞书 API
FEISHU_BASE_URL = "https://open.feishu.cn/open-apis/calendar/v4"


def get_access_token() -> str:
    """获取飞书 access token"""
    if FEISHU_ACCESS_TOKEN:
        return FEISHU_ACCESS_TOKEN
    
    if not FEISHU_APP_ID or not FEISHU_APP_SECRET:
        return ""
    
    try:
        response = httpx.post(
            "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
            json={
                "app_id": FEISHU_APP_ID,
                "app_secret": FEISHU_APP_SECRET
            },
            timeout=30
        )
        data = response.json()
        if data.get("code") == 0:
            return data["tenant_access_token"]
        return ""
    except Exception:
        return ""


def get_calendar_events(start_time: str, end_time: str, limit: int = 20) -> list:
    """获取日历事件"""
    token = get_access_token()
    if not token:
        return [{"error": "未配置飞书凭证"}]
    
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        params = {
            "time_min": start_time,
            "time_max": end_time,
            "limit": limit
        }
        
        response = httpx.get(
            f"{FEISHU_BASE_URL}/calendars/{FEISHU_CALENDAR_ID}/events",
            headers=headers,
            params=params,
            timeout=30
        )
        
        data = response.json()
        if data.get("code") == 0:
            return data.get("data", {}).get("items", [])
        return [{"error": data.get("msg", "未知错误")}]
        
    except Exception as e:
        return [{"error": str(e)}]


def create_event(title: str, start_time: str, end_time: str, attendees: list = None) -> dict:
    """创建日历事件"""
    token = get_access_token()
    if not token:
        return {"error": "未配置飞书凭证"}
    
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "summary": title,
            "start_time": {
                "timestamp": start_time,
                "is_all_day": False
            },
            "end_time": {
                "timestamp": end_time,
                "is_all_day": False
            },
            "reminders": {
                "use_default": False,
                "overrides": [
                    {
                        "method": "notification",
                        "minutes": DEFAULT_REMINDER_MINUTES
                    }
                ]
            }
        }
        
        if attendees:
            payload["attendees"] = [{"user_id": uid} for uid in attendees]
        
        response = httpx.post(
            f"{FEISHU_BASE_URL}/calendars/{FEISHU_CALENDAR_ID}/events",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        data = response.json()
        if data.get("code") == 0:
            return data.get("data", {})
        return {"error": data.get("msg", "创建失败")}
        
    except Exception as e:
        return {"error": str(e)}


def parse_time(time_str: str) -> str:
    """解析时间字符串为时间戳"""
    # 支持多种格式
    formats = [
        "%Y-%m-%d %H:%M",
        "%Y/%m/%d %H:%M",
        "%m-%d %H:%M",
        "%H:%M"
    ]
    
    now = datetime.now()
    
    for fmt in formats:
        try:
            dt = datetime.strptime(time_str, fmt)
            # 如果没有年份，使用当前年份
            if dt.year == 1900:
                dt = dt.replace(year=now.year, month=now.month, day=now.day)
            return str(int(dt.timestamp()))
        except ValueError:
            continue
    
    # 默认返回当前时间 +1 小时
    return str(int((now + timedelta(hours=1)).timestamp()))


def cmd_today(args):
    """查看今日日程"""
    rprint(f"\n[bold]📅 今日日程[/bold]\n")
    
    now = datetime.now()
    start = now.replace(hour=0, minute=0, second=0)
    end = now.replace(hour=23, minute=59, second=59)
    
    events = get_calendar_events(
        str(int(start.timestamp())),
        str(int(end.timestamp())),
        limit=args.limit
    )
    
    if "error" in events[0]:
        rprint(f"[red]错误：{events[0]['error']}[/red]")
        return
    
    if not events:
        rprint("[green]✓ 今日没有日程安排[/green]")
        return
    
    table = Table(title=f"{now.strftime('%Y-%m-%d')} ({len(events)} 个日程)")
    table.add_column("时间", width=15)
    table.add_column("主题", style="bold")
    table.add_column("地点", width=20)
    table.add_column("参会人", width=20)
    
    for event in events:
        start_time = event.get("start_time", {})
        ts = start_time.get("timestamp", 0)
        time_str = datetime.fromtimestamp(int(ts)).strftime("%H:%M") if ts else ""
        
        table.add_row(
            time_str,
            event.get("summary", "无主题")[:30],
            event.get("location", "")[:18],
            str(len(event.get("attendees", [])))
        )
    
    console.print(table)


def cmd_week(args):
    """查看本周日程"""
    rprint(f"\n[bold]📅 本周日程[/bold]\n")
    
    now = datetime.now()
    start = now - timedelta(days=now.weekday())
    start = start.replace(hour=0, minute=0, second=0)
    end = start + timedelta(days=7)
    
    events = get_calendar_events(
        str(int(start.timestamp())),
        str(int(end.timestamp())),
        limit=50
    )
    
    if "error" in events[0]:
        rprint(f"[red]错误：{events[0]['error']}[/red]")
        return
    
    if not events:
        rprint("[green]✓ 本周没有日程安排[/green]")
        return
    
    # 按日期分组
    by_date = {}
    for event in events:
        start_time = event.get("start_time", {})
        ts = start_time.get("timestamp", 0)
        if ts:
            date_str = datetime.fromtimestamp(int(ts)).strftime("%m-%d %a")
            if date_str not in by_date:
                by_date[date_str] = []
            by_date[date_str].append(event)
    
    for date_str in sorted(by_date.keys()):
        rprint(f"\n[bold cyan]{date_str}[/bold cyan] ({len(by_date[date_str])} 个)")
        for event in by_date[date_str]:
            ts = event.get("start_time", {}).get("timestamp", 0)
            time_str = datetime.fromtimestamp(int(ts)).strftime("%H:%M") if ts else ""
            rprint(f"  {time_str} {event.get('summary', '无主题')}")


def cmd_create(args):
    """创建日程命令"""
    rprint(f"\n[bold]➕ 创建日程[/bold]")
    rprint(f"主题：{args.title}")
    rprint(f"开始：{args.start_time}")
    rprint(f"结束：{args.end_time}\n")
    
    start_ts = parse_time(args.start_time)
    end_ts = parse_time(args.end_time) if args.end_time else str(int(start_ts) + 3600)
    
    attendees = args.attendees.split(",") if args.attendees else None
    
    result = create_event(args.title, start_ts, end_ts, attendees)
    
    if "error" not in result:
        rprint(f"[green]✓ 日程创建成功！[/green]")
        if "event_id" in result:
            rprint(f"事件 ID: {result['event_id']}")
    else:
        rprint(f"[red]✗ 创建失败：{result['error']}[/red]")


def cmd_find(args):
    """搜索日程命令"""
    rprint(f"\n[bold]🔍 搜索日程：{args.keyword}[/bold]\n")
    
    # 获取未来 30 天的日程
    now = datetime.now()
    end = now + timedelta(days=30)
    
    events = get_calendar_events(
        str(int(now.timestamp())),
        str(int(end.timestamp())),
        limit=100
    )
    
    if "error" in events[0]:
        rprint(f"[red]错误：{events[0]['error']}[/red]")
        return
    
    # 过滤匹配的事件
    matched = [
        e for e in events
        if args.keyword.lower() in e.get("summary", "").lower()
    ]
    
    if not matched:
        rprint("[yellow]未找到匹配的日程[/yellow]")
        return
    
    table = Table(title=f"匹配结果 ({len(matched)} 个)")
    table.add_column("日期", width=12)
    table.add_column("时间", width=8)
    table.add_column("主题", style="bold")
    
    for event in matched:
        start_time = event.get("start_time", {})
        ts = start_time.get("timestamp", 0)
        if ts:
            dt = datetime.fromtimestamp(int(ts))
            table.add_row(
                dt.strftime("%Y-%m-%d"),
                dt.strftime("%H:%M"),
                event.get("summary", "无主题")
            )
    
    console.print(table)


def main():
    parser = argparse.ArgumentParser(
        description="飞书日历技能 - 日程管理、会议创建、智能提醒"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # today 命令
    today_parser = subparsers.add_parser("today", help="查看今日日程")
    today_parser.add_argument("-n", "--limit", type=int, default=20, help="获取数量")
    today_parser.set_defaults(func=cmd_today)
    
    # week 命令
    week_parser = subparsers.add_parser("week", help="查看本周日程")
    week_parser.set_defaults(func=cmd_week)
    
    # create 命令
    create_parser = subparsers.add_parser("create", help="创建日程")
    create_parser.add_argument("title", help="日程主题")
    create_parser.add_argument("start_time", help="开始时间 (YYYY-MM-DD HH:MM)")
    create_parser.add_argument("-e", "--end-time", help="结束时间")
    create_parser.add_argument("-a", "--attendees", help="参会人 ID 列表（逗号分隔）")
    create_parser.set_defaults(func=cmd_create)
    
    # find 命令
    find_parser = subparsers.add_parser("find", help="搜索日程")
    find_parser.add_argument("keyword", help="搜索关键词")
    find_parser.set_defaults(func=cmd_find)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    args.func(args)


if __name__ == "__main__":
    main()
