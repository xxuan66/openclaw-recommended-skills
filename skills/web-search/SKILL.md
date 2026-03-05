# 🔍 网页搜索 & 分析技能

## 描述
智能网页搜索、内容提取、深度分析，快速获取网络信息。

## 功能
- **智能搜索**: 多引擎搜索，结果去重排序
- **内容提取**: 从网页提取正文、图片、数据
- **深度分析**: 分析网页内容，生成摘要和洞察
- **多页对比**: 对比多个网页内容
- **信息验证**: 交叉验证信息来源可靠性
- **趋势分析**: 分析话题热度和趋势

## 使用方法
```
/search <关键词>           # 搜索网页
/search news <关键词>      # 搜索新闻
/search academic <关键词>  # 搜索学术文献
/analyze <URL>            # 分析网页内容
/compare <URL1> <URL2>    # 对比多个网页
/summarize <URL>          # 生成网页摘要
```

## 配置项
- `SEARCH_ENGINE`: 默认搜索引擎 (searxng/brave/google)
- `SEARCH_API_KEY`: 搜索 API 密钥（如需要）
- `MAX_RESULTS`: 默认返回结果数
- `EXTRACT_MODE`: 内容提取模式 (markdown/text)
- `SEARXNG_URL`: SearXNG 实例地址（如使用）

## 输出格式
- 搜索结果列表（标题、URL、摘要）
- 网页正文内容
- 分析摘要和洞察

## 注意事项
- 注意信息来源可靠性
- 尊重网站 robots.txt 规则
- 避免高频请求触发反爬
