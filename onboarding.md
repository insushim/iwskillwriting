# Onboarding Skill (OpenClaw Style)

> 사용자 온보딩 플로우 설계. "온보딩", "튜토리얼", "가이드", "신규 사용자" 트리거.

## 온보딩 원칙

### 1. Aha Moment까지 최단 경로
- 사용자가 가치를 느끼는 순간까지 빠르게
- 불필요한 단계 제거

### 2. 점진적 공개
- 한 번에 모든 기능 X
- 필요할 때 필요한 것만

### 3. 인터랙티브
- 단순 설명 < 직접 해보기
- 실제 데이터로 경험

## 온보딩 플로우 구조

### Step 1: 환영 + 목표 설정
```tsx
<OnboardingStep>
  <h1>환영합니다! 👋</h1>
  <p>어떤 목적으로 사용하시나요?</p>
  <RadioGroup>
    <Radio value="personal">개인 프로젝트</Radio>
    <Radio value="team">팀 협업</Radio>
    <Radio value="business">비즈니스</Radio>
  </RadioGroup>
</OnboardingStep>
```

### Step 2: 프로필 설정
```tsx
<OnboardingStep>
  <h2>프로필을 설정해주세요</h2>
  <AvatarUpload />
  <Input label="이름" />
  <Input label="역할" />
</OnboardingStep>
```

### Step 3: 핵심 기능 체험
```tsx
<OnboardingStep>
  <h2>첫 번째 [항목]을 만들어보세요</h2>
  <InteractiveDemo
    steps={[
      { target: '#create-btn', content: '여기를 클릭하세요' },
      { target: '#name-input', content: '이름을 입력하세요' },
      { target: '#save-btn', content: '저장!' },
    ]}
  />
</OnboardingStep>
```

### Step 4: 완료 + 다음 단계
```tsx
<OnboardingStep>
  <ConfettiAnimation />
  <h2>준비 완료! 🎉</h2>
  <p>다음으로 해볼 것들:</p>
  <Checklist>
    <ChecklistItem>팀원 초대하기</ChecklistItem>
    <ChecklistItem>앱 연동하기</ChecklistItem>
    <ChecklistItem>첫 프로젝트 시작</ChecklistItem>
  </Checklist>
</OnboardingStep>
```

## 온보딩 체크리스트 구현

```typescript
// 온보딩 상태 관리
const ONBOARDING_STEPS = [
  'profile_complete',
  'first_project_created',
  'first_invite_sent',
  'integration_connected',
] as const;

interface OnboardingState {
  completedSteps: string[];
  isComplete: boolean;
}

// 진행률 표시
const progress = (completedSteps.length / ONBOARDING_STEPS.length) * 100;

<ProgressBar value={progress} />
<p>{completedSteps.length}/{ONBOARDING_STEPS.length} 완료</p>
```

## 툴팁 가이드 (Product Tour)

```typescript
// react-joyride 또는 shepherd.js 사용
import Joyride from 'react-joyride';

const steps = [
  {
    target: '.sidebar',
    content: '여기서 메뉴를 탐색할 수 있어요',
  },
  {
    target: '.create-button',
    content: '새 항목을 만들려면 여기를 클릭하세요',
  },
];

<Joyride steps={steps} run={isNewUser} />
```

## 빈 상태 (Empty State)

```tsx
// 데이터 없을 때 가이드 제공
function EmptyState() {
  return (
    <div className="text-center py-12">
      <Illustration />
      <h3>아직 프로젝트가 없어요</h3>
      <p>첫 번째 프로젝트를 만들어보세요</p>
      <Button>프로젝트 만들기</Button>
    </div>
  );
}
```

## 메트릭스

- **완료율**: 온보딩 완료 비율
- **이탈 지점**: 어느 단계에서 이탈하는지
- **Time to Value**: 가입 → 핵심 액션까지 시간
- **활성화율**: 온보딩 완료 → 7일 후 재방문

## A/B 테스트 아이디어
- 단계 수 (3단계 vs 5단계)
- 강제 vs 스킵 가능
- 비디오 vs 인터랙티브
- 이메일 시리즈 병행
