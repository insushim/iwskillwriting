# 게임 밸런싱 가이드

## 난이도 곡선 설계

### 기본 원칙
```
난이도
  │
  │                    ╱
  │                  ╱
  │              ╱──╱  ← 고원기 (숨 고르기)
  │           ╱──
  │        ╱──
  │    ╱───
  │ ╱──
  └────────────────────── 진행도
    초반   중반   후반
```

1. **초반 (웨이브 1~3):** 완만한 상승, 튜토리얼 역할
2. **중반 (웨이브 4~7):** 점진적 상승 + 중간 고원기
3. **후반 (웨이브 8~10):** 급격한 상승 + 보스
4. **고원기:** 3~4웨이브마다 쉬운 구간 삽입 (플레이어 성취감)

---

## 적 스탯 밸런싱 공식

### 웨이브별 적 HP 스케일링
```
적_HP = 기본_HP × (1 + (웨이브 - 1) × 0.15)
적_속도 = 기본_속도 × (1 + (웨이브 - 1) × 0.05)
적_수 = 기본_수 + (웨이브 - 1) × 2
```

### 난이도별 배율

| 난이도 | HP 배율 | 속도 배율 | 적 수 배율 | 보상 배율 |
|--------|---------|----------|-----------|----------|
| 쉬움 | x0.7 | x0.8 | x0.7 | x0.8 |
| 보통 | x1.0 | x1.0 | x1.0 | x1.0 |
| 어려움 | x1.5 | x1.2 | x1.3 | x1.5 |
| 최악 | x2.5 | x1.5 | x1.8 | x2.5 |

### 예시: 10웨이브 적 HP 표

기본 HP = 10일 때:

| 웨이브 | 쉬움 | 보통 | 어려움 | 최악 |
|--------|------|------|--------|------|
| 1 | 7 | 10 | 15 | 25 |
| 2 | 8 | 12 | 17 | 29 |
| 3 | 9 | 13 | 20 | 33 |
| 4 | 10 | 15 | 22 | 37 |
| 5 | 12 | 17 | 25 | 42 |
| 6 | 13 | 19 | 28 | 47 |
| 7 | 14 | 21 | 31 | 52 |
| 8 | 15 | 22 | 34 | 56 |
| 9 | 16 | 24 | 36 | 60 |
| 10(보스) | 50 | 80 | 120 | 200 |

---

## 경제 시스템 밸런싱

### 재화 획득 vs 소비 균형

**핵심 원칙:** 플레이어가 모든 것을 살 수 없어야 함 (선택의 즐거움)

```
획득량 공식:
  웨이브 클리어 보상 = 기본값 x (1 + 웨이브 x 0.1) x 난이도_배율
  적 처치 보상 = 1~3 코인 (랜덤)
  보물상자 보상 = 10~50 코인 (등급별)

소비처:
  무기 구매: 50~500 코인
  무기 강화: 레벨 x 20 코인
  리롤 (카드 재추첨): 30 코인
  부활 (퀴즈 없이): 100 코인
```

### 인플레이션 방지
- 강화 비용을 지수적으로 증가: `비용 = 기본값 x 1.5^(레벨-1)`
- 최대 레벨 설정 (예: 무기 레벨 MAX = 10)
- 고가 아이템으로 재화 흡수 (스킨, 코스메틱)

---

## 무기 밸런싱

### DPS (초당 데미지) 기준 설계

```
무기_DPS = 데미지 x 공격속도
```

모든 무기의 DPS가 비슷하되, **사용 패턴**이 다르게:

| 무기 유형 | 데미지 | 공격속도 | DPS | 특성 |
|-----------|--------|---------|-----|------|
| 빠른 연사 | 낮음 (5) | 빠름 (5/s) | 25 | 꾸준한 데미지 |
| 강력한 일격 | 높음 (50) | 느림 (0.5/s) | 25 | 큰 적에 효과적 |
| 범위 공격 | 낮음 (8) | 보통 (2/s) | 16x다수 | 다수 적에 효과적 |
| 관통 | 보통 (15) | 보통 (2/s) | 30+ | 일렬 적에 효과적 |
| 유도 | 보통 (12) | 보통 (2/s) | 24 | 놓치지 않음 |

### 업그레이드 카드 밸런싱

#### 등급별 효과 크기
| 등급 | 스탯 증가 | 확률 |
|------|----------|------|
| 커먼 | +5~10% | 50% |
| 언커먼 | +10~20% | 30% |
| 레어 | +20~35% 또는 새 효과 | 15% |
| 에픽 | +35~50% 또는 강력한 효과 | 4% |
| 레전더리 | +50~100% 또는 게임체인저 | 1% |

---

## 동적 난이도 조절 (DDA)

### 교육 게임 전용 DDA

```typescript
interface PlayerMetrics {
  recentAccuracy: number;     // 최근 10문제 정답률
  averageResponseTime: number; // 평균 응답 시간 (초)
  consecutiveCorrect: number;  // 연속 정답
  consecutiveWrong: number;    // 연속 오답
  totalAttempts: number;       // 총 시도
}

function adjustDifficulty(metrics: PlayerMetrics, current: number): number {
  let adjustment = 0;

  // 정답률 기반
  if (metrics.recentAccuracy > 0.9) adjustment += 0.3;
  else if (metrics.recentAccuracy > 0.7) adjustment += 0.1;
  else if (metrics.recentAccuracy < 0.4) adjustment -= 0.3;
  else if (metrics.recentAccuracy < 0.6) adjustment -= 0.1;

  // 연속 정답/오답
  if (metrics.consecutiveCorrect >= 5) adjustment += 0.2;
  if (metrics.consecutiveWrong >= 3) adjustment -= 0.3;

  // 응답 시간 (빠르면 쉬운 문제)
  if (metrics.averageResponseTime < 3) adjustment += 0.1;
  if (metrics.averageResponseTime > 10) adjustment -= 0.1;

  // 범위 제한 (1~10)
  return Math.max(1, Math.min(10, current + adjustment));
}
```

### 전투 DDA

```typescript
function adjustBattleDifficulty(
  playerDeaths: number,
  waveAttempts: number,
  lastSurvivalTime: number
): { hpMultiplier: number; speedMultiplier: number; enemyCountMultiplier: number } {
  // 같은 웨이브 3회 이상 실패 시 쉽게
  if (waveAttempts >= 3) {
    return { hpMultiplier: 0.8, speedMultiplier: 0.9, enemyCountMultiplier: 0.8 };
  }
  // 30초 이내 사망 시 살짝 쉽게
  if (lastSurvivalTime < 30) {
    return { hpMultiplier: 0.9, speedMultiplier: 0.95, enemyCountMultiplier: 0.9 };
  }
  // 기본
  return { hpMultiplier: 1.0, speedMultiplier: 1.0, enemyCountMultiplier: 1.0 };
}
```

---

## 보상 심리학

### 가변 비율 강화 (Variable Ratio Reinforcement)
슬롯머신 효과: 보상의 **불확실성**이 중독성을 만듦

```
- 확정 보상: 웨이브 클리어 → 항상 코인 지급 (안정감)
- 확률 보상: 적 드롭 → 1~5% 확률 아이템 (기대감)
- 누적 보상: 100적 처치 → 특별 보상 (목표 의식)
- 시간 보상: 첫 클리어 보너스, 매일 접속 보너스 (습관 형성)
```

### "거의 성공" 효과
플레이어가 목표에 가까워질수록 포기하기 어려워짐:
- 보스 HP 바를 크게 표시
- "n마리만 더!" 표시
- 업적 진행도 바 표시

### 세션 종료 유도 (교육 게임)
중독 방지를 위해 적절한 종료 지점 제공:
- 3 스테이지 클리어 후 "오늘의 학습 완료!" 메시지
- 30분 후 휴식 알림
- 일일 보상 한도 설정
