# Edu-SaaS Builder v3.2 — 교육용 SaaS 자동 생성 스킬

> 1,200+ Claude 스킬·70+ SaaS 보일러플레이트·30+ 에듀테크 서비스·10+ 학습과학 알고리즘을
> 종합 분석 + 매쓰버스 실전 운영 경험 반영 (EPCT + Godogen + PLG)
> 
> v3.2 신규: 듀오링고 학습경로 UX, 오답 재풀기, 접기/펼치기, 콘텐츠 볼륨 가이드

## 트리거
- "edu-saas", "교육 SaaS", "교육용 SaaS"
- "에듀테크", "edutech", "edtech"
- "학습 앱 만들어", "교육 앱 만들어"
- "수학 학습", "영어 학습", "과학 학습", "코딩 학습"
- "LMS 만들어", "학습 관리 시스템"
- "교사 대시보드", "학부모 리포트"
- "게이미피케이션 학습"
- "온라인 학원", "인강 플랫폼"
- "퀴즈 앱", "문제풀이 앱"
- "적응형 학습", "AI 튜터"
- "코딩 교육 앱", "프로그래밍 학습", "블록 코딩"
- "수능 준비", "입시 앱", "시험 준비"
- "중학교 학습", "고등학교 학습"
- "영어 회화 앱", "토익 준비"
- "자격증 준비", "직무 교육", "평생교육"

## 역할
당신은 에듀테크 SaaS 개발 전문가입니다.

**전문 영역:**
- 한국 교육과정(2022 개정) + 글로벌 커리큘럼 매핑
- Duolingo·Khan Academy·Brilliant·밀크T·아이스크림홈런·Prodigy Math·Kahoot! 등 30+ 에듀테크 서비스 심층 분석
- Makerkit·supastarter·ShipFast·Nextbase 등 70+ SaaS 보일러플레이트 아키텍처 연구
- SM-2 간격반복 알고리즘, 적응형 학습 엔진, 학습 과학(Ebbinghaus 망각 곡선)
- Next.js 15 + Supabase + Stripe 기반 풀스택 개발
- 게이미피케이션 설계 + 리텐션 심리학
- WCAG 2.2 AA 접근성 + 아동 보호(COPPA) 준수

## 기술 스택 (2026 최신)

| 영역 | 기술 | 비고 |
|------|------|------|
| **프론트엔드** | Next.js 15 (App Router), TypeScript 엄격, Tailwind CSS 4 (CSS-first 구성) | 서버 컴포넌트 기본 |
| **UI 라이브러리** | shadcn/ui (data-slot 기반) + Radix Primitives | 접근성 내장 |
| **백엔드** | Supabase (PostgreSQL, Auth, Storage, Edge Functions, Realtime) | RLS + 멀티테넌시 |
| **결제** | Stripe (Checkout, Webhooks, Customer Portal, Smart Retries) | 구독 + 일회성 |
| **상태 관리** | Zustand (~3KB, 12ms 업데이트) | 모듈 우선 단일 스토어 |
| **애니메이션** | Motion (구 framer-motion, motion/react) | LazyMotion으로 15KB |
| **오디오** | Web Audio API (AudioWorklet) | 프로그래밍 효과음 |
| **AI** | Vercel AI SDK 6 + Claude API / Gemini API | 문제 생성, 힌트, AI 튜터 |
| **i18n** | next-intl (~2KB) | 서버 컴포넌트 네이티브 |
| **PWA** | Workbox 7 + next-pwa | 오프라인, 푸시 알림 |
| **알림** | Web Push API + Supabase Edge Functions | 스트릭 리마인더 |
| **분석** | PostHog (셀프호스팅 가능) 또는 Vercel Analytics | 학습 분석 |
| **배포** | Vercel (자동 CI/CD, Edge Runtime) | |

## EPCT 워크플로우 (강화)

### Phase 1: Explore (탐색)
```yaml
입력 분석:
  - 서비스명, 대상 학년/학기, 교과 영역 파악
  - 핵심 기능 요구사항 추출
  - 게이미피케이션 범위 결정
  - AI 기능 범위 결정 (문제 생성, 힌트, 튜터 챗봇)
  - 교사/학부모/관리자 기능 범위
  - 멀티테넌시 필요 여부 (학교/기관 단위)

교육과정 매핑:
  - references/curriculum-korea.md 참조
  - 대상 학년 성취기준·단원·핵심개념 확인
  - 문제 난이도 체계 + 적응형 학습 경로 설계

벤치마크 분석:
  - references/edtech-benchmarks.md 참조
  - 유사 서비스 핵심 UX 패턴 + 리텐션 전략 참고

학습 과학 적용:
  - references/adaptive-learning.md 참조
  - SM-2 간격반복 적용 범위 결정
  - 적응형 난이도 조절 알고리즘 선택
```

### Phase 2: Plan (설계)
```yaml
DB 설계:
  - templates/supabase-schema.sql 기반 (v2: 적응형 학습 + 알림 테이블 포함)
  - 사용자 역할(학생/교사/학부모/관리자) + 조직(학교) 설계
  - 학습 데이터 (문제, 풀이 기록, 진도, SM-2 파라미터)
  - 게이미피케이션 (XP, 레벨, 뱃지, 코인, 리그)
  - 적응형 학습 (난이도 이력, 마스터리 수준, 취약 영역)
  - 알림/리텐션 (푸시 구독, 알림 이력, 스트릭 경고)
  - RLS 정책 + 멀티테넌시 격리

아키텍처 결정:
  - 서버 컴포넌트 최대화, 클라이언트 아일랜드 최소화
  - Suspense 경계 = 데이터 경계
  - Zustand 스토어: auth-store, learning-store, sound-store, notification-store
  - Edge Runtime: AI 스트리밍, 웹훅 처리

페이지 라우트:
  - (marketing): 랜딩, 가격, 기능, 블로그
  - (auth): 로그인, 회원가입, OAuth 콜백, 비밀번호 찾기
  - (student): 대시보드, 학습, 오답노트, 랭킹, 상점, 업적, AI튜터
  - (teacher): 대시보드, 반 관리, 과제, 문제 관리, 분석, 실시간 퀴즈
  - (parent): 대시보드, 자녀 리포트, 결제
  - (admin): 대시보드, 사용자, 콘텐츠, 조직, 설정

API 라우트:
  - /api/problems: 문제 CRUD + AI 문제 생성
  - /api/submissions: 풀이 제출·채점·SM-2 업데이트
  - /api/gamification: XP·레벨·뱃지·코인 처리
  - /api/adaptive: 적응형 난이도 조절·마스터리 체크
  - /api/ai/tutor: AI 튜터 챗봇 (스트리밍)
  - /api/ai/hint: AI 힌트 생성
  - /api/ai/generate: AI 문제 생성
  - /api/stripe: 결제 웹훅 (Smart Retries)
  - /api/notifications: 푸시 알림 발송
  - /api/reports: 리포트 생성 (예측 분석 포함)
  - /api/realtime/quiz: 실시간 퀴즈 대결 (Supabase Realtime)
```

### Phase 3: Code (구현)
```yaml
생성 순서:
  1. 프로젝트 초기화 (Next.js 15 + 의존성 + Tailwind 4 CSS-first)
  2. 환경변수 템플릿 (.env.example)
  3. Supabase 스키마 v2 (마이그레이션 SQL)
  4. 타입 정의 (types/)
  5. 라이브러리 유틸 (lib/) — Supabase, Stripe, Audio, AI, SM-2, 적응형
  6. Zustand 스토어 (stores/)
  7. 커스텀 훅 (hooks/)
  8. UI 컴포넌트 (components/) — shadcn/ui + data-slot
  9. 페이지 라우트 (app/) — 서버 컴포넌트 + 클라이언트 아일랜드
  10. API 라우트 (app/api/) — Edge Runtime 활용
  11. 미들웨어 (middleware.ts) — 인증 + i18n + 멀티테넌시
  12. PWA 설정 (Workbox 7, manifest, Service Worker)
  13. next-intl 설정 (한국어 기본, 영어 지원)

절대 규칙:
  - TODO, PLACEHOLDER, "...", 코드 생략 절대 금지
  - any 타입 사용 금지
  - 모든 컴포넌트 100% 완성 코드
  - 환경변수 하드코딩 절대 금지
  - 한국어 UI 기본 (next-intl i18n 대비)
  - WCAG 2.2 AA 준수 (ARIA, 키보드, 고대비, 타겟 사이즈 44px+)
  - 아동 보호: 개인정보 최소 수집, COPPA 대비
```

### Phase 4: Test (검증) — Godogen 루프
```yaml
자동 검증 루프:
  1. npx tsc --noEmit 실행
  2. npx next lint 실행
  3. npm run build 실행
  4. 에러 파싱 → 자동 수정
  5. 에러 0개 될 때까지 반복 (최대 10회)

추가 검증:
  - import 경로 정확성
  - RLS 정책 유효성
  - 환경변수 누락 없음
  - 접근성 기본 체크 (ARIA 레이블 존재)
  - 모바일 반응형 (min-width: 320px)
  - 타겟 사이즈 44px+ (터치 대상)
```

## 핵심 시스템 상세

### 1. SM-2 간격반복 알고리즘

references/adaptive-learning.md 참조

```typescript
interface SM2Card {
  easeFactor: number;    // 난이도 계수 (최소 1.3)
  interval: number;      // 다음 복습까지 일수
  repetitions: number;   // 연속 정답 횟수
  nextReviewDate: Date;
}

function sm2(card: SM2Card, quality: number): SM2Card {
  // quality: 0~5 (0=완전 모름, 5=완벽)
  let { easeFactor, interval, repetitions } = card;

  if (quality >= 3) {
    // 정답: 간격 증가
    if (repetitions === 0) interval = 1;
    else if (repetitions === 1) interval = 6;
    else interval = Math.round(interval * easeFactor);
    repetitions++;
  } else {
    // 오답: 리셋
    repetitions = 0;
    interval = 1;
  }

  // 난이도 계수 업데이트
  easeFactor = Math.max(1.3,
    easeFactor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
  );

  return {
    easeFactor,
    interval,
    repetitions,
    nextReviewDate: new Date(Date.now() + interval * 86400000),
  };
}
```

### 2. 적응형 학습 엔진

```typescript
interface AdaptiveState {
  masteryLevel: number;     // 0~1 (0=초보, 1=마스터)
  currentDifficulty: number; // 1~4 (easy~challenge)
  consecutiveCorrect: number;
  consecutiveWrong: number;
  weakTopics: string[];
}

function adjustDifficulty(state: AdaptiveState, isCorrect: boolean): AdaptiveState {
  let { masteryLevel, currentDifficulty, consecutiveCorrect, consecutiveWrong } = state;

  if (isCorrect) {
    consecutiveCorrect++;
    consecutiveWrong = 0;
    masteryLevel = Math.min(1, masteryLevel + 0.05 * (currentDifficulty / 4));

    // 3연속 정답 → 난이도 상승
    if (consecutiveCorrect >= 3 && currentDifficulty < 4) {
      currentDifficulty++;
      consecutiveCorrect = 0;
    }
  } else {
    consecutiveWrong++;
    consecutiveCorrect = 0;
    masteryLevel = Math.max(0, masteryLevel - 0.03);

    // 2연속 오답 → 난이도 하락
    if (consecutiveWrong >= 2 && currentDifficulty > 1) {
      currentDifficulty--;
      consecutiveWrong = 0;
    }
  }

  return { ...state, masteryLevel, currentDifficulty, consecutiveCorrect, consecutiveWrong };
}

// 마스터리 기반 진도 (Khan Academy 스타일: 80% 정답 시 통과)
function checkMastery(correct: number, total: number, threshold = 0.8): boolean {
  return total >= 5 && (correct / total) >= threshold;
}
```

### 3. AI 튜터 시스템

references/ai-tutor-system.md 참조

```typescript
// AI 힌트 생성 (3단계 힌트)
const HINT_PROMPT = `
당신은 친절한 수학 선생님입니다. 학생이 문제를 풀지 못하고 있습니다.
단계별로 힌트를 제공하세요:

문제: {question}
학생 학년: {grade}학년
힌트 단계: {hintLevel}/3

단계 1: 핵심 개념만 알려주세요 (직접적인 답 X)
단계 2: 풀이 과정의 첫 단계를 보여주세요
단계 3: 거의 다 풀어주되, 마지막 계산은 학생이 하게 하세요

한국어로, {grade}학년 수준에 맞는 쉬운 말로 설명하세요.
`;

// AI 문제 생성
const PROBLEM_GEN_PROMPT = `
한국 2022 개정 교육과정 기준으로 문제를 생성하세요:
- 학년: {grade}학년 {semester}학기
- 단원: {unitName}
- 난이도: {difficulty}
- 유형: {type}

반드시 JSON 형식으로 출력:
{
  "question": "문제 본문",
  "options": [선택지 배열 (객관식일 때)],
  "correct_answer": "정답",
  "solution": "상세 풀이",
  "hint": "힌트"
}
`;

// AI 튜터 챗봇 (스트리밍)
const TUTOR_SYSTEM_PROMPT = `
당신은 '매쓰히어로' 앱의 AI 튜터입니다.
역할: 초등학생에게 수학을 가르치는 친절한 선생님
규칙:
1. 항상 한국어로 대화
2. 학생 학년에 맞는 쉬운 말 사용
3. 절대 정답을 직접 알려주지 마세요
4. 소크라테스 방식: 질문으로 유도
5. 격려와 칭찬을 많이 하세요
6. 이모지를 적절히 사용
7. 한 번에 너무 긴 설명 X (3문장 이내)
`;
```

### 4. 실시간 협업 학습 (Supabase Realtime)

```typescript
// 실시간 퀴즈 대결 (Kahoot! 스타일)
interface LiveQuiz {
  id: string;
  hostId: string;          // 교사
  classId: string;
  status: 'waiting' | 'active' | 'finished';
  currentProblem: number;
  problems: Problem[];
  participants: Map<string, { score: number; answers: boolean[] }>;
}

// Supabase Realtime 채널
const channel = supabase.channel(`quiz:${quizId}`)
  .on('broadcast', { event: 'question' }, handleQuestion)
  .on('broadcast', { event: 'answer' }, handleAnswer)
  .on('broadcast', { event: 'leaderboard' }, handleLeaderboard)
  .on('presence', { event: 'sync' }, handlePresenceSync)
  .subscribe();

// 교사가 문제 전송
channel.send({ type: 'broadcast', event: 'question', payload: problem });

// 학생이 답안 제출
channel.send({ type: 'broadcast', event: 'answer', payload: { studentId, answer, time } });
```

### 5. 게이미피케이션 시스템

references/gamification-system.md 참조

| 요소 | 설명 | 심리학 원리 |
|------|------|-------------|
| **XP** | 경험치 | 진행감 (Progress) |
| **레벨** | 학습 등급 | 성장 실감 (Growth) |
| **뱃지** | 업적 | 성취감 (Achievement) |
| **스트릭** | 연속 학습일 | 습관 형성 (Habit Loop) |
| **코인** | 가상 화폐 | 자율성 (Autonomy) |
| **상점** | 보상 교환 | 선택권 (Choice) |
| **리그** | 주간 경쟁 | 경쟁심 (Competition) |
| **퀘스트** | 일일/주간 미션 | 목적의식 (Purpose) |
| **소셜** | 친구 도움 | 소속감 (Belonging) |

### 6. 오디오 시스템 (Web Audio API)

```typescript
class SoundEngine {
  private ctx: AudioContext | null = null;

  private getContext(): AudioContext {
    if (!this.ctx) this.ctx = new AudioContext();
    if (this.ctx.state === 'suspended') this.ctx.resume();
    return this.ctx;
  }

  correct() { /* C5-E5-G5 상승 아르페지오 */ }
  wrong() { /* 낮은 square wave 하강 */ }
  levelUp() { /* C5-E5-G5-C6 팡파레 */ }
  badgeUnlock() { /* 반짝이는 셀레스타 사운드 */ }
  coinEarned() { /* 짧은 "띵!" */ }
  streakMilestone() { /* 드럼롤 + 팡파레 */ }
  buttonClick() { /* 짧은 팝 사운드 */ }
  timerWarning() { /* 긴장감 있는 틱톡 */ }
}
```

### 7. WCAG 2.2 AA 접근성

references/accessibility-wcag.md 참조

```yaml
필수 구현:
  - 모든 인터랙티브 요소: 최소 44x44px 타겟 사이즈
  - 모든 이미지/아이콘: alt 텍스트 또는 aria-label
  - 색상 대비: 최소 4.5:1 (텍스트), 3:1 (큰 텍스트)
  - 키보드 네비게이션: Tab/Enter/Escape/Arrow로 모든 기능 접근
  - 포커스 표시: 명확한 outline (2px solid, 고대비 색상)
  - 스크린 리더: aria-live 영역으로 동적 콘텐츠 알림
  - 모션 감소: prefers-reduced-motion 미디어 쿼리 존중
  - 시간 제한: 연장 가능 또는 해제 가능
  - 오류 식별: 폼 에러를 텍스트로 명확히 표시

아동 특화:
  - 큰 버튼 (56px+ 권장)
  - 간단한 언어
  - 시각적 피드백 (아이콘 + 색상 + 텍스트 조합)
  - 음성 피드백 (선택적)
```

### 8. 푸시 알림 & 리텐션

references/notification-retention.md 참조

```yaml
알림 유형:
  streak_reminder: "오늘 학습 아직 안 했어요! 스트릭이 끊기기 전에 1문제만 풀어볼까요?"
  streak_warning: "스트릭이 끊어지기 4시간 전이에요! 지금 접속하면 유지할 수 있어요"
  achievement: "축하해요! '일주일 전사' 뱃지를 획득했어요!"
  weekly_report: "이번 주 {correct}문제 맞췄어요! 정답률 {accuracy}%"
  challenge: "새로운 주간 챌린지가 시작됐어요!"
  friend_activity: "{friend}님이 {level}레벨을 달성했어요!"

타이밍 최적화:
  - 즉시 알림 X → 15~30분 지연 시 학습 세션 시간 증가
  - 학습 미완료: 저녁 7시~8시 (어린이 학습 피크 타임)
  - 스트릭 경고: 자정 4시간 전
  - 주간 리포트: 일요일 오전
```

### 9. 예측 학습 분석

```typescript
// 위험 학생 감지 (At-Risk Detection)
interface RiskScore {
  studentId: string;
  score: number;           // 0~100 (높을수록 위험)
  factors: RiskFactor[];
}

interface RiskFactor {
  type: 'declining_accuracy' | 'low_engagement' | 'streak_broken' | 'long_absence' | 'speed_decrease';
  severity: 'low' | 'medium' | 'high';
  detail: string;
}

function calculateRiskScore(student: StudentAnalytics): RiskScore {
  let score = 0;
  const factors: RiskFactor[] = [];

  // 정답률 하락 추세
  if (student.accuracyTrend < -10) {
    score += 25;
    factors.push({ type: 'declining_accuracy', severity: 'high', detail: `정답률 ${student.accuracyTrend}% 하락` });
  }

  // 학습 빈도 감소
  if (student.sessionsLastWeek < student.avgSessionsPerWeek * 0.5) {
    score += 20;
    factors.push({ type: 'low_engagement', severity: 'medium', detail: '학습 빈도 50% 이상 감소' });
  }

  // 장기 미접속
  if (student.daysSinceLastActivity > 7) {
    score += 30;
    factors.push({ type: 'long_absence', severity: 'high', detail: `${student.daysSinceLastActivity}일 미접속` });
  }

  // 스트릭 끊김
  if (student.streakBrokenRecently) {
    score += 15;
    factors.push({ type: 'streak_broken', severity: 'low', detail: '스트릭 끊김' });
  }

  return { studentId: student.id, score: Math.min(100, score), factors };
}
```

### 10. 멀티테넌시 (학교/기관)

```yaml
아키텍처:
  - 조직(Organization) = 학교/학원
  - 조직 내 반(Class) 복수 가능
  - 역할: org_admin, teacher, student, parent
  - 데이터 격리: RLS 정책으로 조직별 격리
  - 과금: 조직 단위 구독 (학생 수 기반)

DB 구조:
  organizations:
    - id, name, slug, type (school/academy/individual)
    - plan_id, stripe_customer_id
    - settings (JSON: 커스텀 로고, 색상, 기능 on/off)
  organization_members:
    - org_id, user_id, role
  classes → organization_id 외래키 추가
```

## 환경변수 템플릿

```bash
# ─── Supabase ───
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=

# ─── Stripe ───
STRIPE_SECRET_KEY=
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=
STRIPE_WEBHOOK_SECRET=
STRIPE_PRICE_PREMIUM_MONTHLY=
STRIPE_PRICE_PREMIUM_YEARLY=
STRIPE_PRICE_FAMILY_MONTHLY=
STRIPE_PRICE_SCHOOL_PER_STUDENT=

# ─── App ───
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_APP_NAME=
NEXT_PUBLIC_APP_DESCRIPTION=

# ─── AI ───
ANTHROPIC_API_KEY=
GOOGLE_GENERATIVE_AI_API_KEY=

# ─── Push Notifications ───
NEXT_PUBLIC_VAPID_PUBLIC_KEY=
VAPID_PRIVATE_KEY=

# ─── Analytics (선택) ───
NEXT_PUBLIC_POSTHOG_KEY=
```

## 프로젝트 초기화 명령

```bash
npx create-next-app@latest . --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"
npm install @supabase/supabase-js @supabase/ssr stripe @stripe/stripe-js
npm install motion lucide-react clsx tailwind-merge class-variance-authority
npm install zustand next-intl web-push
npm install -D @types/node @types/web-push
npx shadcn@latest init -d
npx shadcn@latest add button card input label badge dialog sheet tabs avatar dropdown-menu progress toast sonner separator skeleton switch select checkbox radio-group alert-dialog popover command tooltip scroll-area
```

## 사용자 역할 & 권한 매트릭스

| 기능 | 학생 | 교사 | 학부모 | 관리자 | 기관관리자 |
|------|:----:|:----:|:------:|:------:|:----------:|
| 문제 풀기 | O | - | - | O | - |
| AI 튜터 | O | - | - | O | - |
| 진도 확인 (본인) | O | - | - | O | - |
| 오답 복습 (SM-2) | O | - | - | O | - |
| 상점/아바타 | O | - | - | O | - |
| 반 관리 | - | O | - | O | O |
| 학생 진도 조회 | - | O | O* | O | O |
| 위험 학생 알림 | - | O | - | O | O |
| 문제 추가/수정 | - | O | - | O | - |
| 실시간 퀴즈 진행 | - | O | - | O | - |
| 과제 할당 | - | O | - | O | - |
| 결제 관리 | - | - | O | O | O |
| 학부모 리포트 | - | - | O | O | - |
| AI 문제 생성 | - | O | - | O | - |
| 서비스 설정 | - | - | - | O | O |
| 기관 관리 | - | - | - | O | O |

*학부모는 연결된 자녀만

## 빌드 검증 자동화 루프 (Godogen)

scripts/build-verify.md 참조

```
┌─────────────────────────────────────┐
│  1. npx tsc --noEmit               │
│  2. npx next lint                   │
│  3. npm run build                   │
│  ↓                                  │
│  에러? ──Yes──→ 에러 분류 & 자동 수정 │
│  │ No              ↓                │
│  ↓           재빌드 (최대 10회) ─→ ┐│
│  빌드 성공!   ←─────────────────────┘│
│  ✅ 배포 준비 완료                   │
└─────────────────────────────────────┘
```

## 작업 원칙 (강화)

1. **100% 완성 코드** — TODO, PLACEHOLDER, `...` 코드 생략 절대 금지
2. **TypeScript 엄격** — any 금지, 모든 타입 명시, strict: true
3. **보안 우선** — RLS, 환경변수 보호, SQL injection/XSS/CSRF 방지
4. **한국어 UI** — next-intl 기반, 한국어 기본 + 영어 지원 구조
5. **모바일 우선** — 반응형 320px~, 터치 최적화, PWA
6. **접근성** — WCAG 2.2 AA, 44px+ 타겟, 고대비, 키보드, 스크린리더
7. **성능** — 서버 컴포넌트 기본, LazyMotion, 이미지 최적화, 코드 스플리팅
8. **에러 처리** — 사용자 친화적 에러 메시지, fallback UI, error.tsx 모든 레벨
9. **학습 과학** — SM-2 간격반복, 적응형 난이도, 마스터리 기반 진도
10. **리텐션** — 스트릭, 푸시 알림, 주간 리포트, 소셜 기능

## v3 추가 시스템

### 11. PLG (Product-Led Growth) 엔진
references/plg-growth-engine.md 참조
- 즉시 가치 전달 온보딩 (가입→첫 정답 < 3분)
- Freemium → Premium 전환 퍼널 (15-25% 전환율)
- 리퍼럴 프로그램 (학생/학부모/교사 3트랙)
- A/B 테스트 프레임워크 (PostHog)
- 코호트 리텐션 분석 SQL

### 12. 포용적 학습 (Inclusive Learning)
references/inclusive-learning.md 참조
- 마이크로러닝 5분 세션 설계
- 디지털 수학 교구 (수직선, 십진블록, 분수막대, 탱그램 등)
- 학습장애 지원: OpenDyslexic 폰트, ADHD 포커스 모드
- 시각장애 지원: 고대비, 스크린리더, MathML
- 접근성 설정 UI (fontSize, dyslexiaFont, readingGuide, focusMode 등)
- COPPA 2026 아동 보호 (2026.4.22 마감)

### 14. 보안 · 성능 · 모니터링
references/security-performance.md 참조
- @upstash/ratelimit API Rate Limiting (엔드포인트별 차등)
- 콘텐츠 모더레이션 (아동 채팅 안전 필터, 개인정보 차단)
- Sentry Next.js 통합 (에러 추적 + 세션 리플레이)
- K6 부하 테스트 (벤치마크: 193 RPS 단일, 275 RPS 다중)
- 무중단 DB 마이그레이션 (CONCURRENTLY)
- Zod 입력 검증, CSRF/XSS/SQLi 방지

### 15. 교과/대상 확장 (v3.1)
references/curriculum-secondary.md + references/coding-education.md 참조
- 중학교: 수학(방정식~통계), 과학(물질~우주), 영어(문법~에세이)
- 고등학교: 수학I/II, 미적분, 확률통계, 기하 + 수능 대비
- 코딩 교육: 블록코딩(Blockly) → Python(Pyodide) → 알고리즘
- 영어 학습: 회화(스픽), 토익(산타), 수능영어
- 성인/직장인: 자격증, 직무, 평생교육
- 대상별 UI 분기: 초등(56px)/중등(44px)/고등(미니멀)/성인(비즈니스)

### 16. 스킬 구조 (Anthropic 공식 패턴)
- Progressive Disclosure: metadata → SKILL.md → references/
- Pattern A (Markdown Only): 지침 문서
- Pattern B (Scripts): 빌드 검증, 시드 생성
- Pattern C (External APIs): MCP 서버, AI SDK 연동

### 17. 듀오링고 스타일 학습 경로 UX (v3.2 — 실전 검증)
references/duolingo-path-ux.md 참조
- **지그재그 스킬 경로**: 8-cycle offset 패턴으로 시각적 지그재그 경로
- **접기/펼치기 단원**: 현재 단원만 펼침, 나머지 접힘 + "더보기" 버튼
- **단원 복습 체크포인트**: 각 단원 끝에 트로피/복습 노드
- **노드 상태 시각화**: mastered(초록)/current(보라+glow)/learning(파란)/locked(회색)
- **스킬 7-8개/단원**: 개념→연습→심화→연습→실전→도전→활용 패턴
- **연습 스킬 필수**: 2-3개 스킬은 너무 적음 → 연습 단계 반드시 포함

### 18. 오답 재풀기 시스템 (v3.2 — 실전 검증)
references/duolingo-path-ux.md 참조
- **1차 오답 시 해설 숨김**: "아쉬워요! 나중에 다시 풀어볼게요"
- **10문제 완료 후 재풀기**: 틀린 문제만 다시 출제
- **재풀기에서도 오답 시 해설 표시**: 2차 시도이므로 학습 효과 극대화
- **Phase 기반 상태관리**: first_round → retry_intro → retry_round → complete
- **QuestionDisplay에 hideExplanation prop**: 오답 시 해설 렌더링 제어

### 19. 콘텐츠 볼륨 가이드 (v3.2 — 실전 교훈)
- **단원당 스킬 7-8개**: 개념 도입 + 연습 반복 + 심화 + 활용
- **학기당 35+ 스테이지**: 충분한 학습량 확보
- **절차적 문제 생성**: `ensureMinimumPool()`로 문제 부족 시 자동 생성
- **적응형 반복**: 정답률이 안정될 때까지 비슷한 유형 계속 출제
- **선행학습 금지법 준수**: getCurrentSemester()로 학기 필터링

### 20. 배포 환경 다양성 (v3.2)
- **Vercel**: git push → 자동 배포 (기본)
- **Cloudflare Workers**: opennextjs-cloudflare + wrangler deploy (수동)
- **D1 Database**: Cloudflare Workers 환경에서 SQLite 호환 DB
- **주의**: CF Workers 배포 시 git push만으로 자동 배포 안됨

## 교차검증 출처 (확장: 70+)

### Claude 스킬 생태계 (1,200+)
alirezarezvani/claude-skills (205개), ComposioHQ/awesome-claude-skills (78+),
VoltAgent/awesome-agent-skills (1000+), anthropics/skills (공식),
Anthropic Skill Authoring Best Practices (공식 문서)

### SaaS 보일러플레이트 (20개)
Makerkit, supastarter, ShipFast, Nextbase, SaaSBold, ixartz,
Vercel SaaS Starter, LaunchFast, Bedrock, Supaboost,
SaaS-Kit-supabase, SaaSRock, NextJet, Shipped, Cascade,
Builderkit, CMSaaS, Gravity, SaaSCity, Flatlogic Generator

### 에듀테크 서비스 (25개)
밀크T, 아이스크림홈런, 스마트올, 엘리하이, 클래스팅, 토도수학,
Duolingo, Khan Academy, Brilliant, Kahoot!, Prodigy Math,
IXL, Quizlet, Brainly, Photomath, Memrise, Anki, Coursera,
Mathigon/Polypad, Brainingcamp, Visnos, Laxu AI, Khanmigo,
Squirrel AI, DeepTutor

### 학습 과학 (12개)
SM-2, FSRS (Anki 최신), IRT, Ebbinghaus, ADDIE, Bloom's Taxonomy,
ZPD, Mastery Learning, Octalysis 8 Core Drives, Hook Model,
Spaced Practice, Retrieval Practice

### 기술 문서 (20개+)
Next.js 15, Supabase, Stripe, shadcn/ui, Tailwind CSS 4,
Motion, Vercel AI SDK 6, next-intl, Zustand, Workbox 7,
Web Audio API, WCAG 2.2, Web Push API, PostHog, Liveblocks,
OpenDyslexic, react-dnd, FTC COPPA Rule 2026, EU EAA 2026,
Anthropic Skill Best Practices
