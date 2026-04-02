# 게이미피케이션 시스템 설계 가이드

> Duolingo, Prodigy Math, 밀크T, 아이스크림홈런 등 벤치마크 기반

## 핵심 게이미피케이션 요소

### 1. XP (경험치) 시스템

```typescript
// XP 획득 조건 및 기본값
const XP_TABLE = {
  // 문제 풀이
  correctAnswer: { easy: 10, medium: 20, hard: 30, challenge: 50 },
  wrongAnswer: { easy: 1, medium: 2, hard: 3, challenge: 5 },

  // 보너스
  firstTryBonus: 1.5,          // 첫 시도 정답 × 1.5
  speedBonus: 1.2,             // 시간 내 정답 × 1.2
  streakMultiplier: 0.02,      // 스트릭 1일당 +2% (최대 30일 = +60%)
  perfectDayBonus: 50,         // 하루 목표 전부 정답
  weeklyPerfectBonus: 200,     // 7일 연속 완벽

  // 활동
  dailyLogin: 5,               // 일일 접속
  completeLesson: 30,          // 단원 완료
  helpFriend: 15,              // 친구 도움
  reviewMistakes: 10,          // 오답 복습
};
```

### 2. 레벨 시스템

```typescript
// 레벨별 필요 XP (지수 증가)
const LEVEL_CONFIG = {
  baseXP: 100,
  growthRate: 1.15,
  maxLevel: 100,

  // 레벨 구간별 칭호
  titles: [
    { minLevel: 1, maxLevel: 5, title: '수학 새싹', emoji: '🌱' },
    { minLevel: 6, maxLevel: 10, title: '수학 탐험가', emoji: '🧭' },
    { minLevel: 11, maxLevel: 20, title: '수학 모험가', emoji: '⚔️' },
    { minLevel: 21, maxLevel: 30, title: '수학 용사', emoji: '🛡️' },
    { minLevel: 31, maxLevel: 40, title: '수학 기사', emoji: '🗡️' },
    { minLevel: 41, maxLevel: 50, title: '수학 마법사', emoji: '🧙' },
    { minLevel: 51, maxLevel: 60, title: '수학 현자', emoji: '📖' },
    { minLevel: 61, maxLevel: 70, title: '수학 대마법사', emoji: '🔮' },
    { minLevel: 71, maxLevel: 80, title: '수학 영웅', emoji: '🦸' },
    { minLevel: 81, maxLevel: 90, title: '수학 전설', emoji: '👑' },
    { minLevel: 91, maxLevel: 100, title: '수학 신', emoji: '⭐' },
  ],
};

function getRequiredXP(level: number): number {
  return Math.floor(LEVEL_CONFIG.baseXP * Math.pow(LEVEL_CONFIG.growthRate, level - 1));
}

function getTotalXPForLevel(level: number): number {
  let total = 0;
  for (let i = 1; i < level; i++) {
    total += getRequiredXP(i);
  }
  return total;
}
```

### 3. 뱃지 시스템

```typescript
const BADGES = [
  // 첫 경험
  { id: 'first_solve', name: '첫 발걸음', desc: '첫 문제를 풀었어요!', icon: '👣', condition: 'total_solved >= 1' },
  { id: 'first_streak', name: '꾸준함의 시작', desc: '2일 연속 학습!', icon: '🔥', condition: 'streak >= 2' },

  // 풀이 수 마일스톤
  { id: 'solver_10', name: '열 번째 도전', desc: '10문제 풀기', icon: '🎯', condition: 'total_solved >= 10' },
  { id: 'solver_50', name: '반백 용사', desc: '50문제 풀기', icon: '⚡', condition: 'total_solved >= 50' },
  { id: 'solver_100', name: '백전불태', desc: '100문제 풀기', icon: '💯', condition: 'total_solved >= 100' },
  { id: 'solver_500', name: '오백 전사', desc: '500문제 풀기', icon: '🏆', condition: 'total_solved >= 500' },
  { id: 'solver_1000', name: '천 문제 달인', desc: '1000문제 풀기', icon: '👑', condition: 'total_solved >= 1000' },

  // 스트릭
  { id: 'streak_7', name: '일주일 전사', desc: '7일 연속 학습', icon: '🔥', condition: 'streak >= 7' },
  { id: 'streak_14', name: '2주 마라톤', desc: '14일 연속 학습', icon: '🌟', condition: 'streak >= 14' },
  { id: 'streak_30', name: '한 달 챔피언', desc: '30일 연속 학습', icon: '💎', condition: 'streak >= 30' },
  { id: 'streak_100', name: '100일 전설', desc: '100일 연속 학습', icon: '🏅', condition: 'streak >= 100' },
  { id: 'streak_365', name: '1년 신화', desc: '365일 연속 학습', icon: '🌈', condition: 'streak >= 365' },

  // 정확도
  { id: 'perfect_10', name: '완벽한 10문제', desc: '10문제 연속 정답', icon: '✨', condition: 'consecutive_correct >= 10' },
  { id: 'perfect_day', name: '완벽한 하루', desc: '하루 문제 전부 정답', icon: '🌞', condition: 'daily_accuracy === 100' },
  { id: 'accuracy_90', name: '명사수', desc: '전체 정답률 90%+', icon: '🎯', condition: 'overall_accuracy >= 90' },

  // 속도
  { id: 'speed_demon', name: '번개 계산기', desc: '10초 내 정답 5연속', icon: '⚡', condition: 'fast_correct >= 5' },

  // 단원 완료
  { id: 'chapter_clear', name: '단원 정복자', desc: '한 단원 100% 완료', icon: '📚', condition: 'chapters_completed >= 1' },
  { id: 'grade_clear', name: '학년 마스터', desc: '한 학년 전체 완료', icon: '🎓', condition: 'grades_completed >= 1' },

  // 사회성
  { id: 'helpful', name: '도움의 손길', desc: '친구에게 힌트 공유', icon: '🤝', condition: 'helps_given >= 1' },
  { id: 'team_player', name: '팀 플레이어', desc: '그룹 챌린지 참여', icon: '👥', condition: 'group_challenges >= 1' },

  // 시크릿
  { id: 'midnight', name: '밤의 학자', desc: '자정에 문제 풀기', icon: '🦉', condition: 'solved_at_midnight' },
  { id: 'early_bird', name: '아침형 학생', desc: '오전 6시 전 학습', icon: '🐦', condition: 'solved_before_6am' },
  { id: 'weekend_warrior', name: '주말 전사', desc: '토요일+일요일 연속 학습', icon: '🏋️', condition: 'weekend_streak' },
];
```

### 4. 스트릭 시스템

```typescript
const STREAK_CONFIG = {
  // 스트릭 유지 조건
  dailyMinProblems: 1,          // 하루 최소 1문제 풀기
  resetTime: '04:00',           // 새벽 4시 기준 (날짜 변경)
  timezone: 'Asia/Seoul',

  // 스트릭 보호
  freezePerMonth: 2,            // 월 2회 무료 프리즈 (유료 회원 무제한)
  freezeCost: 50,               // 코인으로 추가 프리즈 구매

  // 스트릭 보상
  milestones: [
    { days: 3, reward: { coins: 10, xp: 30 } },
    { days: 7, reward: { coins: 30, xp: 100 } },
    { days: 14, reward: { coins: 70, xp: 250 } },
    { days: 30, reward: { coins: 200, xp: 500 } },
    { days: 60, reward: { coins: 500, xp: 1000 } },
    { days: 100, reward: { coins: 1000, xp: 2000 } },
    { days: 365, reward: { coins: 5000, xp: 10000 } },
  ],
};
```

### 5. 코인 & 상점 시스템

```typescript
const SHOP_ITEMS = [
  // 아바타
  { id: 'avatar_ninja', name: '닌자 아바타', price: 100, category: 'avatar' },
  { id: 'avatar_wizard', name: '마법사 아바타', price: 100, category: 'avatar' },
  { id: 'avatar_astronaut', name: '우주비행사 아바타', price: 200, category: 'avatar' },
  { id: 'avatar_robot', name: '로봇 아바타', price: 200, category: 'avatar' },

  // 테마
  { id: 'theme_dark', name: '다크 모드', price: 50, category: 'theme' },
  { id: 'theme_ocean', name: '바다 테마', price: 150, category: 'theme' },
  { id: 'theme_forest', name: '숲 테마', price: 150, category: 'theme' },
  { id: 'theme_space', name: '우주 테마', price: 200, category: 'theme' },

  // 효과
  { id: 'effect_confetti', name: '정답 시 폭죽 효과', price: 100, category: 'effect' },
  { id: 'effect_fireworks', name: '레벨업 불꽃놀이', price: 150, category: 'effect' },

  // 기능성
  { id: 'streak_freeze', name: '스트릭 프리즈 (1회)', price: 50, category: 'utility' },
  { id: 'hint_token', name: '힌트 토큰 (3개)', price: 30, category: 'utility' },
  { id: 'double_xp', name: '2배 XP (1시간)', price: 100, category: 'utility' },
];
```

### 6. 랭킹 시스템

```typescript
const RANKING_CONFIG = {
  periods: ['daily', 'weekly', 'monthly', 'allTime'],
  scopes: ['class', 'grade', 'school', 'global'],

  // 리그 시스템 (Duolingo 스타일)
  leagues: [
    { id: 'bronze', name: '브론즈', minRank: 0, color: '#CD7F32' },
    { id: 'silver', name: '실버', minRank: 10, color: '#C0C0C0' },
    { id: 'gold', name: '골드', minRank: 20, color: '#FFD700' },
    { id: 'diamond', name: '다이아', minRank: 30, color: '#B9F2FF' },
    { id: 'master', name: '마스터', minRank: 40, color: '#FF6B6B' },
  ],

  // 주간 리그 승급/강등
  promotionTop: 10,    // 상위 10명 승급
  relegationBottom: 5, // 하위 5명 강등
  leagueSize: 30,      // 리그당 30명
};
```

## 보상 이펙트 (Framer Motion)

```typescript
// 정답 시 축하 애니메이션
const correctAnimation = {
  scale: [1, 1.2, 1],
  rotate: [0, 10, -10, 0],
  transition: { duration: 0.5 }
};

// 레벨업 이펙트
const levelUpAnimation = {
  initial: { scale: 0, opacity: 0 },
  animate: { scale: 1, opacity: 1 },
  exit: { scale: 2, opacity: 0 },
  transition: { type: 'spring', stiffness: 200 }
};

// 뱃지 획득 이펙트
const badgeUnlockAnimation = {
  initial: { y: 50, opacity: 0, rotateY: 180 },
  animate: { y: 0, opacity: 1, rotateY: 0 },
  transition: { type: 'spring', stiffness: 150, damping: 15 }
};

// 코인 획득 (+10 텍스트 날아가기)
const coinAnimation = {
  initial: { y: 0, opacity: 1 },
  animate: { y: -60, opacity: 0 },
  transition: { duration: 1, ease: 'easeOut' }
};
```

## Octalysis 8 Core Drives (게이미피케이션 심리학)

> Yu-kai Chou의 Octalysis 프레임워크 — 인간 동기의 8가지 핵심 동력

```yaml
1. Epic Meaning (서사적 의미):
  설명: "나보다 큰 것에 기여하고 있다"
  적용: "수학 히어로가 되어 세상을 구하자!"
  구현: 스토리라인, 미션, 세계관

2. Development (성장 & 성취):
  설명: "나는 발전하고 있다"
  적용: 레벨업, XP 바, 진행률
  구현: 진도 시각화, 마일스톤 보상

3. Empowerment (창의적 권한):
  설명: "나만의 방법으로 할 수 있다"
  적용: 다양한 풀이 방법 인정, 커스텀 아바타
  구현: 선택지, 커스터마이징, 자유도

4. Ownership (소유 & 수집):
  설명: "이것은 내 것이다"
  적용: 뱃지 컬렉션, 아바타, 코인
  구현: 인벤토리, 수집 시스템

5. Social Influence (사회적 영향):
  설명: "다른 사람과 비교/협력하고 싶다"
  적용: 랭킹, 친구 초대, 그룹 챌린지
  구현: 리더보드, 소셜 피드

6. Scarcity (희소성 & 조급함):
  설명: "지금 아니면 놓친다"
  적용: 한정 이벤트, 데일리 보상, 스트릭
  구현: 시간 제한 챌린지, 일일 미션

7. Unpredictability (예측 불가):
  설명: "다음에 뭐가 나올까?"
  적용: 랜덤 보상, 깜짝 뱃지, 미스터리 박스
  구현: 가변 보상 스케줄

8. Avoidance (손실 회피):
  설명: "잃고 싶지 않다"
  적용: 스트릭 끊김 경고, 리그 강등
  구현: 프리즈 시스템, 경고 알림
```

### 교육 앱에서의 Core Drives 균형

```yaml
권장 비중 (교육 앱):
  Development (성장): 30% — 가장 중요, 학습 진행감
  Empowerment (권한): 20% — 학습 자율성
  Social (사회): 15% — 건전한 경쟁
  Ownership (소유): 15% — 보상 수집
  Meaning (의미): 10% — 학습 목적
  Scarcity (희소): 5% — 적절한 긴장감
  Unpredictability (예측불가): 3% — 재미 요소
  Avoidance (손실): 2% — 최소한만 (아동에게 과도한 압박 X)

주의: 아동 대상 앱에서 Avoidance(손실 회피)는 최소화.
      스트릭 끊김 시 벌칙보다 복귀 보상에 집중.
```

## UX 모범 사례 (벤치마크)

### Duolingo에서 배운 것
- 한 세션 = 5~15분 (짧고 집중)
- 하트 시스템으로 실수 제한 (무료)
- 리그로 경쟁심 자극
- 스트릭으로 습관 형성
- 즉각적인 시각/청각 피드백

### Khan Academy에서 배운 것
- 마스터리 기반 진도 (80% 정답 시 다음 단계)
- 힌트 시스템 (단계별 힌트)
- 포인트 + 에너지 바
- 코스 맵으로 전체 진도 시각화

### Prodigy Math에서 배운 것
- RPG 스토리라인과 학습 결합
- 몬스터 배틀 = 문제 풀이
- 장비/펫 커스터마이징
- 반 단위 과제 할당

### 밀크T/아이스크림홈런에서 배운 것
- 한국 교과서 연계 필수
- AI 기반 취약점 분석
- 학부모 리포트 (일간/주간)
- 영상 강의 + 문제 풀이 결합
