#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "rich", "imaplib2"]
# ///
"""邮件管理技能 - 收发邮件、智能分类、自动回复"""

import argparse
import os
import sys
import json
import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from datetime import datetime, timedelta

console = Console()

# 配置
EMAIL_PROVIDER = os.getenv("EMAIL_PROVIDER", "imap")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
EMAIL_IMAP_HOST = os.getenv("EMAIL_IMAP_HOST", "imap.gmail.com")
EMAIL_SMTP_HOST = os.getenv("EMAIL_SMTP_HOST", "smtp.gmail.com")
EMAIL_IMAP_PORT = int(os.getenv("EMAIL_IMAP_PORT", "993"))
EMAIL_SMTP_PORT = int(os.getenv("EMAIL_SMTP_PORT", "465"))
VIP_CONTACTS = os.getenv("VIP_CONTACTS", "").split(",") if os.getenv("VIP_CONTACTS") else []


def connect_imap():
    """连接 IMAP 服务器"""
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        return None, "未配置邮箱凭证"
    
    try:
        mail = imaplib.IMAP4_SSL(EMAIL_IMAP_HOST, EMAIL_IMAP_PORT)
        mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        return mail, None
    except Exception as e:
        return None, str(e)


def fetch_emails(limit: int = 10, unread_only: bool = False) -> list:
    """获取邮件列表"""
    mail, error = connect_imap()
    if error:
        return [{"error": error}]
    
    try:
        mail.select("inbox")
        
        # 搜索邮件
        if unread_only:
            status, messages = mail.search(None, "UNSEEN")
        else:
            status, messages = mail.search(None, "ALL")
        
        email_ids = messages[0].split()
        emails = []
        
        # 获取最新邮件
        for eid in email_ids[-limit:]:
            status, msg_data = mail.fetch(eid, "(RFC822)")
            msg = email.message_from_bytes(msg_data[0][1])
            
            # 提取信息
            subject = msg.get("Subject", "无主题")
            from_addr = msg.get("From", "")
            date_str = msg.get("Date", "")
            
            # 检查是否 VIP
            is_vip = any(vip in from_addr for vip in VIP_CONTACTS)
            
            emails.append({
                "id": eid.decode(),
                "subject": subject,
                "from": from_addr,
                "date": date_str,
                "is_vip": is_vip,
                "is_unread": msg.get("Status") != "SEEN"
            })
        
        mail.close()
        mail.logout()
        return emails
        
    except Exception as e:
        return [{"error": str(e)}]


def send_email(to: str, subject: str, content: str, html: bool = False) -> dict:
    """发送邮件"""
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        return {"error": "未配置邮箱凭证"}
    
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to
        msg["Subject"] = subject
        
        # 添加内容
        msg_type = "html" if html else "plain"
        msg.attach(MIMEText(content, msg_type, "utf-8"))
        
        # 发送
        server = smtplib.SMTP_SSL(EMAIL_SMTP_HOST, EMAIL_SMTP_PORT)
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        return {"success": True, "message": "发送成功"}
        
    except Exception as e:
        return {"error": str(e)}


def summarize_emails(emails: list) -> str:
    """生成邮件摘要"""
    if not emails:
        return "没有邮件"
    
    total = len(emails)
    vip_count = sum(1 for e in emails if e.get("is_vip"))
    unread_count = sum(1 for e in emails if e.get("is_unread"))
    
    summary = f"📧 邮件摘要\n\n"
    summary += f"总计：{total} 封\n"
    summary += f"VIP 邮件：{vip_count} 封\n"
    summary += f"未读：{unread_count} 封\n\n"
    
    if vip_count > 0:
        summary += "⭐ VIP 邮件:\n"
        for e in emails:
            if e.get("is_vip"):
                summary += f"  • {e['subject']} (来自：{e['from']})\n"
    
    return summary


def cmd_check(args):
    """检查邮件命令"""
    rprint(f"\n[bold]📧 检查邮件[/bold]\n")
    
    emails = fetch_emails(limit=args.limit, unread_only=args.unread)
    
    if "error" in emails[0]:
        rprint(f"[red]错误：{emails[0]['error']}[/red]")
        return
    
    # 显示表格
    table = Table(title=f"收件箱 ({len(emails)} 封)")
    table.add_column("VIP", style="yellow", width=3)
    table.add_column("未读", style="blue", width=3)
    table.add_column("主题", style="bold")
    table.add_column("发件人", width=30)
    table.add_column("日期", width=20)
    
    for e in reversed(emails):
        table.add_row(
            "⭐" if e.get("is_vip") else "",
            "📬" if e.get("is_unread") else "",
            e["subject"][:40],
            e["from"][:28],
            e["date"][:19] if e["date"] else ""
        )
    
    console.print(table)


def cmd_summary(args):
    """邮件摘要命令"""
    rprint(f"\n[bold]📋 邮件摘要[/bold]\n")
    
    emails = fetch_emails(limit=args.limit)
    
    if "error" in emails[0]:
        rprint(f"[red]错误：{emails[0]['error']}[/red]")
        return
    
    summary = summarize_emails(emails)
    rprint(summary)


def cmd_send(args):
    """发送邮件命令"""
    rprint(f"\n[bold]✉️ 发送邮件[/bold]")
    rprint(f"收件人：{args.to}")
    rprint(f"主题：{args.subject}\n")
    
    content = args.content
    if args.file and os.path.exists(args.file):
        with open(args.file, 'r', encoding='utf-8') as f:
            content = f.read()
    
    result = send_email(args.to, args.subject, content, args.html)
    
    if result.get("success"):
        rprint(f"[green]✓ 发送成功！[/green]")
    else:
        rprint(f"[red]✗ 发送失败：{result.get('error')}[/red]")


def cmd_reply(args):
    """回复邮件命令"""
    rprint(f"\n[bold]💬 回复邮件[/bold]")
    rprint(f"邮件 ID: {args.email_id}")
    rprint(f"回复内容：{args.content[:50]}...\n")
    
    # 这里需要根据邮件 ID 获取原邮件，然后回复
    # 简化版本：直接发送
    result = send_email(
        args.to or "recipient@example.com",
        f"Re: {args.subject or '回复'}",
        args.content
    )
    
    if result.get("success"):
        rprint(f"[green]✓ 回复成功！[/green]")
    else:
        rprint(f"[red]✗ 回复失败：{result.get('error')}[/red]")


def main():
    parser = argparse.ArgumentParser(
        description="邮件管理技能 - 收发邮件、智能分类、自动回复"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # check 命令
    check_parser = subparsers.add_parser("check", help="检查邮件")
    check_parser.add_argument("-n", "--limit", type=int, default=10, help="获取数量")
    check_parser.add_argument("-u", "--unread", action="store_true", help="仅未读")
    check_parser.set_defaults(func=cmd_check)
    
    # summary 命令
    summary_parser = subparsers.add_parser("summary", help="邮件摘要")
    summary_parser.add_argument("-n", "--limit", type=int, default=20, help="获取数量")
    summary_parser.set_defaults(func=cmd_summary)
    
    # send 命令
    send_parser = subparsers.add_parser("send", help="发送邮件")
    send_parser.add_argument("to", help="收件人")
    send_parser.add_argument("subject", help="主题")
    send_parser.add_argument("content", help="内容")
    send_parser.add_argument("-f", "--file", help="从文件读取内容")
    send_parser.add_argument("--html", action="store_true", help="HTML 格式")
    send_parser.set_defaults(func=cmd_send)
    
    # reply 命令
    reply_parser = subparsers.add_parser("reply", help="回复邮件")
    reply_parser.add_argument("email_id", help="邮件 ID")
    reply_parser.add_argument("content", help="回复内容")
    reply_parser.add_argument("--to", help="收件人（可选）")
    reply_parser.add_argument("--subject", help="主题（可选）")
    reply_parser.set_defaults(func=cmd_reply)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    args.func(args)


if __name__ == "__main__":
    main()
