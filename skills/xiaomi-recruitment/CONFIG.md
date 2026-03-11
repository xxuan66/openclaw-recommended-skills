# 小米招聘爬虫配置指南

## 重要发现

小米招聘官网使用的是**字节跳动猎头平台**托管：
- 官网：https://hr.xiaomi.com/
- 实际招聘系统：https://xiaomi.jobs.f.mioffice.cn/

## 校招页面 URL

- 校招首页：https://xiaomi.jobs.f.mioffice.cn/campus/?spread=J7NS6YR
- 社会招聘：https://xiaomi.jobs.f.mioffice.cn/index
- 实习生：https://xiaomi.jobs.f.mioffice.cn/internship/?spread=6AA3R7B
- 未来星：https://xiaomi.jobs.f.mioffice.cn/toptalent

## 爬虫策略

由于招聘平台需要登录认证，我们使用 **Selenium 模拟浏览器** 进行爬取：

```bash
# 安装依赖
pip install -r requirements.txt

# 运行爬虫
python spiders/xiaomi_campus.py --update
```

## 如果爬取失败

### 1. 检查 Selenium 安装

```bash
pip install selenium webdriver-manager
```

### 2. 检查 Chrome/Chromium

确保系统已安装 Chrome 或 Chromium 浏览器：

```bash
# Ubuntu/Debian
sudo apt-get install chromium-browser

# CentOS/RHEL
sudo yum install chromium

# 或者使用 Google Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
```

### 3. 显示浏览器窗口调试

```bash
python spiders/xiaomi_campus.py --no-headless
```

### 4. 手动查看页面结构

1. 打开 Chrome 浏览器
2. 访问 https://xiaomi.jobs.f.mioffice.cn/campus/
3. 按 F12 打开开发者工具
4. 查看岗位列表的 HTML 结构
5. 更新 `spiders/xiaomi_campus.py` 中的选择器

## 选择器配置

在 `spiders/xiaomi_campus.py` 中修改岗位元素选择器：

```python
selectors = [
    '.job-item', '.position-item', '.job-list-item',
    '.recruit-item', '[data-job-id]', '.campus-job-item',
    # 添加你找到的新选择器
]
```

## 数据验证

爬取完成后，检查输出文件：

```bash
cat data/xiaomi_campus_jobs.csv
```

预期格式：
```csv
job_id,job_name,department,work_city,education,major,publish_date,deadline,job_type,description,requirements,job_url,crawl_time
,后端开发工程师，技术部，北京，本科，计算机相关，,,campus,,,2026-03-07 22:45:52
```

## 定时任务

```bash
# 每天上午 9 点执行
0 9 * * * cd /path/to/xiaomi-recruitment && python spiders/xiaomi_campus.py --update >> /var/log/xiaomi_crawler.log 2>&1
```

## 常见问题

### Q: 爬取到 0 条数据
A: 可能是页面结构变化或需要登录。尝试：
1. 使用 `--no-headless` 查看浏览器实际渲染
2. 检查是否需要登录
3. 更新选择器

### Q: ChromeDriver 版本不匹配
A: webdriver-manager 会自动处理，如果仍有问题：
```bash
pip install --upgrade webdriver-manager
```

### Q: 被反爬虫拦截
A: 增加请求间隔，添加随机 User-Agent
