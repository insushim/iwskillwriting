# Asset Generation Guide

## 에셋 생성 도구 사용법 상세

### 설치 요구사항
```bash
pip install Pillow --break-system-packages
# 고급 배경 제거 (선택)
pip install rembg --break-system-packages
# 스크린샷 캡처용 (선택)
npm install -g puppeteer
```

### API 키 설정
```bash
# 필수 (하나 이상)
export GOOGLE_API_KEY="your-key"    # Gemini + Imagen
# 선택
export XAI_API_KEY="your-key"       # Grok Imagine
export OPENAI_API_KEY="your-key"    # GPT Image
```

---

## 프로바이더별 특징

### Gemini (Nano Banana 2) — `gemini-3.1-flash-image-preview`
- **장점:** 대화형 편집 가능, 4K 지원, 레퍼런스 이미지 14장까지
- **단점:** 가장 비쌈 ($0.045~0.151/장)
- **적합:** 캐릭터 디자인, 컨셉 아트, 세밀한 수정이 필요한 에셋

### Imagen 4 Fast — `imagen-4.0-fast-generate-001`
- **장점:** 가장 저렴 ($0.02/장), 빠른 생성
- **단점:** 편집 불가 (텍스트→이미지만)
- **적합:** 대량 에셋 (아이콘, 텍스처, UI 요소)

### Grok Imagine — `grok-imagine-image`
- **장점:** 저렴 ($0.02/장), 높은 품질
- **단점:** OpenAI SDK 호환만
- **적합:** 캐릭터, 배경, 스타일 다양

### GPT Image Mini — `gpt-image-1`
- **장점:** 초저가 ($0.005/장 low), OpenAI 호환
- **단점:** 낮은 해상도 (low 품질)
- **적합:** 프로토타이핑, 썸네일

---

## 게임 에셋 프롬프트 공식

### 캐릭터 스프라이트
```
[스타일] [캐릭터설명], game character sprite, front-facing,
[비율/크기], transparent background, consistent design,
[추가 지시사항]
```

**예시:**
```bash
python3 tools/asset_gen.py image \
  --prompt "cute chibi wizard character, blue robe, holding magic wand, pixel art style, game character sprite, front-facing, 64x64 proportions, transparent background, bright colors, clean lines" \
  --provider imagen --quality fast \
  -o assets/img/player.png
```

### 적 캐릭터
```
[스타일] [적설명], game enemy sprite, menacing but [톤],
transparent background, [크기]
```

**예시:**
```bash
python3 tools/asset_gen.py image \
  --prompt "cartoon ink monster, dark purple blob with angry eyes, game enemy sprite, menacing but cute, transparent background, 48x48 proportions, pixel art, clean design" \
  --provider imagen --quality fast \
  -o assets/img/enemy_blob.png
```

### 배경
```
[스타일] [장소설명], game background, [스크롤방향],
[해상도/비율], detailed, atmospheric
```

**예시:**
```bash
python3 tools/asset_gen.py image \
  --prompt "magical library interior, warm amber lighting, towering bookshelves, floating books, game background, horizontal scrolling, detailed pixel art, fantasy atmosphere, cozy and mysterious" \
  --provider gemini --size 2K --aspect-ratio 16:9 \
  -o assets/img/bg_library.png
```

### UI 요소
```
[스타일] game UI [요소], [테마], clean design,
flat/glossy, [크기]
```

**예시:**
```bash
python3 tools/asset_gen.py image \
  --prompt "game UI button set, fantasy book theme, 4 buttons arranged in a row: Play, Shop, Settings, Quit, golden borders, parchment texture, clean pixel art, transparent background" \
  --provider imagen --quality fast \
  -o assets/img/ui_buttons.png
```

### 스프라이트시트 (애니메이션)
```bash
python3 tools/asset_gen.py spritesheet \
  --prompt "Animation: cute wizard walking cycle, 4 directions (down, left, right, up), 4 frames each, pixel art, chibi style" \
  --bg "#00FF00" \
  -o assets/img/player_walk_raw.png

# 슬라이스
python3 tools/asset_gen.py slice \
  --input assets/img/player_walk_raw.png \
  --output assets/img/player_walk/ \
  --frames 16 --cols 4 --remove-bg
```

### 아이콘 세트 (16개 한 번에)
```bash
python3 tools/asset_gen.py spritesheet \
  --prompt "Collection: 16 game item icons, numbered 1-16: 1-sword 2-shield 3-potion 4-scroll 5-ring 6-amulet 7-boots 8-gloves 9-helmet 10-armor 11-bow 12-staff 13-gem 14-key 15-coin 16-heart, pixel art, RPG style, clean icons" \
  --bg "#FF00FF" \
  -o assets/img/items_raw.png

python3 tools/asset_gen.py slice \
  --input assets/img/items_raw.png \
  --output assets/img/items/ \
  --frames 16 --remove-bg \
  --names "sword,shield,potion,scroll,ring,amulet,boots,gloves,helmet,armor,bow,staff,gem,key,coin,heart"
```

---

## 예산 관리

### 일반적인 게임별 비용 추정

| 게임 규모 | 이미지 수 | Imagen Fast | Gemini | 혼합 |
|-----------|----------|-------------|--------|------|
| 미니 게임 | 10~20장 | $0.20~0.40 | $0.45~0.90 | ~$0.50 |
| 중간 게임 | 30~60장 | $0.60~1.20 | $1.35~2.70 | ~$1.50 |
| 대형 게임 | 80~150장 | $1.60~3.00 | $3.60~6.75 | ~$3.50 |
| 재생성 (실패) | +30~50% | +$0.50~1.50 | +$1~3 | ~$1.50 |

### 비용 최적화 전략
1. **프로토타입:** Imagen 4 Fast ($0.02)로 먼저 생성
2. **만족 시:** 그대로 사용
3. **고품질 필요:** 주요 에셋만 Gemini/Grok로 재생성
4. **대량 생성:** 스프라이트시트(16개/장)로 효율 극대화
5. **시각 QA:** Gemini Flash Vision 무료 티어 활용

---

## 에셋 스타일 일관성 유지

### 스타일 키워드 프리셋

**픽셀 아트:**
```
pixel art, 16-bit retro style, clean pixels, limited color palette, crisp edges
```

**카툰:**
```
cartoon style, bold outlines, bright colors, cel-shaded, clean design, chibi proportions
```

**판타지:**
```
fantasy art style, magical atmosphere, warm colors, detailed, RPG aesthetic
```

**미니멀:**
```
minimalist game art, flat design, simple shapes, limited colors, clean geometric
```

### 일관성 팁
1. 모든 에셋에 동일한 스타일 키워드 사용
2. 색상 팔레트를 고정 (hex 코드 명시)
3. 캐릭터 비율 통일 (chibi/SD/실사)
4. 같은 프로바이더 사용 (프로바이더별 화풍 차이)
5. 배경색 통일 (투명 배경 변환 시 일관성)

---

## 문제 해결

### API 에러 대응

| 에러 | 원인 | 해결 |
|------|------|------|
| 429 Rate Limit | 요청 과다 | 5초 대기 후 재시도 |
| 400 Bad Request | 프롬프트 문제 | 프롬프트 단순화 |
| 403 Forbidden | API 키 문제 | 키 확인, 결제 활성화 |
| 500 Server Error | 서버 오류 | 1분 후 재시도 |
| Image not in response | 모델 거부 | 프롬프트에서 민감 키워드 제거 |

### 프로바이더 자동 전환
`--provider auto` 사용 시 순서:
1. Imagen 4 Fast (가장 저렴)
2. Gemini (대화형)
3. Grok (고품질)
4. OpenAI (최후 수단)
