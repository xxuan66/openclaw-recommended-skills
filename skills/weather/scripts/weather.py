#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "rich"]
# ///
"""天气查询技能 - wttr.in + Open-Meteo 双源，无需 API 密钥"""

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
WEATHER_PROVIDER = os.getenv("WEATHER_PROVIDER", "wttr")
WEATHER_UNITS = os.getenv("WEATHER_UNITS", "metric")
WEATHER_LANG = os.getenv("WEATHER_LANG", "zh")
DEFAULT_CITY = os.getenv("DEFAULT_CITY", "Beijing")

# API 端点
WTTR_URL = "https://wttr.in/{city}?format=j1&lang={lang}"
OPENMETEO_URL = "https://api.open-meteo.com/v1/forecast"


def get_weather_wttr(city: str) -> dict:
    """从 wttr.in 获取天气"""
    try:
        url = WTTR_URL.format(city=city, lang=WEATHER_LANG)
        response = httpx.get(url, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        current = data.get("current_condition", [{}])[0]
        forecast = data.get("weather", [])
        
        return {
            "source": "wttr.in",
            "city": city,
            "current": {
                "temp": current.get("temp_C", current.get("temp_F")),
                "feels_like": current.get("FeelsLikeC", current.get("FeelsLikeF")),
                "condition": current.get("weatherDesc", [{}])[0].get("value", ""),
                "humidity": current.get("humidity", ""),
                "wind": current.get("windspeedKmph", current.get("windspeedMiles", "")),
                "direction": current.get("winddir16Point", "")
            },
            "forecast": forecast[:7]
        }
    except Exception as e:
        return {"error": str(e)}


def get_weather_openmeteo(city: str) -> dict:
    """从 Open-Meteo 获取天气（需要经纬度）"""
    # 简单城市坐标映射
    city_coords = {
        "beijing": (39.9, 116.4),
        "shanghai": (31.2, 121.5),
        "guangzhou": (23.1, 113.3),
        "shenzhen": (22.5, 114.1),
        "chengdu": (30.6, 104.1),
        "hangzhou": (30.2, 120.2),
        "new york": (40.7, -74.0),
        "london": (51.5, -0.1),
        "tokyo": (35.7, 139.7)
    }
    
    coords = city_coords.get(city.lower(), (39.9, 116.4))  # 默认北京
    
    try:
        params = {
            "latitude": coords[0],
            "longitude": coords[1],
            "current_weather": True,
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_mean,weathercode",
            "timezone": "auto"
        }
        
        response = httpx.get(OPENMETEO_URL, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        current = data.get("current_weather", {})
        daily = data.get("daily", {})
        
        return {
            "source": "Open-Meteo",
            "city": city,
            "current": {
                "temp": current.get("temperature"),
                "condition": get_weather_condition(current.get("weathercode", 0)),
                "wind": current.get("windspeed"),
                "direction": current.get("winddirection", "")
            },
            "forecast": []
        }
    except Exception as e:
        return {"error": str(e)}


def get_weather_condition(code: int) -> str:
    """将天气代码转换为文字"""
    conditions = {
        0: "晴朗",
        1: "主要晴朗",
        2: "多云",
        3: "阴天",
        45: "雾",
        48: "雾凇",
        51: "毛毛雨",
        53: "毛毛雨",
        55: "毛毛雨",
        61: "小雨",
        63: "中雨",
        65: "大雨",
        71: "小雪",
        73: "中雪",
        75: "大雪",
        95: "雷雨",
        96: "雷阵雨",
        99: "强雷暴"
    }
    return conditions.get(code, "未知")


def cmd_weather(args):
    """查询天气命令"""
    city = args.city or DEFAULT_CITY
    
    rprint(f"\n[bold]🌤️ 天气查询[/bold]")
    rprint(f"城市：{city}")
    rprint(f"数据源：{WEATHER_PROVIDER}\n")
    
    # 获取天气
    if WEATHER_PROVIDER == "open-meteo":
        data = get_weather_openmeteo(city)
    else:
        data = get_weather_wttr(city)
    
    if "error" in data:
        rprint(f"[red]获取失败：{data['error']}[/red]")
        return
    
    current = data.get("current", {})
    
    # 显示当前天气
    rprint(f"[bold cyan]{data.get('city', city)} - 当前天气[/bold cyan]")
    rprint(f"  温度：{current.get('temp', 'N/A')}°C")
    rprint(f"  体感：{current.get('feels_like', 'N/A')}°C")
    rprint(f"  状况：{current.get('condition', 'N/A')}")
    rprint(f"  湿度：{current.get('humidity', 'N/A')}%")
    rprint(f"  风速：{current.get('wind', 'N/A')} km/h {current.get('direction', '')}")
    
    # 显示预报
    forecast = data.get("forecast", [])
    if forecast:
        rprint(f"\n[bold cyan]未来 7 天预报[/bold cyan]")
        
        table = Table(show_lines=False)
        table.add_column("日期", width=10)
        table.add_column("天气", width=15)
        table.add_column("最高", justify="right")
        table.add_column("最低", justify="right")
        table.add_column("降水概率", justify="right")
        
        for day in forecast[:7]:
            date = day.get("date", "")[:10]
            avg_temp = day.get("avgtempC", day.get("maxtempC", ""))
            max_temp = day.get("maxtempC", day.get("maxtempF", ""))
            min_temp = day.get("mintempC", day.get("mintempF", ""))
            condition = day.get("weatherDesc", [{}])[0].get("value", "")
            precip = day.get("chanceofrain", day.get("chanceofsnow", ""))
            
            table.add_row(
                date,
                condition[:13],
                f"{max_temp}°",
                f"{min_temp}°",
                f"{precip}%" if precip else "N/A"
            )
        
        console.print(table)


def cmd_forecast(args):
    """天气预报命令"""
    city = args.city or DEFAULT_CITY
    rprint(f"\n[bold]📅 天气预报：{city}[/bold]\n")
    
    # 调用 weather 命令的逻辑
    args.city = city
    cmd_weather(args)


def cmd_aqi(args):
    """查询空气质量命令"""
    city = args.city or DEFAULT_CITY
    rprint(f"\n[bold]🍃 空气质量：{city}[/bold]\n")
    
    rprint("[yellow]AQI 功能需要配置额外 API[/yellow]")
    rprint("建议使用：https://aqicn.org/ API")


def cmd_alert(args):
    """查询天气预警命令"""
    city = args.city or DEFAULT_CITY
    rprint(f"\n[bold]⚠️ 天气预警：{city}[/bold]\n")
    
    rprint("[yellow]天气预警功能需要配置额外 API[/yellow]")


def main():
    parser = argparse.ArgumentParser(
        description="天气查询技能 - wttr.in + Open-Meteo 双源，无需 API 密钥"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # weather 命令
    weather_parser = subparsers.add_parser("weather", help="查询天气")
    weather_parser.add_argument("city", nargs="?", help="城市名称")
    weather_parser.set_defaults(func=cmd_weather)
    
    # forecast 命令
    forecast_parser = subparsers.add_parser("forecast", help="天气预报")
    forecast_parser.add_argument("city", nargs="?", help="城市名称")
    forecast_parser.set_defaults(func=cmd_forecast)
    
    # aqi 命令
    aqi_parser = subparsers.add_parser("aqi", help="空气质量")
    aqi_parser.add_argument("city", nargs="?", help="城市名称")
    aqi_parser.set_defaults(func=cmd_aqi)
    
    # alert 命令
    alert_parser = subparsers.add_parser("alert", help="天气预警")
    alert_parser.add_argument("city", nargs="?", help="城市名称")
    alert_parser.set_defaults(func=cmd_alert)
    
    args = parser.parse_args()
    
    if not args.command:
        # 默认查询天气
        cmd_weather(args)
        return
    
    args.func(args)


if __name__ == "__main__":
    main()
