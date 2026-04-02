---
name: browser-automation
description: Browser automation with Playwright. "브라우저", "스크린샷", "웹 테스트", "E2E", "크롤링" triggers this.
tools:
  - Bash
  - Read
  - Write
---

# Browser Automation Skill (Playwright)

## Triggers
- "브라우저", "스크린샷", "웹 테스트"
- "E2E", "크롤링", "스크래핑"
- "화면 캡처", "자동화 테스트"

## Setup (On-demand)
```bash
# Install only when needed
npm install -D @playwright/test
npx playwright install chromium
```

## Common Tasks

### Screenshot
```typescript
import { chromium } from 'playwright';

async function takeScreenshot(url: string, path: string) {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto(url);
  await page.screenshot({ path, fullPage: true });
  await browser.close();
}
```

### E2E Test
```typescript
// e2e/example.spec.ts
import { test, expect } from '@playwright/test';

test('homepage loads', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveTitle(/My App/);
  await expect(page.getByRole('heading')).toBeVisible();
});

test('login flow', async ({ page }) => {
  await page.goto('/login');
  await page.fill('[name="email"]', 'test@example.com');
  await page.fill('[name="password"]', 'password123');
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL('/dashboard');
});
```

### Web Scraping
```typescript
async function scrapeData(url: string) {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto(url);

  const data = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('.item')).map(el => ({
      title: el.querySelector('h2')?.textContent,
      price: el.querySelector('.price')?.textContent,
    }));
  });

  await browser.close();
  return data;
}
```

### Responsive Testing
```typescript
const devices = [
  { name: 'Mobile', width: 375, height: 667 },
  { name: 'Tablet', width: 768, height: 1024 },
  { name: 'Desktop', width: 1920, height: 1080 },
];

for (const device of devices) {
  await page.setViewportSize({ width: device.width, height: device.height });
  await page.screenshot({ path: `screenshot-${device.name}.png` });
}
```

## Commands
```bash
# Run tests
npx playwright test

# UI mode
npx playwright test --ui

# Specific test
npx playwright test login.spec.ts

# Generate test
npx playwright codegen localhost:3000
```

## Token Saving
This skill loads Playwright only when explicitly requested, avoiding constant MCP server overhead.
