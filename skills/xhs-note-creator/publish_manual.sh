#!/bin/bash
# 小红书发布脚本 - curl 版本
# 使用 Cookie 直接调用 API

set -e

# 配置
COOKIE="acw_tc=0a00d8df17726763868004375e7b9d208026b23678d14983fa78b1c4c7f52d; abRequestId=e9b8d87a-5362-5d85-ada0-7cf032ea0fcc; webBuild=5.13.1; xsecappid=xhs-pc-web; loadts=1772676388636; a1=19cbbbf171cbik22ft1fozxx896ukct4bxe5e3j8550000316878; webId=db0b55465a5a9e6d195344a671781878; websectiga=3fff3a6f9f07284b62c0f2ebf91a3b10193175c06e4f71492b60e056edcdebb2; sec_poison_id=636a4161-1cb8-476d-bf35-03667a359f7d; gid=yjSDDDiyiiDJyjSDDDiyWCqVySD3TJJi9yildY2uCCYjK2287TS94d888qyKYWY8dy400ffY; web_session=040069b2c69894ccfcc75ead9d3b4be935e626; id_token=VjEAAALQJagM6CD6tgkVp1m5kPhmZXFP7scjg0HjM8W4JIqGnK5AnKG3GxrBSD8D5xk0VwwGoAtHOvw7p4tVaHyxEivx1FEcPcetjjyNq6DkEohl+L+PiYbZarODB8Qk0bPFXj77; unread={%22ub%22:%2269a82266000000002303bf6b%22%2C%22ue%22:%2269a2c26c000000002602c675%22%2C%22uc%22:28}"

TITLE="OpenClaw 技术解析"
DESC="🤖 什么是 OpenClaw？

开源 AI 助理框架，让 AI 真正具备执行能力
不只是聊天机器人，而是能干活的全能助理

⚙️ 核心架构
- 会话管理系统：独立会话隔离、子代理协作、持久化记忆
- 技能系统：模块化设计、动态加载、版本控制

🛠️ 技术栈
- 后端：Node.js + TypeScript
- AI 集成：多模型支持（Qwen/Claude/GPT）
- 统一接口抽象、智能路由

🔌 平台集成
- 消息平台：QQ/微信/Telegram/Discord/钉钉
- 云服务：飞书全家桶（文档/表格/知识库）

📦 技能生态
- 内置技能：天气、搜索、提醒、图片生成
- ClawHub 技能市场：一键安装更新

🎯 自动化能力
- 定时任务：Cron 表达式、周期性执行
- 触发器：消息/时间/事件驱动

💻 开发体验
- 工作区系统：全局空间、文件读写、Git 集成
- 调试工具：状态查看、日志、监控

🔐 安全设计
- 沙箱执行、工具策略、敏感操作确认
- 本地存储优先、加密敏感信息

🌟 特色功能
- 记忆系统：短期 + 长期记忆、自动归档
- 心跳机制：主动检查、批量处理

🎨 媒体处理
- Playwright 渲染、多主题模板
- ElevenLabs 语音合成

OpenClaw AI 助理 自动化 开源框架 技术分享 程序员 效率工具 Node.js 技能系统 多平台集成"

IMAGES_DIR="./output"

echo "📤 开始发布小红书笔记..."
echo "标题：$TITLE"
echo "图片目录：$IMAGES_DIR"

# 由于小红书 API 需要复杂的签名，建议使用官方客户端或网页版手动发布
# 这里只提供文件准备

echo ""
echo "✅ 文件已准备就绪！"
echo ""
echo "📱 请手动发布："
echo "1. 打开 https://www.xiaohongshu.com"
echo "2. 点击'发布笔记'"
echo "3. 上传 $IMAGES_DIR 中的所有图片"
echo "4. 复制以下标题和文案"
echo ""
echo "======================"
echo "标题：$TITLE"
echo "======================"
echo ""
echo "文案："
echo "$DESC"
