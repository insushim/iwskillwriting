# Testing Skill (OpenClaw Style)

> 테스트 작성 및 실행. "테스트 작성", "유닛 테스트", "E2E", "테스트 코드" 트리거.

## 테스트 프레임워크 감지

### 자동 감지
```bash
# package.json에서 확인
- vitest → Vitest 사용
- jest → Jest 사용
- mocha → Mocha 사용
- playwright → Playwright E2E
- cypress → Cypress E2E
```

## Vitest 테스트 (권장)

### 설정
```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node', // 또는 'jsdom'
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html'],
    },
  },
});
```

### 테스트 작성
```typescript
import { describe, it, expect, vi } from 'vitest';

describe('Module', () => {
  it('should work correctly', () => {
    expect(true).toBe(true);
  });

  it('should mock dependencies', () => {
    const mockFn = vi.fn().mockReturnValue('mocked');
    expect(mockFn()).toBe('mocked');
  });
});
```

## Jest 테스트

```typescript
describe('Feature', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('should handle success case', async () => {
    const result = await asyncFunction();
    expect(result).toBeDefined();
  });

  test('should handle error case', async () => {
    await expect(failingFunction()).rejects.toThrow();
  });
});
```

## React 컴포넌트 테스트

```typescript
import { render, screen, fireEvent } from '@testing-library/react';

test('Button click works', () => {
  const onClick = vi.fn();
  render(<Button onClick={onClick}>Click</Button>);

  fireEvent.click(screen.getByText('Click'));
  expect(onClick).toHaveBeenCalledTimes(1);
});
```

## API 테스트

```typescript
import { createMocks } from 'node-mocks-http';

test('API handler', async () => {
  const { req, res } = createMocks({
    method: 'POST',
    body: { data: 'test' },
  });

  await handler(req, res);
  expect(res._getStatusCode()).toBe(200);
});
```

## 실행 명령어
```bash
npm test                    # 전체 실행
npm test -- --watch         # 워치 모드
npm test -- --coverage      # 커버리지
npm test -- path/to/test    # 특정 파일
```
