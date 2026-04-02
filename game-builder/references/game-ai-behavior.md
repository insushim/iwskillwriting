# 게임 AI & 행동 시스템 가이드 v3.0

> 행동트리, FSM, 경로탐색, 보스 패턴, 스폰 시스템

---

## 1. 유한 상태 머신 (FSM)

```typescript
type StateHandler = {
  enter?: () => void;
  update?: (dt: number) => void;
  exit?: () => void;
};

class StateMachine {
  private states = new Map<string, StateHandler>();
  private current: string = '';

  addState(name: string, handler: StateHandler): this {
    this.states.set(name, handler);
    return this;
  }

  setState(name: string) {
    if (this.current === name) return;
    this.states.get(this.current)?.exit?.();
    this.current = name;
    this.states.get(name)?.enter?.();
  }

  update(dt: number) {
    this.states.get(this.current)?.update?.(dt);
  }

  getState(): string { return this.current; }
}

// 사용 예: 적 AI
class EnemyAI {
  private fsm = new StateMachine();
  private target: Phaser.GameObjects.Sprite;
  private sprite: Phaser.Physics.Arcade.Sprite;

  constructor(sprite: any, target: any) {
    this.sprite = sprite;
    this.target = target;

    this.fsm
      .addState('idle', {
        update: () => {
          if (this.distToTarget() < 300) this.fsm.setState('chase');
        },
      })
      .addState('chase', {
        update: () => {
          this.moveToward(this.target, 100);
          if (this.distToTarget() < 50) this.fsm.setState('attack');
          if (this.distToTarget() > 400) this.fsm.setState('idle');
        },
      })
      .addState('attack', {
        enter: () => { this.sprite.anims?.play('attack'); },
        update: () => {
          if (this.distToTarget() > 80) this.fsm.setState('chase');
        },
      })
      .addState('flee', {
        update: () => {
          this.moveAway(this.target, 150);
          if (this.distToTarget() > 300) this.fsm.setState('idle');
        },
      });

    this.fsm.setState('idle');
  }

  update(dt: number) {
    // HP가 낮으면 도주
    if ((this.sprite as any).hp < 20 && this.fsm.getState() !== 'flee') {
      this.fsm.setState('flee');
    }
    this.fsm.update(dt);
  }

  private distToTarget(): number {
    return Phaser.Math.Distance.Between(this.sprite.x, this.sprite.y, this.target.x, this.target.y);
  }

  private moveToward(target: any, speed: number) {
    const angle = Math.atan2(target.y - this.sprite.y, target.x - this.sprite.x);
    this.sprite.setVelocity(Math.cos(angle) * speed, Math.sin(angle) * speed);
  }

  private moveAway(target: any, speed: number) {
    const angle = Math.atan2(this.sprite.y - target.y, this.sprite.x - target.x);
    this.sprite.setVelocity(Math.cos(angle) * speed, Math.sin(angle) * speed);
  }
}
```

---

## 2. 보스 패턴 시스템

```typescript
class BossAI {
  private phases: BossPhase[] = [];
  private currentPhase = 0;
  private attackTimer = 0;
  private attackIndex = 0;

  constructor(private boss: any, private target: any, private scene: Phaser.Scene) {
    this.phases = [
      // Phase 1: HP 100~60%
      {
        hpThreshold: 0.6,
        attacks: [
          { name: 'charge', cooldown: 3000, telegraph: 800, execute: () => this.chargeAttack() },
          { name: 'shoot', cooldown: 1500, telegraph: 400, execute: () => this.shootProjectiles(3) },
        ],
        speed: 80,
      },
      // Phase 2: HP 60~30% — 더 공격적
      {
        hpThreshold: 0.3,
        attacks: [
          { name: 'charge', cooldown: 2000, telegraph: 600, execute: () => this.chargeAttack() },
          { name: 'shoot', cooldown: 1000, telegraph: 300, execute: () => this.shootProjectiles(5) },
          { name: 'summon', cooldown: 5000, telegraph: 1000, execute: () => this.summonMinions(3) },
        ],
        speed: 120,
        onEnter: () => {
          // Phase 전환 연출
          this.scene.cameras.main.shake(500, 0.02);
          this.boss.setTint(0xff8800);
        },
      },
      // Phase 3: HP 30~0% — 폭주
      {
        hpThreshold: 0,
        attacks: [
          { name: 'aoe', cooldown: 2000, telegraph: 1200, execute: () => this.aoeBlast() },
          { name: 'shoot', cooldown: 500, telegraph: 200, execute: () => this.shootProjectiles(8) },
          { name: 'charge', cooldown: 1500, telegraph: 400, execute: () => this.chargeAttack() },
        ],
        speed: 160,
        onEnter: () => {
          this.scene.cameras.main.shake(800, 0.03);
          this.boss.setTint(0xff0000);
        },
      },
    ];
  }

  update(dt: number) {
    // Phase 전환 체크
    const hpRatio = this.boss.hp / this.boss.maxHp;
    while (this.currentPhase < this.phases.length - 1 &&
           hpRatio <= this.phases[this.currentPhase].hpThreshold) {
      this.currentPhase++;
      this.phases[this.currentPhase].onEnter?.();
    }

    const phase = this.phases[this.currentPhase];

    // 공격 실행
    this.attackTimer -= dt;
    if (this.attackTimer <= 0) {
      const attack = phase.attacks[this.attackIndex % phase.attacks.length];
      this.attackIndex++;

      // 텔레그래프 (경고 표시)
      this.showTelegraph(attack.telegraph);
      this.scene.time.delayedCall(attack.telegraph, () => attack.execute());
      this.attackTimer = attack.cooldown;
    }
  }

  private showTelegraph(duration: number) {
    // 경고 원 표시
    const circle = this.scene.add.circle(this.boss.x, this.boss.y, 60, 0xff0000, 0.2);
    this.scene.tweens.add({
      targets: circle, alpha: 0.6, scale: 1.5,
      duration, ease: 'Sine.easeInOut',
      onComplete: () => circle.destroy(),
    });
  }

  private chargeAttack() { /* 돌진 공격 */ }
  private shootProjectiles(count: number) { /* 방사형 발사 */ }
  private summonMinions(count: number) { /* 소환수 생성 */ }
  private aoeBlast() { /* 범위 공격 */ }
}
```

---

## 3. 경로탐색 (A*)

```typescript
class AStarPathfinder {
  private grid: number[][]; // 0=이동가능, 1=벽

  constructor(grid: number[][]) { this.grid = grid; }

  findPath(startX: number, startY: number, endX: number, endY: number): {x:number,y:number}[] {
    const open: PathNode[] = [{ x: startX, y: startY, g: 0, h: 0, f: 0, parent: null }];
    const closed = new Set<string>();
    const key = (x: number, y: number) => `${x},${y}`;

    while (open.length > 0) {
      // f값이 가장 낮은 노드
      open.sort((a, b) => a.f - b.f);
      const current = open.shift()!;

      if (current.x === endX && current.y === endY) {
        return this.reconstructPath(current);
      }

      closed.add(key(current.x, current.y));

      // 8방향 이웃
      const dirs = [[-1,0],[1,0],[0,-1],[0,1],[-1,-1],[1,-1],[-1,1],[1,1]];
      for (const [dx, dy] of dirs) {
        const nx = current.x + dx, ny = current.y + dy;
        if (nx < 0 || ny < 0 || ny >= this.grid.length || nx >= this.grid[0].length) continue;
        if (this.grid[ny][nx] === 1 || closed.has(key(nx, ny))) continue;

        const g = current.g + (dx !== 0 && dy !== 0 ? 1.414 : 1);
        const h = Math.abs(nx - endX) + Math.abs(ny - endY); // Manhattan
        const f = g + h;

        const existing = open.find(n => n.x === nx && n.y === ny);
        if (existing && g >= existing.g) continue;
        if (existing) { existing.g = g; existing.f = f; existing.parent = current; }
        else open.push({ x: nx, y: ny, g, h, f, parent: current });
      }
    }
    return []; // 경로 없음
  }

  private reconstructPath(node: PathNode): {x:number,y:number}[] {
    const path: {x:number,y:number}[] = [];
    let current: PathNode | null = node;
    while (current) {
      path.unshift({ x: current.x, y: current.y });
      current = current.parent;
    }
    return path;
  }
}

interface PathNode {
  x: number; y: number;
  g: number; h: number; f: number;
  parent: PathNode | null;
}
```

---

## 4. 스티어링 행동 (군집/회피)

```typescript
class SteeringBehaviors {
  // 추적 (부드럽게)
  static seek(entity: {x:number,y:number,vx:number,vy:number}, target: {x:number,y:number}, maxSpeed: number, weight: number = 1): {x:number,y:number} {
    const dx = target.x - entity.x, dy = target.y - entity.y;
    const dist = Math.sqrt(dx*dx + dy*dy);
    if (dist < 1) return {x:0, y:0};
    return { x: (dx/dist) * maxSpeed * weight, y: (dy/dist) * maxSpeed * weight };
  }

  // 도주
  static flee(entity: any, threat: any, maxSpeed: number, panicDist: number = 200): {x:number,y:number} {
    const dx = entity.x - threat.x, dy = entity.y - threat.y;
    const dist = Math.sqrt(dx*dx + dy*dy);
    if (dist > panicDist) return {x:0, y:0};
    return { x: (dx/dist) * maxSpeed, y: (dy/dist) * maxSpeed };
  }

  // 배회 (자연스러운 랜덤 이동)
  static wander(entity: any, wanderAngle: number, maxSpeed: number): {angle: number, x: number, y: number} {
    const jitter = (Math.random() - 0.5) * 0.5;
    const newAngle = wanderAngle + jitter;
    return {
      angle: newAngle,
      x: Math.cos(newAngle) * maxSpeed * 0.5,
      y: Math.sin(newAngle) * maxSpeed * 0.5,
    };
  }

  // 군집 (보이드)
  static flock(entity: any, neighbors: any[], separationDist: number = 30): {x:number,y:number} {
    let sx = 0, sy = 0; // 분리
    let ax = 0, ay = 0; // 정렬
    let cx = 0, cy = 0; // 응집
    let count = 0;

    for (const n of neighbors) {
      const dx = entity.x - n.x, dy = entity.y - n.y;
      const dist = Math.sqrt(dx*dx + dy*dy);
      if (dist < separationDist && dist > 0) {
        sx += dx / dist; sy += dy / dist; // 가까우면 밀어냄
      }
      ax += n.vx || 0; ay += n.vy || 0;
      cx += n.x; cy += n.y;
      count++;
    }

    if (count === 0) return {x:0, y:0};
    cx = cx / count - entity.x;
    cy = cy / count - entity.y;
    ax /= count; ay /= count;

    return {
      x: sx * 1.5 + ax * 0.5 + cx * 0.3,
      y: sy * 1.5 + ay * 0.5 + cy * 0.3,
    };
  }
}
```

---

## 5. 웨이브 디렉터 시스템 (L4D 스타일)

```typescript
class WaveDirector {
  private intensity: number = 0; // 0~1
  private buildUpTimer: number = 0;
  private peakTimer: number = 0;
  private relaxTimer: number = 0;
  private phase: 'buildup' | 'peak' | 'relax' = 'buildup';

  // 플레이어 스트레스 기반 동적 스폰
  update(dt: number, playerStress: number) {
    switch (this.phase) {
      case 'buildup':
        this.intensity = Math.min(1, this.intensity + dt * 0.02);
        this.buildUpTimer += dt;
        if (this.buildUpTimer > 20000) { // 20초 빌드업
          this.phase = 'peak';
          this.peakTimer = 0;
        }
        break;

      case 'peak':
        this.intensity = 1;
        this.peakTimer += dt;
        if (this.peakTimer > 10000) { // 10초 피크
          this.phase = 'relax';
          this.relaxTimer = 0;
        }
        break;

      case 'relax':
        this.intensity = Math.max(0.1, this.intensity - dt * 0.03);
        this.relaxTimer += dt;
        if (this.relaxTimer > 15000) { // 15초 휴식
          this.phase = 'buildup';
          this.buildUpTimer = 0;
        }
        break;
    }

    // 플레이어 스트레스 반영 (적응형)
    if (playerStress > 0.8) this.intensity *= 0.8; // 너무 힘들면 완화
    if (playerStress < 0.2) this.intensity = Math.min(1, this.intensity * 1.2); // 너무 쉬우면 강화
  }

  getSpawnRate(): number { return this.intensity; }
  getEnemyTier(): number { return Math.ceil(this.intensity * 3); } // 1~3 티어
  shouldSpawnElite(): boolean { return this.phase === 'peak' && Math.random() < 0.3; }
  shouldSpawnBoss(): boolean { return this.phase === 'peak' && this.peakTimer > 8000; }
}
```
