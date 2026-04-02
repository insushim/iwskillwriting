# 장르별 게임 템플릿 가이드 v2.0

> 1000+ 소스 리서치 기반, 2025-2026 트렌드 반영

---

## 1. Vampire Survivors / Bullet Heaven

### 코어 루프
```
이동(회피) → 자동공격 → 적처치 → 경험치 → 레벨업 → 무기선택 → 더 강한 적 → 반복
메타: 골드축적 → 영구업그레이드 → 캐릭터해금 → 새 시작
```

### 핵심 메카닉
```typescript
// 자동 공격 시스템 - 무기별 타이머
class AutoAttackSystem {
  weapons: WeaponInstance[] = [];

  update(delta: number, playerPos: Vector2, enemies: Enemy[]) {
    for (const weapon of this.weapons) {
      weapon.cooldownTimer -= delta;
      if (weapon.cooldownTimer <= 0) {
        weapon.cooldownTimer = weapon.cooldown;
        this.fireWeapon(weapon, playerPos, enemies);
      }
    }
  }

  // 무기 진화: 레벨 8 + 패시브 아이템 조합
  evolveWeapon(weaponId: string, passiveId: string): EvolvedWeapon | null {
    const recipe = EVOLUTION_RECIPES[weaponId];
    if (!recipe || recipe.passiveRequired !== passiveId) return null;
    const weapon = this.findWeapon(weaponId);
    if (!weapon || weapon.level < 8) return null;
    return { ...recipe.result, level: 1 };
  }
}

// 시너지 시스템
const BUILD_SYNERGIES = {
  "fire": { weapons: ["fireball", "flamering"], bonus: "burnDamage +50%" },
  "ice": { weapons: ["icicle", "frostwave"], bonus: "slowEffect +30%" },
  "lightning": { weapons: ["spark", "thunderstrike"], bonus: "chainDamage +40%" },
};
```

### 밸런싱 수치
```
플레이어 HP: 100 (최대 300, 업그레이드로)
이동속도: 200px/s (최대 350)
무기 슬롯: 6개
패시브 슬롯: 6개
게임 시간: 30분 (시간제)
레벨업 선택지: 3~4개 (리롤 가능)
경험치 곡선: level^1.8 * 10
적 웨이브 밀도: time/60 * baseCount (선형 증가)
보스 출현: 매 5분 + 최종 30분 보스
```

---

## 2. 타워 디펜스 (2026 메타)

### 코어 루프
```
맵분석 → 타워배치 → 웨이브시작 → 타워업그레이드 → 보스전 → 보상 → 다음 스테이지
메타: 타워해금 → 능력치강화 → 챌린지모드 → 랭킹
```

### 핵심 메카닉
```typescript
// 타워 배치 + 경로 계산
class TowerDefenseCore {
  grid: TileGrid;
  towers: Tower[] = [];
  enemies: Enemy[] = [];
  path: Vector2[];

  // A* 경로 탐색 (적 이동 경로)
  calculatePath(start: Vector2, end: Vector2): Vector2[] {
    const openSet = new PriorityQueue<PathNode>();
    openSet.enqueue({ pos: start, g: 0, f: this.heuristic(start, end) });
    // ... A* 구현
    return path;
  }

  // 타워 시너지
  calculateSynergy(tower: Tower): number {
    let bonus = 1.0;
    const nearby = this.getTowersInRange(tower.pos, 2);
    for (const t of nearby) {
      if (t.element === tower.element) bonus += 0.15; // 같은 원소 +15%
      if (SYNERGY_TABLE[tower.element]?.[t.element]) bonus += 0.25; // 상성 +25%
    }
    return bonus;
  }
}

// 적 종류별 AI
const ENEMY_BEHAVIORS = {
  normal: { speed: 1.0, hp: 1.0, reward: 10 },
  fast: { speed: 2.0, hp: 0.5, reward: 15 },
  tank: { speed: 0.5, hp: 3.0, reward: 25 },
  flying: { speed: 1.5, hp: 0.8, reward: 20, ignorePath: true },
  healer: { speed: 0.8, hp: 1.0, reward: 30, heals: true },
  splitter: { speed: 1.0, hp: 2.0, reward: 20, splitOnDeath: 2 },
  boss: { speed: 0.3, hp: 50.0, reward: 500, abilities: ["shield", "summon"] },
};
```

---

## 3. 로그라이크 / 로그라이트

### 코어 루프
```
던전입장 → 방탐색 → 전투/보물/이벤트 → 보스 → 다음층 → 사망→메타보상
```

### 프로시저럴 던전 생성
```typescript
// BSP (Binary Space Partition) 던전 생성
class BSPDungeon {
  generateDungeon(width: number, height: number, depth: number = 4): Room[] {
    const root: BSPNode = { x: 0, y: 0, w: width, h: height };
    this.split(root, depth);
    const rooms = this.createRooms(root);
    this.connectRooms(rooms);
    return rooms;
  }

  private split(node: BSPNode, depth: number): void {
    if (depth <= 0 || node.w < 10 || node.h < 10) return;
    const horizontal = Math.random() > 0.5;
    if (horizontal) {
      const splitY = node.y + Math.floor(node.h * (0.3 + Math.random() * 0.4));
      node.left = { x: node.x, y: node.y, w: node.w, h: splitY - node.y };
      node.right = { x: node.x, y: splitY, w: node.w, h: node.h - (splitY - node.y) };
    } else {
      const splitX = node.x + Math.floor(node.w * (0.3 + Math.random() * 0.4));
      node.left = { x: node.x, y: node.y, w: splitX - node.x, h: node.h };
      node.right = { x: splitX, y: node.y, w: node.w - (splitX - node.x), h: node.h };
    }
    this.split(node.left, depth - 1);
    this.split(node.right, depth - 1);
  }
}

// 아이템 시너지 시스템
class ItemSynergySystem {
  checkSynergies(items: Item[]): Synergy[] {
    const synergies: Synergy[] = [];
    const tags = items.flatMap(i => i.tags);
    const tagCounts = new Map<string, number>();
    for (const tag of tags) tagCounts.set(tag, (tagCounts.get(tag) || 0) + 1);

    // 3개 이상 같은 태그 → 시너지 발동
    for (const [tag, count] of tagCounts) {
      if (count >= 3) {
        synergies.push(SYNERGY_DEFINITIONS[tag]);
      }
    }
    return synergies;
  }
}
```

---

## 4. 아이들/클리커

### 코어 루프
```
클릭 → 자원획득 → 자동화구매 → 오프라인수익 → 프레스티지 → 멀티플라이어 → 반복
```

### 핵심 메카닉
```typescript
// 빅넘버 시스템 (큰 숫자 표시)
class BigNumber {
  static format(n: number): string {
    const suffixes = ['', 'K', 'M', 'B', 'T', 'Qa', 'Qi', 'Sx', 'Sp', 'Oc', 'No', 'Dc'];
    if (n < 1000) return Math.floor(n).toString();
    const tier = Math.floor(Math.log10(n) / 3);
    const suffix = suffixes[Math.min(tier, suffixes.length - 1)];
    const scale = Math.pow(10, tier * 3);
    const scaled = n / scale;
    return scaled.toFixed(scaled < 10 ? 2 : scaled < 100 ? 1 : 0) + suffix;
  }
}

// 프레스티지 시스템
class PrestigeSystem {
  // 프레스티지 포인트 = sqrt(totalEarnings / 1e6)
  calculatePrestigePoints(totalEarnings: number): number {
    return Math.floor(Math.sqrt(totalEarnings / 1e6));
  }

  // 프레스티지 멀티플라이어 = 1 + prestigePoints * 0.1
  getMultiplier(prestigePoints: number): number {
    return 1 + prestigePoints * 0.1;
  }

  // 오프라인 수익 (최대 8시간)
  calculateOfflineEarnings(dps: number, offlineSeconds: number): number {
    const maxSeconds = 8 * 3600;
    const cappedSeconds = Math.min(offlineSeconds, maxSeconds);
    return dps * cappedSeconds * 0.5; // 오프라인은 50% 효율
  }
}

// 업그레이드 비용 곡선
// cost(n) = baseCost * growthRate^n
function upgradeCost(baseCost: number, growthRate: number, owned: number): number {
  return Math.floor(baseCost * Math.pow(growthRate, owned));
}
// 예: upgradeCost(10, 1.15, 50) = 10 * 1.15^50 ≈ 10,836
```

---

## 5. 퍼즐 / Match-3

### 코어 루프
```
보드분석 → 매치 → 캐스케이드 → 특수블록생성 → 콤보 → 목표달성 → 다음레벨
```

### 핵심 메카닉
```typescript
// Match-3 보드 로직
class Match3Board {
  grid: number[][];

  findMatches(): Match[] {
    const matches: Match[] = [];
    // 가로 매치
    for (let y = 0; y < this.rows; y++) {
      let count = 1;
      for (let x = 1; x < this.cols; x++) {
        if (this.grid[y][x] === this.grid[y][x-1] && this.grid[y][x] !== 0) {
          count++;
        } else {
          if (count >= 3) matches.push({ cells: this.getCells(y, x-count, count, 'h'), count });
          count = 1;
        }
      }
      if (count >= 3) matches.push({ cells: this.getCells(y, this.cols-count, count, 'h'), count });
    }
    // 세로도 동일 패턴
    return matches;
  }

  // 캐스케이드 (중력 적용)
  applyGravity(): void {
    for (let x = 0; x < this.cols; x++) {
      let writePos = this.rows - 1;
      for (let y = this.rows - 1; y >= 0; y--) {
        if (this.grid[y][x] !== 0) {
          this.grid[writePos][x] = this.grid[y][x];
          if (writePos !== y) this.grid[y][x] = 0;
          writePos--;
        }
      }
      // 빈 자리 채우기
      for (let y = writePos; y >= 0; y--) {
        this.grid[y][x] = this.randomGem();
      }
    }
  }

  // 특수 블록 생성 규칙
  getSpecialBlock(matchCount: number): SpecialType {
    if (matchCount === 4) return 'line_blast';  // 4매치 → 라인 폭발
    if (matchCount === 5) return 'rainbow';     // 5매치 → 레인보우 (모든 색)
    if (matchCount >= 6) return 'bomb';          // 6매치+ → 폭탄
    return 'none';
  }
}
```

---

## 6. 카드 게임 / 덱빌더

### 코어 루프
```
덱구성 → 카드드로우 → 마나관리 → 카드사용 → 적턴 → 보상(새카드) → 다음전투
```

### 핵심 메카닉
```typescript
// 덱빌딩 시스템
class DeckBuilder {
  deck: Card[] = [];
  hand: Card[] = [];
  drawPile: Card[] = [];
  discardPile: Card[] = [];
  mana: number = 3;
  maxMana: number = 3;

  startTurn(): void {
    this.mana = this.maxMana;
    this.drawCards(5);
  }

  playCard(index: number, target?: Enemy): boolean {
    const card = this.hand[index];
    if (!card || card.cost > this.mana) return false;
    this.mana -= card.cost;
    card.effect(target);
    this.hand.splice(index, 1);
    this.discardPile.push(card);
    return true;
  }

  drawCards(count: number): void {
    for (let i = 0; i < count; i++) {
      if (this.drawPile.length === 0) {
        this.drawPile = [...this.discardPile].sort(() => Math.random() - 0.5);
        this.discardPile = [];
      }
      if (this.drawPile.length > 0) {
        this.hand.push(this.drawPile.pop()!);
      }
    }
  }
}

// 카드 등급 + 희귀도
const CARD_RARITIES = {
  common:    { weight: 60, color: '#9e9e9e', maxInDeck: 4 },
  uncommon:  { weight: 25, color: '#4caf50', maxInDeck: 3 },
  rare:      { weight: 10, color: '#2196f3', maxInDeck: 2 },
  epic:      { weight: 4,  color: '#9c27b0', maxInDeck: 1 },
  legendary: { weight: 1,  color: '#ff9800', maxInDeck: 1 },
};
```

---

## 7. 플랫포머 / 메트로이드바니아

### 물리 시스템
```typescript
class PlatformerPhysics {
  // 코요테 타임: 플랫폼 떠난 후에도 짧은 시간 점프 허용
  coyoteTime: number = 0.1; // 100ms
  coyoteTimer: number = 0;

  // 점프 버퍼: 착지 전에 점프 입력해도 착지 시 점프
  jumpBufferTime: number = 0.15;
  jumpBufferTimer: number = 0;

  // 가변 점프 높이: 버튼 짧게 = 낮은 점프
  handleJump(isGrounded: boolean, jumpPressed: boolean, jumpHeld: boolean): void {
    if (jumpPressed) this.jumpBufferTimer = this.jumpBufferTime;
    if (isGrounded) this.coyoteTimer = this.coyoteTime;

    const canJump = (isGrounded || this.coyoteTimer > 0) && this.jumpBufferTimer > 0;
    if (canJump) {
      this.velocityY = -this.jumpForce;
      this.coyoteTimer = 0;
      this.jumpBufferTimer = 0;
    }

    // 버튼 떼면 점프 높이 감소
    if (!jumpHeld && this.velocityY < 0) {
      this.velocityY *= 0.5;
    }
  }
}
```

---

## 8. 하이브리드 장르 (2026 트렌드)

### 장르 결합 가이드

| 주 장르 | 부 장르 | 결합 예시 | 성공 작품 |
|---------|---------|----------|----------|
| TD | 로그라이크 | 랜덤 타워 드래프트 + 런 기반 진행 | Arcanarena, RogueTD |
| 서바이벌 | 덱빌딩 | 카드 기반 무기 선택 | Inscryption |
| 아이들 | 로그라이크 | 자동 진행 + 프레스티지 | Realm Grinder |
| 퍼즐 | RPG | 매치3 전투 시스템 | Puzzle Quest |
| 플랫포머 | 로그라이크 | 프로시저럴 맵 + 퍼마데스 | Dead Cells |
| 교육 | 서바이벌 | 문제 풀면 무기 획득 | 워드 서바이벌 |

```typescript
// 하이브리드 코어 루프 설계
class HybridGameCore {
  primaryLoop: CoreLoop;   // 주 장르 루프
  secondaryLoop: CoreLoop; // 부 장르 루프
  metaLoop: MetaLoop;      // 장기 진행

  // 두 루프를 자연스럽게 연결하는 브릿지 메카닉
  bridgeMechanic(primaryResult: any): SecondaryInput {
    // 예: TD 웨이브 클리어 → 로그라이크 카드 보상
    return {
      rewardType: 'card_draft',
      options: this.generateOptions(primaryResult.score),
      count: 3,
    };
  }
}
```

---

## 9. 교육 게임 (강화된 학습 시스템)

### 간격 반복 (SRS) 알고리즘
```typescript
// SM-2 알고리즘 (SuperMemo 기반)
class SpacedRepetition {
  calculateNextReview(item: SRSItem, quality: number): SRSItem {
    // quality: 0(완전틀림) ~ 5(완벽)
    if (quality < 3) {
      // 틀리면 처음부터
      item.repetitions = 0;
      item.interval = 1;
    } else {
      if (item.repetitions === 0) item.interval = 1;
      else if (item.repetitions === 1) item.interval = 6;
      else item.interval = Math.round(item.interval * item.easeFactor);
      item.repetitions++;
    }

    // 난이도 조정
    item.easeFactor = Math.max(1.3,
      item.easeFactor + 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)
    );

    item.nextReview = Date.now() + item.interval * 86400000;
    return item;
  }
}

// 적응형 난이도 (DDA)
class AdaptiveDifficulty {
  private window: boolean[] = []; // 최근 N개 정답/오답
  private windowSize = 10;

  recordAnswer(correct: boolean): void {
    this.window.push(correct);
    if (this.window.length > this.windowSize) this.window.shift();
  }

  getRecommendedDifficulty(currentDifficulty: number): number {
    const accuracy = this.window.filter(Boolean).length / this.window.length;

    if (accuracy > 0.85) return Math.min(10, currentDifficulty + 0.5);
    if (accuracy < 0.50) return Math.max(1, currentDifficulty - 0.5);
    if (accuracy < 0.65) return Math.max(1, currentDifficulty - 0.2);
    return currentDifficulty; // 65-85% = 최적 학습 구간
  }
}
```

---

## 10. 범용 시스템 (모든 장르에 적용)

### 세이브/로드 시스템 (강화)
```typescript
class EnhancedSaveSystem {
  static VERSION = 2;

  static save(data: any): void {
    const payload = {
      version: this.VERSION,
      timestamp: Date.now(),
      checksum: this.calculateChecksum(data),
      data: data,
    };
    localStorage.setItem('save', JSON.stringify(payload));
    // 백업
    localStorage.setItem('save_backup', localStorage.getItem('save')!);
  }

  static load(): any | null {
    let raw = localStorage.getItem('save');
    if (!raw) raw = localStorage.getItem('save_backup');
    if (!raw) return null;

    const payload = JSON.parse(raw);
    // 체크섬 검증 (치트 방지)
    if (this.calculateChecksum(payload.data) !== payload.checksum) {
      console.warn('Save data corrupted or tampered');
      return null;
    }
    // 버전 마이그레이션
    if (payload.version < this.VERSION) {
      payload.data = this.migrate(payload.data, payload.version);
    }
    return payload.data;
  }

  private static calculateChecksum(data: any): string {
    const str = JSON.stringify(data);
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      hash = ((hash << 5) - hash) + str.charCodeAt(i);
      hash |= 0;
    }
    return hash.toString(36);
  }
}
```

### 파티클 이펙트 시스템
```typescript
class ParticleSystem {
  particles: Particle[] = [];

  emit(config: ParticleConfig): void {
    for (let i = 0; i < config.count; i++) {
      this.particles.push({
        x: config.x + (Math.random() - 0.5) * config.spread,
        y: config.y + (Math.random() - 0.5) * config.spread,
        vx: (Math.random() - 0.5) * config.speed,
        vy: -Math.random() * config.speed + (config.gravity ? 0 : 0),
        life: config.lifetime * (0.5 + Math.random() * 0.5),
        maxLife: config.lifetime,
        color: config.colors[Math.floor(Math.random() * config.colors.length)],
        size: config.size * (0.5 + Math.random()),
      });
    }
  }

  static PRESETS = {
    explosion: { count: 30, speed: 300, lifetime: 0.5, spread: 10, colors: ['#ff4444','#ff8800','#ffff00'], size: 4 },
    levelUp: { count: 50, speed: 200, lifetime: 1.0, spread: 50, colors: ['#ffff00','#00ff00','#ffffff'], size: 3 },
    heal: { count: 20, speed: 100, lifetime: 0.8, spread: 30, colors: ['#00ff88','#88ffbb','#ffffff'], size: 3 },
    coin: { count: 8, speed: 150, lifetime: 0.4, spread: 5, colors: ['#ffdd00','#ffaa00'], size: 2 },
    damage: { count: 5, speed: 100, lifetime: 0.3, spread: 20, colors: ['#ff0000','#ff4444'], size: 3 },
  };
}
```

### 화면 전환
```typescript
class SceneTransition {
  // 페이드
  static fade(scene: Phaser.Scene, duration: number = 500): Promise<void> {
    return new Promise(resolve => {
      scene.cameras.main.fadeOut(duration);
      scene.time.delayedCall(duration, () => {
        scene.cameras.main.fadeIn(duration);
        resolve();
      });
    });
  }

  // 원형 와이프
  static circleWipe(scene: Phaser.Scene, x: number, y: number): Promise<void> {
    const mask = scene.add.graphics();
    const maxRadius = Math.sqrt(scene.scale.width ** 2 + scene.scale.height ** 2);
    return new Promise(resolve => {
      scene.tweens.add({
        targets: { radius: maxRadius },
        radius: 0,
        duration: 800,
        ease: 'Cubic.easeIn',
        onUpdate: (tween) => {
          mask.clear();
          mask.fillStyle(0x000000);
          mask.fillRect(0, 0, scene.scale.width, scene.scale.height);
          mask.fillStyle(0xffffff);
          mask.fillCircle(x, y, tween.getValue());
        },
        onComplete: resolve,
      });
    });
  }
}
```
