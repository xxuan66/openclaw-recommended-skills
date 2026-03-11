#!/usr/bin/env python3
"""
小米招聘官网校招岗位信息爬虫（Selenium 版本）
适用于 SPA 单页应用，通过浏览器自动化爬取

依赖：pip install selenium webdriver-manager
"""

import csv
import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict
import time

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("警告：Selenium 未安装，请运行：pip install selenium webdriver-manager")


class XiaomiCampusSpiderSelenium:
    """小米校招岗位信息爬虫（Selenium 版本）"""
    
    def __init__(self, output_dir: str = None, headless: bool = True):
        """
        初始化爬虫
        
        Args:
            output_dir: 输出目录
            headless: 是否无头模式
        """
        if not SELENIUM_AVAILABLE:
            raise ImportError("Selenium 未安装")
        
        # 设置输出目录
        if output_dir is None:
            self.output_dir = Path(__file__).parent.parent / 'data'
        else:
            self.output_dir = Path(output_dir)
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 数据文件路径
        self.csv_file = self.output_dir / 'xiaomi_campus_jobs.csv'
        self.state_file = self.output_dir / '.crawler_state.json'
        
        # 浏览器配置
        self.headless = headless
        self.base_url = 'https://hr.xiaomi.com/'
        self.driver = None
    
    def setup_driver(self):
        """配置 Chrome 驱动"""
        try:
            from webdriver_manager.chrome import ChromeDriverManager
        except ImportError:
            print("请安装：pip install webdriver-manager")
            return False
        
        options = Options()
        if self.headless:
            options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            return True
        except Exception as e:
            print(f"启动浏览器失败：{e}")
            return False
    
    def parse_job_element(self, element) -> Dict:
        """解析岗位元素"""
        try:
            job_data = {
                'job_id': element.get_attribute('data-job-id') or '',
                'job_name': '',
                'department': '',
                'work_city': '',
                'education': '',
                'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }
            
            # 尝试获取岗位名称
            try:
                title_elem = element.find_element(By.CSS_SELECTOR, '.job-name, h3, .title')
                job_data['job_name'] = title_elem.text.strip()
            except:
                pass
            
            # 尝试获取部门
            try:
                dept_elem = element.find_element(By.CSS_SELECTOR, '.department, .dept')
                job_data['department'] = dept_elem.text.strip()
            except:
                pass
            
            # 尝试获取城市
            try:
                city_elem = element.find_element(By.CSS_SELECTOR, '.city, .location, .work-city')
                job_data['work_city'] = city_elem.text.strip()
            except:
                pass
            
            # 尝试获取学历要求
            try:
                edu_elem = element.find_element(By.CSS_SELECTOR, '.education, .edu, .degree')
                job_data['education'] = edu_elem.text.strip()
            except:
                pass
            
            # 生成岗位 URL
            if job_data['job_id']:
                job_data['job_url'] = f"{self.base_url}job/{job_data['job_id']}"
            
            return job_data
        except Exception as e:
            print(f"解析岗位元素失败：{e}")
            return {}
    
    def load_existing_data(self) -> Dict[str, Dict]:
        """加载已有的岗位数据"""
        existing_jobs = {}
        if self.csv_file.exists():
            with open(self.csv_file, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    job_id = row.get('job_id', '')
                    if job_id:
                        existing_jobs[job_id] = row
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
        print(f"开始爬取小米校招岗位信息（Selenium 版本）...")
        print(f"模式：{'增量更新' if update else '全量覆盖'}")
        
        if not self.setup_driver():
            return {'error': '无法启动浏览器'}
        
        try:
            # 加载已有数据
            existing_jobs = self.load_existing_data() if update else {}
            
            # 访问招聘网站
            print("正在访问小米招聘官网...")
            self.driver.get(self.base_url)
            
            # 等待页面加载
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # 等待岗位列表加载（可能需要点击校招 tab）
            time.sleep(5)
            
            # 尝试点击校招标签
            try:
                campus_tab = self.driver.find_element(By.XPATH, "//span[contains(text(), '校招')] | //a[contains(text(), '校招')]")
                campus_tab.click()
                time.sleep(3)
            except:
                print("未找到校招标签，可能在社会招聘页面")
            
            # 查找岗位列表
            all_jobs = []
            new_count = 0
            
            # 尝试多种选择器
            selectors = [
                '.job-item', '.position-item', '.job-list-item',
                '[data-job-id]', '.jobs-item', '.recruit-item'
            ]
            
            job_elements = []
            for selector in selectors:
                try:
                    job_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if job_elements:
                        print(f"找到 {len(job_elements)} 个岗位元素（选择器：{selector}）")
                        break
                except:
                    continue
            
            if not job_elements:
                # 尝试 XPath
                try:
                    job_elements = self.driver.find_elements(By.XPATH, "//*[contains(@class, 'job') or contains(@class, 'position')]")
                    print(f"找到 {len(job_elements)} 个岗位元素（XPath）")
                except:
                    pass
            
            # 解析岗位
            for element in job_elements:
                job = self.parse_job_element(element)
                if job and job.get('job_id'):
                    job_id = job['job_id']
                    if job_id not in existing_jobs:
                        new_count += 1
                        all_jobs.append(job)
            
            # 保存数据
            if all_jobs:
                self.save_to_csv(all_jobs, mode='overwrite' if not update else 'append')
            
            # 更新状态
            state = {'last_crawl': datetime.now().isoformat(), 'total_jobs': len(existing_jobs) + new_count, 'new_count': new_count}
            self.save_state(state)
            
            result_summary = {
                'total_crawled': len(all_jobs),
                'new_jobs': new_count,
                'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'output_file': str(self.csv_file),
            }
            
            print(f"\n爬取完成!")
            print(f"  新增岗位：{new_count}")
            print(f"  输出文件：{self.csv_file}")
            
            return result_summary
            
        finally:
            if self.driver:
                self.driver.quit()


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='小米校招岗位信息爬虫（Selenium）')
    parser.add_argument('--update', action='store_true', default=True, help='增量更新')
    parser.add_argument('--full', action='store_true', help='全量覆盖')
    parser.add_argument('--output', type=str, default=None, help='输出目录')
    parser.add_argument('--no-headless', action='store_true', help='显示浏览器窗口')
    
    args = parser.parse_args()
    
    if not SELENIUM_AVAILABLE:
        print("错误：Selenium 未安装")
        print("请运行：pip install selenium webdriver-manager")
        return
    
    spider = XiaomiCampusSpiderSelenium(output_dir=args.output, headless=not args.no_headless)
    result = spider.crawl(update=not args.full)
    
    print("\n爬取结果:")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
