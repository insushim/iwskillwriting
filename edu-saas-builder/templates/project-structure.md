# 교육 SaaS 프로젝트 구조 템플릿

> Next.js 15 (App Router) + Supabase + Stripe 기반

## 디렉토리 구조

```
project-root/
├── .env.example                  # 환경변수 템플릿
├── .env.local                    # 로컬 환경변수 (gitignore)
├── .eslintrc.json
├── .gitignore
├── next.config.ts
├── package.json
├── tailwind.config.ts
├── tsconfig.json
├── components.json               # shadcn/ui 설정
│
├── public/
│   ├── manifest.json             # PWA 매니페스트
│   ├── sw.js                     # Service Worker
│   ├── icons/                    # PWA 아이콘
│   │   ├── icon-192.png
│   │   └── icon-512.png
│   └── og-image.png              # 소셜 미리보기
│
├── src/
│   ├── app/
│   │   ├── layout.tsx            # 루트 레이아웃
│   │   ├── page.tsx              # 랜딩 페이지
│   │   ├── globals.css           # 글로벌 스타일
│   │   ├── not-found.tsx
│   │   ├── error.tsx
│   │   │
│   │   ├── (marketing)/          # 마케팅 페이지
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx          # 랜딩
│   │   │   ├── pricing/
│   │   │   │   └── page.tsx      # 가격 정책
│   │   │   ├── features/
│   │   │   │   └── page.tsx      # 기능 소개
│   │   │   └── about/
│   │   │       └── page.tsx
│   │   │
│   │   ├── (auth)/               # 인증 페이지
│   │   │   ├── layout.tsx
│   │   │   ├── login/
│   │   │   │   └── page.tsx
│   │   │   ├── signup/
│   │   │   │   └── page.tsx
│   │   │   ├── forgot-password/
│   │   │   │   └── page.tsx
│   │   │   └── callback/
│   │   │       └── route.ts      # OAuth 콜백
│   │   │
│   │   ├── (student)/            # 학생 영역
│   │   │   ├── layout.tsx        # 학생 레이아웃 (사이드바, 네비)
│   │   │   ├── dashboard/
│   │   │   │   └── page.tsx      # 학생 대시보드 (진도, 오늘 할 일)
│   │   │   ├── learn/
│   │   │   │   ├── page.tsx      # 학습 메인 (교과 선택)
│   │   │   │   ├── [subjectId]/
│   │   │   │   │   ├── page.tsx  # 교과 > 단원 목록
│   │   │   │   │   └── [unitId]/
│   │   │   │   │       ├── page.tsx      # 단원 > 문제 세트
│   │   │   │   │       └── [sessionId]/
│   │   │   │   │           └── page.tsx  # 문제 풀이 화면
│   │   │   ├── review/
│   │   │   │   └── page.tsx      # 오답 노트
│   │   │   ├── ranking/
│   │   │   │   └── page.tsx      # 랭킹
│   │   │   ├── shop/
│   │   │   │   └── page.tsx      # 상점
│   │   │   ├── achievements/
│   │   │   │   └── page.tsx      # 뱃지/업적
│   │   │   └── profile/
│   │   │       └── page.tsx      # 마이 프로필
│   │   │
│   │   ├── (teacher)/            # 교사 영역
│   │   │   ├── layout.tsx
│   │   │   ├── dashboard/
│   │   │   │   └── page.tsx      # 교사 대시보드
│   │   │   ├── classes/
│   │   │   │   ├── page.tsx      # 반 목록
│   │   │   │   └── [classId]/
│   │   │   │       ├── page.tsx  # 반 상세 (학생 목록)
│   │   │   │       └── [studentId]/
│   │   │   │           └── page.tsx  # 학생 상세 진도
│   │   │   ├── assignments/
│   │   │   │   ├── page.tsx      # 과제 관리
│   │   │   │   └── new/
│   │   │   │       └── page.tsx  # 과제 생성
│   │   │   ├── problems/
│   │   │   │   ├── page.tsx      # 문제 관리
│   │   │   │   └── new/
│   │   │   │       └── page.tsx  # 문제 생성
│   │   │   └── analytics/
│   │   │       └── page.tsx      # 학습 분석
│   │   │
│   │   ├── (parent)/             # 학부모 영역
│   │   │   ├── layout.tsx
│   │   │   ├── dashboard/
│   │   │   │   └── page.tsx      # 학부모 대시보드
│   │   │   ├── children/
│   │   │   │   └── [childId]/
│   │   │   │       └── page.tsx  # 자녀 리포트
│   │   │   └── billing/
│   │   │       └── page.tsx      # 결제 관리
│   │   │
│   │   ├── (admin)/              # 관리자 영역
│   │   │   ├── layout.tsx
│   │   │   ├── dashboard/
│   │   │   │   └── page.tsx
│   │   │   ├── users/
│   │   │   │   └── page.tsx
│   │   │   ├── content/
│   │   │   │   └── page.tsx
│   │   │   └── settings/
│   │   │       └── page.tsx
│   │   │
│   │   └── api/                  # API 라우트
│   │       ├── auth/
│   │       │   └── callback/
│   │       │       └── route.ts
│   │       ├── problems/
│   │       │   └── route.ts
│   │       ├── submissions/
│   │       │   └── route.ts
│   │       ├── gamification/
│   │       │   ├── xp/
│   │       │   │   └── route.ts
│   │       │   ├── badges/
│   │       │   │   └── route.ts
│   │       │   └── streak/
│   │       │       └── route.ts
│   │       ├── stripe/
│   │       │   ├── checkout/
│   │       │   │   └── route.ts
│   │       │   ├── webhook/
│   │       │   │   └── route.ts
│   │       │   └── portal/
│   │       │       └── route.ts
│   │       └── reports/
│   │           └── route.ts
│   │
│   ├── components/
│   │   ├── ui/                   # shadcn/ui 컴포넌트
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── input.tsx
│   │   │   ├── badge.tsx
│   │   │   ├── progress.tsx
│   │   │   ├── dialog.tsx
│   │   │   ├── sheet.tsx
│   │   │   ├── tabs.tsx
│   │   │   ├── avatar.tsx
│   │   │   ├── dropdown-menu.tsx
│   │   │   ├── skeleton.tsx
│   │   │   ├── toast.tsx
│   │   │   └── sonner.tsx
│   │   │
│   │   ├── layout/               # 레이아웃 컴포넌트
│   │   │   ├── header.tsx
│   │   │   ├── sidebar.tsx
│   │   │   ├── footer.tsx
│   │   │   ├── mobile-nav.tsx
│   │   │   └── breadcrumb.tsx
│   │   │
│   │   ├── auth/                 # 인증 컴포넌트
│   │   │   ├── login-form.tsx
│   │   │   ├── signup-form.tsx
│   │   │   ├── social-login.tsx
│   │   │   └── auth-guard.tsx
│   │   │
│   │   ├── learning/             # 학습 컴포넌트
│   │   │   ├── problem-card.tsx
│   │   │   ├── problem-solver.tsx
│   │   │   ├── answer-input.tsx
│   │   │   ├── multiple-choice.tsx
│   │   │   ├── feedback-overlay.tsx
│   │   │   ├── hint-panel.tsx
│   │   │   ├── solution-panel.tsx
│   │   │   ├── progress-bar.tsx
│   │   │   ├── session-result.tsx
│   │   │   ├── unit-map.tsx
│   │   │   └── daily-mission.tsx
│   │   │
│   │   ├── gamification/         # 게이미피케이션 컴포넌트
│   │   │   ├── xp-bar.tsx
│   │   │   ├── level-badge.tsx
│   │   │   ├── streak-counter.tsx
│   │   │   ├── coin-display.tsx
│   │   │   ├── badge-card.tsx
│   │   │   ├── badge-unlock-modal.tsx
│   │   │   ├── level-up-modal.tsx
│   │   │   ├── ranking-table.tsx
│   │   │   ├── shop-item.tsx
│   │   │   └── reward-animation.tsx
│   │   │
│   │   ├── dashboard/            # 대시보드 컴포넌트
│   │   │   ├── student-stats.tsx
│   │   │   ├── teacher-overview.tsx
│   │   │   ├── parent-report.tsx
│   │   │   ├── progress-chart.tsx
│   │   │   ├── accuracy-chart.tsx
│   │   │   ├── streak-calendar.tsx
│   │   │   ├── weak-topics.tsx
│   │   │   └── class-summary.tsx
│   │   │
│   │   └── shared/               # 공통 컴포넌트
│   │       ├── loading.tsx
│   │       ├── error-boundary.tsx
│   │       ├── empty-state.tsx
│   │       ├── confirm-dialog.tsx
│   │       └── theme-toggle.tsx
│   │
│   ├── lib/                      # 유틸리티
│   │   ├── supabase/
│   │   │   ├── client.ts         # 브라우저 클라이언트
│   │   │   ├── server.ts         # 서버 클라이언트
│   │   │   ├── middleware.ts     # 미들웨어 클라이언트
│   │   │   └── admin.ts          # 서비스롤 클라이언트
│   │   ├── stripe/
│   │   │   ├── client.ts         # Stripe 인스턴스
│   │   │   ├── pricing.ts        # 가격 정책 상수
│   │   │   └── helpers.ts        # 구독 관련 헬퍼
│   │   ├── audio/
│   │   │   └── sound-effects.ts  # Web Audio API 효과음
│   │   ├── gamification/
│   │   │   ├── xp-calculator.ts  # XP 계산 로직
│   │   │   ├── level-system.ts   # 레벨 시스템
│   │   │   ├── badge-checker.ts  # 뱃지 달성 확인
│   │   │   └── streak-manager.ts # 스트릭 관리
│   │   ├── problems/
│   │   │   ├── generator.ts      # 문제 생성기
│   │   │   ├── grader.ts         # 채점기
│   │   │   └── difficulty.ts     # 난이도 조절
│   │   ├── utils.ts              # cn() 등 공통 유틸
│   │   └── constants.ts          # 상수 정의
│   │
│   ├── hooks/                    # 커스텀 훅
│   │   ├── use-auth.ts
│   │   ├── use-sound.ts
│   │   ├── use-streak.ts
│   │   ├── use-xp.ts
│   │   └── use-timer.ts
│   │
│   ├── types/                    # TypeScript 타입
│   │   ├── database.ts           # Supabase 자동 생성 타입
│   │   ├── auth.ts               # 인증 관련 타입
│   │   ├── problem.ts            # 문제/풀이 타입
│   │   ├── gamification.ts       # 게이미피케이션 타입
│   │   └── stripe.ts             # 결제 관련 타입
│   │
│   ├── stores/                   # 상태 관리 (선택: zustand)
│   │   ├── auth-store.ts
│   │   ├── learning-store.ts
│   │   └── sound-store.ts
│   │
│   └── middleware.ts             # Next.js 미들웨어 (인증 체크)
│
└── supabase/
    ├── migrations/
    │   └── 001_initial.sql       # 초기 스키마
    ├── seed.sql                  # 시드 데이터
    └── config.toml
```

## 라우트 그룹별 미들웨어 체크

```typescript
// middleware.ts
const publicRoutes = ['/', '/pricing', '/features', '/about', '/login', '/signup'];
const studentRoutes = ['/dashboard', '/learn', '/review', '/ranking', '/shop', '/achievements', '/profile'];
const teacherRoutes = ['/teacher'];
const parentRoutes = ['/parent'];
const adminRoutes = ['/admin'];
```

## 핵심 페이지별 컴포넌트 매핑

```yaml
문제 풀이 화면 (/learn/[subjectId]/[unitId]/[sessionId]):
  - problem-solver.tsx (메인 컨테이너)
  - problem-card.tsx (문제 표시)
  - answer-input.tsx 또는 multiple-choice.tsx (답안 입력)
  - hint-panel.tsx (힌트 표시)
  - feedback-overlay.tsx (정답/오답 피드백)
  - progress-bar.tsx (진행 바 1/10)
  - xp-bar.tsx (XP 변화)
  - reward-animation.tsx (보상 이펙트)

학생 대시보드 (/dashboard):
  - student-stats.tsx (오늘 통계)
  - daily-mission.tsx (오늘의 미션)
  - streak-counter.tsx
  - level-badge.tsx
  - coin-display.tsx
  - progress-chart.tsx (주간 학습량)
  - weak-topics.tsx (취약 단원)

교사 대시보드 (/teacher/dashboard):
  - teacher-overview.tsx (반 현황)
  - class-summary.tsx (반별 요약)
  - accuracy-chart.tsx (정답률 추이)
  - streak-calendar.tsx (학습 달력)
```
