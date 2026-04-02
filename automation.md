---
description: 자동화 및 스크립팅. "자동화", "스크립트", "배치", "크론", "봇", "매크로" 트리거.
---

# 자동화 및 스크립팅

## Python 자동화

### 파일 시스템 자동화
```python
import os
import shutil
from pathlib import Path
from datetime import datetime

def organize_downloads(download_path: str):
    """다운로드 폴더 자동 정리"""
    categories = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'],
        'Documents': ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt'],
        'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv'],
        'Audio': ['.mp3', '.wav', '.flac', '.aac'],
        'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
        'Code': ['.py', '.js', '.ts', '.html', '.css', '.json'],
    }

    download_dir = Path(download_path)

    for file in download_dir.iterdir():
        if file.is_file():
            ext = file.suffix.lower()
            moved = False

            for category, extensions in categories.items():
                if ext in extensions:
                    category_dir = download_dir / category
                    category_dir.mkdir(exist_ok=True)
                    shutil.move(str(file), str(category_dir / file.name))
                    print(f"Moved {file.name} to {category}")
                    moved = True
                    break

            if not moved:
                other_dir = download_dir / 'Others'
                other_dir.mkdir(exist_ok=True)
                shutil.move(str(file), str(other_dir / file.name))

# 사용
organize_downloads('C:/Users/username/Downloads')
```

### 웹 스크래핑 자동화
```python
import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

def scrape_data(urls: list[str], delay: float = 1.0) -> pd.DataFrame:
    """여러 페이지 스크래핑"""
    results = []

    for url in urls:
        try:
            response = requests.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            soup = BeautifulSoup(response.text, 'html.parser')

            # 데이터 추출 (예시)
            items = soup.select('.item')
            for item in items:
                results.append({
                    'title': item.select_one('.title').text.strip(),
                    'price': item.select_one('.price').text.strip(),
                    'url': url
                })

            sleep(delay)  # 서버 부하 방지
        except Exception as e:
            print(f"Error scraping {url}: {e}")

    return pd.DataFrame(results)
```

### 이메일 자동화
```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send_email(
    to: str,
    subject: str,
    body: str,
    attachments: list[str] = None,
    smtp_server: str = 'smtp.gmail.com',
    smtp_port: int = 587,
    username: str = '',
    password: str = ''
):
    """이메일 발송"""
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = to
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))

    # 첨부파일
    if attachments:
        for file_path in attachments:
            with open(file_path, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(file_path)}')
                msg.attach(part)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(username, password)
        server.send_message(msg)

    print(f"Email sent to {to}")
```

### 스케줄링
```python
import schedule
import time
from datetime import datetime

def job_daily_report():
    """일일 리포트 생성"""
    print(f"[{datetime.now()}] Daily report generated")

def job_backup():
    """백업 실행"""
    print(f"[{datetime.now()}] Backup completed")

def job_cleanup():
    """정리 작업"""
    print(f"[{datetime.now()}] Cleanup completed")

# 스케줄 설정
schedule.every().day.at("09:00").do(job_daily_report)
schedule.every().day.at("02:00").do(job_backup)
schedule.every().sunday.at("03:00").do(job_cleanup)
schedule.every(30).minutes.do(lambda: print("Health check"))

# 실행 루프
while True:
    schedule.run_pending()
    time.sleep(60)
```

## Node.js 자동화

### 파일 감시 자동화
```typescript
import chokidar from 'chokidar';
import { exec } from 'child_process';
import path from 'path';

// 파일 변경 감시
const watcher = chokidar.watch('./src/**/*.ts', {
  persistent: true,
  ignoreInitial: true
});

watcher
  .on('change', (filePath) => {
    console.log(`File changed: ${filePath}`);
    exec('npm run build', (error, stdout) => {
      if (error) console.error(error);
      else console.log('Build completed');
    });
  })
  .on('add', (filePath) => {
    console.log(`File added: ${filePath}`);
  })
  .on('unlink', (filePath) => {
    console.log(`File removed: ${filePath}`);
  });

console.log('Watching for file changes...');
```

### Discord 봇
```typescript
import { Client, GatewayIntentBits, Events } from 'discord.js';

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
  ]
});

client.once(Events.ClientReady, (c) => {
  console.log(`Logged in as ${c.user.tag}`);
});

client.on(Events.MessageCreate, async (message) => {
  if (message.author.bot) return;

  if (message.content === '!ping') {
    await message.reply('Pong!');
  }

  if (message.content.startsWith('!echo ')) {
    const text = message.content.slice(6);
    await message.reply(text);
  }
});

client.login(process.env.DISCORD_TOKEN);
```

### Slack 봇
```typescript
import { App } from '@slack/bolt';

const app = new App({
  token: process.env.SLACK_BOT_TOKEN,
  signingSecret: process.env.SLACK_SIGNING_SECRET,
  socketMode: true,
  appToken: process.env.SLACK_APP_TOKEN,
});

// 메시지 응답
app.message('hello', async ({ message, say }) => {
  await say(`Hey there <@${message.user}>!`);
});

// 슬래시 커맨드
app.command('/status', async ({ command, ack, respond }) => {
  await ack();
  await respond({
    text: `Status: All systems operational`,
  });
});

(async () => {
  await app.start();
  console.log('Slack bot is running!');
})();
```

## 시스템 자동화

### Bash 스크립트
```bash
#!/bin/bash

# 백업 스크립트
BACKUP_DIR="/backup"
SOURCE_DIR="/data"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/backup_$DATE.tar.gz"

# 백업 생성
tar -czf "$BACKUP_FILE" "$SOURCE_DIR"

# 7일 이상 된 백업 삭제
find "$BACKUP_DIR" -name "backup_*.tar.gz" -mtime +7 -delete

echo "Backup completed: $BACKUP_FILE"
```

### PowerShell 스크립트
```powershell
# 시스템 정리 스크립트
param(
    [switch]$DryRun = $false
)

$TempFolders = @(
    "$env:TEMP",
    "$env:LOCALAPPDATA\Temp",
    "C:\Windows\Temp"
)

$TotalSize = 0

foreach ($folder in $TempFolders) {
    if (Test-Path $folder) {
        $files = Get-ChildItem -Path $folder -Recurse -File -ErrorAction SilentlyContinue
        $size = ($files | Measure-Object -Property Length -Sum).Sum / 1MB

        Write-Host "Found $($files.Count) files ($([math]::Round($size, 2)) MB) in $folder"
        $TotalSize += $size

        if (-not $DryRun) {
            Remove-Item -Path "$folder\*" -Recurse -Force -ErrorAction SilentlyContinue
            Write-Host "Cleaned $folder"
        }
    }
}

Write-Host "Total: $([math]::Round($TotalSize, 2)) MB"
```

### Cron 설정
```bash
# crontab -e

# 매일 오전 2시 백업
0 2 * * * /scripts/backup.sh >> /var/log/backup.log 2>&1

# 매시간 헬스체크
0 * * * * curl -s https://api.example.com/health || /scripts/alert.sh

# 매주 일요일 정리
0 3 * * 0 /scripts/cleanup.sh

# 매월 1일 리포트
0 9 1 * * python3 /scripts/monthly_report.py
```

## 모니터링 자동화
```python
import psutil
import requests
from datetime import datetime

def monitor_system():
    """시스템 모니터링"""
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    alert = False
    message = []

    if cpu > 90:
        message.append(f"CPU: {cpu}%")
        alert = True
    if memory > 90:
        message.append(f"Memory: {memory}%")
        alert = True
    if disk > 90:
        message.append(f"Disk: {disk}%")
        alert = True

    if alert:
        send_alert(", ".join(message))

def send_alert(message: str):
    """Slack으로 알림 전송"""
    requests.post(
        'https://hooks.slack.com/services/xxx/xxx/xxx',
        json={'text': f'⚠️ Alert: {message}'}
    )
```

$ARGUMENTS
