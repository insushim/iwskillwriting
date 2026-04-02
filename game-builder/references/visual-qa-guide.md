# Visual QA Guide

## 시각적 품질 검증 시스템

Godogen에서 영감을 받은 Visual QA 루프입니다.
게임 화면을 캡처하고 AI 비전으로 분석하여 시각적 버그를 자동 감지합니다.

---

## 설치

```bash
# Puppeteer (웹 게임 스크린샷)
npm install -g puppeteer

# Pillow (이미지 처리)
pip install Pillow --break-system-packages
```

**필수 API 키:** `GOOGLE_API_KEY` (Gemini Flash Vision 사용)
- Gemini 2.5 Flash의 비전 기능은 무료 티어에서 사용 가능
- 이미지 생성과 달리 비전 분석은 비용이 거의 없음

---

## 사용법

### 1. 스크린샷 캡처

```bash
# 웹 게임 (개발 서버 실행 중)
python3 tools/visual_qa.py capture \
  --url http://localhost:5173 \
  --output screenshots/ \
  --count 5 \
  --delay 3.0

# 로컬 HTML 파일
python3 tools/visual_qa.py capture \
  --file index.html \
  --output screenshots/
```

### 2. 개별 분석

```bash
python3 tools/visual_qa.py analyze --image screenshots/screenshot_01.png
```

출력 예시:
```json
{
  "issues": [
    {
      "severity": "critical",
      "category": "texture",
      "description": "Player sprite is missing - only a white square visible",
      "location": "center",
      "suggestion": "Check asset loading in BootScene, verify player.png exists"
    },
    {
      "severity": "minor",
      "category": "ui",
      "description": "Score text slightly clipped at top edge",
      "location": "top-right",
      "suggestion": "Add 10px padding to score text y position"
    }
  ],
  "positives": [
    "Background rendering looks smooth",
    "Enemy sprites are well-designed and consistent"
  ],
  "overall_score": 6,
  "summary": "Game is functional but has a critical missing player texture"
}
```

### 3. 전체 QA 루프

```bash
python3 tools/visual_qa.py qa \
  --url http://localhost:5173 \
  --output qa_results/ \
  --rounds 3
```

이 명령은:
1. 스크린샷 2장 캡처
2. 각각 AI 비전으로 분석
3. 문제 발견 시 `fix_report.json` 생성
4. Claude Code가 수정 후 다시 캡처/분석
5. 문제 0이면 조기 종료, 아니면 최대 3라운드 반복

---

## 검출 가능한 문제 유형

### Critical (즉시 수정 필요)
- 텍스처 완전 누락 (하얀/검은 사각형)
- UI가 전혀 표시되지 않음
- 화면 전체가 한 색상
- 물체가 화면 밖으로 벗어남

### Major (게임플레이에 영향)
- 스프라이트 깨짐/잘림
- UI 요소 겹침
- 텍스트 잘림/가독성 문제
- 물리 오류 (물체 뚫림, 비정상 위치)
- 배경과 전경 대비 부족

### Minor (미관 개선)
- 여백/정렬 미세 조정
- 색상 불균형
- 애니메이션 부자연스러움
- 폰트 크기 불일치

---

## Claude Code와의 연동

### 자동 수정 워크플로우

Visual QA는 Claude Code가 직접 실행합니다:

```
1. Claude Code가 코드 작성 완료
2. `npm run dev` 또는 서버 실행
3. `python3 tools/visual_qa.py qa --url http://localhost:5173`
4. fix_report.json 읽기
5. 보고된 문제 수정
6. 다시 QA 실행
7. 모든 문제 해결될 때까지 반복
```

### Godot 게임 QA

Godot 게임의 경우 headless 모드에서 스크린샷을 캡처합니다:

```gdscript
# tools/capture_screenshot.gd
extends SceneTree

func _init():
    # 게임 씬 로드
    var scene = load("res://scenes/game.tscn").instantiate()
    root.add_child(scene)

    # 2초 대기 후 스크린샷
    await create_timer(2.0).timeout

    var image = root.get_viewport().get_texture().get_image()
    image.save_png("screenshots/godot_capture.png")

    quit()
```

```bash
godot --headless --script tools/capture_screenshot.gd
python3 tools/visual_qa.py analyze --image screenshots/godot_capture.png
```

---

## 비용

Visual QA에 사용되는 Gemini Flash Vision은 **무료 티어**에서 충분히 사용 가능합니다.

| 항목 | 비용 |
|------|------|
| Gemini 2.5 Flash (비전 분석) | 무료 (일 500회+) |
| Gemini 2.5 Flash-Lite | 무료 (더 높은 한도) |
| 스크린샷 캡처 (Puppeteer) | 무료 |

에셋 생성과 달리, 시각 QA는 사실상 무료로 운영 가능합니다.
