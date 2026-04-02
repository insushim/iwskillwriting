# Email Marketing Skill (OpenClaw Style)

> 이메일 마케팅 워크플로우. "이메일", "뉴스레터", "메일링", "이메일 마케팅" 트리거.

## 이메일 유형

### 1. Welcome 시리즈
```
Day 0: 가입 환영 + 시작 가이드
Day 2: 핵심 기능 소개
Day 5: 성공 사례/팁
Day 7: 업그레이드 유도 (선택)
```

### 2. 트랜잭션 이메일
- 가입 확인
- 비밀번호 재설정
- 결제 완료
- 구독 갱신 알림

### 3. 뉴스레터
- 제품 업데이트
- 블로그 콘텐츠
- 업계 소식

### 4. Re-engagement
- 비활성 사용자 복귀 유도
- 할인 제안

## 이메일 구현 (React Email + Resend)

### 설치
```bash
npm install @react-email/components resend
```

### 템플릿 작성
```tsx
// emails/welcome.tsx
import { Html, Head, Body, Container, Text, Button } from '@react-email/components';

export default function WelcomeEmail({ name }: { name: string }) {
  return (
    <Html>
      <Head />
      <Body style={{ fontFamily: 'sans-serif' }}>
        <Container>
          <Text>안녕하세요 {name}님!</Text>
          <Text>서비스에 가입해주셔서 감사합니다.</Text>
          <Button
            href="https://app.example.com/start"
            style={{ background: '#000', color: '#fff', padding: '12px 24px' }}
          >
            시작하기
          </Button>
        </Container>
      </Body>
    </Html>
  );
}
```

### 발송
```typescript
import { Resend } from 'resend';
import WelcomeEmail from '@/emails/welcome';

const resend = new Resend(process.env.RESEND_API_KEY);

await resend.emails.send({
  from: '서비스명 <noreply@example.com>',
  to: user.email,
  subject: '환영합니다!',
  react: WelcomeEmail({ name: user.name }),
});
```

## 이메일 최적화

### 제목 (Subject)
- 50자 이내
- 이모지 활용 (적절히)
- 개인화: "{{name}}님, ..."
- 긴급성/호기심 유발

### 본문
- 짧게 (150단어 이내)
- 단일 CTA
- 모바일 최적화

### 발송 시간
- B2B: 화-목, 오전 10시
- B2C: 주말, 저녁

## 자동화 시퀀스

```typescript
// 드립 캠페인
const welcomeSequence = [
  { delay: 0, template: 'welcome' },
  { delay: 2 * DAY, template: 'features' },
  { delay: 5 * DAY, template: 'tips' },
  { delay: 7 * DAY, template: 'upgrade' },
];

async function sendDripEmail(userId: string) {
  const user = await getUser(userId);
  const daysSinceSignup = getDaysSince(user.createdAt);

  const email = welcomeSequence.find(e => e.delay === daysSinceSignup);
  if (email) {
    await sendEmail(user, email.template);
  }
}
```

## 메트릭스

- **Open Rate**: 20-30% 목표
- **Click Rate**: 2-5% 목표
- **Unsubscribe Rate**: < 0.5%
- **Bounce Rate**: < 2%

## 규정 준수

### 필수 요소
- 발신자 정보
- 구독 취소 링크
- 물리적 주소

### GDPR/개인정보
- 명시적 동의 획득
- 데이터 보관 정책
- 삭제 요청 처리
