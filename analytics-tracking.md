# Analytics & Tracking Skill

> 분석 및 추적. "분석", "analytics", "추적", "GA", "이벤트" 트리거.

## Google Analytics 4

### 설치 (Next.js)
```tsx
// app/layout.tsx
import { GoogleAnalytics } from '@next/third-parties/google';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <GoogleAnalytics gaId="G-XXXXXXXXXX" />
      </body>
    </html>
  );
}
```

### 이벤트 트래킹
```typescript
// lib/analytics.ts
export function trackEvent(
  action: string,
  category: string,
  label?: string,
  value?: number
) {
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('event', action, {
      event_category: category,
      event_label: label,
      value,
    });
  }
}

// 전환 추적
export function trackConversion(transactionId: string, value: number) {
  window.gtag?.('event', 'conversion', {
    send_to: 'AW-XXXXXXX/XXXXXX',
    transaction_id: transactionId,
    value,
    currency: 'KRW',
  });
}
```

### 사용 예시
```tsx
import { trackEvent } from '@/lib/analytics';

function CheckoutButton() {
  const handleClick = () => {
    trackEvent('click', 'checkout', 'pricing_page');
    // 결제 로직
  };

  return <button onClick={handleClick}>결제하기</button>;
}
```

## Vercel Analytics

### 설치
```bash
npm install @vercel/analytics @vercel/speed-insights
```

### 설정
```tsx
// app/layout.tsx
import { Analytics } from '@vercel/analytics/react';
import { SpeedInsights } from '@vercel/speed-insights/next';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
        <SpeedInsights />
      </body>
    </html>
  );
}
```

## PostHog (Product Analytics)

### 설치
```bash
npm install posthog-js
```

### 설정
```typescript
// lib/posthog.ts
import posthog from 'posthog-js';

export function initPostHog() {
  if (typeof window !== 'undefined') {
    posthog.init(process.env.NEXT_PUBLIC_POSTHOG_KEY!, {
      api_host: 'https://app.posthog.com',
      loaded: (posthog) => {
        if (process.env.NODE_ENV === 'development') {
          posthog.debug();
        }
      },
    });
  }
}

// 사용자 식별
export function identifyUser(userId: string, properties?: Record<string, any>) {
  posthog.identify(userId, properties);
}

// 이벤트 추적
export function captureEvent(event: string, properties?: Record<string, any>) {
  posthog.capture(event, properties);
}
```

### Provider
```tsx
'use client';
import { useEffect } from 'react';
import { initPostHog } from '@/lib/posthog';

export function PostHogProvider({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    initPostHog();
  }, []);

  return <>{children}</>;
}
```

## SaaS 핵심 이벤트

```typescript
// 사용자 행동 이벤트
const EVENTS = {
  // 인증
  SIGN_UP: 'user_signed_up',
  SIGN_IN: 'user_signed_in',
  SIGN_OUT: 'user_signed_out',

  // 구독
  SUBSCRIPTION_STARTED: 'subscription_started',
  SUBSCRIPTION_CANCELED: 'subscription_canceled',
  SUBSCRIPTION_UPGRADED: 'subscription_upgraded',

  // 기능 사용
  FEATURE_USED: 'feature_used',
  PROJECT_CREATED: 'project_created',
  EXPORT_COMPLETED: 'export_completed',

  // 전환
  PRICING_VIEWED: 'pricing_page_viewed',
  CHECKOUT_STARTED: 'checkout_started',
  CHECKOUT_COMPLETED: 'checkout_completed',
};

// 이벤트 추적 함수
export function trackSaaSEvent(
  event: keyof typeof EVENTS,
  properties?: Record<string, any>
) {
  const eventName = EVENTS[event];

  // GA4
  window.gtag?.('event', eventName, properties);

  // PostHog
  posthog.capture(eventName, properties);
}
```

## 대시보드 데이터

```typescript
// 자체 분석 데이터 저장
model AnalyticsEvent {
  id        String   @id @default(cuid())
  userId    String?
  event     String
  properties Json?
  timestamp DateTime @default(now())
  sessionId String?
  userAgent String?

  @@index([event])
  @@index([userId])
  @@index([timestamp])
}

// 이벤트 저장
export async function logEvent(event: string, userId?: string, properties?: any) {
  await prisma.analyticsEvent.create({
    data: { event, userId, properties },
  });
}
```
