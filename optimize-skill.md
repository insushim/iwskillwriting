# ⚡ 최적화 스킬

## 설명
번들 사이즈, 로딩 속도, 렌더링 성능, SEO를 최적화합니다.

## 트리거
- "최적화해줘"
- "성능 개선해줘"
- "번들 줄여줘"
- "속도 높여줘"

## 최적화 항목

### 1. 번들 사이즈
```typescript
// ❌ 전체 import
import { Button, Card, Dialog } from '@/components/ui';

// ✅ 개별 import (트리 쉐이킹)
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
```

```typescript
// ❌ 전체 lodash
import _ from 'lodash';

// ✅ 필요한 함수만
import debounce from 'lodash/debounce';
```

### 2. 이미지 최적화
```tsx
// ✅ next/image 사용
import Image from 'next/image';

<Image
  src="/hero.png"
  alt="Hero"
  width={1200}
  height={630}
  priority // LCP 이미지
  placeholder="blur"
/>
```

### 3. 코드 스플리팅
```typescript
// ✅ 동적 import
import dynamic from 'next/dynamic';

const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <Skeleton />,
  ssr: false,
});
```

### 4. 메모이제이션
```tsx
// ✅ useMemo, useCallback
const expensiveValue = useMemo(() => compute(data), [data]);
const handleClick = useCallback(() => onClick(id), [id, onClick]);

// ✅ React.memo
const MemoizedComponent = React.memo(MyComponent);
```

### 5. SEO
```tsx
// app/layout.tsx
export const metadata: Metadata = {
  title: {
    default: '프로젝트명',
    template: '%s | 프로젝트명',
  },
  description: '설명',
  openGraph: { ... },
  twitter: { ... },
};
```

## 측정 도구
```bash
# 번들 분석
npm run build
ANALYZE=true npm run build

# Lighthouse
npx lighthouse http://localhost:3000 --view

# Web Vitals
npm install web-vitals
```

## 목표 지표
- LCP: < 2.5s
- FID: < 100ms
- CLS: < 0.1
- Lighthouse: 90+
