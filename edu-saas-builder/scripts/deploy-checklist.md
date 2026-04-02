# 배포 체크리스트

> Vercel + Supabase + Stripe 배포 가이드

## Pre-Deployment

### 1. Supabase 설정
```yaml
프로젝트 생성:
  - dashboard.supabase.com → New Project
  - Region: Northeast Asia (ap-northeast-1) — 한국 근접
  - 강력한 DB 비밀번호 설정

마이그레이션:
  - supabase/migrations/001_initial.sql 실행
  - SQL Editor → 시드 데이터 실행

Auth 설정:
  - Authentication → Providers
  - Email: 활성화 (Confirm email: 선택)
  - Google OAuth: Client ID/Secret 설정
  - Site URL: 프로덕션 도메인
  - Redirect URLs: https://yourdomain.com/auth/callback

Storage (선택):
  - 버킷 생성: avatars, problem-images
  - Public 정책 또는 Authenticated 정책 설정

Edge Functions (선택):
  - supabase functions deploy
```

### 2. Stripe 설정
```yaml
제품 생성:
  - Products → Add product
  - "프리미엄 개인" (월 ₩9,900, 연 ₩89,000)
  - "프리미엄 가족" (월 ₩14,900)
  - "학교/기관" (학생당 월 ₩5,000)

웹훅:
  - Developers → Webhooks → Add endpoint
  - URL: https://yourdomain.com/api/stripe/webhook
  - Events:
    - checkout.session.completed
    - customer.subscription.updated
    - customer.subscription.deleted
    - invoice.payment_succeeded
    - invoice.payment_failed

Customer Portal:
  - Settings → Billing → Customer portal
  - 구독 변경/취소 허용 설정
```

### 3. Vercel 설정
```yaml
프로젝트 연결:
  - vercel.com → Import Git Repository
  - Framework: Next.js
  - Build Command: npm run build
  - Output Directory: .next

환경변수:
  - NEXT_PUBLIC_SUPABASE_URL
  - NEXT_PUBLIC_SUPABASE_ANON_KEY
  - SUPABASE_SERVICE_ROLE_KEY
  - STRIPE_SECRET_KEY
  - NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY
  - STRIPE_WEBHOOK_SECRET
  - NEXT_PUBLIC_APP_URL (프로덕션 도메인)
  - NEXT_PUBLIC_APP_NAME

도메인:
  - Settings → Domains → 커스텀 도메인 추가
  - DNS: CNAME → cname.vercel-dns.com
```

## Post-Deployment 체크

```yaml
기능 테스트:
  - [ ] 랜딩 페이지 로드
  - [ ] 회원가입 (이메일)
  - [ ] 로그인
  - [ ] 학생 대시보드 접근
  - [ ] 문제 풀기 플로우
  - [ ] XP/레벨 업데이트
  - [ ] 뱃지 획득
  - [ ] 스트릭 카운트
  - [ ] 랭킹 표시
  - [ ] 상점 아이템 구매
  - [ ] 오답 노트 생성
  - [ ] Stripe 결제 (테스트 카드: 4242...)
  - [ ] 교사 대시보드
  - [ ] 학부모 리포트
  - [ ] 모바일 반응형

성능:
  - [ ] Lighthouse 점수 90+
  - [ ] Core Web Vitals 통과
  - [ ] 이미지 최적화

보안:
  - [ ] HTTPS 적용됨
  - [ ] 환경변수 노출 없음
  - [ ] RLS 정책 동작 확인
  - [ ] API 라우트 인증 확인

PWA:
  - [ ] manifest.json 로드
  - [ ] Service Worker 등록
  - [ ] 오프라인 기본 페이지
  - [ ] 모바일 홈 화면 추가 가능
```

## 모니터링 (선택)

```yaml
에러 추적:
  - Sentry (sentry.io) — 무료 티어
  - npm install @sentry/nextjs

분석:
  - Google Analytics 4
  - PostHog (posthog.com) — 오픈소스, 셀프 호스팅 가능
  - Vercel Analytics (내장)

업타임:
  - UptimeRobot (uptimerobot.com) — 무료
  - Better Uptime (betterstack.com)
```
