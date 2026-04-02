# 📚 문서화 스킬

## 설명
README, API 문서, JSDoc 주석, CHANGELOG를 자동 생성합니다.

## 트리거
- "문서 만들어줘"
- "README 작성해줘"
- "API 문서화해줘"
- "주석 달아줘"

## 생성 항목

### README.md
```markdown
# 프로젝트명

> 프로젝트 설명

## 주요 기능
- 기능 1
- 기능 2

## 설치 방법
\`\`\`bash
npm install
\`\`\`

## 사용법
\`\`\`bash
npm run dev
\`\`\`

## 환경 변수
| 변수 | 설명 | 필수 |
|------|------|------|
| DATABASE_URL | DB 연결 | ✅ |

## 기술 스택
- Next.js 15
- TypeScript
- Tailwind CSS

## 라이선스
MIT
```

### JSDoc 주석
```typescript
/**
 * 사용자를 생성합니다.
 * @param {CreateUserInput} input - 사용자 생성 입력
 * @returns {Promise<User>} 생성된 사용자
 * @throws {ValidationError} 입력이 유효하지 않은 경우
 * @example
 * const user = await createUser({ name: 'John', email: 'john@example.com' });
 */
export async function createUser(input: CreateUserInput): Promise<User> {
  // ...
}
```

### API 문서 (OpenAPI)
```yaml
openapi: 3.0.0
info:
  title: API
  version: 1.0.0
paths:
  /api/users:
    post:
      summary: 사용자 생성
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserInput'
      responses:
        '201':
          description: 성공
```

## 규칙
- 정확한 정보 기반
- 예제 코드 포함
- 최신 상태 유지
