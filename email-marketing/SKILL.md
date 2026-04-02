---
name: email-marketing
description: Email marketing workflow. "이메일", "뉴스레터", "메일링", "이메일 마케팅" triggers this.
tools:
  - Read
  - Write
---

# Email Marketing Skill

## Triggers
- "이메일", "뉴스레터", "메일링"
- "이메일 마케팅", "이메일 캠페인"
- "email", "newsletter"

## Email Types

### Welcome Email
```yaml
structure:
  subject: "Welcome to [Brand] - Here's what's next"
  elements:
    - Warm greeting
    - What to expect
    - Quick win / Getting started
    - CTA to engage
    - Social links
```

### Newsletter
```yaml
structure:
  subject: "[Brand] Weekly: [Key Topic]"
  elements:
    - Featured story / Main content
    - 2-3 secondary stories
    - Tips / Resources
    - Community highlights
    - CTA
```

### Promotional Email
```yaml
structure:
  subject: "[Benefit] - [Offer] [Urgency]"
  elements:
    - Hero image
    - Headline (benefit-focused)
    - Brief description
    - Clear CTA button
    - Social proof
    - P.S. (urgency/bonus)
```

### Transactional Email
```yaml
types:
  - Order confirmation
  - Shipping notification
  - Password reset
  - Account updates

best_practices:
  - Clear subject line
  - Essential info first
  - Action buttons prominent
  - Support contact info
```

## Subject Line Formulas
```yaml
formulas:
  - "How to [achieve result]"
  - "[Number] ways to [benefit]"
  - "You're invited: [event]"
  - "Last chance: [offer]"
  - "[Question]?"
  - "New: [feature/product]"
  - "Did you forget something?"
  - "[First name], [personalized message]"

tips:
  - Keep under 50 characters
  - Avoid spam triggers (FREE, !!!)
  - Test emojis carefully
  - A/B test always
```

## Email Template (React Email)
```tsx
import {
  Html, Head, Body, Container,
  Section, Text, Button, Img
} from '@react-email/components';

export function WelcomeEmail({ name }: { name: string }) {
  return (
    <Html>
      <Head />
      <Body style={main}>
        <Container style={container}>
          <Img src="/logo.png" width="150" alt="Logo" />

          <Section style={content}>
            <Text style={heading}>Welcome, {name}!</Text>
            <Text style={paragraph}>
              We're excited to have you on board.
            </Text>

            <Button style={button} href="https://app.example.com">
              Get Started
            </Button>
          </Section>

          <Text style={footer}>
            © 2025 Company. All rights reserved.
          </Text>
        </Container>
      </Body>
    </Html>
  );
}

const main = { backgroundColor: '#f6f9fc', padding: '40px 0' };
const container = { backgroundColor: '#fff', margin: '0 auto', padding: '40px' };
const heading = { fontSize: '24px', fontWeight: 'bold' };
const paragraph = { fontSize: '16px', lineHeight: '1.6' };
const button = { backgroundColor: '#000', color: '#fff', padding: '12px 24px' };
const footer = { color: '#666', fontSize: '12px' };
```

## Metrics to Track
```yaml
metrics:
  - Open rate (target: 20-25%)
  - Click rate (target: 2-5%)
  - Conversion rate
  - Unsubscribe rate (< 0.5%)
  - Bounce rate (< 2%)
  - Spam complaints (< 0.1%)
```

## Automation Sequences
```yaml
welcome_sequence:
  - Day 0: Welcome + Quick start
  - Day 2: Feature highlight
  - Day 5: Success story / Case study
  - Day 7: Tips & tricks
  - Day 14: Feedback request

abandoned_cart:
  - Hour 1: Reminder
  - Hour 24: Benefits + urgency
  - Hour 72: Discount offer
```
