# Automation Skill

> 자동화 전문가 - 워크플로우 자동화, 스크립팅, RPA

## Triggers
- "자동화", "automation", "자동으로"
- "스크립트", "배치", "크론"
- "RPA", "봇", "자동 실행"
- "스케줄", "예약", "정기적으로"

## Capabilities

### 1. Python 자동화

#### 파일 관리 자동화
```python
import os
import shutil
from pathlib import Path
from datetime import datetime

class FileOrganizer:
    def __init__(self, source_dir: str):
        self.source = Path(source_dir)

    def organize_by_extension(self):
        """확장자별로 파일 정리"""
        for file in self.source.iterdir():
            if file.is_file():
                ext = file.suffix.lower()[1:]  # .txt -> txt
                if ext:
                    target_dir = self.source / ext
                    target_dir.mkdir(exist_ok=True)
                    shutil.move(str(file), str(target_dir / file.name))

    def organize_by_date(self):
        """날짜별로 파일 정리"""
        for file in self.source.iterdir():
            if file.is_file():
                mtime = datetime.fromtimestamp(file.stat().st_mtime)
                target_dir = self.source / mtime.strftime("%Y-%m")
                target_dir.mkdir(exist_ok=True)
                shutil.move(str(file), str(target_dir / file.name))

    def find_duplicates(self):
        """중복 파일 찾기"""
        import hashlib

        hashes = {}
        duplicates = []

        for file in self.source.rglob("*"):
            if file.is_file():
                file_hash = hashlib.md5(file.read_bytes()).hexdigest()
                if file_hash in hashes:
                    duplicates.append((file, hashes[file_hash]))
                else:
                    hashes[file_hash] = file

        return duplicates
```

#### 웹 스크래핑 자동화
```python
import requests
from bs4 import BeautifulSoup
import pandas as pd

class WebScraper:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def scrape_page(self, url: str) -> BeautifulSoup:
        response = self.session.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')

    def extract_data(self, soup: BeautifulSoup, selectors: dict) -> dict:
        """CSS 셀렉터로 데이터 추출"""
        data = {}
        for key, selector in selectors.items():
            element = soup.select_one(selector)
            data[key] = element.text.strip() if element else None
        return data

    def scrape_multiple(self, urls: list, selectors: dict) -> pd.DataFrame:
        """여러 페이지 스크래핑"""
        results = []
        for url in urls:
            soup = self.scrape_page(url)
            data = self.extract_data(soup, selectors)
            results.append(data)
        return pd.DataFrame(results)
```

### 2. 스케줄링

#### Python Schedule
```python
import schedule
import time

def job():
    print("Running scheduled job...")

# 매일 오전 10시
schedule.every().day.at("10:00").do(job)

# 매주 월요일
schedule.every().monday.do(job)

# 매 시간
schedule.every().hour.do(job)

# 5분마다
schedule.every(5).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
```

#### Cron (Linux/Mac)
```bash
# crontab -e

# 분 시 일 월 요일 명령
# 매일 오전 9시
0 9 * * * /usr/bin/python3 /path/to/script.py

# 매주 월요일 오전 8시
0 8 * * 1 /path/to/backup.sh

# 매시간
0 * * * * /path/to/hourly-task.sh

# 5분마다
*/5 * * * * /path/to/check.sh
```

#### Windows Task Scheduler (PowerShell)
```powershell
# 매일 오전 9시 실행
$action = New-ScheduledTaskAction -Execute "python.exe" -Argument "C:\scripts\task.py"
$trigger = New-ScheduledTaskTrigger -Daily -At 9am
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "DailyTask"
```

### 3. 이메일 자동화

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

class EmailAutomation:
    def __init__(self, smtp_server: str, port: int, username: str, password: str):
        self.smtp_server = smtp_server
        self.port = port
        self.username = username
        self.password = password

    def send_email(self, to: list, subject: str, body: str,
                   attachments: list = None, html: bool = False):
        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = ', '.join(to)
        msg['Subject'] = subject

        # 본문
        content_type = 'html' if html else 'plain'
        msg.attach(MIMEText(body, content_type))

        # 첨부파일
        if attachments:
            for file_path in attachments:
                with open(file_path, 'rb') as f:
                    part = MIMEApplication(f.read())
                    part.add_header('Content-Disposition', 'attachment',
                                  filename=os.path.basename(file_path))
                    msg.attach(part)

        # 전송
        with smtplib.SMTP(self.smtp_server, self.port) as server:
            server.starttls()
            server.login(self.username, self.password)
            server.send_message(msg)

# 사용 예시
email = EmailAutomation('smtp.gmail.com', 587, 'your@email.com', 'app_password')
email.send_email(
    to=['recipient@email.com'],
    subject='자동 보고서',
    body='<h1>일일 보고서</h1><p>첨부 파일을 확인하세요.</p>',
    attachments=['report.pdf'],
    html=True
)
```

### 4. 브라우저 자동화 (Playwright)

```python
from playwright.sync_api import sync_playwright

class BrowserAutomation:
    def __init__(self, headless: bool = True):
        self.headless = headless

    def run(self, task):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            page = browser.new_page()
            result = task(page)
            browser.close()
            return result

# 예시: 로그인 자동화
def login_task(page):
    page.goto('https://example.com/login')
    page.fill('#username', 'myuser')
    page.fill('#password', 'mypass')
    page.click('button[type="submit"]')
    page.wait_for_url('**/dashboard')
    return page.content()

# 예시: 스크린샷 자동화
def screenshot_task(page):
    page.goto('https://example.com')
    page.screenshot(path='screenshot.png', full_page=True)

automation = BrowserAutomation(headless=False)
automation.run(login_task)
```

### 5. API 자동화

```python
import requests
from typing import Any

class APIAutomation:
    def __init__(self, base_url: str, api_key: str = None):
        self.base_url = base_url
        self.session = requests.Session()
        if api_key:
            self.session.headers['Authorization'] = f'Bearer {api_key}'

    def get(self, endpoint: str, params: dict = None) -> Any:
        response = self.session.get(f"{self.base_url}{endpoint}", params=params)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint: str, data: dict = None) -> Any:
        response = self.session.post(f"{self.base_url}{endpoint}", json=data)
        response.raise_for_status()
        return response.json()

    def batch_request(self, requests_list: list) -> list:
        """여러 요청을 동시에 처리"""
        import concurrent.futures

        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for req in requests_list:
                method = req.get('method', 'GET')
                if method == 'GET':
                    future = executor.submit(self.get, req['endpoint'], req.get('params'))
                else:
                    future = executor.submit(self.post, req['endpoint'], req.get('data'))
                futures.append(future)

            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())

        return results
```

### 6. 워크플로우 자동화 (n8n 스타일)

```python
from abc import ABC, abstractmethod
from typing import Any

class Node(ABC):
    @abstractmethod
    def execute(self, input_data: Any) -> Any:
        pass

class Workflow:
    def __init__(self):
        self.nodes = []

    def add_node(self, node: Node):
        self.nodes.append(node)
        return self

    def run(self, initial_data: Any = None):
        data = initial_data
        for node in self.nodes:
            data = node.execute(data)
        return data

# 노드 예시
class FetchDataNode(Node):
    def __init__(self, url: str):
        self.url = url

    def execute(self, input_data):
        response = requests.get(self.url)
        return response.json()

class FilterNode(Node):
    def __init__(self, condition):
        self.condition = condition

    def execute(self, input_data):
        return [item for item in input_data if self.condition(item)]

class TransformNode(Node):
    def __init__(self, transform_fn):
        self.transform_fn = transform_fn

    def execute(self, input_data):
        return [self.transform_fn(item) for item in input_data]

class SaveNode(Node):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def execute(self, input_data):
        import json
        with open(self.file_path, 'w') as f:
            json.dump(input_data, f)
        return input_data

# 워크플로우 실행
workflow = (
    Workflow()
    .add_node(FetchDataNode('https://api.example.com/data'))
    .add_node(FilterNode(lambda x: x['active']))
    .add_node(TransformNode(lambda x: {'name': x['name'], 'email': x['email']}))
    .add_node(SaveNode('output.json'))
)

result = workflow.run()
```

### 7. 명령어 모음

```bash
# 파일 감시 (watchdog)
pip install watchdog
watchmedo shell-command --patterns="*.py" --command='python $watch_src_path'

# 백그라운드 실행
nohup python script.py &

# 로그 관리
python script.py >> output.log 2>&1
```
