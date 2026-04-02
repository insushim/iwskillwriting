# TDD Skill (OpenClaw Style)

> 테스트 주도 개발 워크플로우. "테스트", "TDD", "테스트 먼저" 트리거.

## TDD 사이클

```
RED → GREEN → REFACTOR
실패하는 테스트 → 통과시키기 → 리팩토링
```

## 실행 단계

### 1. 테스트 먼저 작성
```typescript
// __tests__/feature.test.ts
describe('기능명', () => {
  it('should 예상 동작', () => {
    // Arrange
    const input = 'test';

    // Act
    const result = targetFunction(input);

    // Assert
    expect(result).toBe('expected');
  });
});
```

### 2. 최소 구현
- 테스트를 통과하는 **최소한의 코드**만 작성
- 하드코딩도 OK (일단 통과시키기)

### 3. 리팩토링
- 중복 제거
- 네이밍 개선
- 구조 개선
- **테스트는 계속 통과해야 함**

## 테스트 유형별 가이드

### 단위 테스트 (Unit)
```typescript
// 순수 함수, 유틸리티
test('calculateTotal', () => {
  expect(calculateTotal([10, 20, 30])).toBe(60);
});
```

### 통합 테스트 (Integration)
```typescript
// API, DB 연동
test('POST /api/users creates user', async () => {
  const res = await request(app)
    .post('/api/users')
    .send({ name: 'Test' });
  expect(res.status).toBe(201);
});
```

### E2E 테스트
```typescript
// 전체 흐름
test('user can complete checkout', async ({ page }) => {
  await page.goto('/products');
  await page.click('[data-testid="add-to-cart"]');
  await page.click('[data-testid="checkout"]');
  await expect(page.locator('.success')).toBeVisible();
});
```

## 커버리지 목표
- 핵심 비즈니스 로직: 90%+
- 유틸리티: 80%+
- UI 컴포넌트: 70%+

## 실행 명령어
```bash
# 테스트 실행
npm test

# 워치 모드
npm test -- --watch

# 커버리지
npm test -- --coverage
```
