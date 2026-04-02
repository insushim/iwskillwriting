---
description: 유튜브 자동화 및 콘텐츠 제작. "유튜브", "YouTube", "영상", "동영상", "썸네일", "자막" 트리거.
---

# YouTube 자동화 및 콘텐츠 제작

## 자동화 도구

### 영상 다운로드/처리
```bash
# yt-dlp 설치
pip install yt-dlp

# 영상 다운로드
yt-dlp "https://youtube.com/watch?v=VIDEO_ID"

# 오디오만 추출
yt-dlp -x --audio-format mp3 "URL"

# 자막 다운로드
yt-dlp --write-auto-sub --sub-lang ko "URL"
```

### 썸네일 자동 생성 (Python + Pillow)
```python
from PIL import Image, ImageDraw, ImageFont
import os

def create_thumbnail(
    background_path: str,
    title: str,
    output_path: str,
    size: tuple = (1280, 720)
):
    """YouTube 썸네일 생성 (1280x720)"""

    # 배경 이미지 로드 및 리사이즈
    img = Image.open(background_path)
    img = img.resize(size, Image.Resampling.LANCZOS)

    draw = ImageDraw.Draw(img)

    # 반투명 오버레이
    overlay = Image.new('RGBA', size, (0, 0, 0, 128))
    img = Image.alpha_composite(img.convert('RGBA'), overlay)
    draw = ImageDraw.Draw(img)

    # 텍스트 추가
    try:
        font = ImageFont.truetype("NanumGothicBold.ttf", 80)
    except:
        font = ImageFont.load_default()

    # 텍스트 중앙 배치
    bbox = draw.textbbox((0, 0), title, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2

    # 그림자 효과
    draw.text((x+3, y+3), title, font=font, fill=(0, 0, 0, 200))
    draw.text((x, y), title, font=font, fill=(255, 255, 255, 255))

    img.convert('RGB').save(output_path, quality=95)
    print(f"Thumbnail saved: {output_path}")

# 사용
create_thumbnail(
    "background.jpg",
    "충격적인 결과!",
    "thumbnail.jpg"
)
```

### 자막 생성 (Whisper AI)
```python
import whisper

def generate_subtitles(video_path: str, output_path: str):
    """Whisper로 자막 자동 생성"""
    model = whisper.load_model("medium")
    result = model.transcribe(video_path, language="ko")

    # SRT 형식으로 저장
    with open(output_path, 'w', encoding='utf-8') as f:
        for i, segment in enumerate(result['segments'], 1):
            start = format_timestamp(segment['start'])
            end = format_timestamp(segment['end'])
            text = segment['text'].strip()
            f.write(f"{i}\n{start} --> {end}\n{text}\n\n")

    print(f"Subtitles saved: {output_path}")

def format_timestamp(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
```

### YouTube API 업로드
```python
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_video(
    video_path: str,
    title: str,
    description: str,
    tags: list,
    credentials_path: str = "credentials.json"
):
    """YouTube에 영상 업로드"""

    credentials = Credentials.from_authorized_user_file(credentials_path)
    youtube = build('youtube', 'v3', credentials=credentials)

    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': '22'  # People & Blogs
        },
        'status': {
            'privacyStatus': 'private',  # private, public, unlisted
            'selfDeclaredMadeForKids': False
        }
    }

    media = MediaFileUpload(
        video_path,
        mimetype='video/*',
        resumable=True
    )

    request = youtube.videos().insert(
        part='snippet,status',
        body=body,
        media_body=media
    )

    response = request.execute()
    print(f"Video uploaded: https://youtube.com/watch?v={response['id']}")
    return response
```

### 영상 편집 자동화 (MoviePy)
```python
from moviepy.editor import *

def create_video_from_images(
    image_paths: list,
    audio_path: str,
    output_path: str,
    duration_per_image: float = 5.0
):
    """이미지들로 영상 생성"""

    clips = []
    for img_path in image_paths:
        clip = ImageClip(img_path).set_duration(duration_per_image)
        clips.append(clip)

    video = concatenate_videoclips(clips, method="compose")

    if audio_path:
        audio = AudioFileClip(audio_path)
        video = video.set_audio(audio)

    video.write_videofile(
        output_path,
        fps=24,
        codec='libx264',
        audio_codec='aac'
    )

def add_intro_outro(
    main_video: str,
    intro_video: str,
    outro_video: str,
    output_path: str
):
    """인트로/아웃트로 추가"""

    intro = VideoFileClip(intro_video)
    main = VideoFileClip(main_video)
    outro = VideoFileClip(outro_video)

    final = concatenate_videoclips([intro, main, outro])
    final.write_videofile(output_path)

def add_text_overlay(
    video_path: str,
    text: str,
    output_path: str,
    position: str = 'bottom'
):
    """텍스트 오버레이 추가"""

    video = VideoFileClip(video_path)

    txt_clip = TextClip(
        text,
        fontsize=50,
        color='white',
        font='NanumGothic-Bold',
        stroke_color='black',
        stroke_width=2
    ).set_position(position).set_duration(video.duration)

    final = CompositeVideoClip([video, txt_clip])
    final.write_videofile(output_path)
```

### 콘텐츠 스케줄링
```python
import schedule
import time
from datetime import datetime

def scheduled_upload():
    """예약 업로드"""
    upload_video(
        "video.mp4",
        f"Daily Video - {datetime.now().strftime('%Y-%m-%d')}",
        "자동 업로드된 영상입니다.",
        ["daily", "auto"]
    )

# 매일 오후 6시 업로드
schedule.every().day.at("18:00").do(scheduled_upload)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## 필수 패키지
```bash
pip install yt-dlp whisper moviepy pillow google-api-python-client schedule
```

$ARGUMENTS
