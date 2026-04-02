# 환경변수 템플릿

## .env.example

```bash
# ================================================
# 교육 SaaS 환경변수
# 이 파일을 .env.local로 복사하여 실제 값을 입력하세요
# ================================================

# ─── Supabase ───
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_ROLE_KEY=eyJ...

# ─── Stripe ───
STRIPE_SECRET_KEY=sk_test_...
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Stripe 가격 ID
STRIPE_PRICE_PREMIUM_MONTHLY=price_...
STRIPE_PRICE_PREMIUM_YEARLY=price_...
STRIPE_PRICE_FAMILY_MONTHLY=price_...
STRIPE_PRICE_SCHOOL_PER_STUDENT=price_...

# ─── 앱 설정 ───
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_APP_NAME=MathHero
NEXT_PUBLIC_APP_DESCRIPTION=초등 수학 학습의 영웅이 되자!

# ─── AI (선택) ───
# Claude API (문제 생성, 힌트)
ANTHROPIC_API_KEY=sk-ant-...

# Google Gemini (대안)
GOOGLE_GENERATIVE_AI_API_KEY=AIza...

# ─── Analytics (선택) ───
NEXT_PUBLIC_GA_ID=G-...
NEXT_PUBLIC_POSTHOG_KEY=phc_...
```

## .env.local 생성 스크립트

```bash
#!/bin/bash
if [ ! -f .env.local ]; then
  cp .env.example .env.local
  echo "✅ .env.local 생성됨. 실제 API 키를 입력하세요."
else
  echo "⚠️ .env.local이 이미 존재합니다."
fi
```

## .gitignore에 필수 포함

```
.env.local
.env.*.local
```
