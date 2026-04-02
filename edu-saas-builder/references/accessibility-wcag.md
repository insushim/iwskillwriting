# WCAG 2.2 AA 접근성 가이드 (교육 앱 특화)

> W3C WCAG 2.2, 아동 보호(COPPA), K-12 교육 특화 접근성 요구사항
> **법적 마감일: 2026년 4월 24일까지 WCAG 2.1 Level AA 준수 필수** (EU EAA)

## 핵심 원칙: POUR

```yaml
Perceivable (인지 가능):
  - 모든 콘텐츠를 감각 장애와 무관하게 인식 가능
  - 텍스트 대안, 캡션, 고대비

Operable (조작 가능):
  - 키보드만으로 모든 기능 사용 가능
  - 충분한 시간, 적절한 타겟 크기

Understandable (이해 가능):
  - 읽기 쉽고, 예측 가능하고, 오류 방지
  - 아동 수준에 맞는 언어

Robust (견고):
  - 다양한 보조 기술과 호환
  - 시맨틱 HTML, ARIA
```

## WCAG 2.2 AA 필수 체크리스트

### 시각적 접근성

```typescript
// 1. 색상 대비 (최소 4.5:1, 큰 텍스트 3:1)
const ACCESSIBLE_COLORS = {
  // 배경 #FFFFFF 기준
  text: '#1a1a2e',         // 대비 15.7:1
  textMuted: '#4a4a6a',    // 대비 7.1:1
  success: '#16a34a',      // 대비 3.5:1 (큰 텍스트만)
  error: '#dc2626',        // 대비 4.6:1
  warning: '#d97706',      // 대비 3.2:1 (큰 텍스트만)

  // 다크모드 배경 #0f0f23 기준
  darkText: '#e2e2f0',     // 대비 14.1:1
  darkMuted: '#a0a0c0',    // 대비 7.3:1
};

// 2. 색상만으로 정보 전달 금지 (색상 + 아이콘 + 텍스트)
// 나쁜 예: 정답=초록, 오답=빨강 (색맹 구분 불가)
// 좋은 예: 정답=초록+체크아이콘+"정답!", 오답=빨강+X아이콘+"오답"
```

### 타겟 크기 (WCAG 2.2 신규)

```css
/* 모든 인터랙티브 요소: 최소 44x44px (아동: 56px 권장) */
.interactive-target {
  min-width: 44px;
  min-height: 44px;
  /* 아동용 앱에서는 더 크게 */
}

.child-button {
  min-width: 56px;
  min-height: 56px;
  padding: 12px 24px;
  font-size: 1.125rem; /* 18px */
}

/* 선택지 버튼 (충분한 간격) */
.choice-button {
  min-height: 56px;
  margin-bottom: 12px; /* 터치 실수 방지 간격 */
  border-radius: 12px;
}
```

### 키보드 네비게이션

```typescript
// 문제 풀이 화면 키보드 단축키
const KEYBOARD_SHORTCUTS = {
  '1': '선택지 A',
  '2': '선택지 B',
  '3': '선택지 C',
  '4': '선택지 D',
  'Enter': '답안 제출',
  'Tab': '다음 요소로 이동',
  'Shift+Tab': '이전 요소로 이동',
  'Escape': '모달 닫기 / 뒤로가기',
  'h': '힌트 열기 (학습 화면)',
  'n': '다음 문제 (결과 화면)',
  '?': '키보드 단축키 도움말',
};

// 포커스 트랩 (모달 내부)
function useFocusTrap(ref: React.RefObject<HTMLElement>) {
  useEffect(() => {
    const element = ref.current;
    if (!element) return;

    const focusableElements = element.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    const first = focusableElements[0] as HTMLElement;
    const last = focusableElements[focusableElements.length - 1] as HTMLElement;

    function handleKeyDown(e: KeyboardEvent) {
      if (e.key !== 'Tab') return;
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    }

    element.addEventListener('keydown', handleKeyDown);
    first?.focus();
    return () => element.removeEventListener('keydown', handleKeyDown);
  }, [ref]);
}
```

### 포커스 표시

```css
/* 명확한 포커스 표시 (2px+ outline) */
:focus-visible {
  outline: 3px solid #2563eb;
  outline-offset: 2px;
  border-radius: 4px;
}

/* 마우스 클릭 시에는 outline 숨김 */
:focus:not(:focus-visible) {
  outline: none;
}

/* 고대비 모드 지원 */
@media (forced-colors: active) {
  :focus-visible {
    outline: 3px solid Highlight;
  }
}
```

### 동적 콘텐츠 알림 (aria-live)

```tsx
// 정답/오답 피드백 (스크린 리더에 즉시 전달)
<div aria-live="assertive" aria-atomic="true" className="sr-only">
  {isCorrect ? '정답입니다! 10 XP를 획득했어요.' : '오답입니다. 다시 시도해보세요.'}
</div>

// 진행률 업데이트 (폴라이트하게)
<div aria-live="polite" className="sr-only">
  {`${current}번째 문제 중 ${total}번째. 현재 ${correct}개 정답.`}
</div>

// 타이머 경고
<div aria-live="assertive" role="timer" className="sr-only">
  {timeLeft <= 10 ? `남은 시간 ${timeLeft}초` : ''}
</div>
```

### 모션 감소

```tsx
// prefers-reduced-motion 존중
import { useReducedMotion } from 'motion/react';

function RewardAnimation({ children }: { children: React.ReactNode }) {
  const shouldReduce = useReducedMotion();

  if (shouldReduce) {
    // 애니메이션 대신 정적 표시
    return <div className="scale-100 opacity-100">{children}</div>;
  }

  return (
    <motion.div
      initial={{ scale: 0 }}
      animate={{ scale: 1 }}
      transition={{ type: 'spring' }}
    >
      {children}
    </motion.div>
  );
}
```

### 시간 제한 접근성

```tsx
// 시간 제한 연장/해제 옵션
function TimerAccessibility() {
  const [timerEnabled, setTimerEnabled] = useState(true);
  const [timeMultiplier, setTimeMultiplier] = useState(1);

  // 설정에서 조절 가능
  return (
    <div>
      <label>
        <input type="checkbox" checked={timerEnabled} onChange={...} />
        시간 제한 사용
      </label>
      {timerEnabled && (
        <select value={timeMultiplier} onChange={...}>
          <option value={1}>기본 시간</option>
          <option value={1.5}>1.5배 시간</option>
          <option value={2}>2배 시간</option>
          <option value={3}>3배 시간</option>
        </select>
      )}
    </div>
  );
}
```

## 아동 특화 접근성

```yaml
시각적:
  - 큰 글씨 (최소 16px, 권장 18px+)
  - 둥근 모서리 (border-radius: 12px+)
  - 밝고 따뜻한 색상 팔레트
  - 아이콘 + 텍스트 항상 병행
  - 이모지 활용 (시각적 재미)

인터랙션:
  - 큰 버튼 (56px+)
  - 충분한 간격 (최소 12px)
  - 스와이프, 드래그 최소화 (탭 기본)
  - 실수 방지: 확인 다이얼로그

인지:
  - 간단한 문장 (주어+서술어)
  - 전문 용어 대신 쉬운 말
  - 진행 상태 시각화 (프로그레스 바)
  - 한 화면에 하나의 액션

보호:
  - COPPA 대비: 13세 미만 개인정보 최소 수집
  - 학부모 동의 절차
  - 외부 링크 경고
  - 인앱 구매 학부모 인증
  - 학습 시간 제한 알림 (건강 보호)
```

## 접근성 테스트 체크리스트

```yaml
자동 검사:
  - [ ] axe-core 또는 Lighthouse 접근성 점수 90+
  - [ ] ESLint jsx-a11y 플러그인 경고 0개

수동 검사:
  - [ ] 키보드만으로 전체 학습 플로우 완료 가능
  - [ ] Tab 순서가 시각적 순서와 일치
  - [ ] 포커스가 항상 보임
  - [ ] 색상 제거해도 정보 전달 가능
  - [ ] 200% 확대에서 레이아웃 깨지지 않음
  - [ ] VoiceOver/NVDA로 주요 플로우 테스트
  - [ ] prefers-reduced-motion: reduce에서 애니메이션 비활성화
  - [ ] prefers-color-scheme: dark에서 대비 유지
```
