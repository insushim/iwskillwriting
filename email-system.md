# Email System Skill

> 이메일 발송 시스템. "이메일 보내기", "메일 발송", "Resend", "트랜잭션 이메일" 트리거.

## Resend 설정

### 설치
```bash
npm install resend @react-email/components
```

### 환경변수
```env
RESEND_API_KEY=re_...
```

### 클라이언트 설정
```typescript
// lib/resend.ts
import { Resend } from 'resend';

export const resend = new Resend(process.env.RESEND_API_KEY);
```

## 이메일 템플릿 (React Email)

### 환영 이메일
```tsx
// emails/welcome.tsx
import {
  Body,
  Button,
  Container,
  Head,
  Heading,
  Html,
  Preview,
  Section,
  Text,
} from '@react-email/components';

interface WelcomeEmailProps {
  name: string;
  loginUrl: string;
}

export default function WelcomeEmail({ name, loginUrl }: WelcomeEmailProps) {
  return (
    <Html>
      <Head />
      <Preview>{name}님, 가입을 환영합니다!</Preview>
      <Body style={main}>
        <Container style={container}>
          <Heading style={h1}>환영합니다! 👋</Heading>
          <Text style={text}>
            안녕하세요 {name}님, 서비스에 가입해주셔서 감사합니다.
          </Text>
          <Section style={buttonContainer}>
            <Button style={button} href={loginUrl}>
              시작하기
            </Button>
          </Section>
        </Container>
      </Body>
    </Html>
  );
}

const main = { backgroundColor: '#f6f9fc', fontFamily: 'sans-serif' };
const container = { margin: '0 auto', padding: '40px 20px', maxWidth: '560px' };
const h1 = { color: '#1f2937', fontSize: '24px' };
const text = { color: '#4b5563', fontSize: '16px', lineHeight: '24px' };
const buttonContainer = { textAlign: 'center' as const, marginTop: '32px' };
const button = {
  backgroundColor: '#2563eb',
  borderRadius: '8px',
  color: '#fff',
  fontSize: '16px',
  padding: '12px 24px',
  textDecoration: 'none',
};
```

### 비밀번호 재설정
```tsx
// emails/reset-password.tsx
export default function ResetPasswordEmail({ resetUrl }: { resetUrl: string }) {
  return (
    <Html>
      <Head />
      <Preview>비밀번호 재설정 요청</Preview>
      <Body style={main}>
        <Container style={container}>
          <Heading style={h1}>비밀번호 재설정</Heading>
          <Text style={text}>
            아래 버튼을 클릭하여 비밀번호를 재설정하세요.
            이 링크는 1시간 후 만료됩니다.
          </Text>
          <Button style={button} href={resetUrl}>
            비밀번호 재설정
          </Button>
          <Text style={footer}>
            요청하지 않으셨다면 이 이메일을 무시하세요.
          </Text>
        </Container>
      </Body>
    </Html>
  );
}
```

## 이메일 발송

### API Route
```typescript
// app/api/email/welcome/route.ts
import { resend } from '@/lib/resend';
import WelcomeEmail from '@/emails/welcome';
import { NextResponse } from 'next/server';

export async function POST(req: Request) {
  const { email, name } = await req.json();

  try {
    const { data, error } = await resend.emails.send({
      from: '서비스명 <noreply@yourdomain.com>',
      to: email,
      subject: `${name}님, 환영합니다!`,
      react: WelcomeEmail({
        name,
        loginUrl: `${process.env.NEXT_PUBLIC_URL}/login`,
      }),
    });

    if (error) {
      return NextResponse.json({ error }, { status: 400 });
    }

    return NextResponse.json({ id: data?.id });
  } catch (error) {
    return NextResponse.json({ error: 'Failed to send email' }, { status: 500 });
  }
}
```

### 유틸리티 함수
```typescript
// lib/email.ts
import { resend } from './resend';
import WelcomeEmail from '@/emails/welcome';
import ResetPasswordEmail from '@/emails/reset-password';

export async function sendWelcomeEmail(email: string, name: string) {
  return resend.emails.send({
    from: 'Service <noreply@domain.com>',
    to: email,
    subject: `${name}님, 환영합니다!`,
    react: WelcomeEmail({ name, loginUrl: '...' }),
  });
}

export async function sendPasswordResetEmail(email: string, token: string) {
  const resetUrl = `${process.env.NEXT_PUBLIC_URL}/reset-password?token=${token}`;

  return resend.emails.send({
    from: 'Service <noreply@domain.com>',
    to: email,
    subject: '비밀번호 재설정',
    react: ResetPasswordEmail({ resetUrl }),
  });
}
```

## 이메일 미리보기 (개발 환경)

```bash
# React Email 개발 서버
npx email dev
```

## 구독 알림 이메일
```typescript
export async function sendSubscriptionEmail(
  email: string,
  type: 'created' | 'canceled' | 'renewed'
) {
  const subjects = {
    created: '구독이 시작되었습니다',
    canceled: '구독이 취소되었습니다',
    renewed: '구독이 갱신되었습니다',
  };

  return resend.emails.send({
    from: 'Service <noreply@domain.com>',
    to: email,
    subject: subjects[type],
    react: SubscriptionEmail({ type }),
  });
}
```
