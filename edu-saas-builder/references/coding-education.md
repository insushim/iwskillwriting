# 코딩 교육 SaaS 특화 가이드

> 블록 코딩 → 텍스트 코딩 전환, 자동 채점, 프로젝트 학습, AI 코딩 튜터
> Judge0 코드 실행 엔진 + Pyodide 브라우저 Python + Blockly 블록 에디터

## 코딩 학습 단계별 설계

### Stage 1: 블록 코딩 (초등 3~6학년)

```yaml
개념: 드래그&드롭으로 프로그래밍 기초 학습
도구: 엔트리(Entry), 스크래치(Scratch)
학습 목표:
  - 순차 실행 이해
  - 조건문 (만약 ~이면)
  - 반복문 (N번 반복, ~까지 반복)
  - 이벤트 (클릭하면, 키 누르면)
  - 변수 (점수 저장)
  - 간단한 게임/애니메이션 제작

앱 구현:
  - 웹 기반 블록 에디터 (Blockly 라이브러리)
  - 실시간 미리보기 (캐릭터 움직임)
  - 단계별 미션 (게임화)
  - 힌트: 블록 조합 제안
```

### Stage 2: 블록 → 텍스트 전환 (중1~2)

```yaml
개념: 블록 코드와 텍스트 코드 동시 표시 (듀얼 뷰)
도구: 엔트리 Python 모드, MakeCode
학습 목표:
  - 블록 ↔ Python 1:1 매핑 이해
  - 기본 문법 (print, input, if, for, while)
  - 들여쓰기 규칙
  - 간단한 함수 정의

앱 구현:
  - 듀얼 뷰: 왼쪽 블록 / 오른쪽 Python
  - 블록 변경 → Python 자동 업데이트 (실시간)
  - Python 직접 편집도 가능
  - 점진적 전환: 블록 비율 줄이기
```

### Stage 3: 텍스트 코딩 (중2~고등)

```yaml
개념: Python 중심 텍스트 프로그래밍
도구: 웹 기반 Python IDE
학습 목표:
  - 변수, 자료형 (int, str, list, dict)
  - 조건문, 반복문 심화
  - 함수 정의와 호출
  - 리스트/딕셔너리 활용
  - 파일 입출력
  - 기초 알고리즘 (정렬, 탐색)

고등 심화:
  - 클래스/객체지향
  - 재귀 함수
  - 자료구조 (스택, 큐, 트리)
  - 알고리즘 복잡도
  - AI/ML 프로젝트 (sklearn, pandas)
```

## 웹 기반 코드 에디터 구현

### Monaco Editor (VS Code 기반)

```typescript
// 코드 에디터 컴포넌트
import { Editor } from '@monaco-editor/react';

interface CodeEditorProps {
  language: 'python' | 'javascript' | 'scratch';
  initialCode: string;
  onRun: (code: string) => void;
  readOnly?: boolean;
  theme?: 'light' | 'dark';
}

function CodeEditor({ language, initialCode, onRun, theme = 'light' }: CodeEditorProps) {
  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center justify-between p-2 bg-muted">
        <span className="text-sm font-medium">{language}</span>
        <Button onClick={() => onRun(code)} size="sm">
          ▶ 실행
        </Button>
      </div>
      <Editor
        height="300px"
        language={language}
        value={initialCode}
        theme={theme === 'dark' ? 'vs-dark' : 'light'}
        options={{
          minimap: { enabled: false },
          fontSize: 16,           // 큰 글씨 (학생용)
          lineNumbers: 'on',
          scrollBeyondLastLine: false,
          automaticLayout: true,
          tabSize: 4,
        }}
        onChange={(value) => setCode(value ?? '')}
      />
      <div className="bg-black text-green-400 p-3 font-mono text-sm min-h-[100px]">
        {/* 출력 영역 */}
        {output}
      </div>
    </div>
  );
}
```

### Python 실행 (서버 or 브라우저)

```yaml
옵션 A — Pyodide (브라우저 내 Python):
  장점: 서버 비용 X, 즉시 실행, 오프라인 가능
  단점: 무거움 (~20MB), 일부 라이브러리 미지원
  적합: 기초 Python 학습

옵션 B — 서버 실행 (Supabase Edge Function):
  장점: 모든 Python 기능, 빠른 실행
  단점: 서버 비용, 보안(샌드박스 필수)
  적합: 심화 프로젝트

옵션 C — Judge0 API (코딩 테스트):
  장점: 다중 언어 지원, 시간/메모리 제한
  단점: 외부 의존, API 비용
  적합: 알고리즘 문제 채점
```

```typescript
// Pyodide 브라우저 내 Python 실행
async function runPython(code: string): Promise<string> {
  const pyodide = await loadPyodide();
  try {
    // stdout 캡처
    pyodide.runPython(`
      import sys
      from io import StringIO
      sys.stdout = StringIO()
    `);
    pyodide.runPython(code);
    const output = pyodide.runPython('sys.stdout.getvalue()');
    return output;
  } catch (error) {
    return `오류: ${(error as Error).message}`;
  }
}
```

## 코딩 문제 유형

```typescript
const CODING_PROBLEM_TYPES = {
  // 기초 (초등~중1)
  output_prediction: {
    name: '출력 예측',
    description: '코드를 읽고 출력 결과를 예측하세요',
    example: {
      code: 'for i in range(3):\n    print(i)',
      question: '이 코드의 출력은?',
      answer: '0\n1\n2',
    },
  },
  fill_blank: {
    name: '빈칸 채우기',
    description: '코드의 빈칸을 채워 원하는 결과를 만드세요',
    example: {
      code: 'for i in range(_____):\n    print("안녕")',
      question: '빈칸을 채워 "안녕"을 5번 출력하세요',
      answer: '5',
    },
  },
  block_arrange: {
    name: '블록 배열',
    description: '블록을 올바른 순서로 배열하세요',
  },

  // 중급 (중2~고등)
  write_function: {
    name: '함수 작성',
    description: '조건에 맞는 함수를 작성하세요',
    example: {
      question: '두 수의 합을 반환하는 함수 add(a, b)를 작성하세요',
      testCases: [
        { input: 'add(1, 2)', expected: '3' },
        { input: 'add(-1, 1)', expected: '0' },
      ],
    },
  },
  debug: {
    name: '디버깅',
    description: '버그가 있는 코드를 찾아 수정하세요',
  },
  algorithm: {
    name: '알고리즘',
    description: '주어진 문제를 알고리즘으로 해결하세요',
  },
};
```

## 코딩 교육 게이미피케이션 특화

```yaml
퀘스트 시스템:
  - "첫 Hello World" → 프로그래밍 세계 입문
  - "변수 마법사" → 변수 5개 활용
  - "반복의 달인" → for 루프로 패턴 그리기
  - "조건문 히어로" → if/else로 퀴즈 게임 만들기
  - "함수 건축가" → 함수 3개 정의
  - "버그 헌터" → 버그 10개 수정

프로젝트 뱃지:
  - "나의 첫 게임" → 간단한 게임 완성
  - "계산기 장인" → 계산기 프로그램
  - "데이터 과학자" → 데이터 분석 프로젝트
  - "AI 탐험가" → 간단한 ML 모델

코드 챌린지:
  - 일일 코딩 챌린지 (1문제/일)
  - 주간 프로젝트 챌린지
  - 실시간 코딩 배틀 (Kahoot! 스타일)
```

## Blockly 라이브러리 통합 (블록 코딩)

```typescript
// Google Blockly를 React에서 사용
// npm install blockly @blockly/workspace-backpack

import Blockly from 'blockly';
import { pythonGenerator } from 'blockly/python';

// 블록 → Python 변환
function blockToPython(workspace: Blockly.Workspace): string {
  return pythonGenerator.workspaceToCode(workspace);
}

// 커스텀 블록 정의 (한국어)
Blockly.Blocks['print_korean'] = {
  init: function() {
    this.appendValueInput('TEXT')
        .setCheck('String')
        .appendField('출력하기');
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(160);
  }
};

pythonGenerator.forBlock['print_korean'] = function(block) {
  const text = pythonGenerator.valueToCode(block, 'TEXT', 0) || "''";
  return `print(${text})\n`;
};
```

## AI 코딩 튜터 프롬프트

```typescript
const CODING_TUTOR_PROMPT = `
당신은 코딩 교육 AI 튜터입니다.

규칙:
1. 학생 수준에 맞는 설명 (학년: {grade})
2. 코드를 직접 작성해주지 마세요 (힌트만)
3. 에러 메시지를 쉬운 한국어로 번역
4. "이 부분을 어떻게 바꾸면 될까요?" 식으로 유도
5. 정답을 맞추면 크게 칭찬

에러 번역 예시:
- SyntaxError → "문법 오류예요! 오타가 있는 것 같아요"
- IndentationError → "들여쓰기가 맞지 않아요. 스페이스 4칸 확인!"
- NameError → "이 이름을 아직 만들지 않았어요. 변수를 먼저 만들어볼까요?"
- TypeError → "숫자와 글자를 섞어서 계산하려 했어요"
`;
```

## 자동 채점 시스템 (Auto-Grader)

### 아키텍처: Pyodide (브라우저) + Judge0 (서버 폴백)

```typescript
// 코드 실행 엔진 추상화
interface ExecutionResult {
  stdout: string;
  stderr: string;
  exitCode: number;
  executionTime: number; // ms
  memoryUsage: number;   // KB
}

interface TestCase {
  input: string;
  expectedOutput: string;
  isHidden: boolean;      // 학생에게 숨김 여부
  timeLimit: number;      // ms
  memoryLimit: number;    // KB
}

interface GradingResult {
  passed: number;
  total: number;
  score: number;          // 0~100
  testResults: Array<{
    testCase: number;
    passed: boolean;
    actual: string;
    expected: string;
    time: number;
    error?: string;
  }>;
}

// Pyodide 브라우저 실행 (기본 — 서버 비용 0)
async function executePyodide(code: string, input: string): Promise<ExecutionResult> {
  const pyodide = await loadPyodide();
  const start = performance.now();

  // stdin 시뮬레이션
  pyodide.runPython(`
import sys
from io import StringIO
sys.stdin = StringIO(${JSON.stringify(input)})
sys.stdout = StringIO()
sys.stderr = StringIO()
  `);

  try {
    // 5초 타임아웃
    await Promise.race([
      pyodide.runPythonAsync(code),
      new Promise((_, reject) => setTimeout(() => reject(new Error('시간 초과')), 5000)),
    ]);

    return {
      stdout: pyodide.runPython('sys.stdout.getvalue()'),
      stderr: pyodide.runPython('sys.stderr.getvalue()'),
      exitCode: 0,
      executionTime: performance.now() - start,
      memoryUsage: 0,
    };
  } catch (error) {
    return {
      stdout: '',
      stderr: (error as Error).message,
      exitCode: 1,
      executionTime: performance.now() - start,
      memoryUsage: 0,
    };
  }
}

// Judge0 서버 실행 (고급 — 다중 언어, 정확한 리소스 제한)
async function executeJudge0(
  code: string,
  input: string,
  languageId: number = 71, // Python 3
): Promise<ExecutionResult> {
  const res = await fetch('/api/code/execute', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      source_code: btoa(code),           // base64
      stdin: btoa(input),
      language_id: languageId,
      cpu_time_limit: 5,                  // 5초
      memory_limit: 128000,               // 128MB
    }),
  });
  return res.json();
}

// 자동 채점
function gradeSubmission(
  testCases: TestCase[],
  results: ExecutionResult[],
): GradingResult {
  let passed = 0;
  const testResults = testCases.map((tc, i) => {
    const result = results[i];
    const actual = result.stdout.trim();
    const expected = tc.expectedOutput.trim();
    const isPassed = actual === expected && result.exitCode === 0;
    if (isPassed) passed++;
    return {
      testCase: i + 1,
      passed: isPassed,
      actual: tc.isHidden ? (isPassed ? '통과' : '실패') : actual,
      expected: tc.isHidden ? '(숨김)' : expected,
      time: result.executionTime,
      error: result.stderr || undefined,
    };
  });

  return {
    passed,
    total: testCases.length,
    score: Math.round((passed / testCases.length) * 100),
    testResults,
  };
}
```

## 코딩 교육 DB 스키마 (Supabase 추가 테이블)

```sql
-- 코딩 문제
CREATE TABLE coding_problems (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  title TEXT NOT NULL,
  description TEXT NOT NULL,        -- 마크다운 지원
  difficulty difficulty_level NOT NULL DEFAULT 'medium',
  language TEXT NOT NULL DEFAULT 'python', -- python, javascript, scratch
  stage TEXT NOT NULL,               -- block, transition, text, algorithm
  category TEXT NOT NULL,            -- variable, loop, condition, function, class, data_structure
  starter_code TEXT,                 -- 시작 코드 (빈칸 포함)
  solution_code TEXT NOT NULL,       -- 모범 답안
  hint TEXT,
  tags TEXT[],
  time_limit INTEGER DEFAULT 5000,   -- ms
  memory_limit INTEGER DEFAULT 128000, -- KB
  xp_reward INTEGER NOT NULL DEFAULT 20,
  created_by UUID REFERENCES profiles(id),
  is_active BOOLEAN NOT NULL DEFAULT true,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 테스트 케이스
CREATE TABLE coding_test_cases (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  problem_id UUID NOT NULL REFERENCES coding_problems(id) ON DELETE CASCADE,
  input TEXT NOT NULL DEFAULT '',
  expected_output TEXT NOT NULL,
  is_hidden BOOLEAN NOT NULL DEFAULT false,
  sort_order INTEGER NOT NULL DEFAULT 0
);

-- 코드 제출
CREATE TABLE code_submissions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  student_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  problem_id UUID NOT NULL REFERENCES coding_problems(id) ON DELETE CASCADE,
  code TEXT NOT NULL,
  language TEXT NOT NULL DEFAULT 'python',
  execution_engine TEXT NOT NULL DEFAULT 'pyodide', -- pyodide, judge0
  passed_count INTEGER NOT NULL DEFAULT 0,
  total_count INTEGER NOT NULL DEFAULT 0,
  score INTEGER NOT NULL DEFAULT 0,    -- 0~100
  execution_time INTEGER,              -- ms (최대)
  status TEXT NOT NULL DEFAULT 'pending', -- pending, running, accepted, wrong_answer, error, timeout
  error_message TEXT,
  xp_earned INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 프로젝트 (장기 과제)
CREATE TABLE coding_projects (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  stage TEXT NOT NULL,               -- block, transition, text, algorithm
  difficulty difficulty_level NOT NULL DEFAULT 'medium',
  estimated_minutes INTEGER DEFAULT 30,
  starter_files JSONB DEFAULT '[]'::jsonb, -- [{name, content, language}]
  requirements JSONB NOT NULL,       -- 평가 기준
  sample_output TEXT,                -- 예상 결과 설명
  tags TEXT[],
  xp_reward INTEGER NOT NULL DEFAULT 100,
  is_active BOOLEAN NOT NULL DEFAULT true,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 학생 프로젝트 제출
CREATE TABLE project_submissions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  student_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  project_id UUID NOT NULL REFERENCES coding_projects(id) ON DELETE CASCADE,
  files JSONB NOT NULL,              -- [{name, content, language}]
  status TEXT NOT NULL DEFAULT 'draft', -- draft, submitted, reviewed
  score INTEGER,                     -- 0~100 (교사 채점 또는 AI 채점)
  feedback TEXT,                     -- 교사/AI 피드백
  submitted_at TIMESTAMPTZ,
  reviewed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- RLS
ALTER TABLE coding_problems ENABLE ROW LEVEL SECURITY;
CREATE POLICY "coding_problems_read" ON coding_problems FOR SELECT USING (is_active = true);

ALTER TABLE code_submissions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "code_sub_self" ON code_submissions FOR ALL USING (auth.uid() = student_id);

ALTER TABLE project_submissions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "proj_sub_self" ON project_submissions FOR ALL USING (auth.uid() = student_id);

-- 인덱스
CREATE INDEX idx_coding_problems_stage ON coding_problems(stage, difficulty) WHERE is_active = true;
CREATE INDEX idx_code_subs_student ON code_submissions(student_id, created_at DESC);
CREATE INDEX idx_test_cases_problem ON coding_test_cases(problem_id, sort_order);
```

## 프로젝트 기반 학습 경로 (Project-Based Learning)

```yaml
# Stage 1: 블록 코딩 프로젝트 (초등)
projects_block:
  - title: "인사하는 캐릭터"
    concepts: [순차, 이벤트]
    estimated: 15분
    description: "클릭하면 '안녕하세요!'라고 말하는 캐릭터"

  - title: "움직이는 고양이"
    concepts: [반복, 이동]
    estimated: 20분
    description: "화살표 키로 고양이를 움직여요"

  - title: "숫자 맞추기 게임"
    concepts: [변수, 조건, 비교]
    estimated: 30분
    description: "1~100 사이 숫자를 맞추는 게임"

  - title: "그림판 만들기"
    concepts: [이벤트, 좌표, 펜]
    estimated: 30분
    description: "마우스로 그림을 그릴 수 있는 캔버스"

  - title: "나만의 애니메이션"
    concepts: [종합]
    estimated: 45분
    description: "짧은 스토리 애니메이션 만들기"

# Stage 2: 블록→텍스트 전환 프로젝트 (중1)
projects_transition:
  - title: "Hello World 여행"
    concepts: [print, 문자열]
    estimated: 10분
    dual_view: true  # 블록/Python 동시 표시

  - title: "자기소개 프로그램"
    concepts: [input, 변수, 출력]
    estimated: 15분

  - title: "짝수/홀수 판별기"
    concepts: [조건문, 나머지연산]
    estimated: 20분

  - title: "구구단 출력기"
    concepts: [중첩반복, 포맷문자열]
    estimated: 25분

# Stage 3: 텍스트 코딩 프로젝트 (중2~고등)
projects_text:
  - title: "가위바위보 게임"
    concepts: [random, 조건, 함수]
    estimated: 20분

  - title: "단어장 프로그램"
    concepts: [딕셔너리, 파일입출력, CRUD]
    estimated: 40분

  - title: "성적 관리 시스템"
    concepts: [리스트, 함수, 정렬, 통계]
    estimated: 60분

  - title: "텍스트 RPG 게임"
    concepts: [클래스, 상속, 게임루프]
    estimated: 90분

# Stage 4: 알고리즘 프로젝트 (고등~)
projects_algorithm:
  - title: "정렬 시각화"
    concepts: [버블, 선택, 삽입, 퀵정렬]
    estimated: 60분

  - title: "미로 탐색"
    concepts: [BFS, DFS, 스택, 큐]
    estimated: 90분

  - title: "간단한 챗봇"
    concepts: [문자열처리, 패턴매칭, API]
    estimated: 120분
```

## 코드 실행 아키텍처 결정 가이드

```yaml
Pyodide (브라우저, 권장 기본):
  장점:
    - 서버 비용 0원
    - 즉시 실행 (네트워크 지연 없음)
    - 오프라인 가능 (PWA)
    - Python 3.14 + NumPy/Pandas 지원
    - 서버 비용 30~50% 절감
  단점:
    - 초기 로딩 ~20MB (캐싱으로 1회만)
    - JavaScript 실행 불가
    - 시스템 호출/네트워크 제한
  적합: 초등~중등 Python 학습, 기초 알고리즘

Judge0 (서버, 고급):
  장점:
    - 60+ 언어 지원 (Python, JS, Java, C++ 등)
    - 정확한 시간/메모리 제한
    - 완벽한 샌드박싱
    - 비동기 실행
  단점:
    - 서버 비용 (셀프호스팅 또는 API 요금)
    - 네트워크 지연 (~500ms)
  적합: 다중 언어, 알고리즘 대회, 고급 과정

하이브리드 전략 (권장):
  기본: Pyodide (브라우저 Python) — 무료 사용자
  고급: Judge0 API — 프리미엄 사용자, 다중 언어
  대회: Judge0 셀프호스팅 — 실시간 코딩 배틀

의존성:
  npm install pyodide           # Pyodide WASM
  npm install @monaco-editor/react  # Monaco 에디터
  npm install blockly            # 블록 코딩
  npm install @blockly/workspace-backpack
```

## 실시간 코딩 배틀 (Kahoot! for Code)

```typescript
// Supabase Realtime 기반 실시간 코딩 대결
interface CodingBattle {
  id: string;
  hostId: string;           // 교사
  status: 'waiting' | 'active' | 'finished';
  currentRound: number;
  problems: CodingProblem[];
  participants: Map<string, {
    score: number;
    solvedCount: number;
    totalTime: number;
  }>;
  settings: {
    timePerProblem: number;  // 초
    maxParticipants: number;
    difficulty: string;
    language: string;
  };
}

// 실시간 리더보드 업데이트
const channel = supabase.channel(`battle:${battleId}`)
  .on('broadcast', { event: 'submit' }, ({ payload }) => {
    // 학생이 코드 제출 → 즉시 채점 → 리더보드 업데이트
    const result = gradeSubmission(payload.code, currentProblem);
    channel.send({
      type: 'broadcast',
      event: 'leaderboard',
      payload: { studentId: payload.studentId, score: result.score, time: result.time },
    });
  })
  .subscribe();
```

## 코딩 교육 시드 데이터

```sql
-- Stage 1: 블록 코딩 문제
INSERT INTO coding_problems (title, description, difficulty, language, stage, category, starter_code, solution_code, hint, tags, xp_reward) VALUES
('첫 번째 출력', '화면에 "안녕하세요!"를 출력하세요.', 'easy', 'python', 'text', 'variable', 'print(___)', 'print("안녕하세요!")', '큰따옴표 안에 글자를 넣어보세요', ARRAY['print', '문자열'], 10),
('두 수의 합', '두 수를 입력받아 합을 출력하세요.', 'easy', 'python', 'text', 'variable', 'a = int(input())\nb = int(input())\nprint(___)', 'a = int(input())\nb = int(input())\nprint(a + b)', 'a와 b를 더하면?', ARRAY['input', '연산', '변수'], 15),
('짝수 홀수', '숫자를 입력받아 짝수면 "짝수", 홀수면 "홀수"를 출력하세요.', 'medium', 'python', 'text', 'condition', 'n = int(input())\nif ___:\n    print("짝수")\nelse:\n    print("홀수")', 'n = int(input())\nif n % 2 == 0:\n    print("짝수")\nelse:\n    print("홀수")', '2로 나눈 나머지가 0이면 짝수!', ARRAY['조건문', '나머지연산'], 20),
('구구단', '숫자를 입력받아 해당 구구단을 출력하세요.', 'medium', 'python', 'text', 'loop', 'n = int(input())\nfor i in range(1, ___):\n    print(f"{n} x {i} = {___}")', 'n = int(input())\nfor i in range(1, 10):\n    print(f"{n} x {i} = {n * i}")', 'range(1, 10)은 1부터 9까지!', ARRAY['반복문', 'f-string'], 25),
('최대값 찾기', '숫자 리스트에서 가장 큰 값을 찾는 함수를 작성하세요.', 'hard', 'python', 'text', 'function', 'def find_max(numbers):\n    ___', 'def find_max(numbers):\n    max_val = numbers[0]\n    for n in numbers:\n        if n > max_val:\n            max_val = n\n    return max_val', '첫 번째 값을 최대값으로 두고, 하나씩 비교해보세요', ARRAY['함수', '리스트', '반복'], 30);

-- 테스트 케이스
INSERT INTO coding_test_cases (problem_id, input, expected_output, is_hidden, sort_order)
SELECT id, '', '안녕하세요!', false, 1 FROM coding_problems WHERE title = '첫 번째 출력'
UNION ALL
SELECT id, '3\n5', '8', false, 1 FROM coding_problems WHERE title = '두 수의 합'
UNION ALL
SELECT id, '-1\n1', '0', false, 2 FROM coding_problems WHERE title = '두 수의 합'
UNION ALL
SELECT id, '100\n200', '300', true, 3 FROM coding_problems WHERE title = '두 수의 합';
```

## 코드 시각화 (Python Tutor 스타일)

> 코드 실행을 한 줄씩 시각화하여 변수/메모리 상태를 보여주는 학습 도구
> UC Berkeley, MIT, U of Washington 등 25+ 대학에서 CS1 과정에 사용

### 구현 방식

```typescript
// 코드 실행 시각화 상태
interface ExecutionStep {
  line: number;                // 현재 실행 줄
  globals: Record<string, VisualizableValue>;  // 전역 변수
  stack: StackFrame[];         // 콜 스택
  heap: HeapObject[];          // 힙 객체 (리스트, 딕셔너리 등)
  stdout: string;              // 누적 출력
  event: 'step_line' | 'call' | 'return' | 'exception';
}

interface StackFrame {
  funcName: string;
  locals: Record<string, VisualizableValue>;
  returnValue?: VisualizableValue;
}

interface VisualizableValue {
  type: 'int' | 'str' | 'float' | 'bool' | 'list' | 'dict' | 'None' | 'ref';
  value: unknown;
  id?: number;  // 힙 참조 ID (list, dict 등)
}

// Pyodide + AST 기반 스텝 실행
// 방법 1: Python ast 모듈로 코드를 줄 단위 분해 후 순차 실행
// 방법 2: sys.settrace() 콜백으로 실행 추적
const TRACE_CODE = `
import sys, json
_trace_log = []

def _tracer(frame, event, arg):
    if event in ('line', 'call', 'return', 'exception'):
        _trace_log.append({
            'line': frame.f_lineno,
            'event': event,
            'locals': {k: repr(v) for k, v in frame.f_locals.items() if not k.startswith('_')},
            'func': frame.f_code.co_name,
        })
    return _tracer

sys.settrace(_tracer)
exec(USER_CODE)
sys.settrace(None)
print(json.dumps(_trace_log))
`;

// React 시각화 컴포넌트
// - 왼쪽: 코드 (현재 줄 하이라이트)
// - 오른쪽 상단: 변수 테이블 (이름, 타입, 값)
// - 오른쪽 하단: 콜 스택 시각화
// - 하단: 출력 패널
// - 컨트롤: ◀ 이전 | ▶ 다음 | ⏩ 실행 | ⏸ 일시정지
```

### 시각화 UI 레이아웃

```
┌────────────────────┬─────────────────────┐
│  📝 코드            │  📦 변수             │
│                    │  x = 5   (int)      │
│  1  x = 5         │  y = 10  (int)      │
│  2  y = 10        │  total = 15 (int)   │
│ ▶3  total = x + y │                     │
│  4  print(total)  ├─────────────────────┤
│                    │  📚 콜 스택          │
│                    │  ┌─ <module> ─────┐ │
│                    │  │ line 3        │ │
│                    │  └────────────────┘ │
├────────────────────┴─────────────────────┤
│  💻 출력: (아직 없음)                      │
├──────────────────────────────────────────┤
│  ◀ 이전  │  ▶ 다음  │  ⏩ 끝까지  │ 3/4  │
└──────────────────────────────────────────┘
```

## 터틀 그래픽스 (Turtle Graphics)

> 초등~중등 프로그래밍 입문의 표준 도구, 브라우저 Canvas에서 실행

```typescript
// 브라우저 내 Turtle 구현 (Canvas 기반)
class BrowserTurtle {
  private x = 0;
  private y = 0;
  private angle = 0;        // 도 (0 = 오른쪽)
  private penDown = true;
  private penColor = '#000000';
  private penWidth = 2;
  private speed = 5;        // 1~10 (애니메이션 속도)
  private ctx: CanvasRenderingContext2D;
  private commandQueue: TurtleCommand[] = [];

  // 기본 명령 (Python turtle 호환)
  forward(distance: number) { /* 전진 */ }
  backward(distance: number) { /* 후진 */ }
  right(angle: number) { /* 우회전 */ }
  left(angle: number) { /* 좌회전 */ }
  penup() { this.penDown = false; }
  pendown() { this.penDown = true; }
  color(c: string) { this.penColor = c; }
  width(w: number) { this.penWidth = w; }
  goto(x: number, y: number) { /* 이동 */ }
  circle(radius: number) { /* 원 그리기 */ }

  // 애니메이션 큐 실행 (한 명령씩 보여주기)
  async executeAnimated() {
    for (const cmd of this.commandQueue) {
      await this.animateCommand(cmd);
      await sleep(100 / this.speed);  // 속도 조절
    }
  }
}

// Pyodide에서 turtle 명령을 Canvas로 브릿지
// Python 코드에서 turtle.forward(100)을 호출하면
// JavaScript의 BrowserTurtle.forward(100)이 실행됨
const TURTLE_BRIDGE = `
import js
class Turtle:
    def forward(self, d): js.turtle.forward(d)
    def right(self, a): js.turtle.right(a)
    def left(self, a): js.turtle.left(a)
    def penup(self): js.turtle.penup()
    def pendown(self): js.turtle.pendown()
    def color(self, c): js.turtle.color(c)
    def circle(self, r): js.turtle.circle(r)
    fd = forward
    rt = right
    lt = left
t = Turtle()
`;

// 터틀 그래픽스 문제 예시
const TURTLE_PROBLEMS = [
  {
    title: '정사각형 그리기',
    description: '터틀을 이용해 한 변의 길이가 100인 정사각형을 그리세요.',
    difficulty: 'easy',
    starterCode: 'for i in range(4):\n    t.forward(___)\n    t.right(___)',
    solutionCode: 'for i in range(4):\n    t.forward(100)\n    t.right(90)',
    hint: '정사각형의 각 꼭짓점에서 90도 회전!',
  },
  {
    title: '별 그리기',
    description: '5개 꼭짓점을 가진 별을 그리세요.',
    difficulty: 'medium',
    starterCode: 'for i in range(5):\n    t.forward(100)\n    t.right(___)',
    solutionCode: 'for i in range(5):\n    t.forward(100)\n    t.right(144)',
    hint: '별의 외각은 144도!',
  },
  {
    title: '나선형 그리기',
    description: '점점 커지는 나선형을 그리세요.',
    difficulty: 'hard',
    starterCode: 'for i in range(50):\n    t.forward(___)\n    t.right(___)',
    solutionCode: 'for i in range(50):\n    t.forward(i * 3)\n    t.right(91)',
    hint: '전진 거리를 점점 늘려보세요!',
  },
];
```

## Sandpack 라이브 플레이그라운드 (JavaScript/React)

> CodeSandbox의 오픈소스 라이브러리, React 공식 문서에서도 사용
> npm install @codesandbox/sandpack-react

```typescript
import { Sandpack } from '@codesandbox/sandpack-react';

// JavaScript/React 코딩 교육용 임베디드 플레이그라운드
function JSPlayground({ initialCode, template }: {
  initialCode: Record<string, string>;
  template: 'vanilla' | 'react' | 'vanilla-ts' | 'react-ts';
}) {
  return (
    <Sandpack
      template={template}
      files={initialCode}
      theme="light"
      options={{
        showNavigator: false,
        showTabs: true,
        showLineNumbers: true,
        editorHeight: 400,
        showConsole: true,
        showConsoleButton: true,
      }}
      customSetup={{
        dependencies: {
          // 필요한 npm 패키지 자동 설치
        },
      }}
    />
  );
}

// 사용 예: React 컴포넌트 만들기 과제
<JSPlayground
  template="react"
  initialCode={{
    '/App.js': `export default function App() {
  // TODO: "안녕하세요!" 버튼을 만들어보세요
  // 클릭하면 alert이 뜨도록!
  return (
    <div>
      <h1>내 첫 React 앱</h1>
      {/* 여기에 버튼 추가 */}
    </div>
  );
}`,
  }}
/>
```

## AI 코드 리뷰 시스템

```typescript
const CODE_REVIEW_PROMPT = `
당신은 코딩 교육용 AI 코드 리뷰어입니다.

학생이 제출한 코드를 분석하고 피드백을 제공하세요.

학생 정보:
- 학년: {grade}
- 단계: {stage} (block/transition/text/algorithm)
- 문제: {problemTitle}

분석 항목:
1. **정확성**: 코드가 올바르게 작동하는가?
2. **가독성**: 변수명이 적절한가? 들여쓰기가 맞는가?
3. **효율성**: 더 간단한 방법이 있는가? (고급 단계만)
4. **패턴**: 잘한 점은 무엇인가? 개선할 점은?

피드백 형식:
- 잘한 점 1~2개 (반드시 칭찬 먼저)
- 개선할 점 1~2개 (구체적, 학년 수준에 맞게)
- 추천 다음 단계 (심화 개념 또는 비슷한 문제)

절대 규칙:
- 전체 정답 코드를 보여주지 마세요
- 학년에 맞는 쉬운 한국어 사용
- 격려 톤 유지
`;

// 자동 코드 품질 체크 (AI 없이)
function analyzeCodeQuality(code: string, language: string): CodeQualityReport {
  const issues: CodeIssue[] = [];

  if (language === 'python') {
    // 변수명 체크
    const singleLetterVars = code.match(/\b([a-z])\s*=/g);
    if (singleLetterVars && singleLetterVars.length > 2) {
      issues.push({
        type: 'readability',
        message: '변수 이름을 좀 더 의미 있게 지어보세요. x, y 대신 width, height처럼!',
        severity: 'suggestion',
      });
    }

    // 중복 코드 감지
    const lines = code.split('\n');
    const duplicates = findDuplicateLines(lines, 3);
    if (duplicates.length > 0) {
      issues.push({
        type: 'efficiency',
        message: '비슷한 코드가 반복돼요. 반복문이나 함수로 줄여볼까요?',
        severity: 'suggestion',
      });
    }

    // 주석 체크 (고급 단계)
    if (!code.includes('#') && code.split('\n').length > 10) {
      issues.push({
        type: 'readability',
        message: '코드가 길어지면 주석(#)을 달아두면 나중에 이해하기 쉬워요!',
        severity: 'info',
      });
    }
  }

  return {
    score: Math.max(0, 100 - issues.length * 15),
    issues,
  };
}
```

## 코딩 포트폴리오 & 디지털 뱃지

```yaml
학생 포트폴리오:
  구성:
    - 프로필 (아바타, 레벨, 칭호)
    - 완료한 프로젝트 갤러리 (스크린샷 + 코드)
    - 획득한 뱃지/수료증
    - 기술 스택 태그 (Python, Scratch 등)
    - 활동 히트맵 (GitHub 스타일)
    - 공개/비공개 설정

  공유:
    - 고유 URL (user.app.com/portfolio)
    - 소셜 공유 카드 (OG Image 자동 생성)
    - PDF 내보내기 (입시/자소서용)

디지털 뱃지 (Open Badges 표준):
  코딩 뱃지:
    - "Hello World 마스터" — 첫 프로그램 작성
    - "루프 달인" — 반복문 20문제 통과
    - "함수 건축가" — 함수 10개 정의
    - "디버그 탐정" — 버그 20개 수정
    - "알고리즘 용사" — 정렬/탐색 알고리즘 구현
    - "프로젝트 완주자" — 프로젝트 3개 완성
    - "코드 리뷰어" — 다른 학생 코드에 피드백 3회
    - "오픈소스 기여자" — 공유 프로젝트 참여

  수료증:
    - "Python 기초 수료" — Stage 2 전체 완료
    - "웹 개발 입문 수료" — HTML/CSS/JS 과정 완료
    - "알고리즘 기초 수료" — Stage 4 완료

npm 의존성 추가:
  - @codesandbox/sandpack-react  # JS/React 플레이그라운드
  - pyodide                      # 브라우저 Python
  - blockly                      # 블록 코딩
  - @monaco-editor/react         # 코드 에디터
  - react-dnd                    # 드래그&드롭
```

## 실시간 페어 프로그래밍 (Monaco + Supabase Realtime)

> CodeMirror OT 또는 Monaco + CRDT로 학생 2명이 동시 편집

```typescript
// Supabase Realtime 기반 협업 에디터
// 교사-학생 1:1 코딩 멘토링 또는 학생-학생 페어 프로그래밍

interface CollaborationState {
  sessionId: string;
  participants: Array<{ userId: string; displayName: string; cursorPosition: number; color: string }>;
  code: string;
  language: string;
}

// Supabase Realtime Broadcast로 커서 위치 + 코드 변경 동기화
const channel = supabase.channel(`collab:${sessionId}`)
  .on('broadcast', { event: 'code_change' }, ({ payload }) => {
    // 다른 사용자의 코드 변경 적용
    editor.setValue(payload.code);
  })
  .on('broadcast', { event: 'cursor_move' }, ({ payload }) => {
    // 다른 사용자 커서 위치 표시 (색상 구분)
    showRemoteCursor(payload.userId, payload.position, payload.color);
  })
  .on('presence', { event: 'sync' }, () => {
    // 현재 접속자 목록 업데이트
  })
  .subscribe();

// 코드 변경 시 브로드캐스트
function onCodeChange(newCode: string) {
  channel.send({
    type: 'broadcast',
    event: 'code_change',
    payload: { code: newCode, userId: currentUser.id },
  });
}
```

## Online Judge 시스템 (DMOJ 스타일)

> 경쟁 프로그래밍 + 알고리즘 학습을 위한 자동 채점 플랫폼
> DMOJ: 오픈소스, 60+ 언어, 대회 기능, Markdown/LaTeX 지원

```yaml
OJ 기능 설계:
  문제 목록:
    - 난이도별 필터 (easy/medium/hard/expert)
    - 태그별 필터 (정렬, 탐색, DP, 그래프, 문자열 등)
    - 정답률 표시
    - 풀이 수 표시

  문제 상세:
    - 문제 설명 (마크다운 + LaTeX 수식)
    - 입출력 형식
    - 예제 테스트 케이스 (복사 버튼)
    - 시간/메모리 제한
    - 힌트 (유료 또는 포인트 소모)

  제출 & 채점:
    - 코드 에디터 (Monaco)
    - 언어 선택 (Python, JS, C++, Java)
    - 제출 → Judge0 실행 → 결과
    - 결과: AC(정답), WA(오답), TLE(시간초과), MLE(메모리초과), RE(런타임에러), CE(컴파일에러)
    - 테스트 케이스별 결과 표시

  리더보드:
    - 문제별 최단 시간/최소 메모리 순위
    - 전체 풀이 수 랭킹
    - 주간/월간 활성 사용자

  대회 (Contest):
    - 시작/종료 시간 설정
    - 실시간 스코어보드
    - 패널티 시스템 (ACM-ICPC 스타일)
    - 가상 참가 (Virtual Participation)

채점 상태 코드:
  AC: "정답! 🎉" (초록)
  WA: "오답 😢 — 출력을 다시 확인해보세요" (빨강)
  TLE: "시간 초과 ⏱️ — 더 빠른 알고리즘을 생각해보세요" (노랑)
  MLE: "메모리 초과 💾 — 메모리를 덜 쓰는 방법을 찾아보세요" (노랑)
  RE: "실행 에러 💥 — 배열 범위나 0으로 나누기를 확인하세요" (주황)
  CE: "컴파일 에러 🔧 — 문법 오류를 수정하세요" (회색)
```

## StackBlitz WebContainers (고급 웹 개발 교육)

> 브라우저에서 완전한 Node.js 환경 실행 — 밀리초 단위 부팅

```yaml
용도: 고등/성인 웹 개발 교육 (Next.js, Express, React 프로젝트)
장점:
  - 서버 불필요 (브라우저 내 Node.js)
  - npm install 가능
  - 터미널 지원
  - 실제 프로덕션 환경과 동일
단점:
  - Python/Java 미지원 (Node.js 전용)
  - 무거운 프로젝트는 느릴 수 있음
적합: "Next.js 앱 만들기", "Express API 서버" 같은 실습

통합:
  - npm install @stackblitz/sdk
  - StackBlitz.openProject() 또는 embed()로 임베딩
```
