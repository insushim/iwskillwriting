# Security Skill (OpenClaw Style)

> 보안 검사 및 취약점 수정. "보안", "취약점", "인증", "보안 검사" 트리거.

## 자동 보안 검사 항목

### 1. 의존성 취약점
```bash
npm audit
npm audit fix
```

### 2. 코드 보안 스캔
```bash
# Semgrep (권장)
npx @semgrep/semgrep --config auto .

# ESLint 보안 규칙
npx eslint --ext .ts,.tsx . --rule 'security/*'
```

## OWASP Top 10 체크리스트

### A01: Broken Access Control
```typescript
// ❌ Bad
app.get('/admin', (req, res) => showAdmin(res));

// ✅ Good
app.get('/admin', requireAuth, requireRole('admin'), (req, res) => showAdmin(res));
```

### A02: Cryptographic Failures
```typescript
// ❌ Bad
const hash = md5(password);

// ✅ Good
import bcrypt from 'bcrypt';
const hash = await bcrypt.hash(password, 12);
```

### A03: Injection
```typescript
// ❌ SQL Injection
db.query(`SELECT * FROM users WHERE id = ${userId}`);

// ✅ Parameterized Query
db.query('SELECT * FROM users WHERE id = $1', [userId]);
```

### A07: XSS
```typescript
// ❌ Bad
element.innerHTML = userInput;

// ✅ Good
element.textContent = userInput;
// React는 기본적으로 이스케이프됨
```

## 환경변수 보안

### 검사 항목
- `.env`가 `.gitignore`에 포함되어 있는지
- 하드코딩된 시크릿이 없는지
- API 키가 노출되지 않았는지

```bash
# 시크릿 스캔
git secrets --scan
# 또는
npx secretlint "**/*"
```

## 인증/인가 패턴

### JWT 검증
```typescript
import jwt from 'jsonwebtoken';

function verifyToken(token: string) {
  try {
    return jwt.verify(token, process.env.JWT_SECRET!);
  } catch {
    throw new UnauthorizedError();
  }
}
```

### Rate Limiting
```typescript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15분
  max: 100, // 최대 100 요청
});

app.use('/api/', limiter);
```

## 보안 헤더
```typescript
import helmet from 'helmet';
app.use(helmet());
```

## 결과 보고 형식
```
## 보안 검사 결과

### Critical (즉시 수정 필요)
- [ ] 항목 1

### High
- [ ] 항목 2

### Medium
- [ ] 항목 3

### Low
- [ ] 항목 4
```
