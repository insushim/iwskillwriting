# Pricing Skill (OpenClaw Style)

> SaaS 가격 전략 및 구현. "가격", "pricing", "요금제", "구독" 트리거.

## 가격 모델

### 1. 티어 기반 (Tier-based)
```
Free     → $0/월   → 기본 기능
Pro      → $19/월  → 고급 기능
Business → $49/월  → 팀 기능
Enterprise → 문의  → 맞춤형
```

### 2. 사용량 기반 (Usage-based)
```
API 호출당 $0.001
저장 용량 GB당 $0.1
사용자당 $5/월
```

### 3. 하이브리드
```
기본료 $10/월 + 초과 사용량 과금
```

## Stripe 가격 구현

### 상품/가격 생성
```typescript
// 상품 생성
const product = await stripe.products.create({
  name: 'Pro Plan',
  description: '모든 프리미엄 기능',
});

// 가격 생성 (월간)
const monthlyPrice = await stripe.prices.create({
  product: product.id,
  unit_amount: 1900, // $19.00
  currency: 'usd',
  recurring: { interval: 'month' },
});

// 가격 생성 (연간, 할인)
const yearlyPrice = await stripe.prices.create({
  product: product.id,
  unit_amount: 19000, // $190.00 (2개월 무료)
  currency: 'usd',
  recurring: { interval: 'year' },
});
```

### 체크아웃 세션
```typescript
const session = await stripe.checkout.sessions.create({
  mode: 'subscription',
  payment_method_types: ['card'],
  line_items: [{ price: priceId, quantity: 1 }],
  success_url: `${baseUrl}/success?session_id={CHECKOUT_SESSION_ID}`,
  cancel_url: `${baseUrl}/pricing`,
});
```

## 가격 페이지 UI

```tsx
const plans = [
  {
    name: 'Free',
    price: 0,
    features: ['기능1', '기능2'],
    cta: '시작하기',
  },
  {
    name: 'Pro',
    price: 19,
    features: ['Free 포함', '기능3', '기능4'],
    cta: '업그레이드',
    popular: true, // 추천 표시
  },
];

<div className="grid md:grid-cols-3 gap-8">
  {plans.map(plan => (
    <PricingCard key={plan.name} {...plan} />
  ))}
</div>
```

## 가격 전략 팁

### 앵커링
- 가장 비싼 플랜 먼저 보여주기
- 추천 플랜 강조

### 연간 할인
- 월간 대비 20-30% 할인
- "2개월 무료" 표현

### 심리적 가격
- $20 → $19
- $100 → $99

## 메트릭스

```typescript
// MRR 계산
const mrr = subscriptions.reduce((sum, sub) => {
  const amount = sub.items[0].price.unit_amount;
  const interval = sub.items[0].price.recurring.interval;
  return sum + (interval === 'year' ? amount / 12 : amount);
}, 0);

// ARPU
const arpu = mrr / activeSubscribers;

// Churn Rate
const churnRate = canceledThisMonth / totalAtStartOfMonth;
```
