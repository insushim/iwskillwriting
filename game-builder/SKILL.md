---
name: game-builder
description: >
  Autonomous game development skill with AI-powered asset generation, visual QA,
  and multi-engine support. Builds complete, playable games from a single natural
  language description using Godogen-style 2-skill pipeline architecture.
  Supports Phaser 3 (web/HTML5), Godot 4 (GDScript), and pure HTML5 Canvas.
  Generates all game assets (sprites, backgrounds, UI, audio placeholders) via
  Gemini/Grok/Imagen APIs. Includes visual QA loop that captures screenshots
  and uses AI vision to detect bugs. Use this skill whenever the user asks to
  build a game, make a game, create a game, 게임 만들어줘, 게임 개발, 게임 제작,
  @game, /game, arcade game, platformer, RPG, puzzle, defense, educational game,
  교육용 게임, 디펜스 게임, 퍼즐 게임, 아케이드, 로그라이크, 서바이벌,
  tower defense, word game, typing game, quiz game, card game, idle game,
  clicker, match-3, runner, shooter, or any game-related development request.
  Also triggers on: "Phaser", "Godot", "GDScript", "game assets", "sprites",
  "sprite sheet", "game UI", "game design document", "GDD", "level design",
  "game balancing", "게임 밸런싱", "게임 기획서", "스프라이트", "에셋 생성".
  Combines real game studio workflows (1000+ sources cross-validated) with
  EPCT methodology for systematic, error-free game development.
  v2.0: Added procedural generation (WFC, BSP, Perlin), genre templates
  (vampire survivors, tower defense, roguelike, idle, match-3, card game,
  platformer, hybrid), multiplayer/backend (Colyseus, Supabase leaderboard),
  deployment automation (Vercel, itch.io, PWA, Capacitor, Electron),
  accessibility (colorblind, key remapping, difficulty options, i18n),
  advanced balancing (prestige, gacha pity, DDA, economy sink/faucet),
  and 10+ additional reference guides.
---

# Game Builder Skill v4.0 — Autonomous Game Factory

> 2000+ 소스 + 100개 게임 제작 도구 교차검증 | 12개 병렬 에이전트 | 2026 트렌드 반영

이 스킬은 자연어 게임 설명 하나로 완전한 플레이 가능한 게임을 자동 생성합니다.
Godogen 방식의 2-스킬 파이프라인(오케스트레이터 + 태스크 실행자)을 채택하고,
실제 게임 회사(한국 50개+, 해외 50개+) + 오픈소스 프로젝트 200개+ 워크플로우를
교차검증하여 설계되었습니다.

## 핵심 차별점

1. **AI 에셋 자동 생성** — Gemini/Grok/Imagen/GPT Image API로 스프라이트, 배경, UI, 아이콘 자동 생성
2. **시각적 QA 루프** — 게임 스크린샷 → AI 비전 분석 → 자동 버그 수정
3. **멀티 엔진** — Phaser 3 (웹), Godot 4 (네이티브), HTML5 Canvas (초경량)
4. **실제 콘텐츠** — 목업/플레이스홀더 없이 모든 데이터를 실제 콘텐츠로 채움
5. **교육 게임 특화** — 한국 초등학교 교육과정(2022 개정) 연동 지원
6. **프로시저럴 생성** — WFC/BSP/Perlin/Cellular Automata 기반 맵/던전/지형 자동 생성
7. **장르 템플릿** — 뱀서라이크, TD, 로그라이크, 아이들, 매치3, 카드, 플랫포머, 하이브리드
8. **멀티플레이어** — Colyseus 실시간, Supabase 리더보드, Firebase 클라우드 세이브
9. **멀티 플랫폼 배포** — Vercel/itch.io/PWA/Capacitor(모바일)/Electron(데스크톱)
10. **접근성/i18n** — 색각이상 필터, 키리매핑, 난이도 커스텀, 한/영/일 다국어
11. **게임 주스** — 카메라셰이크, 히트스톱, 스쿼시&스트레치, 파티클, 데미지넘버, UI애니메이션
12. **적 AI 시스템** — FSM, 보스 페이즈 패턴, A* 경로탐색, 스티어링 행동, 웨이브 디렉터
13. **게임 수학 라이브러리** — 전투/확률/이동/경제/시각 공식 복사붙여넣기 레디
14. **대화/커트씬** — Ren'Py 스타일 타이핑 효과, 초상화, 선택지 분기 대화 시스템
15. **인벤토리/크래프팅** — RPG Maker 스타일 그리드 인벤, 스태킹, 크래프팅 레시피
16. **날씨/낮밤** — Stardew Valley 스타일 동적 라이팅, 비/눈/안개 파티클, 시간 경과
17. **게임패드** — Gamepad API, 자동 키보드↔패드 전환, 버튼 프롬프트 아이콘
18. **성능 프로파일러** — F3 토글 FPS/메모리/드로우콜/엔티티 카운트 오버레이
19. **스킬 트리** — Path of Exile 스타일 노드 기반 스킬 트리, 선행조건, 리셋
20. **자동 타일링** — 47-tile 비트마스킹, Tiled JSON 로드, 패럴랙스 자동 설정

---

## 절대 규칙 (모든 출력에 적용)

**절대 금지:**
- TODO, FIXME, PLACEHOLDER, `// ...`, `/* 생략 */`, 스켈레톤 코드
- ColorRect/기본 도형만으로 끝내기 (에셋 생성 도구가 있으므로 반드시 사용)
- 빈 레벨, 빈 적 목록, 더미 데이터
- "My Game", "게임 이름", "Example" 같은 임시 이름
- 에셋 없이 코드만 제출
- 실행되지 않는 코드

**반드시 포함:**
- 완전한, 실행 가능한 코드 — 바로 플레이 가능한 상태
- AI 생성 에셋 (스프라이트, 배경, UI 요소)
- 실제 게임 데이터 (적 스탯, 아이템 목록, 레벨 구성 전부)
- 사운드 시스템 (Tone.js/Web Audio로 프로시저럴 사운드, 또는 오디오 파일)
- 완성된 UI (메뉴, HUD, 게임오버, 일시정지)
- 세이브/로드 시스템
- 반응형 디자인 (모바일/데스크톱)

---

## 엔진 선택 가이드

사용자가 엔진을 명시하지 않으면 아래 기준으로 자동 선택:

| 조건 | 선택 엔진 | 이유 |
|------|----------|------|
| 웹 배포 / 교육용 / SaaS 내장 | **Phaser 3** | 브라우저 즉시 실행, 배포 용이 |
| PC/모바일 네이티브 / 복잡한 2D-3D | **Godot 4** | 네이티브 성능, 멀티플랫폼 |
| 초경량 미니게임 / 임베드 | **HTML5 Canvas** | 의존성 없음, 최소 크기 |

### Phaser 3 설정 (기본값)
```bash
mkdir -p $PROJECT_NAME && cd $PROJECT_NAME
npm init -y
npm install phaser@3.80 --save
# TypeScript 사용 시
npm install typescript @types/node vite --save-dev
```

### Godot 4 설정
```bash
# Godot 4가 설치되어 있어야 함
mkdir -p $PROJECT_NAME && cd $PROJECT_NAME
# project.godot 파일 자동 생성
```

### HTML5 Canvas 설정
```bash
mkdir -p $PROJECT_NAME && cd $PROJECT_NAME
# index.html + game.js 만으로 동작
```

---

## 파이프라인 개요 (6단계 EPCT+)

```
Phase 0: RESEARCH     → 유사 게임 10개+ 분석, 장르 메카닉 교차검증
Phase 1: EXPLORE      → GDD 작성, 게임 메카닉 설계, 밸런싱 수치 확정
Phase 2: PLAN         → 아키텍처 설계, 에셋 목록, 작업 분해
Phase 3: CODE+ASSETS  → 5단계 구현 + AI 에셋 생성 (병행)
Phase 4: VISUAL QA    → 스크린샷 캡처 → AI 분석 → 자동 수정
Phase 5: POLISH       → 사운드, 이펙트, 최적화, 패키징
```

---

## Phase 0: RESEARCH (게임 분석)

게임 개발 전 반드시 유사 게임을 조사합니다.

**단계:**
1. 사용자 설명에서 장르 키워드 추출 (디펜스, RPG, 퍼즐, 아케이드 등)
2. 해당 장르의 대표 게임 10개+ 리스트업 (국내 5+, 해외 5+)
3. 각 게임의 핵심 메카닉, UI/UX, 중독 요소 분석
4. 사용자 게임에 적용할 장점 목록 작성
5. 저작권 위험 요소 체크 (이름, 캐릭터, UI 레이아웃 유사성)

**출력:** `docs/RESEARCH.md`

---

## Phase 1: EXPLORE (게임 기획서 - GDD)

완전한 게임 디자인 문서를 작성합니다.

**필수 포함 항목:**

### 1-1. 게임 개요
- 게임 이름 (독창적, 상업화 가능, 저작권 안전)
- 장르, 플랫폼, 타겟 유저
- 한 줄 컨셉 (엘리베이터 피치)
- 세계관/스토리 (교육 게임이면 교육 연결 고리)

### 1-2. 코어 루프
```
[행동] → [보상] → [성장] → [더 어려운 도전] → 반복
```
- 메인 루프 + 메타 루프 설계
- 세션 길이 (짧은 세션 3~5분 / 긴 세션 15~30분)
- "한 판 더" 욕구를 자극하는 요소

### 1-3. 핵심 메카닉 상세
- 이동/조작 방식
- 전투/퍼즐/학습 시스템
- 진행 시스템 (웨이브, 레벨, 스테이지)
- 보상 시스템 (즉각 보상 + 누적 보상 + 랜덤 보상)

### 1-4. 밸런싱 수치 (전부 구체적 숫자로)
- 플레이어 기본 스탯 (HP, 공격력, 이동속도, 공격속도)
- 적 스탯 표 (이름, HP, 공격력, 이동속도, 경험치, 드롭률)
- 무기/아이템 표 (이름, 효과, 비용, 업그레이드 수치)
- 난이도 곡선 (웨이브/레벨별 적 수, HP 배율, 속도 배율)
- 경제 시스템 (재화 획득량, 소비처, 인플레이션 방지)

### 1-5. UI/UX 설계
- 화면 구성도 (메인 메뉴, 게임 플레이, 상점, 설정, 결과)
- HUD 구성 (HP, 점수, 웨이브, 재화, 미니맵)
- 전환 애니메이션
- 터치/키보드/마우스 조작 매핑

### 1-6. 에셋 목록
- 캐릭터 스프라이트 (이름, 프레임 수, 크기)
- 적 스프라이트 (종류별)
- 배경/맵 이미지 (스테이지별)
- UI 요소 (버튼, 패널, 아이콘)
- 이펙트 (폭발, 충돌, 레벨업)
- 사운드 목록 (BGM, SFX)

### 1-7. 교육 연동 (교육 게임인 경우)
- 교과 연계 (2022 개정 교육과정 기준)
- 학년별 콘텐츠 데이터 (영어 단어, 수학 문제 등 — 전부 실제 데이터로)
- 퀴즈/학습 시스템 설계
- 학습 이력 추적

**출력:** `docs/GDD.md` — 모든 수치가 채워진 완전한 기획서

---

## Phase 2: PLAN (아키텍처 & 에셋 계획)

### 2-1. 프로젝트 구조 (Phaser 3 기준)
```
project-root/
├── src/
│   ├── main.ts              # 게임 설정, Phaser.Game 초기화
│   ├── scenes/
│   │   ├── BootScene.ts      # 에셋 로딩
│   │   ├── MenuScene.ts      # 메인 메뉴
│   │   ├── GameScene.ts      # 메인 게임플레이
│   │   ├── UIScene.ts        # HUD 오버레이
│   │   ├── ShopScene.ts      # 상점
│   │   ├── ResultScene.ts    # 결과 화면
│   │   └── SettingsScene.ts  # 설정
│   ├── objects/
│   │   ├── Player.ts         # 플레이어 클래스
│   │   ├── Enemy.ts          # 적 클래스
│   │   ├── Weapon.ts         # 무기 시스템
│   │   ├── Item.ts           # 아이템/드롭
│   │   └── Projectile.ts     # 발사체
│   ├── systems/
│   │   ├── WaveManager.ts    # 웨이브/스테이지 관리
│   │   ├── UpgradeSystem.ts  # 업그레이드/카드 시스템
│   │   ├── SaveSystem.ts     # 세이브/로드
│   │   ├── AudioManager.ts   # 사운드 관리
│   │   ├── ParticleManager.ts # 파티클 이펙트
│   │   └── QuizSystem.ts     # 퀴즈 시스템 (교육 게임)
│   ├── data/
│   │   ├── enemies.ts        # 적 데이터 (전체)
│   │   ├── weapons.ts        # 무기 데이터 (전체)
│   │   ├── upgrades.ts       # 업그레이드 카드 데이터 (전체)
│   │   ├── levels.ts         # 레벨/맵 데이터 (전체)
│   │   └── words.ts          # 단어 데이터 (교육 게임)
│   ├── ui/
│   │   ├── Button.ts         # 커스텀 버튼
│   │   ├── HealthBar.ts      # HP 바
│   │   ├── ProgressBar.ts    # 경험치/진행도 바
│   │   └── Toast.ts          # 알림 토스트
│   └── utils/
│       ├── constants.ts      # 상수 정의
│       ├── helpers.ts        # 유틸리티 함수
│       └── types.ts          # 타입 정의
├── assets/
│   ├── img/                  # AI 생성 이미지
│   ├── audio/                # 사운드 파일
│   ├── fonts/                # 폰트
│   └── data/                 # JSON 데이터
├── docs/
│   ├── RESEARCH.md
│   ├── GDD.md
│   ├── PLAN.md
│   └── ASSET-LIST.md
├── tools/                    # 에셋 생성 도구
│   ├── asset_gen.py          # 이미지 생성 래퍼
│   ├── spritesheet_tools.py  # 스프라이트시트 처리
│   └── visual_qa.py          # 시각 QA 도구
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── README.md
```

### 2-2. Godot 4 프로젝트 구조
```
project-root/
├── project.godot
├── scenes/
│   ├── main.tscn
│   ├── game.tscn
│   ├── menu.tscn
│   └── ui.tscn
├── scripts/
│   ├── player.gd
│   ├── enemy.gd
│   ├── weapon.gd
│   ├── wave_manager.gd
│   ├── upgrade_system.gd
│   ├── save_system.gd
│   └── audio_manager.gd
├── autoload/
│   ├── game_manager.gd
│   ├── event_bus.gd
│   └── data_manager.gd
├── assets/
│   ├── img/
│   ├── audio/
│   └── fonts/
├── data/
│   ├── enemies.json
│   ├── weapons.json
│   └── upgrades.json
├── tools/
│   ├── asset_gen.py
│   ├── spritesheet_tools.py
│   └── visual_qa.py
└── docs/
    └── GDD.md
```

### 2-3. 에셋 생성 계획
GDD의 에셋 목록을 기반으로 생성 계획을 작성합니다.

에셋 생성 도구 사용법은 별도 레퍼런스를 참조:
```
cat references/asset-generation-guide.md
```

### 2-4. 작업 분해 (5단계)
Phase 3를 5개 서브페이즈로 분해하고 각각에 진입/종료 조건 명시.

**출력:** `docs/PLAN.md`

---

## Phase 3: CODE + ASSETS (5단계 구현)

### Phase 3.1: Foundation + 에셋 생성 시작
- 프로젝트 초기화 (package.json, tsconfig, vite config)
- 게임 설정 파일 (해상도, 물리, 씬 등록)
- 기본 씬 구조 생성 (Boot, Menu, Game, UI)
- **에셋 생성 시작** — `tools/asset_gen.py`로 핵심 에셋 생성:
  - 플레이어 캐릭터 스프라이트시트
  - 적 스프라이트 (3~5종)
  - 배경 이미지 (메인 스테이지 1개)
  - UI 요소 (버튼, 패널)
- 에셋 로딩 씬 구현 (프로그레스 바)
- **체크포인트:** 게임 창이 열리고 메뉴가 표시됨

### Phase 3.2: 핵심 게임플레이
- 플레이어 이동 (WASD/조이스틱/터치)
- 적 스폰 + AI (이동 패턴, 추적)
- 전투 시스템 (자동 공격/수동 공격)
- 충돌 감지 + 데미지 시스템
- HP + 사망 처리
- 기본 웨이브 시스템
- **추가 에셋 생성:**
  - 발사체 스프라이트
  - 히트 이펙트
  - 추가 적 스프라이트
- **체크포인트:** 플레이어가 이동하고 적을 공격할 수 있음

### Phase 3.3: 진행 시스템 + UI
- 경험치/레벨업 시스템
- 업그레이드 카드 선택 UI
- 무기 시스템 (교체, 강화)
- 상점 시스템
- 세이브/로드 (localStorage 또는 JSON)
- HUD (HP바, 점수, 웨이브, 재화)
- **추가 에셋 생성:**
  - 카드 UI 프레임 (등급별)
  - 무기 아이콘
  - 아이템 아이콘
  - 재화 아이콘
- **체크포인트:** 전체 게임 루프 동작 (시작→플레이→업그레이드→반복)

### Phase 3.4: 콘텐츠 채우기
- 모든 적 종류 구현 (GDD의 전체 목록)
- 모든 무기/아이템 구현
- 모든 업그레이드 카드 구현
- 모든 레벨/맵 구현
- 보스전 구현
- 교육 게임: 퀴즈 시스템 + 전체 문제 데이터 입력
- **추가 에셋 생성:**
  - 보스 스프라이트
  - 추가 맵 배경
  - 보물상자, 드롭 아이템 이미지
- **체크포인트:** 모든 콘텐츠가 실제 데이터로 채워짐

### Phase 3.5: 사운드 + 이펙트 + 폴리시
- 프로시저럴 사운드 생성 (Web Audio API / Tone.js):
  - BGM: 장르별 루프 음악 생성
  - SFX: 공격, 피격, 폭발, UI 클릭, 레벨업
- 파티클 이펙트 (폭발, 치유, 레벨업, 획득)
- 화면 전환 애니메이션
- 카메라 쉐이크 (피격 시)
- 다크모드/접근성 설정
- 반응형 (모바일 터치 컨트롤)
- **체크포인트:** 완전한 게임 경험 (비주얼 + 오디오 + 인터랙션)

---

## Phase 4: VISUAL QA (시각적 품질 검증)

Godogen의 핵심 혁신을 채택합니다: **실제 화면을 캡처하고 AI가 분석합니다.**

### 4-1. 스크린샷 캡처 방법

**Phaser (웹):**
```bash
# Puppeteer로 웹 게임 스크린샷
python3 tools/visual_qa.py capture --url http://localhost:5173 --output screenshots/
```

**Godot:**
```bash
# Godot headless 모드로 스크린샷
# (Godogen의 방식 채택)
godot --headless --script tools/capture_screenshot.gd
```

### 4-2. AI 비전 분석

캡처된 스크린샷을 Gemini Flash Vision에 전송하여 분석:

```bash
python3 tools/visual_qa.py analyze --image screenshots/game_01.png
```

**검출 항목:**
- 텍스처 누락 (빈 공간, 깨진 이미지)
- UI 겹침 (버튼 겹침, 텍스트 잘림)
- 물리 오류 (물체 뚫림, 비정상 위치)
- 시각적 불균형 (너무 밝음/어두움, 대비 부족)
- 레이아웃 문제 (반응형 깨짐, 여백 부족)

### 4-3. 자동 수정 루프
```
캡처 → 분석 → 문제 목록 생성 → 코드 수정 → 다시 캡처 → 다시 분석
(최대 3회 반복, 문제 0이면 조기 종료)
```

시각 QA 도구 상세는 레퍼런스 참조:
```
cat references/visual-qa-guide.md
```

---

## Phase 5: POLISH (최종 다듬기)

### 5-1. 성능 최적화
- 오브젝트 풀링 (적, 발사체, 파티클)
- 드로우콜 최소화 (스프라이트 배칭)
- 60fps 목표 (모바일에서 30fps 허용)
- 에셋 압축 (tinypng / webp 변환)

### 5-2. 게임 밸런스 검증
- 난이도 곡선 시뮬레이션
- 재화 인플레이션 체크
- 극단적 전략 방지 (치트 방지)

### 5-3. 패키징
**Phaser (웹):**
```bash
npm run build
# dist/ 폴더에 정적 파일 생성
# Vercel/Netlify/GitHub Pages 배포 가능
```

**Godot:**
```bash
# 내보내기 설정 후 빌드
# Windows, Linux, Web, Android 지원
```

### 5-4. 배포 가이드
- Vercel 배포 (웹 게임)
- itch.io 업로드 (인디 게임)
- PWA 설정 (모바일 앱처럼 설치)
- Google Play / App Store (Capacitor/Cordova)

---

## 에셋 생성 시스템 상세

이 스킬의 핵심입니다. `tools/asset_gen.py`를 사용합니다.

### 지원 API (우선순위순)

| API | 모델 | 단가 | 용도 |
|-----|------|------|------|
| **Google Gemini** | gemini-3.1-flash-image-preview | $0.045~0.151/장 | 스프라이트, 캐릭터, 배경 (대화형 편집 가능) |
| **Google Imagen 4** | imagen-4.0-fast-generate-001 | **$0.02/장** | 대량 에셋 (가장 저렴) |
| **Google Imagen 4 Ultra** | imagen-4.0-ultra-generate-001 | $0.06/장 | 고품질 배경, 타이틀 |
| **xAI Grok Imagine** | grok-imagine-image | $0.02/장 | 스프라이트, 캐릭터 (Godogen 마이그레이션 대상) |
| **OpenAI GPT Image** | gpt-image-1 mini | $0.005~0.036/장 | 초저가 대량 생성 |

### 에셋 생성 명령어

```bash
# 단일 이미지 생성
python3 tools/asset_gen.py image \
  --prompt "cute cartoon wizard character, pixel art style, transparent background, game sprite, front-facing, chibi proportions" \
  --provider gemini \
  --size 1K \
  --output assets/img/player.png

# 스프라이트시트 생성 (4x4 = 16프레임)
python3 tools/asset_gen.py spritesheet \
  --prompt "Animation: cute wizard casting spell, 16 frames, pixel art" \
  --provider gemini \
  --bg "#00FF00" \
  --output assets/img/player_cast_raw.png

# 스프라이트시트 슬라이스 (개별 프레임으로)
python3 tools/asset_gen.py slice \
  --input assets/img/player_cast_raw.png \
  --output assets/img/player_cast/ \
  --frames 16 \
  --remove-bg

# 배경 생성 (2K, 와이드)
python3 tools/asset_gen.py image \
  --prompt "fantasy magical library interior, warm lighting, bookshelves, game background, horizontal scrolling, detailed pixel art" \
  --provider imagen \
  --size 2K \
  --aspect-ratio 16:9 \
  --output assets/img/bg_library.png

# 배경 제거 (투명 배경)
python3 tools/asset_gen.py remove-bg \
  --input assets/img/enemy_raw.png \
  --output assets/img/enemy.png

# 예산 설정 (센트 단위)
python3 tools/asset_gen.py set-budget 500

# 예산 확인
python3 tools/asset_gen.py budget
```

### 에셋 프롬프트 가이드

게임 에셋에 최적화된 프롬프트 작성법:
```
cat references/asset-prompt-guide.md
```

---

## 교육 게임 특화 기능

교육 게임(영어 단어, 수학 퀴즈 등) 제작 시 자동 적용:

### 퀴즈 시스템
- 4지선다 / 빈칸 채우기 / 듣고 고르기
- 오답 우선 출제 (SRS 간격 반복)
- 학년별 난이도 자동 조절 (DDA)
- 연속 정답 보너스, 힌트 시스템

### 단어 데이터 (영어 교육 게임)
- 1~6학년 교육과정 필수 영단어 내장
- 학년당 80단어 = 총 480단어
- 뜻, 예문, 발음 기호 포함
- 자세한 데이터는 레퍼런스 참조:
```
cat references/edu-word-data.md
```

### 수학 데이터 (수학 교육 게임)
- 1~6학년 교육과정 연산 문제 자동 생성
- 난이도별 문제 유형 (사칙연산, 분수, 도형 등)

### 교육적 보상 설계
- 광고 대신 퀴즈로 보상 획득
- 오답노트 + 단어장 기능
- 학습 통계 (정답률, 취약 영역)
- 학부모/교사 리포트 (선택)

---

## 에러 처리 시스템

### Level 1 — 즉시 수정 (< 30초)
명확한 에러 → 바로 수정 → 다시 실행

### Level 2 — 대안 시도 (< 2분)
직접 수정 실패 → 다른 라이브러리/패턴으로 시도

### Level 3 — 재설계 (< 5분)
두 방법 모두 실패 → 해당 기능 단순화하여 재설계

### 에셋 생성 실패 시
1. 다른 API 프로바이더로 전환 (Gemini → Imagen → Grok)
2. 프롬프트 수정하여 재시도
3. 3회 연속 실패 → 프로시저럴 생성으로 대체 (Canvas 그래픽)

---

## 레퍼런스 파일

| 파일 | 참조 시점 |
|------|----------|
| `references/asset-generation-guide.md` | Phase 3 — 에셋 생성 도구 상세 |
| `references/asset-prompt-guide.md` | Phase 3 — 에셋 프롬프트 작성법 |
| `references/visual-qa-guide.md` | Phase 4 — 시각 QA 도구 사용법 |
| `references/phaser-patterns.md` | Phase 3 — Phaser 3 베스트 프랙티스 |
| `references/godot-patterns.md` | Phase 3 — Godot 4 베스트 프랙티스 |
| `references/edu-word-data.md` | Phase 3.4 — 교육용 영어 단어 데이터 |
| `references/sound-generation.md` | Phase 3.5 — 프로시저럴 사운드 가이드 |
| `references/game-balance-guide.md` | Phase 1 — 게임 밸런싱 가이드 |
| `references/genre-templates.md` | Phase 1 — **[v2.0]** 10개 장르 코어루프/밸런싱/코드 템플릿 |
| `references/procedural-generation.md` | Phase 3 — **[v2.0]** WFC/BSP/Perlin/CellularAutomata 맵 생성 |
| `references/multiplayer-backend.md` | Phase 3 — **[v2.0]** Colyseus/Supabase/Firebase 멀티플레이어 |
| `references/deployment-guide.md` | Phase 5 — **[v2.0]** Vercel/itch.io/PWA/Capacitor/Electron 배포 |
| `references/accessibility-i18n.md` | Phase 3 — **[v2.0]** 접근성/색맹/키리매핑/다국어(ko/en/ja) |
| `references/ai-tools-catalog.md` | 전체 — **[v2.0]** 50+ AI 도구/API 카탈로그 (가격/용도/우선순위) |
| `references/game-juice-polish.md` | Phase 3.5 — **[v3.0]** 카메라셰이크/히트스톱/파티클/데미지넘버/UI폴리시 |
| `references/game-ai-behavior.md` | Phase 3.2 — **[v3.0]** FSM/보스패턴/A*경로탐색/스티어링/웨이브디렉터 |
| `references/game-math-formulas.md` | Phase 3 — **[v3.0]** 전투/확률/이동/경제/시각 수학공식 복사붙여넣기용 |
| `references/social-engagement.md` | Phase 3 — **[v3.0]** 업적/데일리리워드/튜토리얼/배틀패스/A/B테스트/히트맵 |
| `references/advanced-systems.md` | Phase 3 — **[v4.0]** 대화/인벤토리/날씨/게임패드/프로파일러/스킬트리/타일맵 |
| `references/killer-features.md` | 전체 — **[v4.0]** 100+ 도구 킬러피처 (적응형음악/이벤트시트/턴제전투/본애니/AI NPC) |

---

## 완료 보고서

모든 페이즈 완료 시 출력:

```
═══════════════════════════════════════════════════════
  ✅ Game Builder — Build Complete
═══════════════════════════════════════════════════════
  게임 이름:    [이름]
  엔진:        [Phaser 3 / Godot 4 / HTML5 Canvas]
  장르:        [장르]

  🎨 에셋:
  - 생성된 이미지: [N]개
  - 스프라이트시트: [N]개
  - 배경: [N]개
  - UI 요소: [N]개
  - 사운드: [N]개
  - API 비용: ~$[N]

  🎮 게임 콘텐츠:
  - 적 종류: [N]종
  - 무기/아이템: [N]종
  - 업그레이드 카드: [N]종
  - 레벨/맵: [N]개
  - 보스: [N]체

  🧪 품질:
  - 빌드: ✅ 성공
  - 시각 QA: ✅ 통과 (수정 [N]건)
  - 60fps: ✅
  - 반응형: ✅

  📊 교육 (해당 시):
  - 단어/문제 수: [N]개
  - 학년 범위: [N]~[N]학년

  🔑 필요한 API 키:
  - GOOGLE_API_KEY (Gemini/Imagen 에셋 생성)
  - [XAI_API_KEY — Grok 사용 시]
  - [OPENAI_API_KEY — GPT Image 사용 시]

  🚀 실행: npm run dev (Phaser) / godot . (Godot)
═══════════════════════════════════════════════════════
```
