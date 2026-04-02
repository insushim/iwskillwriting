# 적응형 학습 & 간격반복 시스템

> SM-2 알고리즘, 적응형 난이도 조절, 마스터리 학습, 망각 곡선 기반 복습

## SM-2 간격반복 알고리즘 (SuperMemo 2)

### 원리
Piotr Wozniak(1987)이 개발한 간격반복 알고리즘. Ebbinghaus 망각 곡선을 기반으로
정보를 잊기 직전에 복습하여 장기 기억으로 전환하는 최적 시점을 계산합니다.

**효과**: 전통적 학습 대비 200~300% 향상된 기억 유지율

### 구현

```typescript
interface SM2State {
  easeFactor: number;     // EF: 난이도 계수 (최소 1.3, 초기값 2.5)
  interval: number;       // I: 다음 복습까지 일수
  repetitions: number;    // n: 연속 정답 횟수
  nextReviewDate: Date;   // 다음 복습 날짜
}

/**
 * SM-2 알고리즘 핵심 함수
 * @param state - 현재 카드 상태
 * @param quality - 응답 품질 (0~5)
 *   0: 완전 모름 (blackout)
 *   1: 틀렸지만 정답 보고 기억남
 *   2: 틀렸지만 정답이 쉬웠음
 *   3: 맞았지만 어려웠음 (심각한 고민)
 *   4: 맞았지만 약간 고민
 *   5: 완벽하게 즉답
 */
function sm2Update(state: SM2State, quality: number): SM2State {
  let { easeFactor, interval, repetitions } = state;

  if (quality >= 3) {
    // 정답: 간격 증가
    switch (repetitions) {
      case 0: interval = 1; break;      // 첫 정답: 1일 후
      case 1: interval = 6; break;      // 두 번째: 6일 후
      default: interval = Math.round(interval * easeFactor); // 이후: EF 곱
    }
    repetitions++;
  } else {
    // 오답: 리셋 (처음부터 다시)
    repetitions = 0;
    interval = 1;
  }

  // EF 업데이트 (학습 난이도 반영)
  easeFactor = Math.max(1.3,
    easeFactor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
  );

  const nextReviewDate = new Date();
  nextReviewDate.setDate(nextReviewDate.getDate() + interval);

  return { easeFactor, interval, repetitions, nextReviewDate };
}

// quality 변환: 교육 앱에서의 매핑
function mapResponseToQuality(params: {
  isCorrect: boolean;
  attemptCount: number;
  timeTaken: number;
  timeLimit: number;
  hintUsed: boolean;
}): number {
  if (!params.isCorrect) {
    return params.attemptCount <= 1 ? 1 : 0;
  }
  if (params.hintUsed) return 3;
  if (params.timeTaken > params.timeLimit * 0.8) return 3;
  if (params.timeTaken > params.timeLimit * 0.5) return 4;
  return 5;  // 빠르고 정확한 응답
}
```

### DB 스키마 (SM-2 파라미터)

```sql
CREATE TABLE student_problem_sm2 (
  student_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  problem_id UUID NOT NULL REFERENCES problems(id) ON DELETE CASCADE,
  ease_factor REAL NOT NULL DEFAULT 2.5,
  interval_days INTEGER NOT NULL DEFAULT 0,
  repetitions INTEGER NOT NULL DEFAULT 0,
  next_review_date DATE NOT NULL DEFAULT CURRENT_DATE,
  last_quality INTEGER,         -- 마지막 응답 품질 (0~5)
  total_reviews INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  PRIMARY KEY (student_id, problem_id)
);

-- 오늘 복습할 문제 조회
CREATE INDEX idx_sm2_review_due
  ON student_problem_sm2(student_id, next_review_date)
  WHERE next_review_date <= CURRENT_DATE;
```

## 적응형 난이도 조절

### IRT 간소화 모델 (Item Response Theory)

```typescript
interface StudentAbility {
  theta: number;           // 학생 능력치 (-3 ~ +3)
  problemHistory: Array<{
    difficulty: number;    // 문제 난이도
    correct: boolean;
  }>;
}

// 문제 선택: 학생 능력치에 맞는 최적 난이도
function selectNextProblem(
  ability: StudentAbility,
  availableProblems: Problem[]
): Problem {
  // 최적 난이도 = 학생 능력 ± 0.5 (약간 어려운 것이 학습에 최적)
  const targetDifficulty = ability.theta + 0.3;

  return availableProblems
    .map(p => ({
      problem: p,
      distance: Math.abs(getDifficultyValue(p.difficulty) - targetDifficulty)
    }))
    .sort((a, b) => a.distance - b.distance)[0].problem;
}

function getDifficultyValue(d: 'easy' | 'medium' | 'hard' | 'challenge'): number {
  return { easy: -1, medium: 0, hard: 1, challenge: 2 }[d];
}

// 능력치 업데이트 (ELO 방식 간소화)
function updateAbility(theta: number, difficulty: number, correct: boolean): number {
  const expected = 1 / (1 + Math.exp(-(theta - difficulty)));
  const k = 0.4; // 학습률
  return theta + k * ((correct ? 1 : 0) - expected);
}
```

### 3단계 적응형 전략

```yaml
Level 1 — 기본 적응:
  규칙: 3연속 정답 → 난이도 ↑, 2연속 오답 → 난이도 ↓
  적합: 대부분의 교육 앱

Level 2 — 마스터리 기반:
  규칙: 단원별 80% 정답 시 다음 단원 unlock
  적합: Khan Academy 스타일

Level 3 — AI 기반:
  규칙: 학생 풀이 패턴 분석 → 취약 유형 자동 감지 → 맞춤 문제 생성
  적합: AI 튜터 통합 시
```

## 마스터리 학습 (Mastery Learning)

Benjamin Bloom(1968) 기반. 학생이 현재 개념을 충분히 이해해야 다음으로 진행.

```typescript
interface MasteryStatus {
  unitId: string;
  totalAttempts: number;
  correctAttempts: number;
  masteryPercent: number;     // 0~100
  status: 'not_started' | 'in_progress' | 'mastered' | 'needs_review';
}

const MASTERY_CONFIG = {
  threshold: 80,            // 80% 정답 시 마스터리 달성
  minAttempts: 5,           // 최소 5문제 풀어야 판정
  reviewAfterDays: 14,      // 마스터리 후 14일 뒤 복습 체크
  decayRate: 0.05,          // 복습 안 하면 일당 5% 감소
};

function updateMastery(status: MasteryStatus, isCorrect: boolean): MasteryStatus {
  const newTotal = status.totalAttempts + 1;
  const newCorrect = status.correctAttempts + (isCorrect ? 1 : 0);
  const percent = Math.round((newCorrect / newTotal) * 100);

  let newStatus = status.status;
  if (newTotal >= MASTERY_CONFIG.minAttempts) {
    if (percent >= MASTERY_CONFIG.threshold) newStatus = 'mastered';
    else if (percent >= 50) newStatus = 'in_progress';
    else newStatus = 'needs_review';
  }

  return {
    ...status,
    totalAttempts: newTotal,
    correctAttempts: newCorrect,
    masteryPercent: percent,
    status: newStatus,
  };
}
```

## 취약 영역 자동 감지

```typescript
interface WeakArea {
  topic: string;           // 예: "받아올림 덧셈"
  accuracy: number;        // 정답률
  attempts: number;
  trend: 'improving' | 'declining' | 'stable';
  recommendation: string;  // 추천 학습 활동
}

function analyzeWeakAreas(submissions: Submission[]): WeakArea[] {
  // 태그별 정답률 집계
  const tagStats = new Map<string, { correct: number; total: number; recent: boolean[] }>();

  for (const sub of submissions) {
    for (const tag of sub.problem.tags) {
      const stat = tagStats.get(tag) || { correct: 0, total: 0, recent: [] };
      stat.total++;
      if (sub.is_correct) stat.correct++;
      stat.recent.push(sub.is_correct);
      if (stat.recent.length > 10) stat.recent.shift();
      tagStats.set(tag, stat);
    }
  }

  return Array.from(tagStats.entries())
    .map(([topic, stat]) => {
      const accuracy = Math.round((stat.correct / stat.total) * 100);
      const recentAccuracy = stat.recent.filter(Boolean).length / stat.recent.length * 100;
      const trend = recentAccuracy > accuracy + 10 ? 'improving'
        : recentAccuracy < accuracy - 10 ? 'declining' : 'stable';

      return {
        topic,
        accuracy,
        attempts: stat.total,
        trend,
        recommendation: accuracy < 50
          ? `${topic} 기초부터 다시 학습하세요`
          : accuracy < 70
          ? `${topic} 추가 연습이 필요해요`
          : `${topic} 심화 문제에 도전해보세요`,
      };
    })
    .filter(w => w.accuracy < 80)
    .sort((a, b) => a.accuracy - b.accuracy);
}
```

## FSRS 알고리즘 (SM-2 후속, 2024~)

> Free Spaced Repetition Scheduler — Anki가 2024년부터 SM-2 대신 채택한 최신 알고리즘

SM-2의 한계를 극복한 차세대 간격반복 알고리즘. 머신러닝 기반으로 개인별 망각 곡선을 학습합니다.

```typescript
// FSRS 간소화 구현 (교육 앱용)
interface FSRSState {
  stability: number;      // S: 기억 안정성 (일수 단위)
  difficulty: number;     // D: 카드 난이도 (1~10)
  lastReview: Date;
  scheduledDays: number;
}

// FSRS는 SM-2 대비 장점:
// 1. "낮은 간격 지옥" 문제 해결 — 쉬운 카드가 빠르게 간격 증가
// 2. 카드 난이도가 초기 학습에 영향받지 않음
// 3. 개인별 학습 패턴에 적응
// 4. 25-40% 더 나은 장기 기억 유지율

// 선택 가이드:
// - SM-2: 구현 간단, 대부분의 교육 앱에 충분
// - FSRS: 정밀한 복습 최적화 필요 시 (플래시카드 중심 앱)
// - 하이브리드: SM-2 기본 + AI로 간격 조정 (권장)
```

## 학습 경로 자동 생성

```yaml
Ebbinghaus 기반 복습 스케줄:
  Day 0: 새로운 개념 학습
  Day 1: 첫 복습 (망각률 ~50%)
  Day 3: 두 번째 복습
  Day 7: 세 번째 복습
  Day 14: 네 번째 복습
  Day 30: 다섯 번째 복습
  Day 90: 여섯 번째 복습 (장기 기억 정착)

하루 학습 구성 (최적):
  1. 오늘의 SM-2 복습 문제 (3~5문제)
  2. 새로운 개념 문제 (5~7문제)
  3. 취약 영역 보충 (2~3문제)
  합계: 10~15문제 (15~20분)
```
