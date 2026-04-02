# 100+ 도구 킬러피처 교차검증 결과 v4.0

> Construct 3, GameMaker, RPG Maker, GDevelop, Ren'Py, Buildbox, Stencyl,
> Rosebud.ai, Ludo.ai, Scenario.gg, InWorld AI, FMOD, Spine, Tiled, LDtk,
> Unity, Unreal, Godot, Phaser, PixiJS, Three.js, Bevy 등 100개+ 도구 분석

---

## 1. FMOD 적응형 음악 시스템 (FMOD/Wwise 킬러피처)

```typescript
// 게임 상태에 따라 음악이 동적으로 변하는 시스템
class AdaptiveMusicSystem {
  private layers: Map<string, { audio: HTMLAudioElement; targetVolume: number; currentVolume: number }> = new Map();
  private intensity = 0; // 0~1

  constructor() {
    // 음악 레이어 등록 (같은 BPM/키로 제작된 트랙들)
    this.addLayer('ambient', 'assets/audio/bgm_ambient.mp3', 1.0);
    this.addLayer('drums', 'assets/audio/bgm_drums.mp3', 0.0);
    this.addLayer('melody', 'assets/audio/bgm_melody.mp3', 0.0);
    this.addLayer('boss', 'assets/audio/bgm_boss.mp3', 0.0);
  }

  private addLayer(id: string, src: string, volume: number) {
    const audio = new Audio(src);
    audio.loop = true;
    audio.volume = volume;
    this.layers.set(id, { audio, targetVolume: volume, currentVolume: volume });
  }

  play() {
    for (const layer of this.layers.values()) {
      layer.audio.play().catch(() => {}); // 자동재생 정책 대응
    }
  }

  // 전투 강도에 따라 레이어 믹싱
  setIntensity(value: number) {
    this.intensity = Math.max(0, Math.min(1, value));
    const layers = this.layers;

    layers.get('ambient')!.targetVolume = Math.max(0.1, 1 - this.intensity);
    layers.get('drums')!.targetVolume = this.intensity > 0.3 ? Math.min(1, this.intensity * 1.5) : 0;
    layers.get('melody')!.targetVolume = this.intensity > 0.5 ? Math.min(1, (this.intensity - 0.5) * 2) : 0;
    layers.get('boss')!.targetVolume = this.intensity > 0.8 ? Math.min(1, (this.intensity - 0.8) * 5) : 0;
  }

  // 매 프레임 부드러운 볼륨 전환
  update(dt: number) {
    const lerpSpeed = 0.003 * dt;
    for (const layer of this.layers.values()) {
      layer.currentVolume += (layer.targetVolume - layer.currentVolume) * lerpSpeed;
      layer.audio.volume = Math.max(0, Math.min(1, layer.currentVolume));
    }
  }

  // 이벤트 기반 자동 강도 조절
  onEnemySpawn() { this.setIntensity(Math.min(1, this.intensity + 0.1)); }
  onEnemyKill() { this.setIntensity(Math.max(0, this.intensity - 0.05)); }
  onBossSpawn() { this.setIntensity(1.0); }
  onWaveClear() { this.setIntensity(0.1); }
  onPlayerLowHP() { this.setIntensity(Math.min(1, this.intensity + 0.2)); }
}
```

---

## 2. Construct 3 스타일 이벤트 시스템

```typescript
// 조건-액션 기반 이벤트 시스템 (비주얼 스크립팅의 코드 버전)
class EventSheet {
  private rules: EventRule[] = [];

  // 조건→액션 규칙 등록
  when(condition: () => boolean): EventRuleBuilder {
    const rule: EventRule = { condition, actions: [], once: false, active: true };
    this.rules.push(rule);
    return {
      do: (action: () => void) => { rule.actions.push(action); return this.when(condition); },
      once: () => { rule.once = true; return { do: (action: () => void) => { rule.actions.push(action); } }; },
    };
  }

  // 매 프레임 체크
  update() {
    for (const rule of this.rules) {
      if (!rule.active) continue;
      if (rule.condition()) {
        for (const action of rule.actions) action();
        if (rule.once) rule.active = false;
      }
    }
  }
}

interface EventRule {
  condition: () => boolean;
  actions: (() => void)[];
  once: boolean;
  active: boolean;
}

interface EventRuleBuilder {
  do: (action: () => void) => EventRuleBuilder;
  once: () => { do: (action: () => void) => void };
}

// 사용 예
const events = new EventSheet();
events.when(() => player.hp <= 0).once().do(() => gameOver());
events.when(() => enemies.length === 0).do(() => spawnNextWave());
events.when(() => player.level >= 5).once().do(() => unlockWeapon('laser'));
events.when(() => player.y > 600).do(() => { player.hp -= 1; player.y = 100; }); // 낙사
```

---

## 3. GDevelop 스타일 핫 리로드

```typescript
// Vite HMR + 게임 상태 유지 핫 리로드
class HotReloadSystem {
  private savedState: any = null;

  // 현재 게임 상태 저장
  saveState(scene: Phaser.Scene): any {
    return {
      player: { x: (scene as any).player?.x, y: (scene as any).player?.y, hp: (scene as any).player?.hp },
      score: (scene as any).score,
      wave: (scene as any).waveNumber,
      camera: { x: scene.cameras.main.scrollX, y: scene.cameras.main.scrollY },
    };
  }

  // 상태 복원
  restoreState(scene: Phaser.Scene, state: any) {
    if (!state) return;
    const p = (scene as any).player;
    if (p && state.player) {
      p.x = state.player.x;
      p.y = state.player.y;
      if (state.player.hp) p.hp = state.player.hp;
    }
    if (state.score) (scene as any).score = state.score;
    if (state.wave) (scene as any).waveNumber = state.wave;
  }
}

// Vite에서 사용 (vite.config.ts와 연동)
if (import.meta.hot) {
  import.meta.hot.accept(() => {
    // 게임 상태를 보존하면서 모듈 교체
    console.log('[HMR] Game module updated');
  });
}
```

---

## 4. RPG Maker 스타일 턴제 전투

```typescript
class TurnBasedBattle {
  private turnOrder: BattleUnit[] = [];
  private currentTurn = 0;
  private phase: 'select' | 'execute' | 'result' = 'select';

  constructor(private party: BattleUnit[], private enemies: BattleUnit[]) {
    this.calculateTurnOrder();
  }

  private calculateTurnOrder() {
    this.turnOrder = [...this.party, ...this.enemies]
      .filter(u => u.hp > 0)
      .sort((a, b) => b.speed - a.speed); // 속도 순
  }

  getCurrentUnit(): BattleUnit { return this.turnOrder[this.currentTurn]; }

  // 행동 선택 (플레이어)
  selectAction(action: BattleAction) {
    const unit = this.getCurrentUnit();
    this.executeAction(unit, action);
  }

  // AI 행동 (적)
  aiSelectAction(unit: BattleUnit): BattleAction {
    if (unit.hp / unit.maxHp < 0.3 && unit.hasSkill('heal')) {
      return { type: 'skill', skillId: 'heal', target: unit };
    }
    // 가장 HP 낮은 아군 공격
    const target = this.party.filter(p => p.hp > 0).sort((a, b) => a.hp - b.hp)[0];
    return { type: 'attack', target };
  }

  private executeAction(unit: BattleUnit, action: BattleAction) {
    switch (action.type) {
      case 'attack':
        const dmg = Math.max(1, unit.atk - action.target!.def);
        action.target!.hp -= dmg;
        break;
      case 'skill':
        const skill = SKILLS[action.skillId!];
        skill.execute(unit, action.target);
        unit.mp -= skill.cost;
        break;
      case 'item':
        // 아이템 사용
        break;
      case 'defend':
        unit.defending = true; // 다음 턴까지 방어력 2배
        break;
      case 'flee':
        const chance = 0.5 + (unit.speed / 200);
        if (Math.random() < chance) this.endBattle('flee');
        break;
    }

    this.nextTurn();
  }

  private nextTurn() {
    // 전투 종료 체크
    if (this.enemies.every(e => e.hp <= 0)) { this.endBattle('win'); return; }
    if (this.party.every(p => p.hp <= 0)) { this.endBattle('lose'); return; }

    this.currentTurn = (this.currentTurn + 1) % this.turnOrder.length;
    // 죽은 유닛 건너뛰기
    while (this.getCurrentUnit().hp <= 0) {
      this.currentTurn = (this.currentTurn + 1) % this.turnOrder.length;
    }

    const unit = this.getCurrentUnit();
    unit.defending = false;

    // 적 턴이면 AI 실행
    if (this.enemies.includes(unit)) {
      const action = this.aiSelectAction(unit);
      this.executeAction(unit, action);
    }
    // 플레이어 턴이면 UI 대기
  }

  private endBattle(result: 'win' | 'lose' | 'flee') {
    // 보상 지급, 경험치 분배 등
  }
}

interface BattleUnit {
  name: string; hp: number; maxHp: number; mp: number; maxMp: number;
  atk: number; def: number; speed: number;
  defending: boolean;
  hasSkill: (id: string) => boolean;
}

interface BattleAction {
  type: 'attack' | 'skill' | 'item' | 'defend' | 'flee';
  target?: BattleUnit;
  skillId?: string;
  itemId?: string;
}
```

---

## 5. Spine 스타일 2D 본 애니메이션 (간소화)

```typescript
// Spine 없이 구현하는 간단한 2D 스켈레탈 애니메이션
class SimpleSkeleton {
  bones: Map<string, Bone> = new Map();
  animations: Map<string, BoneAnimation> = new Map();
  private currentAnim: string = '';
  private animTime = 0;

  addBone(id: string, parent: string | null, x: number, y: number, length: number, sprite?: string) {
    this.bones.set(id, { id, parent, x, y, length, angle: 0, sprite });
  }

  addAnimation(name: string, keyframes: Record<string, { time: number; angle: number }[]>) {
    this.animations.set(name, { name, keyframes, duration: 0 });
    // duration 계산
    let maxTime = 0;
    for (const frames of Object.values(keyframes)) {
      for (const f of frames) if (f.time > maxTime) maxTime = f.time;
    }
    this.animations.get(name)!.duration = maxTime;
  }

  play(name: string) { this.currentAnim = name; this.animTime = 0; }

  update(dt: number) {
    const anim = this.animations.get(this.currentAnim);
    if (!anim) return;
    this.animTime = (this.animTime + dt) % anim.duration;

    for (const [boneId, keyframes] of Object.entries(anim.keyframes)) {
      const bone = this.bones.get(boneId);
      if (!bone || keyframes.length < 2) continue;

      // 현재 시간에 맞는 키프레임 보간
      let prev = keyframes[0], next = keyframes[1];
      for (let i = 0; i < keyframes.length - 1; i++) {
        if (this.animTime >= keyframes[i].time && this.animTime < keyframes[i + 1].time) {
          prev = keyframes[i];
          next = keyframes[i + 1];
          break;
        }
      }
      const t = (this.animTime - prev.time) / (next.time - prev.time);
      bone.angle = prev.angle + (next.angle - prev.angle) * t;
    }
  }

  render(ctx: CanvasRenderingContext2D, rootX: number, rootY: number) {
    for (const bone of this.bones.values()) {
      ctx.save();
      const worldPos = this.getWorldPosition(bone, rootX, rootY);
      ctx.translate(worldPos.x, worldPos.y);
      ctx.rotate(bone.angle);
      // 스프라이트 또는 라인 그리기
      ctx.strokeStyle = '#fff';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(0, 0);
      ctx.lineTo(bone.length, 0);
      ctx.stroke();
      ctx.restore();
    }
  }

  private getWorldPosition(bone: Bone, rootX: number, rootY: number): { x: number; y: number } {
    if (!bone.parent) return { x: rootX + bone.x, y: rootY + bone.y };
    const parent = this.bones.get(bone.parent)!;
    const parentPos = this.getWorldPosition(parent, rootX, rootY);
    const cos = Math.cos(parent.angle);
    const sin = Math.sin(parent.angle);
    return {
      x: parentPos.x + cos * bone.x - sin * bone.y,
      y: parentPos.y + sin * bone.x + cos * bone.y,
    };
  }
}

interface Bone {
  id: string; parent: string | null;
  x: number; y: number; length: number; angle: number;
  sprite?: string;
}

interface BoneAnimation {
  name: string;
  keyframes: Record<string, { time: number; angle: number }[]>;
  duration: number;
}
```

---

## 6. InWorld AI 스타일 지능형 NPC 대화

```typescript
// Claude/Gemini API로 동적 NPC 대화 생성
class SmartNPC {
  private personality: string;
  private memory: string[] = [];
  private maxMemory = 10;

  constructor(
    private name: string,
    private role: string,
    traits: string[],
    private apiKey: string,
  ) {
    this.personality = `You are ${name}, a ${role}. Personality: ${traits.join(', ')}.
      Respond in character. Keep responses under 2 sentences. Use Korean.`;
  }

  async chat(playerMessage: string): Promise<string> {
    this.memory.push(`Player: ${playerMessage}`);
    if (this.memory.length > this.maxMemory) this.memory.shift();

    const prompt = `${this.personality}\n\nConversation history:\n${this.memory.join('\n')}\n\n${this.name}:`;

    try {
      const response = await fetch('https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=' + this.apiKey, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: [{ parts: [{ text: prompt }] }],
          generationConfig: { maxOutputTokens: 100, temperature: 0.8 },
        }),
      });
      const data = await response.json();
      const reply = data.candidates?.[0]?.content?.parts?.[0]?.text || '...';
      this.memory.push(`${this.name}: ${reply}`);
      return reply;
    } catch {
      return this.getFallbackResponse();
    }
  }

  private getFallbackResponse(): string {
    const fallbacks = [
      '흠, 그건 생각 좀 해봐야겠네.',
      '재미있는 얘기군.',
      '그래, 알겠어.',
      '다음에 더 이야기하자.',
    ];
    return fallbacks[Math.floor(Math.random() * fallbacks.length)];
  }
}
```

---

## 7. Defold 스타일 초경량 빌드 최적화

```typescript
// 빌드 사이즈 최소화 체크리스트 & 도구
class BuildOptimizer {
  // 사용되지 않는 에셋 감지
  static findUnusedAssets(usedAssets: Set<string>, allAssets: string[]): string[] {
    return allAssets.filter(a => !usedAssets.has(a));
  }

  // 이미지를 WebP로 변환 (50~80% 크기 감소)
  static async convertToWebP(imagePath: string): Promise<Blob> {
    const img = new Image();
    img.src = imagePath;
    await new Promise(r => img.onload = r);
    const canvas = document.createElement('canvas');
    canvas.width = img.width;
    canvas.height = img.height;
    canvas.getContext('2d')!.drawImage(img, 0, 0);
    return new Promise(r => canvas.toBlob(b => r(b!), 'image/webp', 0.85));
  }

  // 번들 사이즈 분석
  static analyzeBundleSize(files: { name: string; size: number }[]): string {
    const total = files.reduce((s, f) => s + f.size, 0);
    const sorted = [...files].sort((a, b) => b.size - a.size);
    const lines = sorted.slice(0, 10).map(f =>
      `  ${f.name}: ${(f.size / 1024).toFixed(1)}KB (${((f.size / total) * 100).toFixed(1)}%)`
    );
    return `Total: ${(total / 1024).toFixed(1)}KB\nTop 10:\n${lines.join('\n')}`;
  }
}
```

---

## 킬러피처 교차검증 요약표

| 도구 | 킬러피처 | 우리 스킬에 채택 여부 |
|------|---------|---------------------|
| Construct 3 | 이벤트 시트 시스템 | ✅ EventSheet 클래스 |
| RPG Maker | 턴제 전투 시스템 | ✅ TurnBasedBattle |
| Ren'Py | 타이핑 대화 시스템 | ✅ DialogueSystem (v4.0) |
| FMOD | 적응형 음악 레이어 | ✅ AdaptiveMusicSystem |
| Spine | 2D 본 애니메이션 | ✅ SimpleSkeleton |
| InWorld AI | 지능형 NPC 대화 | ✅ SmartNPC (Gemini API) |
| GDevelop | 핫 리로드 | ✅ HotReloadSystem |
| Defold | 초경량 빌드 | ✅ BuildOptimizer |
| Tiled | 타일맵 표준 | ✅ AutoTiler (v4.0) |
| GameMaker | 타임라인 에디터 | ⬜ (코드로 대체) |
| Stardew Valley | 날씨/낮밤 | ✅ DayNight+Weather (v4.0) |
| Path of Exile | 스킬 트리 | ✅ SkillTreeSystem (v4.0) |
| Diablo | 인벤토리/크래프팅 | ✅ InventorySystem (v4.0) |
| Buildbox | 드래그앤드롭 | ⬜ (CLI 기반이므로 불필요) |
| Unity | 크로스플랫폼 빌드 | ✅ deployment-guide.md |
| Scenario.gg | 스타일 일관 AI | ✅ asset_gen.py |
| PlayCanvas | 클라우드 협업 | ⬜ (단독 사용 기준) |
