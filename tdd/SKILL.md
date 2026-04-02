---
name: tdd-workflow
description: TDD 워크플로우. "테스트", "TDD", "테스트 먼저" 언급 시 자동 활성화.
tools:
  - Read
  - Write
  - Edit
  - Bash
---

# 🧪 TDD 워크플로우 스킬

## 자동 활성화 트리거
- "테스트", "TDD", "테스트 먼저"
- "유닛 테스트", "단위 테스트"
- "테스트 코드", "테스트 작성"

## TDD 사이클

### 1. 🔴 RED - 실패하는 테스트 작성
```typescript
import { describe, it, expect } from 'vitest';

describe('기능명', () => {
  // Arrange
  beforeEach(() => {
    // 설정
  });

  // 정상 케이스
  it('정상적인 입력에 대해 올바른 결과 반환', () => {
    // Arrange
    const input = createTestData();
    
    // Act
    const result = functionUnderTest(input);
    
    // Assert
    expect(result).toEqual(expected);
  });

  // 엣지 케이스
  it('경계값에서도 정상 동작', () => {
    const result = functionUnderTest(boundaryInput);
    expect(result).toBeDefined();
  });

  // 에러 케이스
  it('잘못된 입력에 에러 발생', () => {
    expect(() => functionUnderTest(invalidInput)).toThrow();
  });
});
```

### 2. 🟢 GREEN - 최소한의 코드로 통과
- 테스트를 통과하는 가장 간단한 코드
- 완벽하지 않아도 됨
- 일단 통과만!

### 3. 🔵 REFACTOR - 코드 개선
- 중복 제거
- 가독성 향상
- 테스트 계속 통과 확인

## 테스트 패턴

### 팩토리 함수
```typescript
const createMockUser = (overrides?: Partial<User>): User => ({
  id: 'test-id',
  name: 'Test User',
  email: 'test@example.com',
  ...overrides,
});
```

### 모킹
```typescript
vi.mock('@/services/api', () => ({
  fetchUser: vi.fn(),
}));

beforeEach(() => {
  vi.mocked(fetchUser).mockResolvedValue(mockUser);
});
```

### 비동기 테스트
```typescript
it('비동기 작업 테스트', async () => {
  const result = await asyncFunction();
  expect(result).toBeDefined();
});
```

## 보안 TDD 패턴

### SQL Injection 테스트
```typescript
test('SQL injection 방지', async () => {
  const maliciousInput = "'; DROP TABLE users; --";
  const result = await login(maliciousInput, 'password');
  expect(result.success).toBe(false);
});
```

### XSS 테스트
```typescript
test('XSS 방지', () => {
  const maliciousInput = '<script>alert("xss")</script>';
  const result = sanitize(maliciousInput);
  expect(result).not.toContain('<script>');
});
```

## 실행 명령어
```bash
# 실행
npx vitest run

# 워치 모드
npx vitest

# 커버리지
npx vitest run --coverage
```
