# 📝 飞书文档技能

## 描述
读写编辑飞书文档，动嘴就能改文档。支持 Markdown 格式内容生成，知识库文档管理。

## 功能
- **文档读取**: 直接读取飞书文档内容
- **文档创建**: 创建新文档并写入内容
- **文档编辑**: 更新现有文档内容
- **Markdown 支持**: 自动转换 Markdown 为飞书格式
- **知识库管理**: 管理飞书知识库文档
- **文档同步**: 多平台内容同步到飞书

## 使用方法
```
/doc read <文档链接/ID>     # 读取文档内容
/doc create <标题> <内容>   # 创建新文档
/doc update <文档 ID> <内容> # 更新文档
/doc list <知识库 ID>       # 列出知识库文档
/doc summary <文档 ID>      # 生成文档摘要
/doc move <文档 ID> <目标文件夹>  # 移动文档
```

## 配置项
- `FEISHU_APP_ID`: 飞书应用 App ID
- `FEISHU_APP_SECRET`: 飞书应用 App Secret
- `FEISHU_ACCESS_TOKEN`: 飞书 access token
- `DEFAULT_FOLDER_TOKEN`: 默认文档夹 Token

## 输出格式
- 文档内容（Markdown 格式）
- 文档链接
- 操作状态确认

## 注意事项
- 需要飞书开放平台文档读写权限
- 大文档建议分块读取
- 敏感文档注意权限设置
