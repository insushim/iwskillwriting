# SaaS Analytics Skill (OpenClaw Style)

> SaaS 분석 및 메트릭. "분석", "메트릭", "대시보드", "KPI" 트리거.

## 핵심 SaaS 메트릭

### 1. MRR (Monthly Recurring Revenue)
```typescript
// 월간 반복 매출
const calculateMRR = (subscriptions: Subscription[]) => {
  return subscriptions.reduce((total, sub) => {
    if (sub.status !== 'active') return total;

    const price = sub.items[0].price;
    const amount = price.unit_amount / 100;

    if (price.recurring.interval === 'year') {
      return total + (amount / 12);
    }
    return total + amount;
  }, 0);
};
```

### 2. ARR (Annual Recurring Revenue)
```typescript
const arr = mrr * 12;
```

### 3. Churn Rate (이탈률)
```typescript
// 월간 이탈률
const churnRate = (canceledCustomers / totalCustomersAtStartOfMonth) * 100;

// 좋은 기준: < 5% (월간)
```

### 4. LTV (Lifetime Value)
```typescript
// 고객 생애 가치
const ltv = arpu / monthlyChurnRate;

// 또는
const avgCustomerLifetimeMonths = 1 / monthlyChurnRate;
const ltv = arpu * avgCustomerLifetimeMonths;
```

### 5. CAC (Customer Acquisition Cost)
```typescript
// 고객 획득 비용
const cac = totalMarketingSpend / newCustomersAcquired;

// LTV:CAC 비율 > 3:1 이상이어야 건강
```

### 6. ARPU (Average Revenue Per User)
```typescript
const arpu = mrr / activeSubscribers;
```

## 대시보드 구현

### 데이터 수집
```typescript
// Stripe에서 데이터 가져오기
async function getMetrics() {
  const [subscriptions, customers, invoices] = await Promise.all([
    stripe.subscriptions.list({ status: 'active', limit: 100 }),
    stripe.customers.list({ limit: 100 }),
    stripe.invoices.list({ limit: 100 }),
  ]);

  return {
    mrr: calculateMRR(subscriptions.data),
    totalCustomers: customers.data.length,
    activeSubscribers: subscriptions.data.length,
    revenue: invoices.data.reduce((sum, inv) => sum + inv.amount_paid, 0),
  };
}
```

### 시각화 (Chart.js / Recharts)
```tsx
import { LineChart, Line, XAxis, YAxis, Tooltip } from 'recharts';

<LineChart data={mrrHistory}>
  <XAxis dataKey="month" />
  <YAxis />
  <Tooltip />
  <Line type="monotone" dataKey="mrr" stroke="#8884d8" />
</LineChart>
```

## 분석 도구 연동

### Google Analytics 4
```typescript
// gtag 이벤트
gtag('event', 'purchase', {
  transaction_id: 'T12345',
  value: 19.99,
  currency: 'USD',
});
```

### Mixpanel
```typescript
mixpanel.track('Subscription Created', {
  plan: 'pro',
  price: 19,
  interval: 'month',
});
```

### PostHog
```typescript
posthog.capture('subscription_created', {
  plan: 'pro',
  mrr_impact: 19,
});
```

## 코호트 분석

```typescript
// 월별 가입자 유지율
const cohortAnalysis = {
  '2024-01': { month0: 100, month1: 85, month2: 75, month3: 70 },
  '2024-02': { month0: 100, month1: 88, month2: 78 },
  '2024-03': { month0: 100, month1: 82 },
};
```

## 알림 설정

```typescript
// MRR 변동 알림
if (mrrChange < -10) {
  await sendSlackAlert(`⚠️ MRR이 ${mrrChange}% 감소했습니다!`);
}

// 이탈 예측
if (daysSinceLastLogin > 14) {
  await sendEmail(user, 'We miss you!');
}
```
