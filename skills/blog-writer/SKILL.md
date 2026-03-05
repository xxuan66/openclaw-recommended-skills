# ✍️ 博客写手技能

## 描述
长文写作、SEO 优化、系列策划，持续产出高质量内容。个人风格博客，从调研到发布全流程。

## 功能
- **选题调研**: 分析热门话题，生成博客选题建议
- **大纲生成**: 根据主题生成详细文章大纲
- **内容写作**: 撰写符合个人风格的博客文章
- **SEO 优化**: 自动优化标题、关键词、meta 描述
- **自动配图**: 为文章生成或推荐配图
- **多平台发布**: 支持发布到多个博客平台

## 使用方法
```
/blog write <主题>           # 撰写博客文章
/blog outline <主题>         # 生成文章大纲
/blog seo <文章内容>         # SEO 优化建议
/blog publish <文章路径>     # 发布到博客平台
```

## 配置项
- `BLOG_PLATFORM`: 目标博客平台 (wordpress/hexo/ghost/jekyll)
- `BLOG_API_URL`: 博客平台 API 地址
- `BLOG_API_KEY`: 博客平台 API 密钥
- `BLOG_AUTHOR`: 作者名称
- `BLOG_STYLE`: 写作风格 (technical/casual/storytelling)

## 输出格式
- Markdown 格式文章
- SEO 元数据（标题、描述、关键词）
- 发布链接

## 注意事项
- 支持自定义写作风格
- 可配置自动发布或手动确认
- 建议人工审核后再发布
