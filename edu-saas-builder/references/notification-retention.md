# 푸시 알림 & 리텐션 시스템

> Duolingo, 밀크T, Prodigy Math 리텐션 전략 + 행동 심리학 기반

## 리텐션 프레임워크

### Hook Model (Nir Eyal)

```yaml
Trigger (계기):
  외부: 푸시 알림, 이메일, 학부모 리마인더
  내부: 습관 형성 후 자발적 접속 ("매일 학습하는 게 당연")

Action (행동):
  최소 마찰: 앱 열기 → 즉시 오늘의 문제
  단순화: 하루 1문제만 풀어도 스트릭 유지

Variable Reward (가변 보상):
  - 랜덤 보너스 XP
  - 깜짝 뱃지
  - 레어 아이템 드롭
  - 주간 리그 결과

Investment (투자):
  - 스트릭 (잃고 싶지 않은 연속 기록)
  - 레벨/아바타 (쌓아온 것)
  - 친구 관계 (소셜 압력)
```

### 리텐션 타임라인

```yaml
Day 0 (가입):
  - 온보딩 퀴즈 (레벨 테스트) → 맞춤 학습 시작
  - 첫 문제 즉시 풀기 → 즉각 보상 (XP + "첫 발걸음" 뱃지)
  - 목표 설정: "하루 10문제" or "하루 5분"
  - 알림 허용 요청 (가치 설명 후)

Day 1:
  - 알림: "어제 시작한 학습을 이어가볼까요? 🎯"
  - 2일차 보상: 연속 학습 시작!

Day 3:
  - 알림: "3일 연속 학습 중! 🔥 오늘도 이어가요"
  - "3일 연속" 뱃지 획득

Day 7:
  - 주간 리포트 (학부모에게도 발송)
  - 알림: "일주일 전사 뱃지를 획득했어요! 🏆"
  - 주간 리그 첫 참가

Day 14:
  - 알림: "2주 마라톤 달성! 💪"
  - 학습 통계 공유 기능 활성화

Day 30:
  - 월간 리포트 (상세 성장 그래프)
  - 특별 뱃지 + 보너스 코인
  - 학부모 이메일: "자녀의 한 달 학습 성과"

Day 60:
  - 프리미엄 전환 유도 (무료 체험 종료 시)
  - 학습 성과 증명서 (PDF 다운로드)

Day 90+:
  - 습관 형성 완료 (알림 빈도 감소)
  - 시즌/이벤트 참여 유도
```

## 푸시 알림 시스템

### Web Push API 구현

```typescript
// Service Worker 등록 + 구독
async function subscribePush(): Promise<PushSubscription | null> {
  if (!('serviceWorker' in navigator) || !('PushManager' in window)) {
    return null;
  }

  const registration = await navigator.serviceWorker.ready;

  const subscription = await registration.pushManager.subscribe({
    userVisibleOnly: true,
    applicationServerKey: urlBase64ToUint8Array(
      process.env.NEXT_PUBLIC_VAPID_PUBLIC_KEY!
    ),
  });

  // 서버에 구독 정보 저장
  await fetch('/api/notifications/subscribe', {
    method: 'POST',
    body: JSON.stringify(subscription),
    headers: { 'Content-Type': 'application/json' },
  });

  return subscription;
}

// VAPID 키 생성 (서버 측, 최초 1회)
// const vapidKeys = webpush.generateVAPIDKeys();
```

### 알림 유형 & 타이밍

```typescript
const NOTIFICATION_TYPES = {
  // 스트릭 관련
  streak_reminder: {
    title: '오늘 학습 아직 안 했어요!',
    body: '스트릭이 끊기기 전에 1문제만 풀어볼까요? 🔥',
    timing: '19:00', // 저녁 7시 (어린이 학습 피크)
    condition: 'today_not_studied',
    priority: 'high',
  },
  streak_warning: {
    title: '스트릭 위험! ⚠️',
    body: '{streak}일 연속 기록이 끊어지기 {hours}시간 전이에요!',
    timing: '20:00', // 자정 4시간 전
    condition: 'today_not_studied && streak > 3',
    priority: 'urgent',
  },
  streak_broken: {
    title: '스트릭이 끊어졌어요 😢',
    body: '괜찮아요! 오늘부터 다시 시작하면 돼요. 지금 1문제 풀까요?',
    timing: 'next_day_morning',
    condition: 'streak_just_broken',
    priority: 'medium',
  },

  // 성취 관련
  badge_earned: {
    title: '새 뱃지 획득! 🎉',
    body: "'{badge_name}' 뱃지를 획득했어요!",
    timing: 'immediate',
    priority: 'medium',
  },
  level_up: {
    title: '레벨 업! ⬆️',
    body: '{level}레벨 달성! {title} 칭호를 얻었어요!',
    timing: 'immediate',
    priority: 'medium',
  },

  // 소셜 관련
  friend_challenge: {
    title: '{friend}님이 도전장을 보냈어요!',
    body: "'{challenge_name}' 챌린지에 참가할까요?",
    timing: 'immediate',
    priority: 'medium',
  },
  league_result: {
    title: '주간 리그 결과 📊',
    body: '이번 주 {rank}위! {league_change}',
    timing: 'sunday_morning',
    priority: 'low',
  },

  // 학습 관련
  review_due: {
    title: '복습할 문제가 있어요 📝',
    body: '{count}개의 문제가 복습 시간이 됐어요. SM-2 알고리즘 추천!',
    timing: '16:00', // 방과후
    condition: 'has_due_reviews',
    priority: 'low',
  },
  weekly_report: {
    title: '이번 주 학습 리포트 📈',
    body: '{correct}문제 정답, 정답률 {accuracy}%! 자세히 볼까요?',
    timing: 'sunday_09:00',
    priority: 'low',
  },
  new_content: {
    title: '새로운 단원이 열렸어요! 🎊',
    body: "'{unit_name}' 단원을 시작해볼까요?",
    timing: 'immediate',
    condition: 'unit_unlocked',
    priority: 'medium',
  },

  // 교사/학부모
  teacher_at_risk: {
    title: '학생 주의 알림 ⚠️',
    body: '{student_name} 학생의 학습 참여도가 감소하고 있어요.',
    timing: 'morning',
    recipient: 'teacher',
    priority: 'high',
  },
  parent_report: {
    title: '{child_name}의 주간 학습 리포트',
    body: '이번 주 {minutes}분 학습, 정답률 {accuracy}%',
    timing: 'sunday_10:00',
    recipient: 'parent',
    priority: 'medium',
  },
};
```

### 알림 최적화 전략

```yaml
타이밍:
  - 즉시 알림 X → 15~30분 지연 시 학습 세션 +23% 증가 (연구 기반)
  - 개인별 최적 시간 학습 (접속 패턴 분석)
  - 어린이: 16:00~20:00 (방과후~취침전)
  - 주말: 10:00~11:00 (아침 여유 시간)

빈도 제한:
  - 일일 최대: 3회 (초과 시 피로감)
  - 동일 유형: 1일 1회
  - 사용자 미반응 시 빈도 감소
  - 28%의 사용자가 과도한 알림으로 앱 삭제 → 절제 필수

개인화:
  - 이름 포함 (개인화 알림 CTR 4배)
  - 최근 학습 내용 언급
  - 성취에 맞는 메시지 톤 조절
  - A/B 테스트로 최적 메시지 발견

옵트아웃 존중:
  - 카테고리별 알림 on/off
  - "방해금지 시간" 설정
  - 쉬운 구독 해지
```

## 이탈 방지 전략

```yaml
스트릭 프리즈:
  - 무료: 월 2회
  - 프리미엄: 무제한 (자동 적용 옵션)
  - 코인 구매: 50코인/회

복귀 유도:
  - 3일 미접속: "보고 싶었어요!" 알림
  - 7일 미접속: 복귀 보상 (2배 XP 1시간)
  - 14일 미접속: 이메일 (학습 성과 리마인드)
  - 30일 미접속: 특별 복귀 이벤트

이탈 예측:
  - 학습 빈도 감소 추세 감지
  - 세션 시간 단축 감지
  - 스트릭 끊김 직후 = 최대 이탈 위험
  - 선제적 개입: 쉬운 문제 제공 → 성공 경험 → 동기 회복
```

## DB 스키마 (알림)

```sql
-- 푸시 구독
CREATE TABLE push_subscriptions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  endpoint TEXT NOT NULL,
  p256dh TEXT NOT NULL,
  auth_key TEXT NOT NULL,
  device_info JSONB,
  is_active BOOLEAN NOT NULL DEFAULT true,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 알림 설정
CREATE TABLE notification_preferences (
  user_id UUID PRIMARY KEY REFERENCES profiles(id) ON DELETE CASCADE,
  streak_reminder BOOLEAN NOT NULL DEFAULT true,
  achievement_alerts BOOLEAN NOT NULL DEFAULT true,
  social_notifications BOOLEAN NOT NULL DEFAULT true,
  weekly_report BOOLEAN NOT NULL DEFAULT true,
  quiet_start TIME DEFAULT '21:00',
  quiet_end TIME DEFAULT '07:00',
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 알림 이력
CREATE TABLE notification_history (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  type TEXT NOT NULL,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  sent_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  opened_at TIMESTAMPTZ,
  clicked BOOLEAN NOT NULL DEFAULT false
);

-- RLS
ALTER TABLE push_subscriptions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "push_self" ON push_subscriptions FOR ALL USING (auth.uid() = user_id);

ALTER TABLE notification_preferences ENABLE ROW LEVEL SECURITY;
CREATE POLICY "prefs_self" ON notification_preferences FOR ALL USING (auth.uid() = user_id);

ALTER TABLE notification_history ENABLE ROW LEVEL SECURITY;
CREATE POLICY "history_self" ON notification_history FOR SELECT USING (auth.uid() = user_id);
```

## 이메일 리포트 (학부모/교사)

```yaml
학부모 주간 이메일:
  subject: "{child_name}의 이번 주 학습 리포트"
  content:
    - 학습 일수: 5/7일
    - 풀이 수: 47문제
    - 정답률: 82%
    - 가장 잘한 영역: 곱셈구구
    - 보충 필요 영역: 나눗셈
    - 스트릭: 12일 연속 🔥
    - 레벨: 15 (수학 모험가)
    - 교사 코멘트 (있을 경우)
    - CTA: "자세한 리포트 보기" 버튼

교사 주간 이메일:
  subject: "{class_name} 반 주간 학습 현황"
  content:
    - 반 평균 정답률
    - 학습 참여율
    - 위험 학생 알림
    - 반 전체 취약 단원
    - CTA: "대시보드에서 확인" 버튼
```
