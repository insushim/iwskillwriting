# 포용적 학습 & 인터랙티브 교구

> 마이크로러닝, 디지털 수학 교구, 학습장애 지원, COPPA 아동 보호

## 마이크로러닝 설계 (2026)

> 2026년 마이크로러닝 = 짧은 콘텐츠가 아니라 "문제 해결 중심 학습 전략"

```yaml
설계 원칙:
  1. 문제 중심: 주제가 아닌 "해결할 문제"로 시작
  2. 상황 맥락: 실제 상황과 연결된 문제
  3. 일상 통합: 학습이 별도 행위가 아닌 일과의 일부
  4. 연속적: 일회성이 아닌 연결된 학습 경험

세션 구조 (5-10분):
  - 개념 리마인드 (30초): 핵심 개념 1줄 요약
  - 예시 문제 (1분): 풀이 과정 시연
  - 연습 문제 (3-5분): 3~5문제 풀기
  - 즉각 피드백: 맞으면 XP, 틀리면 힌트
  - 마무리 (30초): 오늘 배운 것 + 내일 예고

포맷 다양성:
  - 인터랙티브 퀴즈 (기본)
  - 드래그&드롭 교구
  - 짧은 애니메이션 풀이
  - 음성 문제 (저학년)
  - 이미지 기반 문제 (시각적)
```

## 디지털 수학 교구 (인터랙티브 매니퓰레이티브)

> Mathigon/Polypad, Brainingcamp, Visnos 등 벤치마크

### 구현할 교구 목록

```typescript
const MATH_MANIPULATIVES = {
  // 수와 연산
  numberLine: {
    name: '수직선',
    grades: [1, 2, 3],
    interaction: 'drag-point',
    description: '점을 드래그하여 수 위치 찾기',
  },
  baseTenBlocks: {
    name: '십진 블록',
    grades: [1, 2, 3],
    interaction: 'drag-drop-group',
    description: '1, 10, 100 블록을 조합하여 수 만들기',
  },
  fractionBar: {
    name: '분수 막대',
    grades: [3, 4, 5],
    interaction: 'split-merge',
    description: '막대를 분할/합치기로 분수 이해',
  },
  fractionCircle: {
    name: '분수 원',
    grades: [3, 4, 5],
    interaction: 'rotate-slice',
    description: '원을 회전/분할하여 분수 시각화',
  },

  // 도형
  geoboard: {
    name: '지오보드',
    grades: [2, 3, 4],
    interaction: 'point-connect',
    description: '점을 연결하여 도형 만들기',
  },
  tangram: {
    name: '탱그램',
    grades: [1, 2, 3],
    interaction: 'drag-rotate',
    description: '조각을 이동/회전하여 모양 만들기',
  },
  patternBlocks: {
    name: '패턴 블록',
    grades: [1, 2, 3],
    interaction: 'drag-snap',
    description: '도형 블록으로 패턴/테셀레이션 만들기',
  },

  // 측정
  ruler: {
    name: '자',
    grades: [1, 2, 3],
    interaction: 'measure-drag',
    description: '가상 자로 길이 측정',
  },
  protractor: {
    name: '각도기',
    grades: [3, 4],
    interaction: 'rotate-measure',
    description: '각도 측정',
  },
  clock: {
    name: '시계',
    grades: [1, 2],
    interaction: 'rotate-hands',
    description: '시계 바늘 돌려 시각 읽기',
  },
};

// Canvas/SVG 기반 구현 (React)
// 라이브러리: react-dnd + SVG 또는 HTML5 Canvas
```

## 학습장애 지원 (Inclusive Design)

### 난독증 (Dyslexia) 지원

```css
/* OpenDyslexic 폰트 옵션 */
@font-face {
  font-family: 'OpenDyslexic';
  src: url('/fonts/OpenDyslexic-Regular.woff2') format('woff2');
  font-weight: normal;
}

/* 난독증 친화적 설정 */
.dyslexia-mode {
  font-family: 'OpenDyslexic', sans-serif;
  line-height: 1.8;          /* 넓은 줄 간격 */
  letter-spacing: 0.05em;     /* 문자 간격 */
  word-spacing: 0.1em;        /* 단어 간격 */
  max-width: 70ch;            /* 한 줄 최대 너비 */
  text-align: left;           /* 양쪽 정렬 X */
  background: #fdf6e3;        /* 부드러운 배경 (순백 X) */
  color: #2d2d2d;             /* 순검정 X */
}

/* 읽기 가이드 (줄 하이라이트) */
.reading-guide {
  background: linear-gradient(
    transparent 0%,
    transparent 40%,
    rgba(255, 255, 0, 0.2) 40%,
    rgba(255, 255, 0, 0.2) 60%,
    transparent 60%
  );
}
```

### ADHD 지원

```yaml
디자인 원칙:
  - 한 화면에 하나의 작업
  - 시각적 방해 최소화 (깔끔한 UI)
  - 타이머 시각화 (남은 시간 바)
  - 짧은 세션 (5분 단위)
  - 자주 그리고 즉각적인 보상
  - 중간 저장 (진행 자동 저장)
  - 포커스 모드 (사이드바/네비 숨김)
```

### 시각 장애 지원

```yaml
저시력:
  - 글씨 크기 조절 (100%~200%)
  - 고대비 모드 (배경: 검정, 글자: 노랑)
  - 색맹 모드 (색상 대신 패턴/아이콘)
  - 확대 가능한 수식/이미지

전맹:
  - 스크린 리더 완전 호환 (ARIA)
  - 수식을 텍스트로 읽기 (MathML → aria-label)
  - 키보드만으로 모든 기능
  - 음성 피드백 (정답/오답 알림)
```

### 접근성 설정 UI

```typescript
interface AccessibilitySettings {
  // 시각
  fontSize: 'small' | 'medium' | 'large' | 'xlarge';  // 14/16/18/22px
  highContrast: boolean;
  colorBlindMode: 'none' | 'protanopia' | 'deuteranopia' | 'tritanopia';
  reducedMotion: boolean;

  // 읽기
  dyslexiaFont: boolean;        // OpenDyslexic
  readingGuide: boolean;        // 줄 하이라이트
  lineSpacing: 'normal' | 'wide' | 'extra-wide';

  // 인터랙션
  focusMode: boolean;           // 불필요 요소 숨김
  timerDisabled: boolean;       // 시간 제한 해제
  timerMultiplier: number;      // 시간 배율 (1~3)

  // 오디오
  soundEnabled: boolean;
  soundVolume: number;          // 0~100
  voiceFeedback: boolean;       // 음성 피드백
}
```

## COPPA 아동 보호 규정 (2026년 4월 개정)

> FTC COPPA Rule 개정: 2025년 6월 23일 발효, 2026년 4월 22일 전체 준수 마감

```yaml
핵심 요구사항:
  1. 수집 최소화:
     - 서비스에 필요한 최소한의 정보만 수집
     - 이름, 학년만 수집 (주소, 전화번호 X)
     - 13세 미만: 학부모 동의 필수

  2. 학부모 동의:
     - 가입 시 학부모 이메일 수집
     - 인증 이메일 발송 → 동의 확인
     - 동의 없이 개인정보 수집 금지

  3. 데이터 보존:
     - 목적 달성 후 삭제 (무기한 보존 금지)
     - 데이터 생명주기 정의 필수
     - 학부모 요청 시 즉시 삭제

  4. 제3자 보호:
     - 제3자에 아동 데이터 공유 시 서면 확인
     - 광고/AI 학습용 데이터 공유: 별도 학부모 동의

  5. 생체 데이터 (신규):
     - 지문, 얼굴, 음성 등 보호 대상 추가
     - 수집 시 별도 학부모 동의 필수

구현 체크리스트:
  - [ ] 13세 미만 연령 확인 절차
  - [ ] 학부모 동의 플로우 (이메일 인증)
  - [ ] 프라이버시 정책 (아동용 쉬운 언어)
  - [ ] 데이터 삭제 API (학부모 요청)
  - [ ] 데이터 보존 기간 정책
  - [ ] 제3자 데이터 공유 제한
  - [ ] 광고 표시 시 학부모 동의
  - [ ] 인앱 구매 학부모 인증
```

## 수학 교구 구현 패턴

### HTML5 Canvas + React 패턴

```typescript
// 드래그 가능한 수학 교구 기본 구조
interface ManipulativeProps {
  width: number;
  height: number;
  onInteraction: (event: InteractionEvent) => void;
  accessibilityLabel: string;
}

// 수직선 교구 예시
function NumberLine({ min, max, target, onAnswer }: {
  min: number;
  max: number;
  target: number;
  onAnswer: (value: number) => void;
}) {
  // SVG 기반 (접근성 우수)
  // - 포인터 드래그로 값 선택
  // - 키보드 좌/우 화살표로 이동
  // - aria-valuenow로 현재 값 알림
  // - 터치 지원 (모바일)
}

// 십진 블록 교구
function BaseTenBlocks({ targetNumber, onComplete }: {
  targetNumber: number;
  onComplete: (correct: boolean) => void;
}) {
  // react-dnd 기반
  // - 1블록, 10막대, 100판 드래그
  // - 드롭존에 놓으면 합산
  // - 목표 수 만들면 정답
}
```
