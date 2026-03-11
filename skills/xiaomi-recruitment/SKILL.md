---
name: xiaomi-recruitment
description: 爬取小米招聘官网 2026 年春季校招岗位信息。使用 Playwright 或 Selenium 模拟浏览器访问字节跳动猎头平台 (xiaomi.jobs.f.mioffice.cn)，保存为 CSV 格式，支持增量更新和全量覆盖。使用场景：监控校招岗位、保存岗位信息、定期更新岗位数据。
---

# 小米招聘爬虫技能

爬取小米招聘官网的校招岗位信息，保存为 CSV 格式，支持增量更新。

## 重要提示

⚠️ 小米招聘官网使用**字节跳动猎头平台**托管：
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

# 全量爬取（首次使用）
python spiders/xiaomi_campus_playwright.py --full

# 增量更新（日常使用）
python spiders/xiaomi_campus_playwright.py --update
```

### 备选方案（Selenium）

```bash
# 安装 Selenium
pip install selenium webdriver-manager

# 运行（需要 ChromeDriver）
python spiders/xiaomi_campus.py --full
```

## 输出文件

- `data/xiaomi_campus_jobs.csv` - 岗位数据 CSV 文件
- `data/.crawler_state.json` - 爬虫状态文件

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
| job_type | 岗位类型（campus=校招） |
| description | 岗位描述 |
| requirements | 任职要求 |
| job_url | 岗位详情页 URL |
| crawl_time | 爬取时间 |

## 更新策略

### 增量更新（推荐）

```bash
python spiders/xiaomi_campus_playwright.py --update
```

- 只添加新发现的岗位
- 基于岗位名称去重
- 保留历史数据
- 适合定期执行（如每天/每周）

### 全量覆盖

```bash
python spiders/xiaomi_campus_playwright.py --full
```

- 重新爬取所有岗位
- 覆盖现有 CSV 文件
- 适合首次使用或数据重置

## 定时任务示例

### Linux cron（每天上午 9 点执行）

```bash
# 编辑 crontab
crontab -e

# 添加任务
0 9 * * * cd /path/to/xiaomi-recruitment && python spiders/xiaomi_campus_playwright.py --update >> /var/log/xiaomi_crawler.log 2>&1
```

### Python 脚本定期执行

```python
import schedule
import time
import subprocess

def daily_update():
    result = subprocess.run(
        ['python', 'spiders/xiaomi_campus_playwright.py', '--update'],
        capture_output=True,
        text=True,
        cwd='/path/to/xiaomi-recruitment'
    )
    print(result.stdout)

# 每天上午 9 点执行
schedule.every().day.at("09:00").do(daily_update)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## 故障排查

### 问题 1：爬取到 0 条数据

**原因**：网站结构调整或需要登录

**解决方法**：
1. 使用 `--no-headless` 查看浏览器实际渲染
2. 手动访问 https://xiaomi.jobs.f.mioffice.cn/campus/ 确认页面可访问
3. 检查是否需要登录认证
4. 更新选择器（见 CONFIG.md）

### 问题 2：Playwright 安装失败

**解决方法**：
```bash
# 使用国内镜像
pip install playwright -i https://pypi.tuna.tsinghua.edu.cn/simple

# 安装浏览器
playwright install chromium
```

### 问题 3：ChromeDriver 版本不匹配

**解决方法**：使用 Playwright 版本，它自动管理浏览器驱动。

### 问题 4：权限错误

**解决方法**：
```bash
pip install --user playwright
```

## 注意事项

1. **遵守 robots.txt**：爬取前检查网站 robots.txt 政策
2. **请求频率**：避免频繁请求，建议间隔至少 5 分钟
3. **数据备份**：定期备份 CSV 文件，防止数据丢失
4. **网站变更**：如网站结构调整，需更新爬虫代码

## 扩展功能

如需添加以下功能，可修改爬虫脚本：

- **邮件通知**：新岗位出现时发送邮件提醒
- **微信推送**：通过企业微信/钉钉推送新岗位
- **数据去重**：基于岗位名称和部门的模糊匹配
- **多格式导出**：支持 JSON、Excel 等格式
- **岗位详情爬取**：深入爬取每个岗位的详细信息

## 依赖说明

### Playwright 版本（推荐）
- `playwright>=1.40.0` - 浏览器自动化
- 自动管理 Chromium 浏览器

### Selenium 版本（备选）
- `selenium>=4.15.0` - 浏览器自动化
- `webdriver-manager>=4.0.0` - ChromeDriver 自动管理
- 需要安装 Chrome/Chromium 浏览器

## 相关文档

- `README.md` - 快速入门指南
- `INSTALL.md` - 详细安装指南
- `CONFIG.md` - API 配置指南
