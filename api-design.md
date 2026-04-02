# API Design Skill

> API 설계 및 구현. "API", "엔드포인트", "REST", "라우트" 트리거.

## Next.js App Router API

### 기본 구조
```
app/
├── api/
│   ├── users/
│   │   ├── route.ts          # GET /api/users, POST /api/users
│   │   └── [id]/
│   │       └── route.ts      # GET/PUT/DELETE /api/users/:id
│   ├── projects/
│   │   └── route.ts
│   └── webhook/
│       └── stripe/
│           └── route.ts
```

### CRUD API 패턴
```typescript
// app/api/users/route.ts
import { prisma } from '@/lib/prisma';
import { NextResponse } from 'next/server';
import { auth } from '@/auth';

// GET /api/users
export async function GET(req: Request) {
  const session = await auth();
  if (!session) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const { searchParams } = new URL(req.url);
  const page = parseInt(searchParams.get('page') || '1');
  const limit = parseInt(searchParams.get('limit') || '10');

  const [users, total] = await Promise.all([
    prisma.user.findMany({
      skip: (page - 1) * limit,
      take: limit,
      select: { id: true, email: true, name: true, createdAt: true },
    }),
    prisma.user.count(),
  ]);

  return NextResponse.json({
    data: users,
    pagination: {
      page,
      limit,
      total,
      totalPages: Math.ceil(total / limit),
    },
  });
}

// POST /api/users
export async function POST(req: Request) {
  try {
    const body = await req.json();

    // Validation
    if (!body.email) {
      return NextResponse.json(
        { error: 'Email is required' },
        { status: 400 }
      );
    }

    const user = await prisma.user.create({
      data: { email: body.email, name: body.name },
    });

    return NextResponse.json(user, { status: 201 });
  } catch (error) {
    return NextResponse.json(
      { error: 'Internal Server Error' },
      { status: 500 }
    );
  }
}
```

### 동적 라우트
```typescript
// app/api/users/[id]/route.ts
import { prisma } from '@/lib/prisma';
import { NextResponse } from 'next/server';

type Params = { params: { id: string } };

// GET /api/users/:id
export async function GET(req: Request, { params }: Params) {
  const user = await prisma.user.findUnique({
    where: { id: params.id },
  });

  if (!user) {
    return NextResponse.json({ error: 'Not found' }, { status: 404 });
  }

  return NextResponse.json(user);
}

// PUT /api/users/:id
export async function PUT(req: Request, { params }: Params) {
  const body = await req.json();

  const user = await prisma.user.update({
    where: { id: params.id },
    data: body,
  });

  return NextResponse.json(user);
}

// DELETE /api/users/:id
export async function DELETE(req: Request, { params }: Params) {
  await prisma.user.delete({
    where: { id: params.id },
  });

  return new Response(null, { status: 204 });
}
```

## 입력 검증 (Zod)

```typescript
import { z } from 'zod';

const createUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2).max(50).optional(),
  password: z.string().min(8).optional(),
});

export async function POST(req: Request) {
  const body = await req.json();

  const result = createUserSchema.safeParse(body);
  if (!result.success) {
    return NextResponse.json(
      { error: 'Validation Error', details: result.error.flatten() },
      { status: 400 }
    );
  }

  // result.data 사용
}
```

## 에러 핸들링

```typescript
// lib/api-error.ts
export class ApiError extends Error {
  constructor(
    public statusCode: number,
    message: string
  ) {
    super(message);
  }
}

// 사용
export async function GET() {
  try {
    // 로직
  } catch (error) {
    if (error instanceof ApiError) {
      return NextResponse.json(
        { error: error.message },
        { status: error.statusCode }
      );
    }
    return NextResponse.json(
      { error: 'Internal Server Error' },
      { status: 500 }
    );
  }
}
```

## Rate Limiting

```typescript
import { Ratelimit } from '@upstash/ratelimit';
import { Redis } from '@upstash/redis';

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(10, '10 s'),
});

export async function POST(req: Request) {
  const ip = req.headers.get('x-forwarded-for') ?? '127.0.0.1';
  const { success } = await ratelimit.limit(ip);

  if (!success) {
    return NextResponse.json(
      { error: 'Too Many Requests' },
      { status: 429 }
    );
  }

  // 로직 계속
}
```

## 응답 표준화

```typescript
// 성공
{ "data": {...}, "message": "Success" }

// 목록
{ "data": [...], "pagination": { "page": 1, "total": 100 } }

// 에러
{ "error": "에러 메시지", "code": "ERROR_CODE" }
```
