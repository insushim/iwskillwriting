# Performance Skill (OpenClaw Style)

> 성능 최적화. "느려", "성능", "최적화", "빠르게" 트리거.

## 자동 성능 분석

### 1. 번들 분석
```bash
# Next.js
ANALYZE=true npm run build

# Vite
npx vite-bundle-visualizer

# Webpack
npx webpack-bundle-analyzer stats.json
```

### 2. Lighthouse 점수
```bash
npx lighthouse https://your-site.com --output json --output-path ./report.json
```

## 프론트엔드 최적화

### 이미지 최적화
```typescript
// Next.js Image
import Image from 'next/image';
<Image src="/photo.jpg" width={800} height={600} loading="lazy" />

// 포맷 변환
// .jpg/.png → .webp/.avif
```

### 코드 스플리팅
```typescript
// Dynamic Import
const HeavyComponent = dynamic(() => import('./Heavy'), {
  loading: () => <Spinner />,
  ssr: false,
});

// React.lazy
const LazyComponent = React.lazy(() => import('./Component'));
```

### 메모이제이션
```typescript
// useMemo - 계산 결과 캐싱
const computed = useMemo(() => expensiveCalc(data), [data]);

// useCallback - 함수 캐싱
const handler = useCallback(() => doSomething(id), [id]);

// React.memo - 컴포넌트 캐싱
const MemoizedComponent = React.memo(Component);
```

## 백엔드 최적화

### DB 쿼리 최적화
```typescript
// ❌ N+1 문제
const users = await prisma.user.findMany();
for (const user of users) {
  const posts = await prisma.post.findMany({ where: { userId: user.id } });
}

// ✅ Include로 해결
const users = await prisma.user.findMany({
  include: { posts: true },
});
```

### 인덱스 추가
```prisma
model Post {
  id        Int @id
  authorId  Int
  createdAt DateTime

  @@index([authorId])
  @@index([createdAt])
}
```

### 캐싱
```typescript
import { Redis } from 'ioredis';
const redis = new Redis();

async function getCached<T>(key: string, fetcher: () => Promise<T>, ttl = 3600): Promise<T> {
  const cached = await redis.get(key);
  if (cached) return JSON.parse(cached);

  const data = await fetcher();
  await redis.setex(key, ttl, JSON.stringify(data));
  return data;
}
```

## 측정 도구

### Web Vitals
```typescript
import { getCLS, getFID, getLCP } from 'web-vitals';

getCLS(console.log);  // Cumulative Layout Shift < 0.1
getFID(console.log);  // First Input Delay < 100ms
getLCP(console.log);  // Largest Contentful Paint < 2.5s
```

### 프로파일링
```bash
# Node.js 프로파일링
node --inspect app.js
# Chrome DevTools에서 분석
```

## 목표 지표
- LCP < 2.5s
- FID < 100ms
- CLS < 0.1
- TTI < 3.8s
- 번들 크기 < 200KB (gzipped)
