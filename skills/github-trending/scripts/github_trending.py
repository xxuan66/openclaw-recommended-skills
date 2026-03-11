#!/usr/bin/env python3
"""
GitHub Trending 爬虫 - 获取 GitHub 热门项目信息

用法:
    python github_trending.py [--period daily|weekly|monthly] [--limit N] [--language LANG] [--json] [--output FILE]

示例:
    python github_trending.py                     # 今日热门
    python github_trending.py -p weekly           # 本周热门
    python github_trending.py -L Python -l 5      # Python 项目 Top5
    python github_trending.py --json > data.json  # JSON 输出
"""

import argparse
import json
import re
import sys
from datetime import datetime
from typing import List, Dict, Optional, Any

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("❌ 缺少依赖：pip install requests beautifulsoup4")
    print("   或：apt install python3-requests python3-bs4")
    sys.exit(1)


# GitHub Trending URL
TRENDING_URL = "https://github.com/trending"

# 时间范围映射
PERIOD_MAP = {
    "daily": "今日",
    "weekly": "本周",
    "monthly": "本月"
}

# 排名 Emoji
RANK_EMOJI = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]


def fetch_trending(period: str = "daily") -> str:
    """获取 GitHub Trending 页面 HTML"""
    url = f"{TRENDING_URL}?since={period}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"❌ 网络错误：{e}", file=sys.stderr)
        sys.exit(1)


def parse_trending(html: str, limit: int = 10, language: Optional[str] = None) -> List[Dict[str, Any]]:
    """解析 HTML 提取项目信息"""
    soup = BeautifulSoup(html, 'html.parser')
    projects = []
    
    # 查找所有项目块（GitHub 使用 article 标签）
    articles = soup.find_all('article', class_='Box-row')
    
    for i, article in enumerate(articles[:limit]):
        try:
            # 项目名称和链接
            title_tag = article.find('h2', class_='h3').find('a')
            if not title_tag:
                continue
            
            name = title_tag['href'].lstrip('/')
            url = f"https://github.com{name}"
            
            # 项目简介
            desc_tag = article.find('p', class_='col-9')
            description = ''
            if desc_tag:
                description = desc_tag.get_text(strip=True)
                # 清理多余空格
                description = ' '.join(description.split())
                if description and len(description) > 100:
                    description = description[:100] + '...'
            
            # 编程语言
            lang_tag = article.find('span', itemprop='programmingLanguage')
            language_name = lang_tag.get_text(strip=True) if lang_tag else 'Unknown'
            
            # 过滤语言
            if language and language_name.lower() != language.lower():
                continue
            
            # Stars 统计
            stars_tags = article.find_all('a', href=re.compile(r'/stargazers'))
            
            stars_today = '0'
            stars_total = '0'
            
            if len(stars_tags) >= 1:
                # 总 Stars
                total_text = stars_tags[0].get_text(strip=True)
                stars_total = total_text.replace(',', '').replace(' ', '')
            
            # 今日 Stars 在单独的 span 中
            today_tag = article.find('span', class_='d-inline-block')
            if today_tag:
                today_text = today_tag.get_text(strip=True)
                # 提取数字
                match = re.search(r'([\d,.]+[kKmM]?)', today_text)
                if match:
                    stars_today = match.group(1)
            
            # 构建项目信息
            project = {
                'rank': len(projects) + 1,
                'name': name,
                'url': url,
                'language': language_name,
                'stars_today': stars_today,
                'stars_total': stars_total,
                'description': description,
            }
            
            projects.append(project)
            
        except Exception as e:
            if args.debug:
                print(f"⚠️ 解析项目失败：{e}", file=sys.stderr)
            continue
    
    return projects


def format_emoji(rank: int) -> str:
    """获取排名 Emoji"""
    if rank <= len(RANK_EMOJI):
        return RANK_EMOJI[rank - 1]
    return f"{rank}."


def output_text(projects: List[Dict[str, Any]], period: str) -> str:
    """生成文本格式输出"""
    lines = []
    lines.append(f"🔥 GitHub Trending - {PERIOD_MAP.get(period, '热门')} 🔥")
    lines.append("━" * 50)
    lines.append("")
    
    for project in projects:
        emoji = format_emoji(project['rank'])
        lines.append(f"{emoji} {project['rank']}. {project['name']}")
        
        if project['description']:
            lines.append(f"   📝 {project['description']}")
        
        lines.append(f"   💻 {project['language']} | ⭐ +{project['stars_today']} today | 📊 {project['stars_total']} total")
        lines.append(f"   🔗 {project['url']}")
        lines.append("")
    
    lines.append(f"📅 更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return '\n'.join(lines)


def output_markdown(projects: List[Dict[str, Any]], period: str) -> str:
    """生成 Markdown 格式输出"""
    lines = []
    lines.append(f"# 🔥 GitHub Trending - {PERIOD_MAP.get(period, '热门')}")
    lines.append("")
    lines.append(f"**更新时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append("| 排名 | 项目 | 语言 | 今日 Stars | 总 Stars |")
    lines.append("|------|------|------|------------|----------|")
    
    for project in projects:
        emoji = format_emoji(project['rank'])
        name_link = f"[{project['name']}]({project['url']})"
        lines.append(f"| {emoji} | {name_link} | {project['language']} | +{project['stars_today']} | {project['stars_total']} |")
    
    lines.append("")
    lines.append("## 项目详情")
    lines.append("")
    
    for project in projects:
        emoji = format_emoji(project['rank'])
        lines.append(f"### {emoji} {project['name']}")
        lines.append("")
        if project['description']:
            lines.append(f"> {project['description']}")
            lines.append("")
        lines.append(f"- 💻 语言：{project['language']}")
        lines.append(f"- ⭐ 今日：+{project['stars_today']}")
        lines.append(f"- 📊 总计：{project['stars_total']}")
        lines.append(f"- 🔗 [查看项目]({project['url']})")
        lines.append("")
    
    return '\n'.join(lines)


def output_json(projects: List[Dict[str, Any]], period: str) -> str:
    """生成 JSON 格式输出"""
    data = {
        'period': period,
        'period_name': PERIOD_MAP.get(period, '热门'),
        'fetched_at': datetime.now().isoformat(),
        'count': len(projects),
        'projects': projects
    }
    return json.dumps(data, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description='GitHub Trending 热门项目获取工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python github_trending.py                     # 今日热门
  python github_trending.py -p weekly           # 本周热门
  python github_trending.py -L Python -l 5      # Python 项目 Top5
  python github_trending.py --json > data.json  # JSON 输出
        '''
    )
    
    parser.add_argument(
        '-p', '--period',
        choices=['daily', 'weekly', 'monthly'],
        default='daily',
        help='时间范围 (default: daily)'
    )
    
    parser.add_argument(
        '-l', '--limit',
        type=int,
        default=10,
        help='获取数量 (default: 10)'
    )
    
    parser.add_argument(
        '-L', '--language',
        help='编程语言过滤 (e.g., Python, JavaScript)'
    )
    
    parser.add_argument(
        '-f', '--format',
        choices=['text', 'markdown', 'json'],
        default='text',
        help='输出格式 (default: text)'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='输出文件路径 (default: 终端输出)'
    )
    
    parser.add_argument(
        '-d', '--debug',
        action='store_true',
        help='调试模式'
    )
    
    global args
    args = parser.parse_args()
    
    # 获取数据
    if args.debug:
        print(f"🌐 获取 {PERIOD_MAP.get(args.period, '热门')} Trending...", file=sys.stderr)
    
    html = fetch_trending(args.period)
    
    # 解析数据
    if args.debug:
        print(f"🔍 解析 HTML...", file=sys.stderr)
    
    projects = parse_trending(html, args.limit, args.language)
    
    if not projects:
        print("❌ 未找到任何项目", file=sys.stderr)
        sys.exit(2)
    
    # 格式化输出
    if args.format == 'json':
        output = output_json(projects, args.period)
    elif args.format == 'markdown':
        output = output_markdown(projects, args.period)
    else:
        output = output_text(projects, args.period)
    
    # 输出
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"✅ 已保存到：{args.output}")
    else:
        print(output)


if __name__ == '__main__':
    main()
