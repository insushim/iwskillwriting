---
name: landing-page
description: Landing page creation. "랜딩페이지", "랜딩", "LP", "마케팅 페이지" triggers this.
tools:
  - Read
  - Write
  - Edit
---

# Landing Page Skill

## Triggers
- "랜딩페이지", "랜딩", "LP"
- "마케팅 페이지", "세일즈 페이지"
- "landing page", "conversion page"

## Landing Page Structure

### Above the Fold
```yaml
elements:
  - Navigation (minimal)
  - Headline (clear value proposition)
  - Subheadline (expand on benefit)
  - Hero image/video
  - Primary CTA button
  - Social proof snippet
```

### Problem Section
```yaml
content:
  - Identify pain points (3-5)
  - Empathize with reader
  - Agitate the problem
```

### Solution Section
```yaml
content:
  - Introduce your solution
  - Key features (3-5)
  - Benefits, not features
  - Screenshots/demos
```

### Social Proof
```yaml
types:
  - Customer testimonials (with photos)
  - Company logos
  - Star ratings
  - Case study results
  - User count ("10,000+ users")
```

### Features/Benefits
```yaml
format:
  - Icon + Headline + Description
  - 3-6 features
  - Benefit-focused copy
  - Visual examples
```

### Pricing (Optional)
```yaml
layout:
  - 3 tiers recommended
  - Highlight recommended plan
  - Clear feature comparison
  - Money-back guarantee
```

### FAQ Section
```yaml
content:
  - Common objections
  - How it works questions
  - Pricing questions
  - Support questions
```

### Final CTA
```yaml
elements:
  - Restate value proposition
  - Urgency/scarcity (if authentic)
  - Clear button
  - Risk reversal (guarantee)
```

## React Component Template
```tsx
export function LandingPage() {
  return (
    <main>
      {/* Hero */}
      <section className="min-h-screen flex items-center">
        <div className="container mx-auto px-4">
          <h1 className="text-5xl font-bold mb-4">
            [Clear Value Proposition]
          </h1>
          <p className="text-xl text-muted-foreground mb-8">
            [Subheadline explaining benefit]
          </p>
          <div className="flex gap-4">
            <Button size="lg">Get Started Free</Button>
            <Button size="lg" variant="outline">Watch Demo</Button>
          </div>
          <p className="mt-4 text-sm text-muted-foreground">
            ✓ No credit card required ✓ 14-day free trial
          </p>
        </div>
      </section>

      {/* Social Proof Bar */}
      <section className="py-8 bg-muted">
        <div className="container mx-auto px-4">
          <p className="text-center text-muted-foreground mb-4">
            Trusted by 10,000+ companies
          </p>
          <div className="flex justify-center gap-12">
            {logos.map(logo => <img key={logo} src={logo} />)}
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">
            Everything you need to [outcome]
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            {features.map(f => (
              <Card key={f.title}>
                <CardHeader>
                  <f.icon className="w-10 h-10 mb-4" />
                  <CardTitle>{f.title}</CardTitle>
                </CardHeader>
                <CardContent>{f.description}</CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-20 bg-muted">
        <h2 className="text-3xl font-bold text-center mb-12">
          What our customers say
        </h2>
        {/* Testimonial cards */}
      </section>

      {/* CTA */}
      <section className="py-20">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold mb-4">
            Ready to get started?
          </h2>
          <p className="text-xl text-muted-foreground mb-8">
            Join thousands of satisfied customers today.
          </p>
          <Button size="lg">Start Free Trial</Button>
        </div>
      </section>
    </main>
  );
}
```

## Conversion Checklist
```yaml
must_have:
  - [ ] Clear headline (8 words or less)
  - [ ] Single focused CTA
  - [ ] Social proof visible
  - [ ] Mobile responsive
  - [ ] Fast loading (< 3s)
  - [ ] Trust signals (SSL, guarantees)

nice_to_have:
  - [ ] Video demo
  - [ ] Live chat
  - [ ] Exit intent popup
  - [ ] A/B testing setup
```
