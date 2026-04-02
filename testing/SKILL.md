---
name: testing-workflow
description: Testing workflow. "테스트 작성", "유닛 테스트", "E2E", "테스트 코드" triggers this.
tools:
  - Read
  - Write
  - Edit
  - Bash
---

# Testing Workflow Skill

## Triggers
- "테스트 작성", "유닛 테스트", "테스트 코드"
- "E2E 테스트", "통합 테스트"
- "test", "unit test", "coverage"

## Testing Stack
- Unit/Integration: Vitest + Testing Library
- E2E: Playwright
- Mocking: MSW (Mock Service Worker)

## Unit Test Pattern (Vitest)
```typescript
// src/utils/math.test.ts
import { describe, it, expect, vi } from 'vitest';
import { add, multiply } from './math';

describe('Math utils', () => {
  describe('add', () => {
    it('should add two positive numbers', () => {
      expect(add(1, 2)).toBe(3);
    });

    it('should handle negative numbers', () => {
      expect(add(-1, 1)).toBe(0);
    });
  });
});
```

## Component Test Pattern
```typescript
// src/components/Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './Button';

describe('Button', () => {
  it('renders with text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button')).toHaveTextContent('Click me');
  });

  it('calls onClick when clicked', () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click</Button>);
    fireEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('is disabled when loading', () => {
    render(<Button loading>Submit</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});
```

## E2E Test Pattern (Playwright)
```typescript
// e2e/auth.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Authentication', () => {
  test('user can log in', async ({ page }) => {
    await page.goto('/login');
    await page.fill('[name="email"]', 'user@example.com');
    await page.fill('[name="password"]', 'password123');
    await page.click('button[type="submit"]');

    await expect(page).toHaveURL('/dashboard');
    await expect(page.getByText('Welcome')).toBeVisible();
  });
});
```

## API Mocking (MSW)
```typescript
// mocks/handlers.ts
import { http, HttpResponse } from 'msw';

export const handlers = [
  http.get('/api/users', () => {
    return HttpResponse.json([
      { id: 1, name: 'John' },
      { id: 2, name: 'Jane' },
    ]);
  }),

  http.post('/api/users', async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json({ id: 3, ...body }, { status: 201 });
  }),
];
```

## Commands
```bash
# Run all tests
npm test

# Watch mode
npm test -- --watch

# Coverage
npm test -- --coverage

# E2E
npx playwright test
npx playwright test --ui
```
