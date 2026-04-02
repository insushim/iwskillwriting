# AI 튜터 시스템 설계 가이드

> Khanmigo, Duolingo Max, Brilliant 등 AI 에듀테크 벤치마크 기반

## AI 기능 3대 축

### 1. AI 힌트 생성 (3단계 스캐폴딩)

소크라테스 방식: 직접 답을 주지 않고 사고를 유도

```typescript
const HINT_SYSTEM_PROMPT = `
당신은 친절한 수학 선생님입니다.
학생이 문제를 풀지 못하고 있습니다.

규칙:
1. 절대 정답을 직접 알려주지 마세요
2. 학생 스스로 생각할 수 있도록 유도하세요
3. 학년 수준에 맞는 쉬운 한국어를 사용하세요
4. 격려와 칭찬을 포함하세요
`;

interface HintRequest {
  problem: {
    question: string;
    correctAnswer: string;
    solution: string;
    unitName: string;
    tags: string[];
  };
  student: {
    grade: number;
    wrongAnswer?: string;
    attemptCount: number;
  };
  hintLevel: 1 | 2 | 3;
}

const HINT_LEVEL_INSTRUCTIONS = {
  1: `
    [힌트 1단계: 방향 제시]
    - 핵심 개념만 간단히 알려주세요
    - 어떤 방법을 사용해야 하는지 힌트만 주세요
    - 구체적인 숫자나 계산 과정은 보여주지 마세요
    - 1~2문장으로 짧게
    예: "이 문제는 덧셈을 사용하면 돼요! 두 수를 합치면 얼마일까요?"
  `,
  2: `
    [힌트 2단계: 풀이 시작]
    - 풀이 과정의 첫 번째 단계를 보여주세요
    - 중간 계산까지만 보여주고 최종 답은 학생이 구하게 하세요
    - 시각적 보조 (수직선, 그림 설명 등) 활용
    예: "3 + ? = 7 에서, 3에서부터 7까지 세어볼까요? 3, 4, 5..."
  `,
  3: `
    [힌트 3단계: 거의 풀어주기]
    - 풀이 과정을 대부분 보여주세요
    - 마지막 한 단계만 학생이 완성하게 하세요
    - 비슷한 쉬운 문제를 예시로 들어주세요
    예: "3 + 4 = 7이에요. 그러면 이 문제에서 답은 뭘까요?"
  `,
};
```

### 2. AI 문제 생성

```typescript
const PROBLEM_GENERATION_PROMPT = `
한국 2022 개정 교육과정 기준으로 수학 문제를 생성하세요.

요구사항:
- 학년: {grade}학년 {semester}학기
- 단원: {unitName}
- 난이도: {difficulty} (easy/medium/hard/challenge)
- 유형: {type} (multiple_choice/short_answer/fill_blank/true_false)
- 개수: {count}문제

규칙:
1. 교과서 수준에 맞는 문제
2. 다양한 상황/맥락 활용 (실생활 연계)
3. 풀이 과정을 상세히 작성
4. 힌트는 학생이 스스로 생각할 수 있도록
5. 객관식은 매력적인 오답 포함 (흔한 실수 기반)

JSON 배열로 출력:
[{
  "question": "문제 본문",
  "options": [{"label":"A","text":"..."}] (객관식일 때),
  "correct_answer": "정답",
  "solution": "상세 풀이 (단계별)",
  "hint": "힌트 (직접 답 X)",
  "tags": ["관련 태그"],
  "difficulty": "난이도",
  "time_limit": 초단위
}]
`;

// AI 문제 생성 후 품질 검증
function validateGeneratedProblem(problem: GeneratedProblem): ValidationResult {
  const errors: string[] = [];

  if (!problem.question || problem.question.length < 10)
    errors.push('문제가 너무 짧습니다');
  if (!problem.correct_answer)
    errors.push('정답이 없습니다');
  if (!problem.solution || problem.solution.length < 20)
    errors.push('풀이가 너무 짧습니다');
  if (problem.type === 'multiple_choice' && (!problem.options || problem.options.length < 4))
    errors.push('객관식은 4개 이상의 선택지가 필요합니다');

  // 정답이 선택지에 포함되어 있는지 확인
  if (problem.type === 'multiple_choice') {
    const hasCorrect = problem.options?.some(o =>
      o.text === problem.correct_answer || o.label === problem.correct_answer
    );
    if (!hasCorrect) errors.push('정답이 선택지에 없습니다');
  }

  return { valid: errors.length === 0, errors };
}
```

### 3. AI 튜터 챗봇 (대화형)

```typescript
const TUTOR_CHAT_SYSTEM = `
당신은 교육용 AI 튜터 "{appName}"입니다.

## 성격
- 친절하고 인내심 있는 선생님
- 학생의 수준에 맞춰 대화
- 격려와 칭찬을 자주 함
- 유머를 적절히 사용

## 소크라테스 교수법
1. 학생이 문제를 가져오면 바로 풀어주지 않음
2. "이 문제에서 뭘 구해야 할까?" 같은 질문으로 시작
3. 학생의 생각을 먼저 들음
4. 틀린 부분만 짚어주고 다시 생각하게 함
5. 정답을 맞추면 크게 칭찬

## 대화 규칙
- 한국어 사용
- 학생 학년에 맞는 어휘
- 한 번에 3문장 이내
- 수식은 쉽게 풀어서 설명
- 절대 정답 직접 제공 X (3회 이상 틀렸을 때만 풀이 공개)

## 현재 학생 정보
- 학년: {grade}학년
- 현재 단원: {currentUnit}
- 최근 취약 영역: {weakAreas}
- 현재 레벨: {level}
`;

// Vercel AI SDK 스트리밍 통합
// app/api/ai/tutor/route.ts
import { streamText } from 'ai';
import { anthropic } from '@ai-sdk/anthropic';

export async function POST(req: Request) {
  const { messages, studentContext } = await req.json();

  const result = streamText({
    model: anthropic('claude-sonnet-4-20250514'),
    system: TUTOR_CHAT_SYSTEM
      .replace('{grade}', studentContext.grade)
      .replace('{currentUnit}', studentContext.currentUnit)
      .replace('{weakAreas}', studentContext.weakAreas.join(', '))
      .replace('{level}', studentContext.level),
    messages,
    maxTokens: 300,
    temperature: 0.7,
  });

  return result.toDataStreamResponse();
}
```

## AI 통합 아키텍처

```yaml
프론트엔드:
  - useChat() 훅 (Vercel AI SDK)
  - 스트리밍 응답 실시간 표시
  - 타이핑 인디케이터
  - 마크다운 렌더링 (수식 지원)

API 라우트:
  /api/ai/hint:
    - POST: 힌트 요청 (비스트리밍, 짧은 응답)
    - Rate limit: 문제당 3회
  /api/ai/tutor:
    - POST: 대화형 튜터 (스트리밍)
    - Rate limit: 분당 10회
  /api/ai/generate:
    - POST: 문제 생성 (비스트리밍, 배치)
    - 교사/관리자 전용

비용 최적화:
  - 힌트: Claude Haiku (빠르고 저렴)
  - 튜터: Claude Sonnet (균형)
  - 문제 생성: Claude Sonnet (품질 중요)
  - 캐싱: 동일 문제 힌트는 캐시
  - 무료 사용자: 일일 AI 사용 제한 (5회)
  - 프리미엄: 무제한
```

## 안전장치

```yaml
콘텐츠 필터링:
  - 교육과 무관한 질문 거부
  - 부적절한 콘텐츠 차단
  - 개인정보 수집 방지

응답 품질:
  - 수학적 정확성 검증 (간단한 계산은 서버에서 재검증)
  - 학년 수준 적합성 체크
  - 할루시네이션 방지 (교과서 기반 답변 유도)

비용 제어:
  - 토큰 사용량 모니터링
  - 사용자별 일일 제한
  - 비정상 사용 감지
```
