# NextAuth Authentication Skill

> 인증 시스템 구현. "로그인", "인증", "NextAuth", "OAuth", "회원가입" 트리거.

## NextAuth.js v5 설정

### 1. 설치
```bash
npm install next-auth@beta @auth/prisma-adapter
```

### 2. 환경변수
```env
AUTH_SECRET=생성된_시크릿_키
AUTH_URL=http://localhost:3000

# OAuth Providers
AUTH_GOOGLE_ID=
AUTH_GOOGLE_SECRET=
AUTH_GITHUB_ID=
AUTH_GITHUB_SECRET=
```

### 3. Auth 설정
```typescript
// auth.ts
import NextAuth from 'next-auth';
import Google from 'next-auth/providers/google';
import GitHub from 'next-auth/providers/github';
import Credentials from 'next-auth/providers/credentials';
import { PrismaAdapter } from '@auth/prisma-adapter';
import { prisma } from '@/lib/prisma';
import bcrypt from 'bcryptjs';

export const { handlers, auth, signIn, signOut } = NextAuth({
  adapter: PrismaAdapter(prisma),
  providers: [
    Google,
    GitHub,
    Credentials({
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' },
      },
      async authorize(credentials) {
        const user = await prisma.user.findUnique({
          where: { email: credentials.email as string },
        });
        if (!user?.password) return null;

        const isValid = await bcrypt.compare(
          credentials.password as string,
          user.password
        );
        return isValid ? user : null;
      },
    }),
  ],
  callbacks: {
    async session({ session, token }) {
      if (token.sub) session.user.id = token.sub;
      return session;
    },
    async jwt({ token, user }) {
      if (user) token.sub = user.id;
      return token;
    },
  },
  pages: {
    signIn: '/login',
    error: '/login',
  },
});
```

### 4. API Route
```typescript
// app/api/auth/[...nextauth]/route.ts
import { handlers } from '@/auth';
export const { GET, POST } = handlers;
```

### 5. Middleware
```typescript
// middleware.ts
import { auth } from '@/auth';

export default auth((req) => {
  const isLoggedIn = !!req.auth;
  const isAuthPage = req.nextUrl.pathname.startsWith('/login');
  const isProtected = req.nextUrl.pathname.startsWith('/dashboard');

  if (isProtected && !isLoggedIn) {
    return Response.redirect(new URL('/login', req.url));
  }

  if (isAuthPage && isLoggedIn) {
    return Response.redirect(new URL('/dashboard', req.url));
  }
});

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
};
```

## 컴포넌트

### 로그인 폼
```tsx
'use client';
import { signIn } from 'next-auth/react';

export function LoginForm() {
  return (
    <div className="space-y-4">
      <button onClick={() => signIn('google')}>
        Google로 로그인
      </button>
      <button onClick={() => signIn('github')}>
        GitHub으로 로그인
      </button>
    </div>
  );
}
```

### 세션 사용
```tsx
// 서버 컴포넌트
import { auth } from '@/auth';

export default async function Dashboard() {
  const session = await auth();
  if (!session) redirect('/login');

  return <div>Welcome {session.user.name}</div>;
}

// 클라이언트 컴포넌트
'use client';
import { useSession } from 'next-auth/react';

export function Profile() {
  const { data: session } = useSession();
  return <div>{session?.user?.name}</div>;
}
```

## Prisma 스키마
```prisma
model User {
  id            String    @id @default(cuid())
  email         String    @unique
  password      String?
  name          String?
  image         String?
  accounts      Account[]
  sessions      Session[]
}

model Account {
  // NextAuth 표준 스키마
}

model Session {
  // NextAuth 표준 스키마
}
```
