# Error Handling Skill

> 에러 처리. "에러 처리", "예외", "try catch", "에러 핸들링" 트리거.

## 전역 에러 타입

```typescript
// lib/errors.ts
export class AppError extends Error {
  constructor(
    public statusCode: number,
    public code: string,
    message: string
  ) {
    super(message);
    this.name = 'AppError';
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string) {
    super(404, 'NOT_FOUND', `${resource}을(를) 찾을 수 없습니다`);
  }
}

export class UnauthorizedError extends AppError {
  constructor(message = '인증이 필요합니다') {
    super(401, 'UNAUTHORIZED', message);
  }
}

export class ForbiddenError extends AppError {
  constructor(message = '권한이 없습니다') {
    super(403, 'FORBIDDEN', message);
  }
}

export class ValidationError extends AppError {
  constructor(message: string, public details?: any) {
    super(400, 'VALIDATION_ERROR', message);
  }
}

export class ConflictError extends AppError {
  constructor(message: string) {
    super(409, 'CONFLICT', message);
  }
}
```

## API 에러 핸들러

```typescript
// lib/api-handler.ts
import { NextResponse } from 'next/server';
import { AppError } from './errors';
import { ZodError } from 'zod';

type Handler = (req: Request, context?: any) => Promise<Response>;

export function withErrorHandler(handler: Handler): Handler {
  return async (req, context) => {
    try {
      return await handler(req, context);
    } catch (error) {
      console.error('API Error:', error);

      // 커스텀 에러
      if (error instanceof AppError) {
        return NextResponse.json(
          { error: error.message, code: error.code },
          { status: error.statusCode }
        );
      }

      // Zod 검증 에러
      if (error instanceof ZodError) {
        return NextResponse.json(
          { error: 'Validation Error', details: error.flatten() },
          { status: 400 }
        );
      }

      // Prisma 에러
      if (error?.code === 'P2002') {
        return NextResponse.json(
          { error: '이미 존재하는 데이터입니다', code: 'DUPLICATE' },
          { status: 409 }
        );
      }

      if (error?.code === 'P2025') {
        return NextResponse.json(
          { error: '데이터를 찾을 수 없습니다', code: 'NOT_FOUND' },
          { status: 404 }
        );
      }

      // 기타 에러
      return NextResponse.json(
        { error: '서버 오류가 발생했습니다', code: 'INTERNAL_ERROR' },
        { status: 500 }
      );
    }
  };
}
```

### 사용 예시
```typescript
// app/api/users/route.ts
import { withErrorHandler } from '@/lib/api-handler';
import { NotFoundError } from '@/lib/errors';

export const GET = withErrorHandler(async (req) => {
  const user = await prisma.user.findUnique({ where: { id } });

  if (!user) {
    throw new NotFoundError('사용자');
  }

  return NextResponse.json(user);
});
```

## React Error Boundary

```tsx
// components/error-boundary.tsx
'use client';
import { Component, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false };

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, info: any) {
    console.error('Error caught:', error, info);
    // 에러 리포팅 서비스로 전송
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div className="p-4 text-center">
          <h2>문제가 발생했습니다</h2>
          <button onClick={() => this.setState({ hasError: false })}>
            다시 시도
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}
```

## Next.js Error Pages

```tsx
// app/error.tsx
'use client';

export default function Error({
  error,
  reset,
}: {
  error: Error;
  reset: () => void;
}) {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h2 className="text-2xl font-bold mb-4">문제가 발생했습니다</h2>
      <p className="text-gray-600 mb-4">{error.message}</p>
      <button
        onClick={reset}
        className="px-4 py-2 bg-blue-500 text-white rounded"
      >
        다시 시도
      </button>
    </div>
  );
}

// app/not-found.tsx
export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h1 className="text-4xl font-bold">404</h1>
      <p>페이지를 찾을 수 없습니다</p>
    </div>
  );
}
```

## 클라이언트 에러 처리

```typescript
// hooks/use-api.ts
export function useApi<T>(fetcher: () => Promise<T>) {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const execute = async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await fetcher();
      setData(result);
      return result;
    } catch (err: any) {
      const message = err.response?.data?.error || err.message || '오류 발생';
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { data, error, loading, execute };
}
```

## 에러 로깅 (Sentry)

```typescript
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  tracesSampleRate: 1.0,
});

// 에러 캡처
Sentry.captureException(error);

// 컨텍스트 추가
Sentry.setUser({ id: userId, email });
Sentry.setTag('feature', 'checkout');
```
