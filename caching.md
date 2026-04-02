# Caching Skill

> 캐싱 전략. "캐싱", "캐시", "Redis", "성능" 트리거.

## Next.js 캐싱

### Data Cache (fetch)
```typescript
// 기본 캐싱 (무제한)
const data = await fetch('https://api.example.com/data');

// 시간 기반 재검증
const data = await fetch('https://api.example.com/data', {
  next: { revalidate: 3600 }, // 1시간
});

// 캐시 없음
const data = await fetch('https://api.example.com/data', {
  cache: 'no-store',
});
```

### Route Segment Config
```typescript
// app/api/data/route.ts
export const revalidate = 3600; // 1시간마다 재검증
export const dynamic = 'force-static'; // 정적 생성
```

### unstable_cache (서버 함수)
```typescript
import { unstable_cache } from 'next/cache';

const getCachedUser = unstable_cache(
  async (userId: string) => {
    return prisma.user.findUnique({ where: { id: userId } });
  },
  ['user'],
  { revalidate: 3600, tags: ['user'] }
);

// 사용
const user = await getCachedUser(userId);

// 무효화
import { revalidateTag } from 'next/cache';
revalidateTag('user');
```

## Redis 캐싱

### 설치
```bash
npm install ioredis
```

### 클라이언트
```typescript
// lib/redis.ts
import Redis from 'ioredis';

export const redis = new Redis(process.env.REDIS_URL!);

// 캐시 유틸리티
export async function getOrSetCache<T>(
  key: string,
  fetcher: () => Promise<T>,
  ttl: number = 3600
): Promise<T> {
  const cached = await redis.get(key);
  if (cached) {
    return JSON.parse(cached);
  }

  const data = await fetcher();
  await redis.setex(key, ttl, JSON.stringify(data));
  return data;
}

// 캐시 삭제
export async function invalidateCache(pattern: string) {
  const keys = await redis.keys(pattern);
  if (keys.length > 0) {
    await redis.del(...keys);
  }
}
```

### 사용 예시
```typescript
// 캐시된 데이터 조회
const user = await getOrSetCache(
  `user:${userId}`,
  () => prisma.user.findUnique({ where: { id: userId } }),
  3600 // 1시간
);

// 데이터 변경 시 캐시 무효화
await prisma.user.update({ where: { id: userId }, data });
await invalidateCache(`user:${userId}`);
```

## Upstash Redis (Serverless)

### 설치
```bash
npm install @upstash/redis
```

### 사용
```typescript
import { Redis } from '@upstash/redis';

const redis = new Redis({
  url: process.env.UPSTASH_REDIS_URL!,
  token: process.env.UPSTASH_REDIS_TOKEN!,
});

// 캐시
await redis.set('key', 'value', { ex: 3600 });
const value = await redis.get('key');
```

## React Query 캐싱

```typescript
const { data } = useQuery({
  queryKey: ['user', userId],
  queryFn: () => fetchUser(userId),
  staleTime: 5 * 60 * 1000, // 5분간 fresh
  gcTime: 30 * 60 * 1000, // 30분간 캐시 유지
});
```

## 캐시 전략

### Cache-Aside
```typescript
async function getUser(id: string) {
  // 1. 캐시 확인
  const cached = await redis.get(`user:${id}`);
  if (cached) return JSON.parse(cached);

  // 2. DB 조회
  const user = await prisma.user.findUnique({ where: { id } });

  // 3. 캐시 저장
  await redis.setex(`user:${id}`, 3600, JSON.stringify(user));

  return user;
}
```

### Write-Through
```typescript
async function updateUser(id: string, data: any) {
  // 1. DB 업데이트
  const user = await prisma.user.update({ where: { id }, data });

  // 2. 캐시 업데이트
  await redis.setex(`user:${id}`, 3600, JSON.stringify(user));

  return user;
}
```

### Cache Invalidation 패턴
```typescript
// 태그 기반 무효화
const CACHE_TAGS = {
  user: (id: string) => `user:${id}`,
  userList: () => 'users:list',
  userAll: (id: string) => [`user:${id}`, 'users:list'],
};

async function onUserUpdate(userId: string) {
  const tags = CACHE_TAGS.userAll(userId);
  await Promise.all(tags.map(tag => redis.del(tag)));
}
```

## TTL 가이드
| 데이터 유형 | TTL |
|-------------|-----|
| 사용자 세션 | 24시간 |
| 사용자 프로필 | 1시간 |
| 목록 데이터 | 5분 |
| 설정 데이터 | 1일 |
| 정적 콘텐츠 | 7일 |
