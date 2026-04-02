# ⚖️ 게임 밸런스 스킬

## 설명
게임의 난이도, 경제, 진행 시스템의 밸런스를 설계하고 조정합니다.

## 트리거
- "게임 밸런스"
- "난이도 조절"
- "레벨 디자인"
- "경제 시스템"
- "진행 곡선"

## 난이도 곡선

### 이상적인 난이도 곡선
```
난이도
  ^
  |              ___________
  |           __/           (엔드게임)
  |        __/
  |     __/   (중반 - 도전)
  |   _/
  |  /  (초반 - 학습)
  +-------------------------> 진행도
```

### 난이도 공식
```typescript
// 레벨 기반 난이도
function getDifficulty(level: number, baseValue: number): number {
  // 지수 성장 (빠른 난이도 상승)
  return baseValue * Math.pow(1.15, level - 1);
  
  // 선형 성장 (일정한 난이도 상승)
  // return baseValue + (level - 1) * increment;
  
  // 로그 성장 (초반 급성장, 후반 완만)
  // return baseValue * (1 + Math.log(level));
}

// 적 체력
const enemyHealth = getDifficulty(level, 100);  // 100, 115, 132, 152...

// 적 공격력
const enemyDamage = getDifficulty(level, 10);   // 10, 11.5, 13.2, 15.2...

// 점수 보상
const scoreReward = getDifficulty(level, 100);  // 100, 115, 132, 152...
```

## 경제 밸런스

### 인플레이션 방지
```typescript
// 비용 증가 공식 (idle 게임)
function getUpgradeCost(baseCost: number, level: number, multiplier: number = 1.15): number {
  return Math.floor(baseCost * Math.pow(multiplier, level));
}

// 예: 기본 비용 100, 레벨 10
// getUpgradeCost(100, 10, 1.15) = 404

// 수익률 계산
function getROI(cost: number, incomeIncrease: number): number {
  return cost / incomeIncrease; // 회수 시간 (초)
}
```

### 보상 시스템
```typescript
interface RewardConfig {
  // 기본 보상
  baseGold: number;
  baseExp: number;
  
  // 레벨별 증가
  goldPerLevel: number;
  expPerLevel: number;
  
  // 콤보/보너스
  comboMultiplier: number;
  maxCombo: number;
  
  // 희귀 보상 확률
  rareDropRate: number;
  epicDropRate: number;
}

const REWARD_CONFIG: RewardConfig = {
  baseGold: 10,
  baseExp: 5,
  goldPerLevel: 2,
  expPerLevel: 1,
  comboMultiplier: 1.1,
  maxCombo: 10,
  rareDropRate: 0.1,   // 10%
  epicDropRate: 0.01,  // 1%
};
```

## 진행 시스템

### 레벨업 경험치 공식
```typescript
// 총 필요 경험치
function getExpForLevel(level: number): number {
  // 제곱 공식 (적당한 성장)
  return Math.floor(100 * Math.pow(level, 2));
  
  // 예: 레벨 1→2: 100, 2→3: 400, 3→4: 900
}

// 레벨 10까지 필요 총 경험치: 100+400+900+...+10000 = 38,500
```

### 스테이지 해금
```typescript
interface StageConfig {
  id: number;
  name: string;
  requiredLevel: number;
  requiredStars: number;
  difficulty: number;
  rewards: {
    gold: number;
    exp: number;
    items: string[];
  };
}

const STAGES: StageConfig[] = [
  { id: 1, name: '초원', requiredLevel: 1, requiredStars: 0, difficulty: 1, ... },
  { id: 2, name: '숲', requiredLevel: 3, requiredStars: 5, difficulty: 2, ... },
  { id: 3, name: '동굴', requiredLevel: 5, requiredStars: 15, difficulty: 3, ... },
  // ...
];
```

## 전투 밸런스

### 데미지 공식
```typescript
function calculateDamage(
  attackPower: number,
  defense: number,
  critRate: number = 0,
  critDamage: number = 1.5
): number {
  // 기본 데미지 (방어력 감소)
  let damage = attackPower * (100 / (100 + defense));
  
  // 크리티컬
  if (Math.random() < critRate) {
    damage *= critDamage;
  }
  
  // 최소 데미지 보장
  return Math.max(1, Math.floor(damage));
}
```

### DPS 밸런스
```typescript
// 예상 DPS 계산
function calculateDPS(
  attackPower: number,
  attackSpeed: number,  // 초당 공격 횟수
  critRate: number,
  critDamage: number
): number {
  const baseDPS = attackPower * attackSpeed;
  const critBonus = critRate * (critDamage - 1);
  return baseDPS * (1 + critBonus);
}
```

## 플레이어 성장 곡선

```typescript
// 스탯 성장 시스템
interface PlayerStats {
  level: number;
  health: number;
  attack: number;
  defense: number;
  speed: number;
}

function getStatsForLevel(level: number): PlayerStats {
  return {
    level,
    health: 100 + (level - 1) * 20,    // 100, 120, 140...
    attack: 10 + (level - 1) * 2,       // 10, 12, 14...
    defense: 5 + (level - 1) * 1,       // 5, 6, 7...
    speed: 100 + (level - 1) * 5,       // 100, 105, 110...
  };
}
```

## 밸런스 체크리스트

### 난이도
- [ ] 초반 튜토리얼 쉬움
- [ ] 점진적 난이도 상승
- [ ] 난이도 스파이크 없음
- [ ] 숙련자를 위한 도전 요소

### 경제
- [ ] 인플레이션 통제
- [ ] 의미 있는 선택 (트레이드오프)
- [ ] 과금 vs 무과금 밸런스
- [ ] 후반 콘텐츠 접근성

### 진행
- [ ] 적절한 보상 주기
- [ ] 성취감 있는 레벨업
- [ ] 막힘 없는 진행
- [ ] 엔드게임 콘텐츠

### 전투
- [ ] 클래스/캐릭터 밸런스
- [ ] 무기/스킬 밸런스
- [ ] PvE/PvP 분리 밸런스
- [ ] 메타 다양성
