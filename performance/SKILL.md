---
name: performance-workflow
description: 성능 최적화. "느려", "성능", "최적화", "빠르게" 언급 시 활성화.
tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
---

# ⚡ 성능 최적화 워크플로우 스킬

## 자동 활성화 트리거
- "느려", "느림", "느린", "답답해"
- "성능", "최적화", "빠르게", "속도"
- "로딩", "렉", "버벅"

## 성능 체크리스트

### 🔴 Critical (즉시 수정)

#### 1. 번들 크기 분석
```bash
# Next.js 번들 분석
npm run build
npx @next/bundle-analyzer
```

#### 2. 불필요한 리렌더링
```typescript
// ❌ 느림
function Component({ items }) {
  const filtered = items.filter(x => x.active); // 매번 실행
  return <List items={filtered} />;
}

// ✅ 빠름
function Component({ items }) {
  const filtered = useMemo(
    () => items.filter(x => x.active),
    [items]
  );
  return <List items={filtered} />;
}
```

#### 3. 무거운 컴포넌트 지연 로딩
```typescript
// ❌ 전체 로딩
import HeavyChart from '@/components/HeavyChart';

// ✅ 지연 로딩
const HeavyChart = dynamic(() => import('@/components/HeavyChart'), {
  loading: () => <Skeleton />,
  ssr: false,
});
```

### 🟠 High (빠른 수정)

#### 4. 이미지 최적화
```typescript
// ❌ 느림
<img src="/large-image.jpg" />

// ✅ 빠름
<Image 
  src="/large-image.jpg"
  width={800}
  height={600}
  placeholder="blur"
  loading="lazy"
/>
```

#### 5. API 요청 최적화
```typescript
// ❌ 여러 번 요청
const user = await fetchUser(id);
const posts = await fetchPosts(id);
const comments = await fetchComments(id);

// ✅ 병렬 요청
const [user, posts, comments] = await Promise.all([
  fetchUser(id),
  fetchPosts(id),
  fetchComments(id),
]);
```

#### 6. React Query 캐싱
```typescript
const { data } = useQuery({
  queryKey: ['users', id],
  queryFn: () => fetchUser(id),
  staleTime: 5 * 60 * 1000, // 5분 캐시
  cacheTime: 30 * 60 * 1000, // 30분 유지
});
```

### 🟡 Medium (권장)

#### 7. 코드 스플리팅
```typescript
// 페이지별 자동 스플리팅 (App Router)
// app/dashboard/page.tsx → 자동 분리

// 컴포넌트 수동 스플리팅
const HeavyComponent = dynamic(() => import('./HeavyComponent'));
```

#### 8. 메모이제이션
```typescript
// 컴포넌트 메모이제이션
const MemoizedComponent = memo(Component);

// 콜백 메모이제이션
const handleClick = useCallback(() => {
  // ...
}, [dependencies]);

// 값 메모이제이션
const expensiveValue = useMemo(() => {
  return computeExpensiveValue(data);
}, [data]);
```

## 성능 측정
```bash
# Lighthouse
npx lighthouse http://localhost:3000 --output html

# 번들 분석
npm run build && npm run analyze
```

## 출력 형식
```
## ⚡ 성능 최적화 결과

### 발견된 이슈
| 심각도 | 유형 | 파일 | 문제 |
|--------|------|------|------|

### 적용된 최적화
- [ ] 번들 사이즈 감소: XX KB → YY KB
- [ ] 불필요한 리렌더링 제거
- [ ] 이미지 최적화 적용

### 성능 지표
- LCP: X.Xs → Y.Ys
- FCP: X.Xs → Y.Ys
```
