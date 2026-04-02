# 에셋 프롬프트 작성 가이드

## 프롬프트 공식

### 기본 구조
```
[스타일] + [주제 설명] + [용도] + [기술 요구사항]
```

### 게임 에셋 종류별 프롬프트 템플릿

---

## 1. 캐릭터 스프라이트

### 플레이어 캐릭터
```
[art style] game character sprite of [character description],
[pose/action], [proportions], [color scheme],
transparent background, clean lines, game-ready asset
```

**예시:**
```
cute chibi pixel art game character sprite of a young wizard
with blue robe and golden wand, front-facing idle pose,
32x32 pixel proportions, warm color palette,
transparent background, clean pixel lines, game-ready asset
```

### 적 캐릭터
```
[art style] game enemy sprite of [enemy description],
[mood: menacing/cute/scary], [size relative to player],
transparent background, consistent with [theme]
```

**예시:**
```
cartoon pixel art game enemy sprite of a dark ink blob monster
with angry glowing purple eyes, cute but menacing,
slightly smaller than player character,
transparent background, fantasy library theme
```

### 보스 캐릭터
```
[art style] game boss character of [boss description],
large and imposing, [special features],
[attack stance/idle], transparent background,
detailed design, [theme] boss monster
```

---

## 2. 스프라이트시트 (애니메이션)

### 규칙
- 반드시 4x4 = **16프레임** 요청
- 배경색 명시 (`--bg "#00FF00"`)
- 프레임 순서 명시

### 걷기 애니메이션
```
4x4 spritesheet, 16 frames total:
Row 1 (frames 1-4): [character] walking DOWN cycle
Row 2 (frames 5-8): [character] walking LEFT cycle
Row 3 (frames 9-12): [character] walking RIGHT cycle
Row 4 (frames 13-16): [character] walking UP cycle
[art style], consistent character across all frames,
background color: [hex]
```

### 공격 애니메이션
```
4x4 spritesheet, 16 frames total:
Animation sequence of [character] performing [attack type],
frames progress left-to-right, top-to-bottom,
wind-up (frames 1-4), strike (frames 5-8),
impact (frames 9-12), recovery (frames 13-16),
[art style], background color: [hex]
```

### 아이콘 컬렉션
```
4x4 spritesheet of 16 game item icons:
1-[item1] 2-[item2] ... 16-[item16]
Each icon in its own cell, [art style],
clean design, [theme] RPG style, background color: [hex]
```

---

## 3. 배경/맵

### 스크롤링 배경
```
[art style] game background for [location],
horizontal/vertical scrolling, seamless tileable edges,
[lighting], [atmosphere], [resolution hint],
detailed environment, [theme]
```

**사이즈 옵션:**
- 가로 스크롤: `--aspect-ratio 16:9 --size 2K`
- 세로 스크롤: `--aspect-ratio 9:16 --size 2K`
- 정사각형: `--size 1K` (기본)

### 타일맵 타일셋
```
[art style] tileset for [environment type],
organized grid layout, seamless tiles,
includes: [ground], [walls], [decorations], [obstacles],
each tile clearly separated, background color: [hex]
```

---

## 4. UI 요소

### 버튼 세트
```
game UI button set, [theme] style,
[N] buttons arranged in a row/grid:
[Button1 label], [Button2 label], ...
[border style], [texture], clean design,
transparent background
```

### 패널/프레임
```
game UI panel frame, [theme] style,
[shape: rounded/angular/ornate],
[border details], semi-transparent center,
suitable for text overlay, [size description]
```

### 카드 프레임 (등급별)
```
set of 5 game card frames showing different rarity tiers:
Common (gray border), Uncommon (green glow),
Rare (blue glow), Epic (purple glow),
Legendary (golden glow with particles),
[theme] fantasy style, clean design, transparent background
```

### HP바 / 진행도 바
```
game UI health bar and progress bar set,
[theme] style, includes:
full bar, 75% bar, 50% bar, 25% bar, empty bar,
clean design, [color scheme]
```

---

## 5. 이펙트

### 폭발/충돌
```
game VFX spritesheet of [effect type],
4x4 grid, 16 frames, animation sequence,
[color scheme], transparent background,
bright and dynamic, game-ready
```

### 파티클
```
set of particle sprites for [effect]:
[particle1], [particle2], ...,
small size, transparent background,
[color], glowing/sparkling
```

---

## 스타일 일관성 키워드 모음

### 픽셀 아트
```
pixel art, 16-bit retro, clean pixels, limited palette,
crisp edges, no anti-aliasing, nostalgic gaming aesthetic
```

### 카툰/셀 셰이딩
```
cartoon style, bold black outlines, flat colors,
cel-shaded, bright vibrant palette, chibi proportions,
clean vector-like design
```

### 판타지
```
fantasy art, magical atmosphere, warm amber lighting,
ornate details, medieval RPG aesthetic, enchanted
```

### 사이버/네온
```
cyberpunk neon, dark background, glowing edges,
electric blue and pink, futuristic, high tech
```

### 미니멀/플랫
```
minimalist flat design, simple geometric shapes,
limited color palette, clean sans-serif,
modern UI aesthetic, no textures
```

### 수채화
```
watercolor painting style, soft edges, organic textures,
blended colors, hand-painted feel, artistic
```

---

## 프롬프트 최적화 팁

1. **구체적으로:** "character" → "small wizard child with blue pointy hat"
2. **용도 명시:** "game sprite", "game background", "UI element"
3. **배경 지정:** "transparent background" (스프라이트), "seamless" (타일)
4. **크기 힌트:** "32x32 proportions", "64x64 style"
5. **스타일 고정:** 프로젝트 전체에서 동일 스타일 키워드 사용
6. **부정 표현:** 원치 않는 것도 명시 "no realistic proportions, no photorealism"
7. **색상 팔레트:** 구체적 색상 명시 "blue #4A90D9, gold #FFD700"

---

## 프로바이더별 프롬프트 차이

### Gemini (대화형)
- 자연어로 상세 설명 가능
- "이전 이미지를 수정해서..." 가능
- 레퍼런스 이미지 첨부 가능 (최대 14장)

### Imagen 4 (텍스트→이미지)
- 간결하고 구체적인 키워드 중심
- 편집 불가, 한 번에 원하는 결과 얻어야 함
- 텍스트 렌더링 우수

### Grok Imagine
- 다양한 스타일 적응력 우수
- 포토리얼~애니메이션까지 폭넓음
- 비교적 자유로운 프롬프트

### OpenAI GPT Image
- 구조화된 프롬프트 선호
- "In the style of..." 잘 작동
- Mini는 품질 낮음 주의
