# 🔍 搜索类 Skill 推荐

## 1. searxng

**版本:** 1.0.3  
**Slug:** `searxng`  
**类别:** 搜索  

### 简介
隐私保护的本地元搜索引擎，聚合多个搜索结果源。

### 推荐理由
- ✅ 隐私优先，不追踪用户
- ✅ 本地部署，数据不出境
- ✅ 支持多个搜索引擎后端
- ✅ 可自定义搜索源

### 安装命令
```bash
clawhub install searxng
```

### 配置要求
- 需要配置 SEARXNG_URL 环境变量
- 默认：`http://localhost:8080`

### 使用示例
```bash
# 搜索天气
openclaw agent -m "搜索上海天气"
```

---

## 2. tavily-search

**版本:** 1.0.0  
**Slug:** `tavily-search`  
**类别:** 搜索  

### 简介
AI 优化的实时网络搜索 API，返回简洁相关的结果。

### 推荐理由
- ✅ AI 优化结果，质量高
- ✅ 实时数据
- ✅ 适合 AI Agent 使用
- ✅ 返回格式友好

### 安装命令
```bash
clawhub install tavily-search
```

### 配置要求
- 需要 Tavily API Key

### 使用示例
```bash
# 搜索最新新闻
openclaw agent -m "搜索今天的科技新闻"
```

---

## 3. baidu-search

**版本:** 1.1.1  
**Slug:** `baidu-search`  
**类别:** 搜索  

### 简介
百度 AI 搜索引擎集成，支持中文搜索优化。

### 推荐理由
- ✅ 中文搜索结果质量高
- ✅ 支持热搜榜数据
- ✅ 免费使用
- ✅ 适合国内用户

### 安装命令
```bash
clawhub install baidu-search
```

### 配置要求
- 无需 API Key

### 使用示例
```bash
# 搜索中文内容
openclaw agent -m "搜索 AI  Agent 最新进展"
```

---

## 对比总结

| Skill | 隐私性 | 实时性 | 中文支持 | API Key |
|-------|--------|--------|----------|---------|
| searxng | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | 否 |
| tavily-search | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 是 |
| baidu-search | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 否 |

**推荐组合:** searxng (日常) + tavily-search (实时) + baidu-search (中文)
