# AI 도구 카탈로그 v2.0

> 5개 리서치 에이전트 × 200+ 소스 = 1000+ 소스 교차검증 결과

---

## 1. 이미지 생성 API (게임 에셋)

| 도구 | 모델 | 가격 | 강점 | 용도 |
|------|------|------|------|------|
| **Imagen 4 Fast** | imagen-4.0-fast-generate-001 | $0.02/장 | 최저가, 빠름 | 대량 에셋 |
| **Imagen 4 Standard** | imagen-4.0-generate-001 | $0.04/장 | 고품질 | 최종 에셋 |
| **Imagen 4 Ultra** | imagen-4.0-ultra-generate-001 | $0.06/장 | 2K 해상도 | 배경, 타이틀 |
| **Gemini Flash** | gemini-2.5-flash | $0.039/장 | 대화형 편집 | 캐릭터 디자인 |
| **Flux Schnell** | flux-schnell | $0.02/장 | 초고속, 오픈소스 | 프로토타이핑 |
| **Flux Pro** | flux-pro | $0.12/장 | 최고 품질 | 고품질 컨셉 |
| **Flux.2 Max** | flux-2-max | $0.25/장 | 4K 출력 | 배경, 포스터 |
| **Grok Imagine** | grok-imagine-image | $0.02/장 | 다양한 스타일 | 캐릭터, 배경 |
| **GPT Image** | gpt-image-1 | $0.005~0.036/장 | 초저가(mini) | 프로토타이핑 |
| **Leonardo.ai** | - | $12~60/월 | 게임 에셋 특화 | 프로덕션 에셋 |
| **Scenario.gg** | 커스텀 모델 | 구독제 | 스타일 일관성 | 시리즈 에셋 |

### 우선순위 전략
```
프로토타입: Imagen Fast ($0.02) 또는 Flux Schnell ($0.02)
    ↓ 만족하면 그대로 사용
    ↓ 고품질 필요 시
최종 에셋: Gemini Flash ($0.039) 또는 Imagen Standard ($0.04)
    ↓ 4K 배경/타이틀
고해상도: Flux.2 Max ($0.25) 또는 Imagen Ultra ($0.06)
```

---

## 2. 픽셀 아트 전문 도구

| 도구 | 특징 | 가격 |
|------|------|------|
| **Sprite AI** | 16×16~128×128, 내장 에디터, PNG/SVG | 무료 티어 |
| **PixelLab** | 4/8방향 캐릭터 자동 생성 | 구독제 |
| **SEELE** | 45분→10초, 완전한 2D 에셋 라이브러리 | 구독제 |
| **ZzSprite** | 오픈소스 픽셀 아트 생성기 | 무료 |
| **Aseprite** | 전문 픽셀 에디터 (후처리용) | $19.99 |

### 최적 픽셀 아트 프롬프트
```
"GBA-style [캐릭터 설명], [크기]px, [프레임수]-frame [애니메이션 타입],
[방향] view, [색상/장비 설명], transparent background, [참조 게임] style"

예시:
"GBA-style human paladin, 32x32px, 8-frame walk cycle, side view,
silver armor with blue cape, transparent background, Fire Emblem style"
```

---

## 3. 3D 에셋 생성

| 도구 | 가격 | 강점 | 출력 |
|------|------|------|------|
| **Meshy** | $0.01/크레딧 (2000 무료) | 97% 프린트 성공률 | GLB, FBX, OBJ |
| **Tripo** | $0.01/크레딧 | 깔끔한 쿼드 토폴로지 | 게임 준비 메시 |
| **CSM** | $0.75/모델 | PBR 텍스처, 리깅 | 게임 준비 에셋 |
| **Blockade Labs** | $12~60/월 | 360° 스카이박스, 8K | HDR, GLB |

### 환경/스카이박스 생성 (Blockade Labs)
```bash
# 360° 환경 생성 → Unity/Godot/Phaser 배경으로 사용
curl -X POST "https://backend.blockadelabs.com/api/v1/skybox" \
  -H "x-api-key: YOUR_KEY" \
  -d '{"prompt": "fantasy medieval village at sunset, warm lighting"}'
```

---

## 4. 오디오 생성 (BGM + SFX)

| 도구 | 용도 | 가격 | 강점 |
|------|------|------|------|
| **Suno v4** | BGM | ~$0.05/곡 | 풀송 + 보컬, 동적 BGM |
| **ElevenLabs** | SFX + 보이스 | $0.33~0.80/분 | 효과음, NPC 보이스 |
| **AudioCraft/MusicGen** | BGM | 무료 (로컬) | 오픈소스, 커스텀 |
| **AIVA** | 오케스트라 BGM | 구독제 | 시네마틱, MIDI 출력 |
| **Google Lyria RealTime** | 적응형 BGM | API 가격 | 게임플레이 반응형 |
| **Web Audio API** | SFX (프로시저럴) | 무료 | 코드만으로 생성 |

### 게임 유형별 추천 조합
```
캐주얼/아케이드: Web Audio SFX + Suno BGM
RPG/어드벤처:   ElevenLabs SFX + AIVA 오케스트라 BGM
교육/퀴즈:      Web Audio SFX + Suno 차분한 BGM
액션/서바이벌:  Web Audio SFX + Suno 전투 BGM
무료 대안:      Web Audio API (SFX+BGM 전부 프로시저럴)
```

---

## 5. 배경 제거 & 업스케일링

### 배경 제거 (우선순위)
| 도구 | 품질 | 속도 | 설치 |
|------|------|------|------|
| **rembg** | 9/10 | 빠름 | `pip install rembg` |
| **BiRefNet** | 9.5/10 | 보통 | ComfyUI 플러그인 |
| **SAM/SAM2** | 10/10 | 느림 | Meta, 로컬 전용 |
| **RMBG-2.0** | 9/10 | 빠름 | BRIA AI |

### 업스케일링 (게임 에셋용)
| 도구 | 품질 | 속도 | 추천 용도 |
|------|------|------|----------|
| **Real-ESRGAN** | 9.2/10 | 6초 | 사진, 범용 |
| **SwinIR** | 9.7/10 | 12초 | 디지털 아트 |
| **Waifu2X** | 8.5/10 | 3초 | 애니메/픽셀 아트 |

```bash
# Real-ESRGAN 업스케일링
pip install realesrgan
python -m realesrgan -i assets/img/ -o assets/img_hd/ -s 4
```

---

## 6. 애니메이션 생성

| 도구 | 용도 | 가격 |
|------|------|------|
| **Spine** | 2D 스켈레탈 애니메이션 | $69~$300 |
| **Live2D** | 정적 이미지 → 라이브 애니메이션 | 라이선스별 |
| **Rive** | SVG/PNG → 인터랙티브 애니메이션 | 구독제 |
| **AI Spine Generator** | 단일 이미지 → 게임 애니메이션 | 구독제 |

---

## 7. 대화/스토리 생성 (NPC)

| 도구 | 용도 | 품질 |
|------|------|------|
| **Claude API** | NPC 대화, 퀘스트 생성 | 최고 |
| **Gemini API** | NPC 대화, 월드빌딩 | 우수 |
| **WorldAnvil** | 네이티브 AI 내러티브 | 우수 |
| **NovelCrafter** | 멀티 LLM 스토리 | 우수 |

### NPC 대화 생성 프롬프트 템플릿
```
게임: [게임 이름]
NPC: [이름], [직업], [성격 3단어]
맥락: [현재 퀘스트/상황]

이 NPC의 대화를 생성해줘:
- 인사 (3개 변형)
- 퀘스트 제안 (메인 대사 + 수락/거절 응답)
- 상점 대사 (구매/판매/재화 부족)
- 잡담 (5개)
- 퀘스트 완료 축하
JSON 형식으로 출력.
```

---

## 8. 게임 백엔드 서비스

| 서비스 | 용도 | 가격 | 강점 |
|--------|------|------|------|
| **Supabase** | 리더보드, 인증, DB | 무료 티어 | 오픈소스 Postgres |
| **Firebase** | 실시간 DB, 인증 | 무료 티어 | NoSQL, 빠른 설정 |
| **Colyseus** | 실시간 멀티플레이어 | 자체호스팅 무료 | WebSocket, 상태 동기화 |
| **Nakama** | 매치메이킹, 리더보드 | 오픈소스 무료 | 풀 게임 백엔드 |
| **PlayFab** | 경제, 라이브옵스 | 무료 티어 | 기업급, Azure |
| **GameAnalytics** | 분석, 리텐션 | 무료 | 인디 게임 특화 |

---

## 9. 테스팅 & QA

| 도구 | 용도 | 가격 |
|------|------|------|
| **Playwright** | 웹 게임 자동 테스트 | 무료 |
| **Percy** | 비주얼 회귀 테스트 | 5000 스크린샷/월 무료 |
| **Chromatic** | UI 컴포넌트 테스트 | 무료 티어 |
| **Applitools** | AI 비주얼 테스트 | 유료 |

---

## 10. 배포 플랫폼

| 플랫폼 | 월간 트래픽 | 수익 모델 | 추천 장르 |
|--------|-----------|----------|----------|
| **Poki** | 141M | 광고 수익 공유 | 캐주얼, 아케이드 |
| **CrazyGames** | 89M | 광고 수익 공유 | 멀티플레이어, 캐주얼 |
| **itch.io** | - | 자유 수익 공유 | 인디, 실험적 |
| **Newgrounds** | - | 광고 + 후원 | 플래시 스타일 |
| **GameJolt** | 9M | 광고 + 판매 | 인디 |
| **Vercel** | - | 호스팅 | 자체 배포 |
| **Steam** | - | 30% 수수료 | 상용 게임 |

---

## 비용 최적화 총정리

### 미니 게임 (10~20 에셋)
```
이미지: Imagen Fast × 15장 = $0.30
사운드: Web Audio (무료) = $0.00
배경제거: rembg (무료) = $0.00
---
총: ~$0.30
```

### 중간 게임 (30~60 에셋)
```
이미지: Imagen Fast × 40장 = $0.80
배경: Gemini Flash × 5장 = $0.20
사운드: Suno BGM × 3곡 = $0.15
배경제거: rembg (무료) = $0.00
---
총: ~$1.15
```

### 대형 게임 (100+ 에셋)
```
이미지: Imagen Fast × 80장 = $1.60
배경: Imagen Ultra × 10장 = $0.60
캐릭터: Gemini Flash × 10장 = $0.39
사운드: Suno BGM × 5곡 = $0.25
사운드: ElevenLabs SFX × 20개 = ~$2.00
3D (선택): Meshy × 10개 = $0.10
---
총: ~$4.94
```
