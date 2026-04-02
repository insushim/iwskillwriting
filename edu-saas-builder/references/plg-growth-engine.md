# PLG (Product-Led Growth) & 수익화 엔진

> 58% SaaS가 PLG 모델 채택, 전환율 15-25% (영업 주도 대비 3배)

## PLG 온보딩 설계

### 즉시 가치 전달 (Time-to-Value = 초 단위)

```yaml
Step 1 — 가입 (30초):
  - 소셜 로그인 1클릭 (Google/카카오)
  - 최소 정보: 이름, 학년만 수집
  - 비밀번호 입력 X (매직링크 또는 OAuth)

Step 2 — 레벨 테스트 (2분):
  - "실력을 알아볼까요?" 5문제 퀴즈
  - 즉시 결과: "3학년 2학기 수준이에요!"
  - AI가 맞춤 학습 경로 자동 생성

Step 3 — 첫 학습 (3분):
  - 바로 문제 풀기 시작
  - 첫 정답 → 즉각 보상 (XP + 뱃지 + 효과음)
  - "첫 발걸음" 뱃지 획득

Step 4 — 습관 형성:
  - "내일도 올 거죠? 알림 받을까요?"
  - 푸시 알림 허용 요청 (가치 설명 후)
```

### PLG 퍼널 지표

```typescript
const PLG_METRICS = {
  // 획득 (Acquisition)
  signupRate: '방문자 → 가입 비율 (목표: 5-10%)',
  signupToActivation: '가입 → 첫 문제 풀기 (목표: 70%+)',

  // 활성화 (Activation)
  timeToFirstValue: '가입 → 첫 정답 시간 (목표: < 3분)',
  onboardingCompletion: '온보딩 완료율 (목표: 80%+)',
  day1Retention: 'D1 리텐션 (목표: 40%+)',

  // 리텐션 (Retention)
  day7Retention: 'D7 리텐션 (목표: 25%+)',
  day30Retention: 'D30 리텐션 (목표: 15%+)',
  weeklyActiveUsers: '주간 활성 사용자',
  streakRate: '스트릭 유지율',

  // 수익화 (Revenue)
  freeToTrialRate: '무료 → 체험 전환 (목표: 10%)',
  trialToPaidRate: '체험 → 유료 전환 (목표: 15-25%)',
  arpu: '사용자당 평균 수익',
  ltv: '고객 생애 가치',
  churnRate: '월간 이탈률 (목표: < 5%)',

  // 추천 (Referral)
  nps: 'Net Promoter Score (목표: 50+)',
  viralCoefficient: '바이럴 계수 (목표: > 0.5)',
  referralRate: '추천 가입 비율',
};
```

## Freemium → Premium 전환 전략

### 가격 정책 (한국 시장 최적화)

```yaml
무료:
  - 하루 5문제 제한
  - 기본 게이미피케이션 (XP, 레벨)
  - 광고 배너 (하단)
  - 기본 오답 노트
  - 1개 교과
  제한: AI 기능 X, 상세 리포트 X

프리미엄 개인 (₩9,900/월, 연 ₩89,000):
  - 무제한 문제
  - 광고 제거
  - AI 튜터 챗봇
  - AI 힌트 무제한
  - 전 교과 접근
  - 상세 학습 리포트
  - 오프라인 학습 (PWA)
  - 스트릭 프리즈 무제한

프리미엄 가족 (₩14,900/월):
  - 자녀 3명까지
  - 학부모 대시보드
  - 형제 비교 리포트
  - 가족 챌린지

학교/기관 (학생당 ₩3,000/월, 최소 30명):
  - 교사 대시보드
  - 반 관리 & 과제
  - 실시간 퀴즈
  - 학습 분석
  - 커리큘럼 커스텀
  - 화이트라벨 옵션
```

### 페이월 트리거 포인트

```yaml
자연스러운 전환 유도:
  - 일일 문제 제한 도달 시: "더 풀고 싶으세요? 프리미엄이면 무제한!"
  - AI 힌트 3회 소진 시: "AI 튜터가 도와줄 수 있어요"
  - 랭킹 상위 진입 시: "프리미엄 유저는 2배 XP!"
  - 학부모 리포트 요청 시: "자세한 리포트는 프리미엄에서"
  - 30일 무료 사용 후: "지금까지 {n}문제 풀었어요! 계속할까요?"

절대 하지 말 것:
  - 학습 중간에 팝업 X
  - 기능을 막아놓고 광고 X
  - 아이에게 직접 결제 유도 X (학부모에게만)
```

## 리퍼럴 프로그램

```yaml
학생 → 학생:
  추천인: 100 코인 + "친구 초대왕" 뱃지
  피추천인: 50 코인 + 첫 주 무제한 문제
  메커니즘: 초대 코드 / 카카오톡 공유

학부모 → 학부모:
  추천인: 1개월 무료 + ₩5,000 할인
  피추천인: 2주 프리미엄 무료 체험
  메커니즘: 이메일 / 카카오톡 공유

교사 → 학교:
  추천인: 교사용 프리미엄 영구 무료
  피추천 학교: 첫 학기 30% 할인
  메커니즘: 교사 네트워크 / 교육청 세미나
```

## A/B 테스트 프레임워크

```typescript
// PostHog 또는 자체 구현
const AB_TESTS = {
  onboarding_flow: {
    variants: ['quiz_first', 'tutorial_first', 'instant_play'],
    metric: 'day1_retention',
  },
  paywall_timing: {
    variants: ['day_7', 'day_14', 'day_30', 'after_limit'],
    metric: 'trial_to_paid_rate',
  },
  streak_reminder: {
    variants: ['7pm', '8pm', '9pm', 'adaptive'],
    metric: 'streak_continuation_rate',
  },
  xp_display: {
    variants: ['bar_only', 'bar_plus_number', 'animated_bar'],
    metric: 'session_duration',
  },
};
```

## 코호트 분석

```sql
-- 주간 코호트 리텐션 쿼리 (Supabase)
WITH cohorts AS (
  SELECT
    id AS student_id,
    DATE_TRUNC('week', created_at) AS cohort_week
  FROM profiles WHERE role = 'student'
),
activity AS (
  SELECT
    student_id,
    DATE_TRUNC('week', created_at) AS activity_week
  FROM learning_sessions
  GROUP BY student_id, DATE_TRUNC('week', created_at)
)
SELECT
  c.cohort_week,
  COUNT(DISTINCT c.student_id) AS cohort_size,
  COUNT(DISTINCT CASE WHEN a.activity_week = c.cohort_week + INTERVAL '1 week' THEN a.student_id END)::float
    / COUNT(DISTINCT c.student_id) * 100 AS week1_retention,
  COUNT(DISTINCT CASE WHEN a.activity_week = c.cohort_week + INTERVAL '4 weeks' THEN a.student_id END)::float
    / COUNT(DISTINCT c.student_id) * 100 AS week4_retention
FROM cohorts c
LEFT JOIN activity a ON c.student_id = a.student_id
GROUP BY c.cohort_week
ORDER BY c.cohort_week DESC;
```
