---
name: saas-analytics
description: SaaS analytics and metrics. "분석", "메트릭", "대시보드", "KPI" triggers this.
tools:
  - Read
  - Write
  - Edit
---

# SaaS Analytics Skill

## Triggers
- "분석", "메트릭", "대시보드"
- "KPI", "통계", "리포트"
- "analytics", "metrics", "dashboard"

## Key SaaS Metrics

### Revenue Metrics
```yaml
MRR: Monthly Recurring Revenue
  formula: Sum of all monthly subscriptions
  target: Growth 10-20% MoM (early stage)

ARR: Annual Recurring Revenue
  formula: MRR × 12
  use: Long-term planning

ARPU: Average Revenue Per User
  formula: MRR / Total customers

LTV: Lifetime Value
  formula: ARPU × Average customer lifespan (months)

CAC: Customer Acquisition Cost
  formula: Total sales & marketing spend / New customers

LTV:CAC Ratio:
  target: > 3:1 (healthy)
```

### Growth Metrics
```yaml
MoM Growth:
  formula: (This month - Last month) / Last month × 100

Net Revenue Retention (NRR):
  formula: (Starting MRR + Expansion - Contraction - Churn) / Starting MRR
  target: > 100% (great), > 120% (excellent)

Quick Ratio:
  formula: (New MRR + Expansion MRR) / (Churned MRR + Contraction MRR)
  target: > 4 (healthy growth)
```

### Customer Metrics
```yaml
Churn Rate:
  formula: Lost customers / Starting customers × 100
  target: < 5% monthly (B2C), < 2% monthly (B2B)

Retention Rate:
  formula: 100% - Churn Rate

DAU/MAU Ratio:
  formula: Daily Active Users / Monthly Active Users
  target: > 20% (good engagement)

NPS: Net Promoter Score
  formula: % Promoters (9-10) - % Detractors (0-6)
  target: > 50 (excellent)
```

## Dashboard Component
```tsx
'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { TrendingUp, TrendingDown, Users, DollarSign } from 'lucide-react';

interface MetricCardProps {
  title: string;
  value: string;
  change: number;
  changeLabel: string;
}

function MetricCard({ title, value, change, changeLabel }: MetricCardProps) {
  const isPositive = change >= 0;

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle className="text-sm font-medium text-muted-foreground">
          {title}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        <div className={`flex items-center text-sm ${
          isPositive ? 'text-green-600' : 'text-red-600'
        }`}>
          {isPositive ? <TrendingUp className="w-4 h-4 mr-1" /> : <TrendingDown className="w-4 h-4 mr-1" />}
          {Math.abs(change)}% {changeLabel}
        </div>
      </CardContent>
    </Card>
  );
}

export function Dashboard() {
  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      <MetricCard
        title="Monthly Revenue"
        value="$45,231"
        change={12.5}
        changeLabel="from last month"
      />
      <MetricCard
        title="Active Users"
        value="2,350"
        change={8.2}
        changeLabel="from last month"
      />
      <MetricCard
        title="Churn Rate"
        value="2.4%"
        change={-0.3}
        changeLabel="from last month"
      />
      <MetricCard
        title="NPS Score"
        value="67"
        change={5}
        changeLabel="from last quarter"
      />
    </div>
  );
}
```

## Chart Libraries
```yaml
recommended:
  - recharts: Simple, React-native
  - tremor: Dashboard-focused
  - chart.js: Flexible

example_install: npm install recharts
```

## Tracking Setup
```typescript
// lib/analytics.ts
export function trackEvent(name: string, properties?: Record<string, any>) {
  // Send to your analytics provider
  if (typeof window !== 'undefined' && window.analytics) {
    window.analytics.track(name, properties);
  }
}

// Usage
trackEvent('subscription_started', {
  plan: 'pro',
  price: 29,
  trial: true,
});
```
