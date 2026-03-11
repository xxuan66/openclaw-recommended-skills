# 小米招聘爬虫安装指南

## 快速开始

### 方法 1：使用 Playwright（推荐）

Playwright 比 Selenium 更稳定，自动管理浏览器驱动。

```bash
# 1. 安装 Playwright
pip install playwright

# 2. 安装 Chromium 浏览器
playwright install chromium

# 3. 运行爬虫
python spiders/xiaomi_campus_playwright.py --full
```

### 方法 2：使用 Selenium + ChromeDriver

```bash
# 1. 安装 Selenium
pip install selenium webdriver-manager

# 2. 确保已安装 Chrome 浏览器
google-chrome --version

# 3. 安装 ChromeDriver（自动）
# webdriver-manager 会自动下载匹配的 ChromeDriver

# 4. 运行爬虫
python spiders/xiaomi_campus.py --full
```

### 方法 3：无浏览器模式（仅 API）

如果无法安装浏览器，可以手动配置 API 端点。

## 系统要求

- Python 3.6+
- Chrome/Chromium 浏览器
- 稳定的网络连接

## 常见问题

### Q: ChromeDriver 版本不匹配
A: 使用 webdriver-manager 自动管理：
```bash
pip install --upgrade webdriver-manager
```

### Q: 权限错误
A: 使用 `--user` 安装：
```bash
pip install --user selenium playwright
```

### Q: 爬取到 0 条数据
A: 可能是网站结构变化，需要更新选择器或 API 端点。

## 手动查找 API 端点

1. 打开 Chrome 浏览器
2. 访问 https://xiaomi.jobs.f.mioffice.cn/campus/
3. 按 F12 打开开发者工具
4. 切换到 Network 标签
5. 刷新页面，查找 XHR/Fetch 请求
6. 找到返回岗位数据的 API

## 输出验证

爬取成功后，检查输出文件：

```bash
cat data/xiaomi_campus_jobs.csv
head -5 data/xiaomi_campus_jobs.csv
```
