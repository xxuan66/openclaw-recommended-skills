# 小米招聘爬虫

爬取小米招聘官网的 2026 年春季校招岗位信息，保存为 CSV 格式，支持增量更新。

## ⚠️ 重要提示

小米招聘官网使用**字节跳动猎头平台**托管：
- 官网入口：https://hr.xiaomi.com/
- 实际招聘系统：https://xiaomi.jobs.f.mioffice.cn/

## 快速开始

### 安装依赖（推荐 Playwright）

```bash
cd /path/to/xiaomi-recruitment

# 安装 Playwright
pip install playwright

# 安装 Chromium 浏览器
playwright install chromium

# 运行爬虫
python spiders/xiaomi_campus_playwright.py --full
```

### 查看结果

```bash
cat data/xiaomi_campus_jobs.csv
```

## 文件说明

```
xiaomi-recruitment/
├── README.md                      # 本文件
├── INSTALL.md                     # 详细安装指南
├── CONFIG.md                      # API 配置指南
├── SKILL.md                       # 技能使用文档
├── requirements.txt               # Python 依赖
├── spiders/
│   ├── xiaomi_campus_playwright.py  # Playwright 版本（推荐）
│   └── xiaomi_campus.py             # Selenium 版本（备选）
└── data/
    ├── xiaomi_campus_jobs.csv       # 输出数据
    └── .crawler_state.json          # 爬虫状态
```

## 使用方式

```bash
# 全量爬取（首次使用）
python spiders/xiaomi_campus_playwright.py --full

# 增量更新（日常使用）
python spiders/xiaomi_campus_playwright.py --update

# 显示浏览器窗口（调试用）
python spiders/xiaomi_campus_playwright.py --no-headless

# 指定输出目录
python spiders/xiaomi_campus_playwright.py --output /path/to/output
```

## CSV 字段说明

| 字段 | 说明 |
|------|------|
| job_id | 岗位 ID |
| job_name | 岗位名称 |
| department | 所属部门 |
| work_city | 工作城市 |
| education | 学历要求 |
| major | 专业要求 |
| publish_date | 发布日期 |
| deadline | 截止日期 |
| job_type | 岗位类型 |
| description | 岗位描述 |
| requirements | 任职要求 |
| job_url | 详情 URL |
| crawl_time | 爬取时间 |

## 定时任务

```bash
# 每天上午 9 点执行增量更新
0 9 * * * cd /path/to/xiaomi-recruitment && python spiders/xiaomi_campus_playwright.py --update >> /var/log/xiaomi_crawler.log 2>&1
```

## 常见问题

### Q: 爬取到 0 条数据
A: 可能是网站结构变化。尝试：
1. 使用 `--no-headless` 查看浏览器实际渲染
2. 检查页面是否需要登录
3. 更新选择器或联系技能维护者

### Q: Playwright 安装失败
A: 参考 `INSTALL.md` 中的详细安装指南。

### Q: ChromeDriver 版本不匹配
A: 使用 Playwright 版本，它自动管理浏览器驱动。

## 示例输出

```csv
job_id,job_name,department,work_city,education,major,publish_date,deadline,job_type,description,requirements,job_url,crawl_time
,后端工程师，,北京，本科，,2026-03-01,2026-03-31,campus,,,https://xiaomi.jobs.f.mioffice.cn/campus/,2026-03-07 22:45:52
,前端工程师，,上海，本科，,2026-03-01,2026-03-31,campus,,,https://xiaomi.jobs.f.mioffice.cn/campus/,2026-03-07 22:45:52
```

## 技术支持

如遇到问题，请提供：
1. 错误信息或日志
2. 使用的 Python 版本
3. 操作系统信息
