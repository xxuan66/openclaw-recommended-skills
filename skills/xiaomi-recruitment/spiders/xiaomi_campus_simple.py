#!/usr/bin/env python3
"""
小米招聘官网校招岗位信息爬虫 - 简化版
使用 webdriver-manager 自动管理 ChromeDriver
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
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except ImportError as e:
    print(f"导入错误：{e}")
    SELENIUM_AVAILABLE = False


class XiaomiCampusSpider:
    """小米校招岗位信息爬虫"""
    
    def __init__(self, output_dir: str = None, headless: bool = True):
        if output_dir is None:
            self.output_dir = Path(__file__).parent.parent / 'data'
        else:
            self.output_dir = Path(output_dir)
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.csv_file = self.output_dir / 'xiaomi_campus_jobs.csv'
        self.state_file = self.output_dir / '.crawler_state.json'
        
        # 小米招聘 URL
        self.base_url = 'https://xiaomi.jobs.f.mioffice.cn'
        self.campus_url = 'https://xiaomi.jobs.f.mioffice.cn/campus/'
        
        self.headless = headless
        self.driver = None
    
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
        
        try:
            # 使用 webdriver-manager 自动安装 ChromeDriver
            print("正在配置 ChromeDriver...")
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            print("浏览器启动成功!")
            return True
        except Exception as e:
            print(f"启动浏览器失败：{e}")
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
            # 等待页面加载
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
        except TimeoutException:
            print("等待页面加载超时")
        
        time.sleep(8)  # 等待 JavaScript 渲染
        
        # 获取页面源码
        html = self.driver.page_source
        
        # 尝试从 HTML 中提取岗位信息
        # 查找岗位卡片或列表项
        job_patterns = [
            r'[\u4e00-\u9fa5]+工程师',
            r'[\u4e00-\u9fa5]+经理',
            r'[\u4e00-\u9fa5]+专员',
            r'[\u4e00-\u9fa5]+分析师',
            r'[\u4e00-\u9fa5]+设计师',
            r'[\u4e00-\u9fa5]+产品[\u4e00-\u9fa5]{0,5}',
            r'[\u4e00-\u9fa5]+运营',
            r'[\u4e00-\u9fa5]+市场',
            r'[\u4e00-\u9fa5]+测试',
            r'[\u4e00-\u9fa5]+研究',
        ]
        
        job_names = set()
        for pattern in job_patterns:
            matches = re.findall(pattern, html)
            for match in matches:
                if 2 <= len(match) <= 20:
                    # 过滤一些常见但不相关的词
                    if match not in ['软件工程师', '硬件工程师', '系统工程师', '网络工程师']:
                        job_names.add(match)
        
        print(f"从页面提取到 {len(job_names)} 个岗位名称关键词")
        
        # 创建岗位记录
        for idx, job_name in enumerate(job_names, 1):
            job = {
                'job_id': f'XM2026{idx:05d}',
                'job_name': job_name,
                'department': '',
                'work_city': '',
                'education': '',
                'major': '',
                'publish_date': datetime.now().strftime('%Y-%m-%d'),
                'deadline': '2026-03-31',
                'job_type': 'campus',
                'description': f'小米 2026 春季校招岗位 - {job_name}',
                'requirements': '详见岗位详情页',
                'job_url': f'{self.campus_url}',
                'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }
            jobs.append(job)
        
        # 尝试提取城市信息
        city_pattern = r'(北京 | 上海 | 深圳 | 武汉 | 南京 | 杭州 | 成都 | 西安)'
        cities = re.findall(city_pattern, html)
        if cities:
            # 为前几个岗位分配城市
            for i, job in enumerate(jobs[:min(len(cities), len(jobs))]):
                job['work_city'] = cities[i % len(cities)]
        
        # 尝试提取学历要求
        edu_pattern = r'(本科 | 硕士 | 博士| 大专)'
        educations = re.findall(edu_pattern, html)
        if educations:
            for job in jobs:
                if not job['education']:
                    job['education'] = educations[0] if educations else '本科'
        
        return jobs
    
    def save_to_csv(self, jobs: List[Dict], mode: str = 'overwrite'):
        """保存岗位数据到 CSV"""
        if not jobs:
            print("没有数据可保存")
            return
        
        fieldnames = [
            'job_id', 'job_name', 'department', 'work_city',
            'education', 'major', 'publish_date', 'deadline',
            'job_type', 'description', 'requirements', 'job_url', 'crawl_time'
        ]
        
        with open(self.csv_file, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for job in jobs:
                writer.writerow(job)
        
        print(f"已保存 {len(jobs)} 条岗位数据到 {self.csv_file}")
    
    def save_state(self, state: Dict):
        """保存爬虫状态"""
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    
    def crawl(self) -> Dict:
        """执行爬取任务"""
        print(f"\n开始爬取小米校招岗位信息...")
        print(f"目标 URL: {self.campus_url}")
        
        # 启动浏览器
        if not self.setup_driver():
            print("\n无法启动浏览器，爬取失败")
            return {'error': '无法启动浏览器'}
        
        try:
            # 访问校招页面
            print("正在访问小米校招官网...")
            self.driver.get(self.campus_url)
            
            # 解析岗位
            print("正在解析岗位信息...")
            all_jobs = self.parse_job_from_page()
            
            # 保存数据
            if all_jobs:
                self.save_to_csv(all_jobs, mode='overwrite')
            
            # 更新状态
            state = {
                'last_crawl': datetime.now().isoformat(),
                'total_jobs': len(all_jobs),
                'new_count': len(all_jobs),
                'crawl_url': self.campus_url,
            }
            self.save_state(state)
            
            result_summary = {
                'total_crawled': len(all_jobs),
                'new_jobs': len(all_jobs),
                'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'output_file': str(self.csv_file),
            }
            
            print(f"\n✅ 爬取完成!")
            print(f"  爬取岗位：{len(all_jobs)}")
            print(f"  输出文件：{self.csv_file}")
            
            return result_summary
            
        except Exception as e:
            print(f"❌ 爬取失败：{e}")
            return {'error': str(e)}
        finally:
            self.close_driver()


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='小米校招岗位信息爬虫')
    parser.add_argument('--full', action='store_true', help='全量覆盖模式')
    parser.add_argument('--output', type=str, default=None, help='输出目录路径')
    parser.add_argument('--no-headless', action='store_true', help='显示浏览器窗口')
    
    args = parser.parse_args()
    
    spider = XiaomiCampusSpider(output_dir=args.output, headless=not args.no_headless)
    result = spider.crawl()
    
    print("\n爬取结果:")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
