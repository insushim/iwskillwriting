# 게임 수학 & 물리 공식 가이드 v3.0

> 게임에서 자주 쓰는 수학 공식 모음. 복사해서 바로 쓸 수 있는 코드.

---

## 1. 보간 (Interpolation)

```typescript
const GameMath = {
  // 선형 보간
  lerp: (a: number, b: number, t: number) => a + (b - a) * t,

  // 부드러운 보간 (가속→감속)
  smoothstep: (t: number) => t * t * (3 - 2 * t),

  // 더 부드러운 보간
  smootherstep: (t: number) => t * t * t * (t * (t * 6 - 15) + 10),

  // 스프링 댐핑 (UI 탄성 애니메이션)
  springDamp: (current: number, target: number, velocity: number, stiffness: number = 100, damping: number = 10, dt: number = 0.016) => {
    const force = (target - current) * stiffness;
    const dampForce = -velocity * damping;
    const newVelocity = velocity + (force + dampForce) * dt;
    const newValue = current + newVelocity * dt;
    return { value: newValue, velocity: newVelocity };
  },

  // 각도 보간 (최단 경로)
  lerpAngle: (a: number, b: number, t: number) => {
    let diff = ((b - a + Math.PI) % (Math.PI * 2)) - Math.PI;
    if (diff < -Math.PI) diff += Math.PI * 2;
    return a + diff * t;
  },
};
```

---

## 2. 전투 수학

```typescript
const CombatMath = {
  // 데미지 공식 (방어력 비율 감소)
  calcDamage: (atk: number, def: number) => {
    // 방어력이 높을수록 감소하지만 절대 0은 아님
    return Math.max(1, Math.round(atk * (100 / (100 + def))));
  },

  // 데미지 공식 (플랫 감소 + 비율 감소)
  calcDamageHybrid: (atk: number, flatDef: number, percentDef: number) => {
    const afterFlat = Math.max(0, atk - flatDef);
    return Math.max(1, Math.round(afterFlat * (1 - percentDef / 100)));
  },

  // 크리티컬 히트
  rollCrit: (critRate: number, critDamage: number = 1.5): { isCrit: boolean; multiplier: number } => {
    const isCrit = Math.random() < critRate / 100;
    return { isCrit, multiplier: isCrit ? critDamage : 1.0 };
  },

  // DOT (Damage Over Time)
  dotTick: (totalDamage: number, duration: number, tickInterval: number) => {
    const ticks = duration / tickInterval;
    return totalDamage / ticks;
  },

  // 넉백 벡터
  knockbackVector: (fromX: number, fromY: number, toX: number, toY: number, force: number) => {
    const angle = Math.atan2(toY - fromY, toX - fromX);
    return { x: Math.cos(angle) * force, y: Math.sin(angle) * force };
  },

  // 범위 판정 (원형)
  isInRange: (x1: number, y1: number, x2: number, y2: number, range: number) => {
    const dx = x2 - x1, dy = y2 - y1;
    return dx * dx + dy * dy <= range * range; // sqrt 회피 (성능)
  },

  // 부채꼴 판정 (콘 공격)
  isInCone: (originX: number, originY: number, targetX: number, targetY: number,
    facing: number, coneAngle: number, range: number) => {
    const dx = targetX - originX, dy = targetY - originY;
    const dist = Math.sqrt(dx*dx + dy*dy);
    if (dist > range) return false;
    const angleToTarget = Math.atan2(dy, dx);
    let angleDiff = Math.abs(angleToTarget - facing);
    if (angleDiff > Math.PI) angleDiff = Math.PI * 2 - angleDiff;
    return angleDiff <= coneAngle / 2;
  },
};
```

---

## 3. 확률 & 랜덤

```typescript
const RandomMath = {
  // 가중 랜덤 선택
  weightedRandom: <T>(items: { item: T; weight: number }[]): T => {
    const total = items.reduce((s, i) => s + i.weight, 0);
    let r = Math.random() * total;
    for (const { item, weight } of items) {
      r -= weight;
      if (r <= 0) return item;
    }
    return items[items.length - 1].item;
  },

  // 의사 랜덤 분배 (PRD — 도타2 스타일, 연속 실패 보상)
  prd: (baseChance: number, failures: number): number => {
    // C값 (근사치): 연속 실패할수록 확률 증가
    const C = baseChance / 5.5; // 근사
    return Math.min(1.0, C * (failures + 1));
  },

  // 셔플백 (공정한 분배 — 같은 결과 연속 방지)
  createShuffleBag: <T>(items: T[]): (() => T) => {
    let bag = [...items];
    let index = bag.length;
    return () => {
      if (index >= bag.length) {
        bag = [...items].sort(() => Math.random() - 0.5);
        index = 0;
      }
      return bag[index++];
    };
  },

  // 시드 랜덤 (리플레이/공유용)
  seededRandom: (seed: number) => {
    return () => {
      seed = (seed * 16807) % 2147483647;
      return (seed - 1) / 2147483646;
    };
  },

  // 정규 분포 랜덤 (자연스러운 분포)
  gaussian: (mean: number = 0, stdDev: number = 1) => {
    const u1 = Math.random(), u2 = Math.random();
    return mean + stdDev * Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
  },
};
```

---

## 4. 이동 & 물리

```typescript
const MovementMath = {
  // 호밍 미사일 (유도탄)
  homingStep: (missileX: number, missileY: number, missileAngle: number,
    targetX: number, targetY: number, turnRate: number, speed: number, dt: number) => {
    const desired = Math.atan2(targetY - missileY, targetX - missileX);
    let angleDiff = desired - missileAngle;
    // 최단 회전
    while (angleDiff > Math.PI) angleDiff -= Math.PI * 2;
    while (angleDiff < -Math.PI) angleDiff += Math.PI * 2;
    const newAngle = missileAngle + Math.sign(angleDiff) * Math.min(Math.abs(angleDiff), turnRate * dt);
    return {
      x: missileX + Math.cos(newAngle) * speed * dt,
      y: missileY + Math.sin(newAngle) * speed * dt,
      angle: newAngle,
    };
  },

  // 포물선 발사체 (던지기, 포탄)
  projectileArc: (startX: number, startY: number, endX: number, endY: number,
    height: number, t: number) => {
    // t: 0~1 진행도
    return {
      x: GameMath.lerp(startX, endX, t),
      y: GameMath.lerp(startY, endY, t) - height * 4 * t * (1 - t), // 포물선
    };
  },

  // 부메랑 궤도
  boomerangPath: (originX: number, originY: number, angle: number,
    range: number, t: number) => {
    const outT = Math.min(t * 2, 1); // 0~0.5 → 나감
    const backT = Math.max((t - 0.5) * 2, 0); // 0.5~1 → 돌아옴
    const dist = range * (outT - backT);
    const curve = Math.sin(t * Math.PI) * range * 0.3; // 곡선
    return {
      x: originX + Math.cos(angle) * dist + Math.cos(angle + Math.PI/2) * curve,
      y: originY + Math.sin(angle) * dist + Math.sin(angle + Math.PI/2) * curve,
    };
  },

  // 궤도 운동 (위성, 방패 회전)
  orbit: (centerX: number, centerY: number, radius: number, angle: number, speed: number, dt: number) => {
    const newAngle = angle + speed * dt;
    return {
      x: centerX + Math.cos(newAngle) * radius,
      y: centerY + Math.sin(newAngle) * radius,
      angle: newAngle,
    };
  },
};
```

---

## 5. 경제 & 진행

```typescript
const EconomyMath = {
  // 업그레이드 비용 (기하급수)
  upgradeCost: (baseCost: number, growthRate: number, level: number) =>
    Math.floor(baseCost * Math.pow(growthRate, level)),

  // 업그레이드 10개 한번에 구매 비용
  bulkCost: (baseCost: number, growthRate: number, currentLevel: number, count: number) => {
    let total = 0;
    for (let i = 0; i < count; i++) total += EconomyMath.upgradeCost(baseCost, growthRate, currentLevel + i);
    return Math.floor(total);
  },

  // 최대 구매 가능 수 (자금 내에서)
  maxAffordable: (baseCost: number, growthRate: number, currentLevel: number, money: number) => {
    let count = 0, total = 0;
    while (true) {
      const next = EconomyMath.upgradeCost(baseCost, growthRate, currentLevel + count);
      if (total + next > money) break;
      total += next;
      count++;
    }
    return { count, totalCost: Math.floor(total) };
  },

  // 경험치 곡선
  xpForLevel: (level: number, base: number = 100, exponent: number = 1.5) =>
    Math.floor(base * Math.pow(level, exponent)),

  // 누적 XP (레벨 N까지 총 필요량)
  totalXpForLevel: (level: number, base: number = 100, exponent: number = 1.5) => {
    let total = 0;
    for (let i = 1; i <= level; i++) total += EconomyMath.xpForLevel(i, base, exponent);
    return total;
  },

  // 감소 수익률 (소프트캡)
  diminishingReturns: (value: number, softCap: number) =>
    softCap * (1 - Math.exp(-value / softCap)),

  // 복리 (아이들 게임 오프라인 수익)
  compoundGrowth: (principal: number, rate: number, time: number) =>
    principal * Math.pow(1 + rate, time),

  // 큰 숫자 포맷
  formatNumber: (n: number): string => {
    const tiers = ['', 'K', 'M', 'B', 'T', 'Qa', 'Qi', 'Sx', 'Sp', 'Oc', 'No', 'Dc'];
    if (n < 1000) return n.toFixed(0);
    const tier = Math.min(Math.floor(Math.log10(n) / 3), tiers.length - 1);
    const scale = Math.pow(10, tier * 3);
    const scaled = n / scale;
    return (scaled < 10 ? scaled.toFixed(2) : scaled < 100 ? scaled.toFixed(1) : scaled.toFixed(0)) + tiers[tier];
  },
};
```

---

## 6. 시각 수학

```typescript
const VisualMath = {
  // 베지어 곡선 (경로 따라가기)
  quadraticBezier: (p0: number, p1: number, p2: number, t: number) => {
    const mt = 1 - t;
    return mt * mt * p0 + 2 * mt * t * p1 + t * t * p2;
  },

  cubicBezier: (p0: number, p1: number, p2: number, p3: number, t: number) => {
    const mt = 1 - t;
    return mt*mt*mt*p0 + 3*mt*mt*t*p1 + 3*mt*t*t*p2 + t*t*t*p3;
  },

  // 색상 보간
  lerpColor: (color1: number, color2: number, t: number): number => {
    const r1 = (color1 >> 16) & 0xff, g1 = (color1 >> 8) & 0xff, b1 = color1 & 0xff;
    const r2 = (color2 >> 16) & 0xff, g2 = (color2 >> 8) & 0xff, b2 = color2 & 0xff;
    const r = Math.round(r1 + (r2 - r1) * t);
    const g = Math.round(g1 + (g2 - g1) * t);
    const b = Math.round(b1 + (b2 - b1) * t);
    return (r << 16) | (g << 8) | b;
  },

  // 퍼린 노이즈 기반 화면 셰이크 (자연스러운)
  perlinShake: (time: number, intensity: number): {x: number, y: number} => {
    // 간소화된 사인 기반 의사 퍼린
    return {
      x: Math.sin(time * 25) * Math.cos(time * 13.7) * intensity,
      y: Math.cos(time * 19.3) * Math.sin(time * 11.2) * intensity,
    };
  },

  // 패럴랙스 스크롤링 레이어 위치
  parallaxOffset: (cameraX: number, layerDepth: number): number => {
    return cameraX * (1 - 1 / layerDepth);
    // layerDepth: 1=전경(카메라와 같은 속도), 2=중경(절반), 4=원경(1/4)
  },

  // 이징 함수 모음
  easing: {
    linear: (t: number) => t,
    easeInQuad: (t: number) => t * t,
    easeOutQuad: (t: number) => t * (2 - t),
    easeInOutQuad: (t: number) => t < 0.5 ? 2*t*t : -1 + (4-2*t)*t,
    easeOutBounce: (t: number) => {
      if (t < 1/2.75) return 7.5625*t*t;
      if (t < 2/2.75) return 7.5625*(t-=1.5/2.75)*t+0.75;
      if (t < 2.5/2.75) return 7.5625*(t-=2.25/2.75)*t+0.9375;
      return 7.5625*(t-=2.625/2.75)*t+0.984375;
    },
    easeOutElastic: (t: number) => {
      if (t === 0 || t === 1) return t;
      return Math.pow(2, -10*t) * Math.sin((t-0.075)*2*Math.PI/0.3) + 1;
    },
    easeOutBack: (t: number) => { const c = 1.70158; return 1 + (c+1)*Math.pow(t-1,3) + c*Math.pow(t-1,2); },
  },
};
```
