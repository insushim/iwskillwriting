# Database & Prisma Skill

> 데이터베이스 설계/연동. "DB", "데이터베이스", "Prisma", "스키마", "모델" 트리거.

## Prisma 설정

### 1. 설치
```bash
npm install prisma @prisma/client
npx prisma init
```

### 2. 스키마 (SaaS 기본)
```prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

// 사용자
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  image     String?
  password  String?
  role      Role     @default(USER)
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  // Relations
  subscription Subscription?
  accounts     Account[]
  projects     Project[]

  @@index([email])
}

enum Role {
  USER
  ADMIN
}

// 구독 (Stripe 연동)
model Subscription {
  id                 String   @id @default(cuid())
  userId             String   @unique
  user               User     @relation(fields: [userId], references: [id], onDelete: Cascade)

  stripeCustomerId   String   @unique
  stripeSubscriptionId String? @unique
  stripePriceId      String?
  stripeCurrentPeriodEnd DateTime?
  status             SubscriptionStatus @default(INACTIVE)

  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([stripeCustomerId])
}

enum SubscriptionStatus {
  ACTIVE
  INACTIVE
  PAST_DUE
  CANCELED
}

// 프로젝트 (멀티테넌시)
model Project {
  id        String   @id @default(cuid())
  name      String
  slug      String   @unique
  userId    String
  user      User     @relation(fields: [userId], references: [id], onDelete: Cascade)

  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([userId])
  @@index([slug])
}
```

### 3. Prisma Client
```typescript
// lib/prisma.ts
import { PrismaClient } from '@prisma/client';

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

export const prisma = globalForPrisma.prisma ?? new PrismaClient();

if (process.env.NODE_ENV !== 'production') {
  globalForPrisma.prisma = prisma;
}
```

## CRUD 패턴

### Create
```typescript
const user = await prisma.user.create({
  data: {
    email: 'user@example.com',
    name: 'User',
  },
});
```

### Read
```typescript
// 단일 조회
const user = await prisma.user.findUnique({
  where: { id: userId },
  include: { subscription: true },
});

// 목록 조회 (페이지네이션)
const users = await prisma.user.findMany({
  skip: (page - 1) * limit,
  take: limit,
  orderBy: { createdAt: 'desc' },
});
```

### Update
```typescript
const user = await prisma.user.update({
  where: { id: userId },
  data: { name: 'New Name' },
});
```

### Delete
```typescript
await prisma.user.delete({
  where: { id: userId },
});
```

## 마이그레이션
```bash
# 개발 환경
npx prisma migrate dev --name init

# 프로덕션
npx prisma migrate deploy

# 스키마 동기화 (빠른 테스트용)
npx prisma db push

# 시드 데이터
npx prisma db seed
```

## 시드 파일
```typescript
// prisma/seed.ts
import { prisma } from '../lib/prisma';

async function main() {
  await prisma.user.upsert({
    where: { email: 'admin@example.com' },
    update: {},
    create: {
      email: 'admin@example.com',
      name: 'Admin',
      role: 'ADMIN',
    },
  });
}

main();
```

## 트랜잭션
```typescript
const [user, project] = await prisma.$transaction([
  prisma.user.create({ data: { email: 'test@test.com' } }),
  prisma.project.create({ data: { name: 'Project', slug: 'project', userId: 'xxx' } }),
]);
```

## 성능 최적화
```typescript
// select로 필요한 필드만
const users = await prisma.user.findMany({
  select: { id: true, email: true, name: true },
});

// include 대신 select 사용
const user = await prisma.user.findUnique({
  where: { id },
  select: {
    id: true,
    subscription: { select: { status: true } },
  },
});
```
