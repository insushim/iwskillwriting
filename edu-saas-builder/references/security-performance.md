# 보안 · 성능 · 모니터링 가이드

> Rate Limiting, COPPA, 콘텐츠 모더레이션, Sentry, 부하 테스트 패턴

## API Rate Limiting

### @upstash/ratelimit (권장)

```typescript
// lib/rate-limit.ts
import { Ratelimit } from '@upstash/ratelimit';
import { Redis } from '@upstash/redis';

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(10, '10 s'), // 10초에 10회
  analytics: true,
});

// API 라우트에서 사용
export async function POST(req: Request) {
  const ip = req.headers.get('x-forwarded-for') ?? '127.0.0.1';
  const { success, limit, remaining } = await ratelimit.limit(ip);

  if (!success) {
    return new Response('Too Many Requests', {
      status: 429,
      headers: {
        'X-RateLimit-Limit': String(limit),
        'X-RateLimit-Remaining': String(remaining),
        'Retry-After': '10',
      },
    });
  }
  // ... 정상 처리
}
```

### 엔드포인트별 제한 설정

```yaml
/api/submissions: 분당 30회 (문제 풀이)
/api/ai/tutor: 분당 10회 (AI 챗봇)
/api/ai/hint: 문제당 3회 (힌트)
/api/ai/generate: 시간당 5회 (문제 생성, 교사만)
/api/stripe/checkout: 분당 3회 (결제)
/api/auth/login: 분당 5회 (로그인 시도)
/api/auth/signup: 시간당 10회 (가입)
```

## 콘텐츠 모더레이션 (아동 안전)

### AI 채팅 안전 필터

```typescript
// AI 튜터 응답 필터링
const BLOCKED_PATTERNS = [
  /개인\s*정보/i,     // 개인정보 요청 감지
  /전화\s*번호/i,
  /주소/i,
  /비밀\s*번호/i,
];

const EDUCATIONAL_SCOPE = [
  '수학', '국어', '영어', '과학', '사회',
  '덧셈', '뺄셈', '곱셈', '나눗셈', '분수',
];

function moderateInput(text: string): { safe: boolean; reason?: string } {
  // 개인정보 요청 차단
  for (const pattern of BLOCKED_PATTERNS) {
    if (pattern.test(text)) {
      return { safe: false, reason: '개인정보 관련 대화는 할 수 없어요.' };
    }
  }

  // 교육 범위 벗어나는 대화 제한
  const isEducational = EDUCATIONAL_SCOPE.some(topic =>
    text.includes(topic)
  );
  if (text.length > 200 && !isEducational) {
    return { safe: false, reason: '학습과 관련된 질문을 해주세요!' };
  }

  return { safe: true };
}

// 학생 간 채팅 모더레이션 (선택 기능)
function moderateChat(message: string): { allowed: boolean; filtered?: string } {
  // 비속어 필터 (한국어)
  // 따돌림/사이버불링 감지
  // URL/링크 차단 (외부 사이트 보호)
  // 전화번호/이메일 마스킹
}
```

## 에러 모니터링 (Sentry)

### Next.js + Sentry 통합

```bash
# 원클릭 설정
npx @sentry/wizard -i nextjs
```

```typescript
// sentry.client.config.ts
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  tracesSampleRate: 0.1,        // 프로덕션: 10% 샘플링
  replaysSessionSampleRate: 0.01, // 세션 리플레이: 1%
  replaysOnErrorSampleRate: 1.0,  // 에러 시: 100% 리플레이
  environment: process.env.NODE_ENV,
});

// 커스텀 에러 태깅
Sentry.setTag('user_role', 'student');
Sentry.setTag('grade', '3');
```

### 핵심 모니터링 지표

```yaml
에러 추적:
  - Unhandled Exceptions
  - API 4xx/5xx 응답률
  - Hydration 에러 (SSR/CSR 불일치)
  - Supabase RLS 거부 (접근 권한 문제)

성능:
  - Core Web Vitals (LCP, FID, CLS)
  - API 응답 시간 (p50, p95, p99)
  - 빌드 번들 크기
  - Supabase 쿼리 시간

비즈니스:
  - 로그인 실패율
  - 결제 실패율
  - AI API 호출 실패율
  - 학습 세션 중단율
```

## 부하 테스트

### K6 부하 테스트 (Grafana)

```javascript
// k6-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 50 },   // ramp up
    { duration: '1m', target: 100 },    // steady
    { duration: '30s', target: 0 },     // ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],   // 95% < 500ms
    http_req_failed: ['rate<0.01'],     // 에러율 < 1%
  },
};

export default function () {
  const res = http.get('https://your-app.vercel.app/api/problems?unit=math-1-1');
  check(res, { 'status 200': (r) => r.status === 200 });
  sleep(1);
}
```

### 성능 벤치마크 (Next.js 참고)

```yaml
단일 인스턴스: ~193 RPS
다중 인스턴스: ~275 RPS (+42%)
Edge Runtime: 더 빠른 cold start

Core Web Vitals 목표:
  LCP: < 2.5s
  FID: < 100ms
  CLS: < 0.1
  TTFB: < 800ms
```

## 데이터베이스 마이그레이션 (무중단)

```yaml
Supabase 마이그레이션 전략:
  1. 버전 관리: supabase/migrations/ 디렉토리
  2. 로컬 테스트: supabase db reset (로컬)
  3. 스테이징 적용: supabase db push (스테이징)
  4. 프로덕션: supabase db push (프로덕션)

무중단 마이그레이션 규칙:
  - 컬럼 추가: 즉시 가능 (NOT NULL 시 DEFAULT 필수)
  - 컬럼 삭제: 코드에서 먼저 제거 → 다음 배포에서 컬럼 삭제
  - 인덱스: CREATE INDEX CONCURRENTLY (락 없이)
  - 타입 변경: 새 컬럼 추가 → 데이터 마이그레이션 → 이전 컬럼 삭제
```

## 보안 체크리스트

```yaml
인증/인가:
  - [ ] Supabase RLS 모든 테이블 활성화
  - [ ] 역할 기반 접근 제어 (RBAC)
  - [ ] JWT 만료 시간 적절 설정 (1시간)
  - [ ] 리프레시 토큰 관리

입력 검증:
  - [ ] Zod 스키마로 모든 API 입력 검증
  - [ ] SQL injection 방지 (파라미터 바인딩)
  - [ ] XSS 방지 (React 기본 이스케이핑)
  - [ ] CSRF 보호 (SameSite 쿠키)

데이터 보호:
  - [ ] 환경변수에 시크릿 저장
  - [ ] HTTPS 강제
  - [ ] Stripe 웹훅 서명 검증
  - [ ] 학생 데이터 최소 수집 (COPPA)
  - [ ] 데이터 보존 기간 정책

모니터링:
  - [ ] Sentry 에러 추적
  - [ ] Rate limiting 모든 API
  - [ ] 비정상 접근 패턴 감지
  - [ ] 로그인 실패 알림
```
