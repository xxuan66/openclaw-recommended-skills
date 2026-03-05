# 📅 飞书日历技能

## 描述
管理飞书日历事件，创建、查询、修改会议和日程，自动提醒。

## 功能
- **事件创建**: 快速创建会议和日程
- **日程查询**: 查看今日/本周/本月日程
- **冲突检测**: 自动检测时间冲突
- **会议邀请**: 自动发送飞书会议邀请
- **智能提醒**: 会前自动提醒参会人
- **会议纪要**: 会后自动生成纪要并关联日历

## 使用方法
```
/calendar today           # 查看今日日程
/calendar week            # 查看本周日程
/calendar create <主题> <时间> <参会人>  # 创建事件
/calendar find <关键词>    # 搜索事件
/calendar update <事件 ID> <修改内容>  # 修改事件
/calendar cancel <事件 ID>  # 取消事件
```

## 配置项
- `FEISHU_APP_ID`: 飞书应用 App ID
- `FEISHU_APP_SECRET`: 飞书应用 App Secret
- `FEISHU_ACCESS_TOKEN`: 飞书 access token（可自动获取）
- `FEISHU_CALENDAR_ID`: 默认日历 ID
- `DEFAULT_REMINDER_MINUTES`: 默认提醒时间（分钟）

## 输出格式
- 日程列表（主题、时间、地点、参会人）
- 事件创建/修改确认
- 会议链接（如为线上会议）

## 注意事项
- 需要飞书开放平台应用权限
- 跨时区会议需明确时区
- 敏感会议建议设置私密
