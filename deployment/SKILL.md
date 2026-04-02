---
name: deployment-workflow
description: Deployment workflow. "배포", "deploy", "올려줘", "프로덕션" triggers this.
tools:
  - Read
  - Bash
---

# Deployment Workflow Skill

## Triggers
- "배포", "배포해줘", "올려줘"
- "deploy", "프로덕션", "라이브"
- "Vercel", "Netlify"

## Pre-deployment Checklist
```yaml
essential:
  - [ ] npm run build succeeds
  - [ ] No TypeScript errors
  - [ ] No ESLint errors
  - [ ] Tests pass
  - [ ] Environment variables set

recommended:
  - [ ] Bundle size acceptable
  - [ ] Lighthouse score > 90
  - [ ] Mobile responsive
  - [ ] Error boundaries in place
```

## Vercel Deployment

### CLI Commands
```bash
# Login
vercel login

# Preview deployment
vercel

# Production deployment
vercel --prod

# With environment variables
vercel --prod --env DATABASE_URL=xxx
```

### Environment Variables
```bash
# Add env var
vercel env add DATABASE_URL production

# List env vars
vercel env ls

# Pull env to local
vercel env pull .env.local
```

### vercel.json Configuration
```json
{
  "framework": "nextjs",
  "regions": ["icn1"],
  "env": {
    "NEXT_PUBLIC_APP_URL": "https://myapp.vercel.app"
  },
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "X-Frame-Options", "value": "DENY" }
      ]
    }
  ]
}
```

## Netlify Deployment
```bash
# Install CLI
npm install -g netlify-cli

# Login
netlify login

# Deploy
netlify deploy

# Production
netlify deploy --prod
```

## Docker Deployment
```dockerfile
# Dockerfile
FROM node:20-alpine AS base

FROM base AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM base AS runner
WORKDIR /app
ENV NODE_ENV production
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3000
ENV PORT 3000
CMD ["node", "server.js"]
```

## Post-deployment
```yaml
verify:
  - [ ] Site loads correctly
  - [ ] All routes work
  - [ ] API endpoints respond
  - [ ] Auth flow works
  - [ ] No console errors
```
