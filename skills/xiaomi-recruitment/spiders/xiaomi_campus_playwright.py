#!/usr/bin/env python3
"""
小米招聘官网校招岗位信息爬虫（Playwright 版本）
Playwright 比 Selenium 更稳定，自动管理浏览器驱动

依赖：pip install playwright
      playwright install chromium
"""

import csv
import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict
import time
import re

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


class XiaomiCampusSpiderPlaywright:
    """小米校招岗位信息爬虫（Playwright 版本）"""
    
    def __init__(self, output_dir: str = None, headless: bool = True):
        """
        初始化爬虫
        
        Args:
            output_dir: 输出目录
            headless: 是否无头模式
        """
        # 设置输出目录
        if output_dir is None:
            self.output_dir = Path(__file__).parent.parent / 'data'
        else:
            self.output_dir = Path(output_dir)
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 数据文件路径
        self.csv_file = self.output_dir / 'xiaomi_campus_jobs.csv'
        self.state_file = self.output_dir / '.crawler_state.json'
        
        # 小米招聘 URL
        self.base_url = 'https://xiaomi.jobs.f.mioffice.cn'
        self.campus_url = 'https://xiaomi.jobs.f.mioffice.cn/campus/?spread=J7NS6YR'
        
        self.headless = headless
        self.browser = None
        self.context = None
        self.page = None
    
    def setup_browser(self):
        """配置浏览器"""
        if not PLAYWRIGHT_AVAILABLE:
            print("Playwright 未安装，请运行：pip install playwright")
            print("然后运行：playwright install chromium")
            return False
        
        try:
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(
                headless=self.headless,
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                ]
            )
            self.context = self.browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                viewport={'width': 1920, 'height': 1080}
            )
            self.page = self.context.new_page()
            return True
        except Exception as e:
            print(f"启动浏览器失败：{e}")
            return False
    
    def close_browser(self):
        """关闭浏览器"""
        try:
            if self.page:
                self.page.close()
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
            if hasattr(self, 'playwright'):
                self.playwright.stop()
        except:
            pass
    
    def parse_job_from_page(self) -> List[Dict]:
        """从页面解析岗位信息"""
        jobs = []
        
        if not self.page:
            return jobs
        
        try:
            # 等待页面加载
            self.page.wait_for_load_state('networkidle', timeout=30000)
        except PlaywrightTimeout:
            print("等待页面加载超时，继续...")
        
        time.sleep(3)  # 等待 JavaScript 渲染
        
        # 获取页面内容
        content = self.page.content()
        text = self.page.inner_text('body')
        
        # 尝试多种选择器查找岗位元素
        selectors = [
            '.job-item', '.position-item', '.job-list-item', '.recruit-item',
            '[data-job-id]', '.campus-job-item', '.recruitment-item',
            '.position-card', '.job-card', '.job', '.position'
        ]
        
        job_elements = []
        for selector in selectors:
            try:
                elements = self.page.query_selector_all(selector)
                if elements:
                    print(f"找到 {len(elements)} 个岗位元素（选择器：{selector}）")
                    job_elements = elements
                    break
            except:
                continue
        
        # 如果找到元素，解析每个岗位
        if job_elements:
            for element in job_elements[:100]:
                try:
                    job = self.extract_job_info(element)
                    if job and job.get('job_name'):
                        jobs.append(job)
                except:
                    continue
        else:
            # 没找到元素，从文本中提取
            print("未找到岗位元素，尝试从文本提取...")
            jobs = self.extract_jobs_from_text(text)
        
        return jobs
    
    def extract_job_info(self, element) -> Dict:
        """从元素提取岗位信息"""
        job = {
            'job_id': '',
            'job_name': '',
            'department': '',
            'work_city': '',
            'education': '',
            'major': '',
            'publish_date': '',
            'deadline': '',
            'job_type': 'campus',
            'description': '',
            'requirements': '',
            'job_url': '',
            'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }
        
        try:
            # 获取文本内容
            text = element.inner_text()
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            
            if lines:
                job['job_name'] = lines[0]
            
            # 尝试获取 job_id
            job_id = element.get_attribute('data-job-id') or element.get_attribute('data-id') or ''
            job['job_id'] = str(job_id)
            
            # 尝试获取链接
            try:
                link = element.query_selector('a')
                if link:
                    href = link.get_attribute('href')
                    if href:
                        job['job_url'] = href if href.startswith('http') else f"{self.base_url}{href}"
            except:
                pass
            
            # 从文本中提取城市
            city_pattern = r'(北京 | 上海 | 深圳 | 武汉 | 南京 | 杭州)'
            cities = re.findall(city_pattern, text)
            if cities:
                job['work_city'] = cities[0]
            
            # 从文本中提取学历
            edu_pattern = r'(本科 | 硕士 | 博士 | 大专)'
            edus = re.findall(edu_pattern, text)
            if edus:
                job['education'] = edus[0]
            
        except Exception as e:
            print(f"提取岗位信息失败：{e}")
        
        return job
    
    def extract_jobs_from_text(self, text: str) -> List[Dict]:
        """从文本中提取岗位信息"""
        jobs = []
        
        # 岗位名称模式
        job_patterns = [
            r'([\u4e00-\u9fa5]{2,8}工程师)',
            r'([\u4e00-\u9fa5]{2,8}经理)',
            r'([\u4e00-\u9fa5]{2,8}专员)',
            r'([\u4e00-\u9fa5]{2,8}分析师)',
            r'([\u4e00-\u9fa5]{2,8}设计师)',
            r'([\u4e00-\u9fa5]{2,6}产品)',
            r'([\u4e00-\u9fa5]{2,6}运营)',
            r'([\u4e00-\u9fa5]{2,6}市场)',
            r'([\u4e00-\u9fa5]{2,6}开发)',
            r'([\u4e00-\u9fa5]{2,6}测试)',
            r'([\u4e00-\u9fa5]{2,6}算法)',
            r'([\u4e00-\u9fa5]{2,6}数据)',
        ]
        
        job_names = set()
        for pattern in job_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if 2 <= len(match) <= 15:
                    job_names.add(match)
        
        # 提取城市
        city_pattern = r'(北京 | 上海 | 深圳 | 武汉 | 南京 | 杭州)'
        cities = re.findall(city_pattern, text)
        
        # 提取学历
        edu_pattern = r'(本科 | 硕士 | 博士 | 大专)'
        educations = re.findall(edu_pattern, text)
        
        # 创建岗位记录
        for i, job_name in enumerate(list(job_names)[:50]):
            job = {
                'job_id': '',
                'job_name': job_name,
                'department': '',
                'work_city': cities[0] if cities else '',
                'education': educations[0] if educations else '',
                'major': '',
                'publish_date': '',
                'deadline': '',
                'job_type': 'campus',
                'description': '',
                'requirements': '',
                'job_url': self.campus_url,
                'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }
            jobs.append(job)
        
        return jobs
    
    def load_existing_data(self) -> Dict[str, Dict]:
        """加载已有的岗位数据"""
        existing_jobs = {}
        if self.csv_file.exists():
            with open(self.csv_file, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    job_key = row.get('job_name', '')
                    if job_key:
                        existing_jobs[job_key] = row
        return existing_jobs
    
    def save_to_csv(self, jobs: List[Dict], mode: str = 'append'):
        """保存岗位数据到 CSV"""
        if not jobs:
            print("没有数据可保存")
            return
        
        fieldnames = [
            'job_id', 'job_name', 'department', 'work_city',
            'education', 'major', 'publish_date', 'deadline',
            'job_type', 'description', 'requirements', 'job_url', 'crawl_time'
        ]
        
        file_exists = self.csv_file.exists() and os.path.getsize(self.csv_file) > 0
        
        with open(self.csv_file, 'a' if mode == 'append' and file_exists else 'w', 
                  encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not file_exists or mode == 'overwrite':
                writer.writeheader()
            for job in jobs:
                writer.writerow(job)
        
        print(f"已保存 {len(jobs)} 条岗位数据到 {self.csv_file}")
    
    def save_state(self, state: Dict):
        """保存爬虫状态"""
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    
    def crawl(self, update: bool = True) -> Dict:
        """执行爬取任务"""
        print(f"开始爬取小米校招岗位信息（Playwright 版本）...")
        print(f"模式：{'增量更新' if update else '全量覆盖'}")
        print(f"目标 URL: {self.campus_url}")
        
        if not PLAYWRIGHT_AVAILABLE:
            print("\n错误：Playwright 未安装")
            print("请运行以下命令：")
            print("  pip install playwright")
            print("  playwright install chromium")
            return {'error': 'Playwright 未安装'}
        
        # 加载已有数据
        existing_jobs = self.load_existing_data() if update else {}
        
        all_jobs = []
        new_count = 0
        
        # 启动浏览器
        if not self.setup_browser():
            return {'error': '无法启动浏览器'}
        
        try:
            # 访问校招页面
            print("正在访问小米校招官网...")
            self.page.goto(self.campus_url, wait_until='domcontentloaded', timeout=60000)
            
            # 解析岗位
            print("正在解析岗位信息...")
            all_jobs = self.parse_job_from_page()
            
            # 统计新增
            for job in all_jobs:
                job_key = job.get('job_name', '')
                if job_key not in existing_jobs:
                    new_count += 1
            
            # 保存数据
            if all_jobs:
                self.save_to_csv(all_jobs, mode='overwrite' if not update else 'append')
            
            # 更新状态
            state = {
                'last_crawl': datetime.now().isoformat(),
                'total_jobs': len(existing_jobs) + new_count,
                'new_count': new_count,
                'crawl_url': self.campus_url,
            }
            self.save_state(state)
            
            result_summary = {
                'total_crawled': len(all_jobs),
                'new_jobs': new_count,
                'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'output_file': str(self.csv_file),
            }
            
            print(f"\n爬取完成!")
            print(f"  爬取岗位：{len(all_jobs)}")
            print(f"  新增岗位：{new_count}")
            print(f"  输出文件：{self.csv_file}")
            
            return result_summary
            
        except Exception as e:
            print(f"爬取失败：{e}")
            return {'error': str(e)}
        finally:
            self.close_browser()


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='小米校招岗位信息爬虫（Playwright）')
    parser.add_argument('--update', action='store_true', default=True, help='增量更新模式（默认）')
    parser.add_argument('--full', action='store_true', help='全量覆盖模式')
    parser.add_argument('--output', type=str, default=None, help='输出目录路径')
    parser.add_argument('--no-headless', action='store_true', help='显示浏览器窗口')
    
    args = parser.parse_args()
    
    if not PLAYWRIGHT_AVAILABLE:
        print("\n错误：Playwright 未安装")
        print("请运行以下命令：")
        print("  pip install playwright")
        print("  playwright install chromium")
        return
    
    spider = XiaomiCampusSpiderPlaywright(output_dir=args.output, headless=not args.no_headless)
    result = spider.crawl(update=not args.full)
    
    print("\n爬取结果:")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
