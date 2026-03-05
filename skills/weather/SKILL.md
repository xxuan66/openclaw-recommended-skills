# 🌤️ 天气查询技能

## 描述
查询全球天气信息，支持 wttr.in + Open-Meteo 双源，无需 API 密钥。

## 功能
- **当前天气**: 查询当前位置天气
- **天气预报**: 获取 7-14 天天气预报
- **多地查询**: 同时查询多个城市天气
- **天气提醒**: 恶劣天气自动提醒
- **历史天气**: 查询历史天气数据
- **空气质量**: 查询 AQI 空气质量指数

## 使用方法
```
/weather <城市>            # 查询当前天气
/weather forecast <城市>   # 查询天气预报
/weather compare <城市 1> <城市 2>  # 对比多地天气
/weather aqi <城市>        # 查询空气质量
/weather alert <城市>      # 查询天气预警
```

## 配置项
- `WEATHER_PROVIDER`: 默认天气服务 (wttr/open-meteo)
- `WEATHER_UNITS`: 温度单位 (celsius/fahrenheit)
- `WEATHER_LANG`: 语言 (zh/en)
- `DEFAULT_CITY`: 默认查询城市

## 输出格式
- 当前天气（温度、湿度、风速、天气状况）
- 天气预报（每日最高/最低温、降水概率）
- 天气预警信息

## 注意事项
- 无需 API 密钥，直接调用公开服务
- 恶劣天气建议提前提醒用户
- 出行前可自动查询目的地天气
