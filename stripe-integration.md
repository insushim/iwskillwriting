# Stripe Integration Skill

> Stripe 결제 연동. "결제", "Stripe", "구독", "billing", "payment" 트리거.

## Stripe 설정 가이드

### 1. 설치
```bash
npm install stripe @stripe/stripe-js
```

### 2. 환경변수
```env
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

### 3. 서버 설정 (Next.js App Router)
```typescript
// lib/stripe.ts
import Stripe from 'stripe';

export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2023-10-16',
});
```

## 결제 플로우

### Checkout Session 생성
```typescript
// app/api/checkout/route.ts
import { stripe } from '@/lib/stripe';
import { NextResponse } from 'next/server';

export async function POST(req: Request) {
  const { priceId, userId } = await req.json();

  const session = await stripe.checkout.sessions.create({
    mode: 'subscription',
    payment_method_types: ['card'],
    line_items: [{ price: priceId, quantity: 1 }],
    success_url: `${process.env.NEXT_PUBLIC_URL}/success?session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: `${process.env.NEXT_PUBLIC_URL}/pricing`,
    client_reference_id: userId,
    metadata: { userId },
  });

  return NextResponse.json({ url: session.url });
}
```

### 웹훅 처리
```typescript
// app/api/webhook/stripe/route.ts
import { stripe } from '@/lib/stripe';
import { headers } from 'next/headers';

export async function POST(req: Request) {
  const body = await req.text();
  const signature = headers().get('stripe-signature')!;

  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(
      body,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET!
    );
  } catch (err) {
    return new Response('Webhook Error', { status: 400 });
  }

  switch (event.type) {
    case 'checkout.session.completed':
      const session = event.data.object;
      // 구독 활성화 처리
      await activateSubscription(session.client_reference_id);
      break;
    case 'invoice.payment_succeeded':
      // 결제 성공 처리
      break;
    case 'customer.subscription.deleted':
      // 구독 취소 처리
      break;
  }

  return new Response('OK');
}
```

### 클라이언트 결제 버튼
```tsx
'use client';

export function CheckoutButton({ priceId }: { priceId: string }) {
  const handleCheckout = async () => {
    const res = await fetch('/api/checkout', {
      method: 'POST',
      body: JSON.stringify({ priceId }),
    });
    const { url } = await res.json();
    window.location.href = url;
  };

  return <button onClick={handleCheckout}>구독하기</button>;
}
```

## Customer Portal (구독 관리)
```typescript
// 고객 포털 세션 생성
const portalSession = await stripe.billingPortal.sessions.create({
  customer: customerId,
  return_url: `${process.env.NEXT_PUBLIC_URL}/dashboard`,
});
```

## 테스트 카드
- 성공: `4242 4242 4242 4242`
- 실패: `4000 0000 0000 0002`
- 3D Secure: `4000 0025 0000 3155`
