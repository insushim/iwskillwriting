# Publishing Formats Reference

출판 포맷 변환 가이드. DOCX, EPUB, PDF 표준 사양.

---

## 1. DOCX (Microsoft Word)

### 표준 원고 포맷 (한국어)

```
페이지 설정:
- 용지: A4 (210mm × 297mm)
- 여백: 상 30mm, 하 25mm, 좌 30mm, 우 25mm
- 머리글/바닥글: 15mm

본문:
- 폰트: 나눔명조 또는 바탕체
- 크기: 11pt
- 줄간격: 1.6 (160%)
- 단락 간격: 앞 0pt, 뒤 6pt
- 들여쓰기: 첫 줄 10mm
- 정렬: 양쪽 정렬

제목:
- 챕터 제목: 나눔고딕 Bold 16pt, 가운데 정렬
- 챕터 부제: 나눔고딕 12pt, 가운데 정렬
- 새 챕터는 새 페이지에서 시작

페이지 번호:
- 바닥글 가운데
- 첫 페이지 제외
- 아라비아 숫자

머리글:
- 짝수 페이지: 책 제목
- 홀수 페이지: 챕터 제목
```

### python-docx 설정 코드

```python
from docx import Document
from docx.shared import Pt, Mm, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_ORIENT

def create_manuscript_doc():
    doc = Document()

    # 페이지 설정
    section = doc.sections[0]
    section.page_height = Mm(297)
    section.page_width = Mm(210)
    section.top_margin = Mm(30)
    section.bottom_margin = Mm(25)
    section.left_margin = Mm(30)
    section.right_margin = Mm(25)

    # 기본 스타일
    style = doc.styles['Normal']
    font = style.font
    font.name = '바탕체'
    font.size = Pt(11)

    paragraph_format = style.paragraph_format
    paragraph_format.line_spacing = 1.6
    paragraph_format.first_line_indent = Mm(10)
    paragraph_format.space_after = Pt(6)

    return doc
```

### 원고 구조

```
표지 페이지
├── 제목 (중앙, 큰 글씨)
├── 부제 (있는 경우)
├── 저자명
└── 날짜

(빈 페이지)

목차
├── Part/부 제목
├── 챕터 번호 + 제목
└── 페이지 번호

(빈 페이지)

본문
├── Chapter 1
│   ├── 챕터 제목
│   └── 본문...
├── Chapter 2
│   └── ...
└── ...

후기/에필로그 (선택)
감사의 글 (선택)
참고문헌 (비소설)
```

---

## 2. EPUB (전자책)

### EPUB 3.0 표준 구조

```
book.epub (ZIP 파일)
├── mimetype                    # "application/epub+zip"
├── META-INF/
│   └── container.xml          # OPF 파일 위치
├── OEBPS/
│   ├── content.opf            # 패키지 문서 (메타데이터)
│   ├── toc.ncx                # 목차 (EPUB 2 호환)
│   ├── nav.xhtml              # 목차 (EPUB 3)
│   ├── css/
│   │   └── style.css          # 스타일시트
│   ├── images/                # 이미지 파일
│   │   └── cover.jpg
│   └── text/
│       ├── cover.xhtml        # 표지
│       ├── title.xhtml        # 속표지
│       ├── toc.xhtml          # 목차
│       ├── ch01.xhtml         # 챕터 1
│       ├── ch02.xhtml         # 챕터 2
│       └── ...
```

### 메타데이터 (content.opf)

```xml
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:title>책 제목</dc:title>
    <dc:creator>저자명</dc:creator>
    <dc:language>ko</dc:language>
    <dc:identifier id="bookid">urn:uuid:unique-id</dc:identifier>
    <dc:date>2024-01-01</dc:date>
    <dc:publisher>출판사</dc:publisher>
    <dc:description>책 설명</dc:description>
    <dc:subject>장르/분야</dc:subject>
    <meta property="dcterms:modified">2024-01-01T00:00:00Z</meta>
</metadata>
```

### CSS 스타일 (한국어 전자책)

```css
@charset "UTF-8";

body {
    font-family: "나눔명조", "Nanum Myeongjo", serif;
    font-size: 1em;
    line-height: 1.8;
    margin: 1em;
    text-align: justify;
    word-break: keep-all;
}

h1 {
    font-family: "나눔고딕", "Nanum Gothic", sans-serif;
    font-size: 1.5em;
    text-align: center;
    margin-top: 3em;
    margin-bottom: 2em;
    page-break-before: always;
}

h2 {
    font-family: "나눔고딕", "Nanum Gothic", sans-serif;
    font-size: 1.2em;
    text-align: center;
    margin-top: 2em;
    margin-bottom: 1.5em;
}

p {
    text-indent: 1em;
    margin: 0.3em 0;
}

p.first {
    text-indent: 0;
}

blockquote {
    margin: 1em 2em;
    font-style: italic;
    color: #555;
}

.chapter-number {
    font-size: 0.9em;
    text-align: center;
    color: #888;
    margin-bottom: 0.5em;
}

.scene-break {
    text-align: center;
    margin: 2em 0;
}

.scene-break::after {
    content: "* * *";
}
```

### ebooklib 코드 예시

```python
from ebooklib import epub

def create_epub(title, author, chapters):
    book = epub.EpubBook()

    # 메타데이터
    book.set_identifier('id-' + title.replace(' ', '-'))
    book.set_title(title)
    book.set_language('ko')
    book.add_author(author)

    # CSS
    style = epub.EpubItem(
        uid="style",
        file_name="style/default.css",
        media_type="text/css",
        content=open('style.css').read()
    )
    book.add_item(style)

    # 챕터 생성
    epub_chapters = []
    for i, ch in enumerate(chapters):
        c = epub.EpubHtml(
            title=ch['title'],
            file_name=f'ch{i+1:02d}.xhtml',
            lang='ko'
        )
        c.content = f'<h1>{ch["title"]}</h1>{ch["content"]}'
        c.add_item(style)
        book.add_item(c)
        epub_chapters.append(c)

    # 목차
    book.toc = epub_chapters
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # 스파인
    book.spine = ['nav'] + epub_chapters

    # 저장
    epub.write_epub(f'{title}.epub', book)
```

---

## 3. PDF (인쇄용)

### 인쇄 표준 (한국어 단행본)

```
판형: 신국판 (152mm × 225mm) 또는 A5 (148mm × 210mm)
여백:
  - 천(위): 20mm
  - 지(아래): 25mm
  - 안쪽(제본): 25mm
  - 바깥: 20mm

본문:
- 폰트: 나눔명조 10pt
- 줄간격: 170%
- 들여쓰기: 1em
- 양쪽 정렬 + 하이프네이션
```

### weasyprint 변환 (선택적)

```python
import weasyprint

def markdown_to_pdf(html_content, output_path):
    css = weasyprint.CSS(string='''
        @page {
            size: 152mm 225mm;
            margin: 20mm 20mm 25mm 25mm;
            @bottom-center {
                content: counter(page);
                font-size: 9pt;
            }
        }
        body {
            font-family: "나눔명조", serif;
            font-size: 10pt;
            line-height: 1.7;
            text-align: justify;
        }
    ''')
    html = weasyprint.HTML(string=html_content)
    html.write_pdf(output_path, stylesheets=[css])
```

---

## 4. 마크다운 (중간 포맷)

모든 챕터는 마크다운으로 작성하고, 최종 단계에서 DOCX/EPUB/PDF로 변환합니다.

### 챕터 마크다운 구조

```markdown
---
chapter: 1
title: "챕터 제목"
pov: "주인공 이름"
location: "장소"
timeline: "시간 정보"
wordcount: 0
status: draft
---

# 1장. 챕터 제목

본문 시작...

첫 번째 문단.

두 번째 문단.

---

씬 전환 (씬 브레이크)

---

새로운 씬 시작...

> 인용문이나 편지, 일기 등

"대화문입니다," 캐릭터가 말했다.

"응답 대화문이요."

*이탤릭 강조*

**볼드 강조**

<!-- 작가 노트: 이 부분 나중에 수정 필요 -->
```

### 프론트매터 필드 설명

| 필드 | 설명 | 필수 |
|------|------|------|
| chapter | 챕터 번호 | O |
| title | 챕터 제목 | O |
| pov | 시점 캐릭터 | 소설 |
| location | 주요 장소 | 선택 |
| timeline | 시간 정보 (작품 내) | 선택 |
| wordcount | 글자수 (자동 계산) | 자동 |
| status | draft/review/final | O |

---

## 변환 파이프라인

```
작성 (MD) → 편집 (MD) → 변환
                          ├── DOCX (python-docx)
                          ├── EPUB (ebooklib)
                          └── PDF (weasyprint, 선택)
```

### format_manuscript.py 실행

```bash
# DOCX 변환
python format_manuscript.py --project ~/my-novel --format docx

# EPUB 변환
python format_manuscript.py --project ~/my-novel --format epub

# 모든 포맷
python format_manuscript.py --project ~/my-novel --format all

# PDF (weasyprint 필요)
python format_manuscript.py --project ~/my-novel --format pdf
```

---

## 파일 네이밍 규칙

```
{프로젝트명}/output/
├── {제목}_원고_v{버전}_{날짜}.docx
├── {제목}_v{버전}_{날짜}.epub
├── {제목}_인쇄용_v{버전}_{날짜}.pdf
├── {제목}_오디오스크립트_{날짜}.txt
└── {제목}_투고샘플_{날짜}.md
```

---

## 5. 오디오북 변환 가이드 (2026 최신)

### AI 오디오북 제작 워크플로우

```
원고 (MD) → TTS 최적화 텍스트 → AI 내레이션 → 후처리 → 배포
```

### ElevenLabs Projects (2026)

**핵심 기능:**
- ePub/텍스트 파일 업로드로 챕터별 자동 분할
- Eleven v3 모델: 감정을 담은 "연기" 가능
- 캐릭터별 음성 할당 (대화마다 다른 목소리)
- 전문 음성 복제 (30분+ 오디오로 방송 품질)

**TTS 최적화 규칙:**
1. 대화문에 캐릭터명 태그 삽입 (`[주인공]`, `[히로인]`)
2. 서술과 대화 분리 마킹
3. 발음 가이드 (고유명사, 외래어)
4. 숫자를 한글로 변환 ("300명" → "삼백 명")
5. 약어 풀어쓰기 ("vs" → "대")
6. 감정/톤 지시 삽입 (`<속삭이듯>`, `<분노>`)

### AI TTS 플랫폼 비교 (2026)

| 플랫폼 | 한국어 | 품질 | 가격 | 비고 |
|--------|--------|------|------|------|
| ElevenLabs | O (30개 언어) | 최고 | 프리미엄 | 감정 연기, 음성 복제 |
| Play.ht | O | 높음 | 보통 | 대량 제작 적합 |
| Murf.ai | O (20개 언어) | 높음 | 보통 | 초보자 친화적 |
| Clova Voice | O (한국어 특화) | 높음 | 보통 | 네이버 생태계 |
| Google TTS | O | 보통 | 저렴 | API 기반 |

### 배포 플랫폼 (2026)

| 플랫폼 | AI 내레이션 허용 | 비고 |
|--------|---------------|------|
| Audible | O (Virtual Voice 프로그램) | 2025년부터 허용 |
| Findaway Voices | O (ElevenLabs 수용) | 2025.2월부터 |
| Google Play Books | O | |
| Apple Books | 미확인 | 개별 심사 |
| ACX | X | AI 내레이션 금지 유지 |

---

## 6. 소설→스크린플레이 변환 가이드 (2026 신규)

### 변환 워크플로우

```
소설 (MD) → 장면 추출 → 스크린플레이 포맷 → 산업 표준 출력
```

### 스크린플레이 포맷 규격

```
장면 제목: INT./EXT. 장소 - 시간
액션 라인: 현재 시제, 시각적 묘사만
대화: 캐릭터명 (가운데 정렬)
     (괄호 지시)
     대화 내용
```

### 소설→스크린플레이 변환 규칙
1. **묘사 → 액션 라인**: 내면 묘사 제거, 시각/청각만 유지
2. **내적 독백 → 보이스오버(V.O.)**: 꼭 필요한 경우만
3. **대화 유지**: 서브텍스트 강화
4. **시간/장소 명시**: 모든 장면에 INT./EXT. 태그
5. **페이지 = 1분**: 스크린플레이 1페이지 ≈ 스크린 1분

### 웹툰 변환 가이드 (2026 트렌드)
- 웹툰이 "Authorized Data"로 각광 — 시각적 스토리보드 + 독자 참여 데이터 제공
- 각 챕터를 에피소드 단위로 분할
- 장면별 패널 구성안 생성 (1페이지 = 3-5컷)
- 대화 풍선/나레이션 박스 분류

---

## 7. KDP 최적화 가이드 (2026 최신)

### Amazon KDP 현황
- 전자책 67%, 인쇄책 50% 시장 점유율
- 자체 출간 35-70% 로열티 vs 전통 출간 8-15%

### 최적 가격 전략

| 가격대 | 로열티율 | 전략 |
|--------|---------|------|
| $0.99 | 35% | 시리즈 첫 권 미끼 |
| $2.99 | 70% | 최소 70% 로열티 |
| $3.99-$4.99 | 70% | **최적 전환율** |
| $9.99 | 70% | 최대 70% 로열티 |
| $9.99+ | 35% | 프리미엄 논픽션 |

### KDP 메타데이터 최적화
- **키워드**: 7개 슬롯, 구체적 + 검색량 높은 키워드
- **카테고리**: 3개 슬롯 (니치 + 보완 + 넓은 범위)
- **설명**: SEO 최적화 + 키워드 자연스럽게 통합
