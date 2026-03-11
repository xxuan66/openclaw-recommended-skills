#!/usr/bin/env python3
"""
小米招聘官网校招岗位信息爬虫
支持 2026 年春季校招岗位信息爬取，保存为 CSV，支持增量更新

注意：小米招聘使用字节跳动猎头平台 (xiaomi.jobs.f.mioffice.cn)
需要 Selenium 模拟浏览器访问
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
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait, Select
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False


class XiaomiCampusSpider:
    """小米校招岗位信息爬虫"""
    
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
        
        # 小米招聘 URL（使用字节跳动猎头平台）
        self.base_url = 'https://xiaomi.jobs.f.mioffice.cn'
        self.campus_url = 'https://xiaomi.jobs.f.mioffice.cn/campus/?spread=J7NS6YR'
        
        # 浏览器配置
        self.headless = headless
        self.driver = None
        
        if not SELENIUM_AVAILABLE:
            print("警告：Selenium 未安装，将使用简易模式")
    
    def setup_driver(self):
        """配置 Chrome 驱动"""
        if not SELENIUM_AVAILABLE:
            return False
        
        options = Options()
        if self.headless:
            options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        
        # 尝试多种 ChromeDriver 路径
        driver_paths = [
            '/usr/bin/chromedriver',
            '/usr/local/bin/chromedriver',
            '/home/admin/.local/bin/chromedriver',
            '/snap/bin/chromedriver',
        ]
        
        driver_path = None
        for path in driver_paths:
            if os.path.exists(path):
                driver_path = path
                break
        
        try:
            if driver_path:
                service = Service(executable_path=driver_path)
                self.driver = webdriver.Chrome(service=service, options=options)
            else:
                # 尝试自动查找
                self.driver = webdriver.Chrome(options=options)
            
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return True
        except Exception as e:
            print(f"启动浏览器失败：{e}")
            print("\n请安装 ChromeDriver:")
            print("  方法 1: sudo yum install chromedriver")
            print("  方法 2: pip install webdriver-manager (需要 Selenium 4+)")
            return False
    
    def close_driver(self):
        """关闭浏览器"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None
    
    def parse_job_from_page(self) -> List[Dict]:
        """从页面解析岗位信息"""
        jobs = []
        
        if not self.driver:
            return jobs
        
        try:
            # 等待岗位列表加载
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
        except TimeoutException:
            print("等待页面加载超时，尝试继续...")
        
        time.sleep(5)  # 等待 JavaScript 渲染
        
        # 获取页面源码，手动解析
        html = self.driver.page_source
        
        # 尝试从页面文本中提取岗位信息
        # 查找可能的岗位名称模式
        job_patterns = [
            r'[\u4e00-\u9fa5]+工程师',
            r'[\u4e00-\u9fa5]+经理',
            r'[\u4e00-\u9fa5]+专员',
            r'[\u4e00-\u9fa5]+分析师',
            r'[\u4e00-\u9fa5]+设计师',
            r'[\u4e00-\u9fa5]+产品',
            r'[\u4e00-\u9fa5]+运营',
            r'[\u4e00-\u9fa5]+市场',
            r'[\u4e00-\u9fa5]+开发',
            r'[\u4e00-\u9fa5]+测试',
        ]
        
        job_names = set()
        for pattern in job_patterns:
            matches = re.findall(pattern, html)
            for match in matches:
                if len(match) >= 2 and len(match) <= 20:
                    job_names.add(match)
        
        # 创建岗位记录
        for job_name in job_names:
            job = {
                'job_id': '',
                'job_name': job_name,
                'department': '',
                'work_city': '',
                'education': '',
                'major': '',
                'publish_date': '',
                'deadline': '',
                'job_type': 'campus',
                'description': '',
                'requirements': '',
                'job_url': f"{self.base_url}/campus/",
                'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }
            jobs.append(job)
        
        # 尝试查找城市信息
        city_pattern = r'(北京 | 上海 | 深圳 | 武汉 | 南京 | 杭州)'
        cities = re.findall(city_pattern, html)
        
        # 尝试查找学历要求
        edu_pattern = r'(本科 | 硕士 | 博士 | 大专)'
        educations = re.findall(edu_pattern, html)
        
        # 为岗位添加城市和学历信息
        if cities:
            for job in jobs[:len(cities)]:
                job['work_city'] = cities[0]  # 默认第一个城市
        if educations:
            for job in jobs[:len(educations)]:
                job['education'] = educations[0]  # 默认本科
        
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
    
    def load_state(self) -> Dict:
        """加载爬虫状态"""
        if self.state_file.exists():
            with open(self.state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'last_crawl': None, 'total_jobs': 0}
    
    def crawl(self, update: bool = True) -> Dict:
        """执行爬取任务"""
        print(f"开始爬取小米校招岗位信息...")
        print(f"模式：{'增量更新' if update else '全量覆盖'}")
        print(f"目标 URL: {self.campus_url}")
        
        # 加载已有数据
        existing_jobs = self.load_existing_data() if update else {}
        
        all_jobs = []
        new_count = 0
        
        # 启动浏览器
        if not self.setup_driver():
            print("无法启动浏览器，尝试使用 requests 直接获取...")
            return self.crawl_fallback(update)
        
        try:
            # 访问校招页面
            print("正在访问小米校招官网...")
            self.driver.get(self.campus_url)
            
            # 等待页面加载
            time.sleep(5)
            
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
            self.close_driver()
    
    def crawl_fallback(self, update: bool = True) -> Dict:
        """备用爬取方法（使用 requests）"""
        import requests
        
        print("使用备用方法爬取...")
        
        try:
            session = requests.Session()
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            })
            
            response = session.get(self.campus_url, timeout=30)
            html = response.text
            
            # 解析岗位名称
            job_patterns = [
                r'[\u4e00-\u9fa5]+工程师',
                r'[\u4e00-\u9fa5]+经理',
                r'[\u4e00-\u9fa5]+专员',
                r'[\u4e00-\u9fa5]+分析师',
                r'[\u4e00-\u9fa5]+产品',
                r'[\u4e00-\u9fa5]+运营',
            ]
            
            job_names = set()
            for pattern in job_patterns:
                matches = re.findall(pattern, html)
                for match in matches:
                    if 2 <= len(match) <= 20:
                        job_names.add(match)
            
            all_jobs = []
            for job_name in job_names:
                all_jobs.append({
                    'job_id': '',
                    'job_name': job_name,
                    'department': '',
                    'work_city': '',
                    'education': '',
                    'major': '',
                    'publish_date': '',
                    'deadline': '',
                    'job_type': 'campus',
                    'description': '',
                    'requirements': '',
                    'job_url': self.campus_url,
                    'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                })
            
            if all_jobs:
                self.save_to_csv(all_jobs, mode='overwrite' if not update else 'append')
            
            return {
                'total_crawled': len(all_jobs),
                'new_jobs': len(all_jobs),
                'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'output_file': str(self.csv_file),
            }
            
        except Exception as e:
            return {'error': f'备用方法失败：{e}'}


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='小米校招岗位信息爬虫')
    parser.add_argument('--update', action='store_true', default=True, help='增量更新模式（默认）')
    parser.add_argument('--full', action='store_true', help='全量覆盖模式')
    parser.add_argument('--output', type=str, default=None, help='输出目录路径')
    parser.add_argument('--no-headless', action='store_true', help='显示浏览器窗口')
    
    args = parser.parse_args()
    
    spider = XiaomiCampusSpider(output_dir=args.output, headless=not args.no_headless)
    result = spider.crawl(update=not args.full)
    
    print("\n爬取结果:")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
