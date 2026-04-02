# YouTube Automation Skill

> 유튜브 영상 자동 생성 - 스크립트, 썸네일, 편집, 업로드 자동화

## Triggers
- "유튜브", "YouTube", "영상 만들어", "동영상"
- "자동 영상", "영상 자동화", "콘텐츠 자동화"
- "썸네일", "자막", "편집"

## Capabilities

### 1. 영상 스크립트 생성
```yaml
script_types:
  - 교육/튜토리얼
  - 뉴스/정보
  - 엔터테인먼트
  - 리뷰/언박싱
  - 브이로그
  - Shorts/릴스

structure:
  hook: 0-10초 (시선 끌기)
  intro: 10-30초 (주제 소개)
  content: 본문 (가치 전달)
  cta: 마무리 (구독/좋아요)
```

### 2. 스크립트 템플릿
```markdown
# [제목]

## Hook (0:00-0:10)
[충격적인 사실/질문/문제 제기]
"여러분, [주제]에 대해 알고 계셨나요?"

## Intro (0:10-0:30)
[채널 소개 + 영상 개요]
"안녕하세요, [채널명]입니다. 오늘은 [주제]에 대해 알아보겠습니다."

## Content Section 1 (0:30-3:00)
[첫 번째 핵심 포인트]
- 설명
- 예시
- 시각 자료 설명

## Content Section 2 (3:00-5:30)
[두 번째 핵심 포인트]

## Content Section 3 (5:30-8:00)
[세 번째 핵심 포인트]

## Conclusion (8:00-8:30)
[요약 + CTA]
"오늘 영상이 도움이 되셨다면 좋아요와 구독 부탁드립니다!"

---
예상 길이: 8분 30초
타겟 키워드: [키워드1], [키워드2]
```

### 3. 썸네일 설계
```yaml
design_principles:
  - 얼굴 클로즈업 (감정 표현)
  - 대비되는 색상 (노랑/빨강)
  - 큰 텍스트 (3-5단어)
  - 화살표/원형 강조
  - 1280x720 해상도

text_formulas:
  - "이것만 알면 끝!"
  - "[숫자]가지 방법"
  - "절대 하지 마세요"
  - "[충격] 실화입니다"
```

### 4. 영상 편집 자동화 (Python + MoviePy)
```python
from moviepy.editor import *
from gtts import gTTS
import os

class VideoGenerator:
    def __init__(self, script, images, output_path):
        self.script = script
        self.images = images
        self.output_path = output_path

    def generate_voiceover(self, text, lang='ko'):
        """TTS로 나레이션 생성"""
        tts = gTTS(text=text, lang=lang)
        audio_path = "temp_audio.mp3"
        tts.save(audio_path)
        return AudioFileClip(audio_path)

    def create_video(self):
        """이미지 + 오디오로 영상 생성"""
        clips = []

        for i, (text, image_path) in enumerate(zip(self.script, self.images)):
            # 나레이션 생성
            audio = self.generate_voiceover(text)
            duration = audio.duration

            # 이미지 클립 생성
            img_clip = ImageClip(image_path).set_duration(duration)
            img_clip = img_clip.set_audio(audio)

            # 자막 추가
            txt_clip = TextClip(text, fontsize=40, color='white',
                               font='Malgun-Gothic', size=(1080, None))
            txt_clip = txt_clip.set_position(('center', 'bottom'))
            txt_clip = txt_clip.set_duration(duration)

            # 합성
            video = CompositeVideoClip([img_clip, txt_clip])
            clips.append(video)

        # 모든 클립 연결
        final = concatenate_videoclips(clips, method="compose")
        final.write_videofile(self.output_path, fps=24)

        return self.output_path
```

### 5. YouTube API 업로드
```python
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow

class YouTubeUploader:
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

    def __init__(self, credentials_path):
        self.credentials_path = credentials_path
        self.youtube = self._authenticate()

    def _authenticate(self):
        flow = InstalledAppFlow.from_client_secrets_file(
            self.credentials_path, self.SCOPES)
        credentials = flow.run_local_server(port=8080)
        return build('youtube', 'v3', credentials=credentials)

    def upload(self, video_path, title, description, tags, category_id='22'):
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': category_id
            },
            'status': {
                'privacyStatus': 'private',  # 먼저 비공개로 업로드
                'selfDeclaredMadeForKids': False
            }
        }

        media = MediaFileUpload(video_path,
                               mimetype='video/*',
                               resumable=True)

        request = self.youtube.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=media
        )

        response = request.execute()
        return f"https://youtube.com/watch?v={response['id']}"
```

### 6. Shorts 자동화
```python
class ShortsGenerator:
    """세로 영상 (9:16) 자동 생성"""

    def create_short(self, text, background_video, duration=30):
        # 배경 영상 로드 (9:16 비율)
        bg = VideoFileClip(background_video)
        bg = bg.resize(height=1920)
        bg = bg.crop(x_center=bg.w/2, width=1080)
        bg = bg.subclip(0, duration)

        # 자막 스타일
        txt = TextClip(text,
                      fontsize=60,
                      color='white',
                      stroke_color='black',
                      stroke_width=2,
                      font='Malgun-Gothic-Bold',
                      size=(900, None),
                      method='caption')
        txt = txt.set_position('center').set_duration(duration)

        # 합성
        final = CompositeVideoClip([bg, txt])
        return final
```

## SEO 최적화

### 제목 공식
```
[숫자] + [키워드] + [이익/호기심]
예: "5분만에 배우는 Python | 코딩 입문자 필수"
```

### 설명 템플릿
```
[첫 줄: 핵심 키워드 포함]

📌 타임스탬프
0:00 인트로
1:00 첫 번째 포인트
...

🔗 관련 링크
- 블로그:
- 인스타:

#키워드1 #키워드2 #키워드3
```

### 태그 전략
```yaml
primary: 주요 키워드 (3-5개)
secondary: 관련 키워드 (5-10개)
long_tail: 롱테일 키워드 (5-10개)
branded: 채널명, 시리즈명
```

## 자동화 파이프라인
```
1. 주제 선정 (트렌드 분석)
   ↓
2. 스크립트 생성 (AI)
   ↓
3. 이미지/영상 소스 수집
   ↓
4. 나레이션 생성 (TTS)
   ↓
5. 영상 편집 (MoviePy)
   ↓
6. 썸네일 생성
   ↓
7. 메타데이터 최적화
   ↓
8. 업로드 (예약)
```
