---
name: pricing-strategy
description: SaaS pricing strategy and implementation. "가격", "pricing", "요금제", "구독" triggers this.
tools:
  - Read
  - Write
  - Edit
---

# Pricing Strategy Skill

## Triggers
- "가격", "요금제", "가격 정책"
- "pricing", "구독", "플랜"
- "subscription", "tier"

## Pricing Models

### Flat-Rate
```yaml
example: $29/month for everything
pros:
  - Simple to understand
  - Predictable revenue
cons:
  - No room for expansion
  - May underprice or overprice
best_for: Simple products, early stage
```

### Tiered Pricing
```yaml
example:
  starter: $9/mo (basic features)
  pro: $29/mo (most features)
  enterprise: Custom (all features + support)
pros:
  - Captures different segments
  - Natural upgrade path
cons:
  - Complexity in feature allocation
best_for: Most SaaS products
```

### Usage-Based
```yaml
example: $0.01 per API call
pros:
  - Fair pricing
  - Scales with customer success
cons:
  - Unpredictable revenue
  - Hard to forecast costs
best_for: APIs, infrastructure
```

### Per-Seat
```yaml
example: $10/user/month
pros:
  - Scales with organization
  - Easy to understand
cons:
  - Discourages adoption
  - User management overhead
best_for: B2B collaboration tools
```

## Pricing Page Component
```tsx
'use client';

import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '@/components/ui/card';
import { Check } from 'lucide-react';

const plans = [
  {
    name: 'Starter',
    price: 9,
    description: 'Perfect for individuals',
    features: [
      '5 projects',
      '1 team member',
      '5GB storage',
      'Email support',
    ],
    cta: 'Start Free Trial',
    popular: false,
  },
  {
    name: 'Pro',
    price: 29,
    description: 'Best for growing teams',
    features: [
      'Unlimited projects',
      '10 team members',
      '100GB storage',
      'Priority support',
      'Advanced analytics',
      'API access',
    ],
    cta: 'Start Free Trial',
    popular: true,
  },
  {
    name: 'Enterprise',
    price: null,
    description: 'For large organizations',
    features: [
      'Everything in Pro',
      'Unlimited team members',
      'Unlimited storage',
      'Dedicated support',
      'Custom integrations',
      'SLA guarantee',
      'SSO/SAML',
    ],
    cta: 'Contact Sales',
    popular: false,
  },
];

export function PricingSection() {
  return (
    <section className="py-20">
      <div className="container mx-auto px-4">
        <h2 className="text-3xl font-bold text-center mb-4">
          Simple, transparent pricing
        </h2>
        <p className="text-center text-muted-foreground mb-12">
          No hidden fees. Cancel anytime.
        </p>

        <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          {plans.map((plan) => (
            <Card
              key={plan.name}
              className={plan.popular ? 'border-primary shadow-lg relative' : ''}
            >
              {plan.popular && (
                <div className="absolute -top-3 left-1/2 -translate-x-1/2">
                  <span className="bg-primary text-primary-foreground text-sm px-3 py-1 rounded-full">
                    Most Popular
                  </span>
                </div>
              )}

              <CardHeader>
                <CardTitle>{plan.name}</CardTitle>
                <CardDescription>{plan.description}</CardDescription>
                <div className="mt-4">
                  {plan.price ? (
                    <span className="text-4xl font-bold">${plan.price}</span>
                  ) : (
                    <span className="text-4xl font-bold">Custom</span>
                  )}
                  {plan.price && <span className="text-muted-foreground">/month</span>}
                </div>
              </CardHeader>

              <CardContent>
                <ul className="space-y-3">
                  {plan.features.map((feature) => (
                    <li key={feature} className="flex items-center gap-2">
                      <Check className="w-4 h-4 text-green-500" />
                      <span>{feature}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>

              <CardFooter>
                <Button
                  className="w-full"
                  variant={plan.popular ? 'default' : 'outline'}
                >
                  {plan.cta}
                </Button>
              </CardFooter>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
```

## Pricing Psychology
```yaml
tactics:
  anchoring: Show highest price first
  decoy: Middle tier looks like best deal
  charm_pricing: $29 instead of $30
  annual_discount: 2 months free yearly

trust_signals:
  - Money-back guarantee
  - No credit card required for trial
  - Cancel anytime
  - Secure payment badges
```

## Stripe Integration
```typescript
// lib/stripe.ts
import Stripe from 'stripe';

export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2023-10-16',
});

// Create checkout session
export async function createCheckoutSession(priceId: string, customerId?: string) {
  return stripe.checkout.sessions.create({
    mode: 'subscription',
    payment_method_types: ['card'],
    line_items: [{ price: priceId, quantity: 1 }],
    success_url: `${process.env.NEXT_PUBLIC_URL}/success?session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: `${process.env.NEXT_PUBLIC_URL}/pricing`,
    customer: customerId,
  });
}
```
