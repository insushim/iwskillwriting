# 프로시저럴 생성 가이드 v2.0

> WFC, BSP, Perlin Noise, Cellular Automata, L-Systems 등 구현 가이드

---

## 1. Wave Function Collapse (WFC) — 타일맵 생성

```typescript
// 간소화된 WFC 구현
class WaveFunctionCollapse {
  grid: Set<number>[][];
  rules: Map<number, { up: number[], down: number[], left: number[], right: number[] }>;

  constructor(width: number, height: number, tileCount: number) {
    this.grid = Array.from({ length: height }, () =>
      Array.from({ length: width }, () => new Set(Array.from({ length: tileCount }, (_, i) => i)))
    );
  }

  // 엔트로피가 가장 낮은 (선택지가 적은) 셀 찾기
  findLowestEntropy(): [number, number] | null {
    let minEntropy = Infinity;
    let candidates: [number, number][] = [];

    for (let y = 0; y < this.grid.length; y++) {
      for (let x = 0; x < this.grid[0].length; x++) {
        const entropy = this.grid[y][x].size;
        if (entropy <= 1) continue;
        if (entropy < minEntropy) {
          minEntropy = entropy;
          candidates = [[x, y]];
        } else if (entropy === minEntropy) {
          candidates.push([x, y]);
        }
      }
    }

    if (candidates.length === 0) return null;
    return candidates[Math.floor(Math.random() * candidates.length)];
  }

  // 셀 확정 (collapse)
  collapse(x: number, y: number): void {
    const options = Array.from(this.grid[y][x]);
    const chosen = options[Math.floor(Math.random() * options.length)];
    this.grid[y][x] = new Set([chosen]);
    this.propagate(x, y);
  }

  // 제약 전파
  propagate(startX: number, startY: number): void {
    const stack: [number, number][] = [[startX, startY]];
    while (stack.length > 0) {
      const [x, y] = stack.pop()!;
      const current = this.grid[y][x];

      const neighbors = [
        { dx: 0, dy: -1, dir: 'up' as const },
        { dx: 0, dy: 1, dir: 'down' as const },
        { dx: -1, dy: 0, dir: 'left' as const },
        { dx: 1, dy: 0, dir: 'right' as const },
      ];

      for (const { dx, dy, dir } of neighbors) {
        const nx = x + dx, ny = y + dy;
        if (ny < 0 || ny >= this.grid.length || nx < 0 || nx >= this.grid[0].length) continue;

        const allowed = new Set<number>();
        for (const tile of current) {
          for (const compatible of this.rules.get(tile)![dir]) {
            allowed.add(compatible);
          }
        }

        const neighbor = this.grid[ny][nx];
        const before = neighbor.size;
        for (const tile of neighbor) {
          if (!allowed.has(tile)) neighbor.delete(tile);
        }

        if (neighbor.size < before) stack.push([nx, ny]);
      }
    }
  }

  // 전체 생성 실행
  generate(): number[][] {
    while (true) {
      const cell = this.findLowestEntropy();
      if (!cell) break;
      this.collapse(cell[0], cell[1]);
    }
    return this.grid.map(row => row.map(cell => Array.from(cell)[0]));
  }
}
```

---

## 2. BSP 던전 생성

```typescript
interface BSPRoom {
  x: number; y: number; w: number; h: number;
  center: { x: number; y: number };
}

class BSPDungeonGenerator {
  minRoomSize = 6;

  generate(width: number, height: number, splits: number = 5): { rooms: BSPRoom[], corridors: Corridor[] } {
    const root = { x: 1, y: 1, w: width - 2, h: height - 2 };
    const leaves = this.splitRecursive(root, splits);
    const rooms = leaves.map(leaf => this.createRoom(leaf));
    const corridors = this.connectRooms(rooms);
    return { rooms, corridors };
  }

  private splitRecursive(node: any, depth: number): any[] {
    if (depth <= 0 || node.w < this.minRoomSize * 2 || node.h < this.minRoomSize * 2) {
      return [node];
    }

    const splitH = node.w / node.h < 0.8 ? true : node.w / node.h > 1.2 ? false : Math.random() > 0.5;

    if (splitH) {
      const split = node.y + this.minRoomSize + Math.floor(Math.random() * (node.h - this.minRoomSize * 2));
      return [
        ...this.splitRecursive({ x: node.x, y: node.y, w: node.w, h: split - node.y }, depth - 1),
        ...this.splitRecursive({ x: node.x, y: split, w: node.w, h: node.h - (split - node.y) }, depth - 1),
      ];
    } else {
      const split = node.x + this.minRoomSize + Math.floor(Math.random() * (node.w - this.minRoomSize * 2));
      return [
        ...this.splitRecursive({ x: node.x, y: node.y, w: split - node.x, h: node.h }, depth - 1),
        ...this.splitRecursive({ x: split, y: node.y, w: node.w - (split - node.x), h: node.h }, depth - 1),
      ];
    }
  }

  private createRoom(leaf: any): BSPRoom {
    const padding = 1;
    const x = leaf.x + padding + Math.floor(Math.random() * Math.max(1, leaf.w / 4));
    const y = leaf.y + padding + Math.floor(Math.random() * Math.max(1, leaf.h / 4));
    const w = Math.max(this.minRoomSize - 2, Math.floor(leaf.w * (0.5 + Math.random() * 0.3)));
    const h = Math.max(this.minRoomSize - 2, Math.floor(leaf.h * (0.5 + Math.random() * 0.3)));
    return { x, y, w, h, center: { x: Math.floor(x + w / 2), y: Math.floor(y + h / 2) } };
  }

  private connectRooms(rooms: BSPRoom[]): Corridor[] {
    const corridors: Corridor[] = [];
    for (let i = 1; i < rooms.length; i++) {
      const a = rooms[i - 1].center;
      const b = rooms[i].center;
      // L자 복도
      if (Math.random() > 0.5) {
        corridors.push({ x1: a.x, y1: a.y, x2: b.x, y2: a.y }); // 가로
        corridors.push({ x1: b.x, y1: a.y, x2: b.x, y2: b.y }); // 세로
      } else {
        corridors.push({ x1: a.x, y1: a.y, x2: a.x, y2: b.y }); // 세로
        corridors.push({ x1: a.x, y1: b.y, x2: b.x, y2: b.y }); // 가로
      }
    }
    return corridors;
  }
}
```

---

## 3. Cellular Automata — 동굴 생성

```typescript
class CaveGenerator {
  generate(width: number, height: number, fillProb: number = 0.45, iterations: number = 5): number[][] {
    // 초기화: 랜덤 노이즈
    let grid = Array.from({ length: height }, () =>
      Array.from({ length: width }, () => Math.random() < fillProb ? 1 : 0)
    );

    // 가장자리는 벽
    for (let y = 0; y < height; y++) {
      grid[y][0] = grid[y][width - 1] = 1;
    }
    for (let x = 0; x < width; x++) {
      grid[0][x] = grid[height - 1][x] = 1;
    }

    // Cellular Automata 반복
    for (let i = 0; i < iterations; i++) {
      const newGrid = grid.map(row => [...row]);
      for (let y = 1; y < height - 1; y++) {
        for (let x = 1; x < width - 1; x++) {
          const neighbors = this.countNeighbors(grid, x, y);
          // 4-5 규칙: 이웃 5개 이상이면 벽, 벽이 2개 미만이면 빈칸
          if (neighbors >= 5) newGrid[y][x] = 1;
          else if (neighbors <= 2) newGrid[y][x] = 0;
        }
      }
      grid = newGrid;
    }

    return grid;
  }

  private countNeighbors(grid: number[][], x: number, y: number): number {
    let count = 0;
    for (let dy = -1; dy <= 1; dy++) {
      for (let dx = -1; dx <= 1; dx++) {
        if (dx === 0 && dy === 0) continue;
        count += grid[y + dy]?.[x + dx] ?? 1;
      }
    }
    return count;
  }
}
```

---

## 4. Perlin Noise — 지형 생성

```typescript
// 간소화된 Perlin Noise (게임용)
class SimpleNoise {
  private permutation: number[];

  constructor(seed: number = 42) {
    this.permutation = this.generatePermutation(seed);
  }

  private generatePermutation(seed: number): number[] {
    const p = Array.from({ length: 256 }, (_, i) => i);
    // Fisher-Yates with seed
    let s = seed;
    for (let i = 255; i > 0; i--) {
      s = (s * 16807) % 2147483647;
      const j = s % (i + 1);
      [p[i], p[j]] = [p[j], p[i]];
    }
    return [...p, ...p]; // 더블링
  }

  noise2D(x: number, y: number): number {
    const X = Math.floor(x) & 255;
    const Y = Math.floor(y) & 255;
    const xf = x - Math.floor(x);
    const yf = y - Math.floor(y);
    const u = this.fade(xf);
    const v = this.fade(yf);

    const p = this.permutation;
    const a = p[X] + Y, b = p[X + 1] + Y;

    return this.lerp(v,
      this.lerp(u, this.grad(p[a], xf, yf), this.grad(p[b], xf - 1, yf)),
      this.lerp(u, this.grad(p[a + 1], xf, yf - 1), this.grad(p[b + 1], xf - 1, yf - 1))
    );
  }

  // 옥타브 노이즈 (자연스러운 지형)
  octaveNoise(x: number, y: number, octaves: number = 4): number {
    let value = 0, amplitude = 1, frequency = 1, maxValue = 0;
    for (let i = 0; i < octaves; i++) {
      value += this.noise2D(x * frequency, y * frequency) * amplitude;
      maxValue += amplitude;
      amplitude *= 0.5;
      frequency *= 2;
    }
    return value / maxValue;
  }

  private fade(t: number): number { return t * t * t * (t * (t * 6 - 15) + 10); }
  private lerp(t: number, a: number, b: number): number { return a + t * (b - a); }
  private grad(hash: number, x: number, y: number): number {
    const h = hash & 3;
    return (h < 2 ? x : -x) + (h === 0 || h === 3 ? y : -y);
  }

  // 지형 맵 생성
  generateTerrainMap(width: number, height: number, scale: number = 0.05): number[][] {
    return Array.from({ length: height }, (_, y) =>
      Array.from({ length: width }, (_, x) =>
        (this.octaveNoise(x * scale, y * scale) + 1) / 2 // 0~1 정규화
      )
    );
  }
}

// 지형 타입 분류
function classifyTerrain(value: number): string {
  if (value < 0.3) return 'water';
  if (value < 0.4) return 'sand';
  if (value < 0.6) return 'grass';
  if (value < 0.75) return 'forest';
  if (value < 0.85) return 'mountain';
  return 'snow';
}
```

---

## 5. 아이템/전리품 생성

```typescript
class LootGenerator {
  // 가중 랜덤 선택
  weightedRandom<T extends { weight: number }>(items: T[]): T {
    const totalWeight = items.reduce((sum, item) => sum + item.weight, 0);
    let random = Math.random() * totalWeight;
    for (const item of items) {
      random -= item.weight;
      if (random <= 0) return item;
    }
    return items[items.length - 1];
  }

  // 가챠 시스템 (피티 포함)
  generateDrop(pityCounter: number): { rarity: string; pity: number } {
    const SOFT_PITY = 75;
    const HARD_PITY = 90;
    const BASE_SSR_RATE = 0.006; // 0.6%

    let ssrRate = BASE_SSR_RATE;
    if (pityCounter >= HARD_PITY) ssrRate = 1.0;
    else if (pityCounter >= SOFT_PITY) {
      ssrRate += (pityCounter - SOFT_PITY) * 0.06;
    }

    const roll = Math.random();
    if (roll < ssrRate) return { rarity: 'SSR', pity: 0 };
    if (roll < ssrRate + 0.05) return { rarity: 'SR', pity: pityCounter + 1 };
    if (roll < ssrRate + 0.15) return { rarity: 'R', pity: pityCounter + 1 };
    return { rarity: 'N', pity: pityCounter + 1 };
  }

  // 랜덤 스탯 접미사/접두사
  generateAffixes(itemLevel: number): Affix[] {
    const prefixes = [
      { name: '강력한', stat: 'attack', value: () => 5 + Math.floor(itemLevel * 1.5) },
      { name: '견고한', stat: 'defense', value: () => 3 + Math.floor(itemLevel * 1.2) },
      { name: '신속한', stat: 'speed', value: () => 2 + Math.floor(itemLevel * 0.8) },
      { name: '치명적인', stat: 'critRate', value: () => 1 + Math.floor(itemLevel * 0.5) },
    ];
    const suffixes = [
      { name: '화염의', stat: 'fireDmg', value: () => itemLevel * 2 },
      { name: '빙결의', stat: 'iceDmg', value: () => itemLevel * 2 },
      { name: '번개의', stat: 'lightDmg', value: () => itemLevel * 2 },
      { name: '흡혈의', stat: 'lifeSteal', value: () => Math.floor(itemLevel * 0.3) },
    ];

    const result: Affix[] = [];
    if (Math.random() < 0.7) result.push(this.weightedRandom(prefixes.map(p => ({ ...p, weight: 1 }))));
    if (Math.random() < 0.4) result.push(this.weightedRandom(suffixes.map(s => ({ ...s, weight: 1 }))));
    return result;
  }
}
```
