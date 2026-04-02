# Browser Automation Skill (OpenClaw Style)

> Playwright 기반 브라우저 자동화. "브라우저", "스크린샷", "웹 테스트", "E2E", "크롤링" 트리거.

## 자동 실행 조건
- 사용자가 웹페이지 조작 요청
- 스크린샷/캡처 요청
- 폼 자동 입력 요청
- 웹 스크래핑 요청

## 실행 단계

### 1. Playwright 설치 확인
```bash
npm list playwright || npm install playwright
npx playwright install chromium
```

### 2. 브라우저 스크립트 생성
```typescript
import { chromium } from 'playwright';

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();

// 작업 수행
await page.goto('URL');
await page.screenshot({ path: 'screenshot.png' });

await browser.close();
```

### 3. 주요 작업
- **스크린샷**: `page.screenshot({ path: 'name.png', fullPage: true })`
- **클릭**: `page.click('selector')`
- **입력**: `page.fill('input[name="field"]', 'value')`
- **대기**: `page.waitForSelector('selector')`
- **스크래핑**: `page.$$eval('selector', els => els.map(e => e.textContent))`

### 4. E2E 테스트 패턴
```typescript
test('로그인 테스트', async ({ page }) => {
  await page.goto('/login');
  await page.fill('#email', 'test@test.com');
  await page.fill('#password', 'password');
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL('/dashboard');
});
```

## 결과 보고
- 스크린샷 파일 경로
- 추출된 데이터
- 테스트 결과 (pass/fail)
