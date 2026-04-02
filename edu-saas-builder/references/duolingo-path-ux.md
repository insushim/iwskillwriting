# 듀오링고 스타일 학습 경로 UX 구현 가이드

> 실전 구현 경험 기반 (매쓰버스 프로젝트 2026.04)

## 핵심 원칙

### 1. 스테이지 기반 학습 경로
- 각 스킬 = 10문제 스테이지
- 스테이지 완료 → 다음 스테이지 잠금해제
- 마스터리 기반: 80% 정답률 × 최소 5문제 → 마스터

### 2. 지그재그 시각 경로
```typescript
// 노드를 좌우로 오프셋하여 지그재그 효과
const OFFSETS = [0, -24, -36, -24, 0, 24, 36, 24]; // 8-cycle
// 각 노드에 transform: translateX(offset)px 적용
```

### 3. 노드 상태별 시각화
```yaml
mastered:   초록 원 + ✓/⭐/👑 (crown 레벨에 따라)
current:    보라 원 + ▶ + ring glow + bounce 화살표 + "10문제" 뱃지
learning:   파란 원 + 정답률% + progress ring
review:     주황 원 + 새로고침 아이콘
locked:     회색 원 + 자물쇠
```

## 접기/펼치기 (Collapsible Units)

### 문제점 (실전 교훈)
- 단원이 5+개이고 단원당 7-8개 스킬이면 **경로가 너무 길어서** 스크롤 피로도 높음
- PC에서 특히 길게 느껴짐 (모바일은 스크롤에 익숙)

### 해결책: 단원별 카드 접기/펼치기
```typescript
// 현재 단원만 펼치고 나머지는 접기
const visibleUnits = showAll
  ? unitGroups
  : unitGroups.filter((_, i) => i >= activeIdx - 1 && i <= activeIdx + 1);

// 접힌 단원 헤더에 진행도 표시
<button onClick={() => setExpanded(!expanded)}>
  <span>{masteredCount}/{stages.length}</span>
  <span>{unit.nameKo}</span>
  {expanded ? <ChevronDown/> : <ChevronRight/>}
</button>
```

### 더보기 버튼
- "나머지 N개 단원 더보기" / "접기" 토글
- 이전 단원: "이전 N개 단원 보기"

## 단원별 복습 체크포인트

### 구조
각 단원 마지막에 복습 노드 추가:
```
스킬1 → 스킬2 → ... → 스킬N → [단원 복습]
```

### 복습 노드 상태
- **전부 마스터**: 트로피 아이콘 + "단원 완료!"
- **진행중**: 새로고침 아이콘 + "복습 N/M 마스터"
- **잠김**: 회색 + 마지막 스킬이 잠김 상태

## 스킬 설계 패턴 (단원당 7-8개)

### 실전 교훈: 2-3개는 너무 적음
사용자 피드백: "한단원에 복습까지 포함해서 5개라니"

### 권장 구조 (개념-연습-심화 패턴)
```yaml
1. 개념 도입 (난이도 0.3)      - 핵심 개념 이해
2. 개념 연습 (난이도 0.4)      - 기본 문제 반복
3. 심화 개념 (난이도 0.5)      - 두 번째 개념 도입
4. 심화 연습 (난이도 0.6)      - 심화 문제 반복
5. 실전 적용 (난이도 0.7)      - 두 개념 결합
6. 도전 문제 (난이도 0.8)      - 고난도 문제
7. 문장제/활용 (난이도 0.8)    - 실생활 적용
(+ 단원 복습 체크포인트)
```

### 연습 스킬의 중요성
- 개념 스킬만으로는 **충분한 반복 연습이 안됨**
- "연습" 스킬은 같은 유형 문제를 다양한 숫자로 반복
- 적응형 엔진이 정답률이 안정될 때까지 비슷한 문제 계속 출제
- `ensureMinimumPool()`로 문제가 부족하면 절차적 생성

## 오답 재풀기 시스템 (Retry Wrong Questions)

### 실전 교훈: "틀리면 바로 답을 알려주지 말고 다시 풀게 해줘"
기존: 틀리면 즉시 정답+해설 표시 → 학생이 답만 외움
개선: 틀린 문제를 나중에 다시 풀어서 **실제 학습**이 일어나게

### 구현 흐름
```
Phase 1: first_round (10문제)
├─ 정답 → "정답이에요! 🎉" + 해설 표시
├─ 오답 → "아쉬워요 😢" + 해설 숨김 + "나중에 다시 풀어볼게요 💪"
└─ wrongIndices에 오답 인덱스 저장

Phase 2: retry_intro (오답이 있을 때만)
├─ "틀린 문제를 다시 풀어봐요!" 화면
├─ 맞은 개수 / 틀린 개수 표시
└─ "다시 풀기" 버튼

Phase 3: retry_round (오답만 재출제)
├─ "오답 재풀기" 뱃지 표시
├─ 정답 → 해설 표시
└─ 오답 → 이번에는 해설 표시 (이미 한번 시도했으므로)

Phase 4: complete (결과)
├─ 전체 정답률/XP/맞은 문제
└─ "재풀기 N/M 성공" 뱃지
```

### QuestionDisplay에 hideExplanation prop 추가
```typescript
interface QuestionDisplayProps {
  // ...기존 props
  hideExplanation?: boolean; // 오답 시 해설 숨김
}

// 렌더링 시
{!(hideExplanation && !isCorrect) && (
  <p>{content.explanation}</p>
)}
```

### 핵심 타입
```typescript
type Phase = 'first_round' | 'retry_intro' | 'retry_round' | 'complete';

// 상태
const [phase, setPhase] = useState<Phase>('first_round');
const [wrongIndices, setWrongIndices] = useState<number[]>([]);
const [retryQueue, setRetryQueue] = useState<SeedQuestion[]>([]);
const [retryIndex, setRetryIndex] = useState(0);
```

## Cloudflare Workers 배포 주의사항

### 실전 교훈: Vercel이 아닌 CF Workers 환경
```bash
# 빌드만으로는 배포 안됨! 수동 배포 필요
npm run cf:deploy  # = opennextjs-cloudflare build + wrangler deploy

# package.json scripts
"cf:build": "npx opennextjs-cloudflare build",
"cf:deploy": "npx opennextjs-cloudflare build && wrangler deploy"
```

### git push만으로는 자동 배포 안될 수 있음
- Vercel: git push → 자동 배포
- CF Workers: git push 후 `npm run cf:deploy` 별도 실행 필요
- 또는 GitHub Actions CI/CD 설정

## CSS/Tailwind 패턴

### 그래디언트 노드
```tsx
// mastered 노드
'border-emerald-400 bg-gradient-to-br from-emerald-400 to-emerald-500 text-white shadow-lg shadow-emerald-200'

// current 노드 (가장 눈에 띄게)
'border-violet-400 bg-gradient-to-br from-violet-500 to-purple-600 text-white shadow-lg ring-4 ring-violet-200'
```

### rounded-2xl 통일
모든 카드, 버튼, 컨테이너에 `rounded-2xl` 적용하여 Duolingo 느낌 통일

### 스탯 스트립 (가로 배치)
4열 그리드 대신 가로 flex + 구분선으로 한 줄에 배치:
```tsx
<div className="flex items-center justify-between rounded-2xl bg-gradient-to-r from-slate-50 to-slate-100 p-3">
  <StatPill icon={<Flame/>} value={streak} label="연속" color="text-orange-500"/>
  <div className="h-6 w-px bg-border"/>
  <StatPill icon={<Star/>} value={xp} label="XP" color="text-purple-500"/>
  ...
</div>
```
