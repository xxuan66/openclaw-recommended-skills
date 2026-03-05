# 📧 邮件管理技能

## 描述
收发邮件、智能分类、自动回复，告别邮箱焦虑。支持飞书邮件 API + 通用 IMAP/SMTP。

## 功能
- **邮件收发**: 发送和接收邮件
- **VIP 提醒**: 重要邮件秒级通知（老板、客户等）
- **智能分类**: 按紧急程度自动排序邮件
- **自动摘要**: 长邮件自动提炼要点
- **批量回复**: 模板化回复常规邮件
- **邮件搜索**: 快速查找历史邮件

## 使用方法
```
/email check              # 检查未读邮件
/email read <邮件 ID>      # 阅读指定邮件
/email reply <邮件 ID> <内容>  # 回复邮件
/email send <收件人> <主题> <内容>  # 发送邮件
/email summary            # 生成今日邮件摘要
/email vip <设置>         # 配置 VIP 联系人
```

## 配置项
- `EMAIL_PROVIDER`: 邮件服务商 (feishu/gmail/outlook/imap)
- `EMAIL_ADDRESS`: 邮箱地址
- `EMAIL_PASSWORD`: 邮箱密码或应用专用密码
- `EMAIL_IMAP_HOST`: IMAP 服务器地址
- `EMAIL_SMTP_HOST`: SMTP 服务器地址
- `EMAIL_IMAP_PORT`: IMAP 端口 (默认 993)
- `EMAIL_SMTP_PORT`: SMTP 端口 (默认 465)
- `VIP_CONTACTS`: VIP 联系人列表

## 输出格式
- 邮件列表（主题、发件人、时间、摘要）
- 邮件全文内容
- 发送状态确认

## 注意事项
- 建议使用应用专用密码而非主密码
- VIP 提醒需要配置通知渠道
- 定期清理已处理邮件避免堆积
