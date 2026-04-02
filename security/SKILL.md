---
name: security-workflow
description: 보안 검사 및 취약점 수정. "보안", "취약점", "해킹" 언급 시 활성화.
tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# 🔒 보안 워크플로우 스킬

## 자동 활성화 트리거
- "보안", "취약점", "해킹"
- "XSS", "SQL Injection", "CSRF"
- "API 키", "비밀번호", "인증"

## 보안 체크리스트

### 🔴 Critical (즉시 수정)

#### 1. 민감정보 노출
```bash
# API 키, 비밀번호 검색
grep -r "sk-" --include="*.ts" --include="*.tsx" .
grep -r "password" --include="*.ts" --include="*.tsx" .
grep -r "secret" --include="*.ts" --include="*.tsx" .
grep -r "api_key" --include="*.ts" --include="*.tsx" .
```

#### 2. SQL Injection
```typescript
// ❌ 위험
const query = `SELECT * FROM users WHERE id = ${userId}`;

// ✅ 안전
const query = await prisma.user.findUnique({ where: { id: userId } });
```

#### 3. XSS (Cross-Site Scripting)
```typescript
// ❌ 위험
<div dangerouslySetInnerHTML={{ __html: userInput }} />

// ✅ 안전
<div>{sanitizedInput}</div>
```

### 🟠 High (빠른 수정)

#### 4. CSRF 보호
```typescript
// Next.js API Route에서
export async function POST(req: Request) {
  // CSRF 토큰 검증
  const csrfToken = req.headers.get('x-csrf-token');
  if (!validateCsrfToken(csrfToken)) {
    return new Response('Forbidden', { status: 403 });
  }
}
```

#### 5. 인증/인가 확인
```typescript
// 모든 보호된 API에서
const session = await auth();
if (!session?.user) {
  return new Response('Unauthorized', { status: 401 });
}
```

### 🟡 Medium (권장)

#### 6. 입력 검증
```typescript
import { z } from 'zod';

const userSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

// 항상 검증
const validated = userSchema.parse(input);
```

#### 7. Rate Limiting
```typescript
// API 호출 제한
const rateLimiter = new Map();

function checkRateLimit(ip: string): boolean {
  const now = Date.now();
  const windowMs = 60 * 1000; // 1분
  const maxRequests = 100;
  // ... 구현
}
```

## .env 파일 확인
```bash
# .gitignore에 .env 포함 확인
cat .gitignore | grep -E "\.env"

# .env.example만 커밋
ls -la .env*
```

## 의존성 취약점 검사
```bash
# npm audit
npm audit

# pnpm audit
pnpm audit
```

## 출력 형식
```
## 🔒 보안 검사 결과

### 🔴 Critical
| 유형 | 파일:라인 | 문제 | 해결방법 |
|------|-----------|------|----------|

### 🟠 High
| 유형 | 파일:라인 | 문제 | 해결방법 |
|------|-----------|------|----------|

### ✅ 통과 항목
- [ ] 민감정보 노출 없음
- [ ] SQL Injection 방지됨
- [ ] XSS 방지됨
```
