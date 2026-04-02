# 고급 게임 시스템 v4.0

> 100+ 게임 제작 도구 교차검증 결과 — 대화/인벤토리/스킬트리/날씨/컨트롤러 등
> Construct 3, GameMaker, RPG Maker, GDevelop, Ren'Py 등의 킬러피처 채택

---

## 1. 대화/커트씬 시스템 (Ren'Py/RPG Maker 스타일)

```typescript
interface DialogueLine {
  speaker: string;
  text: string;
  portrait?: string;
  choices?: { text: string; next: string; condition?: () => boolean }[];
  onShow?: () => void;
  speed?: number; // 타이핑 속도 (ms/글자)
}

class DialogueSystem {
  private dialogues = new Map<string, DialogueLine[]>();
  private current: { id: string; index: number } | null = null;
  private container!: Phaser.GameObjects.Container;
  private nameText!: Phaser.GameObjects.Text;
  private bodyText!: Phaser.GameObjects.Text;
  private portrait!: Phaser.GameObjects.Image;
  private isTyping = false;
  private fullText = '';
  private charIndex = 0;
  private typeTimer?: Phaser.Time.TimerEvent;

  constructor(private scene: Phaser.Scene) {
    this.createUI();
  }

  private createUI() {
    const w = this.scene.scale.width;
    const h = this.scene.scale.height;
    const boxH = 150;
    const y = h - boxH;

    this.container = this.scene.add.container(0, y).setDepth(1000).setVisible(false);

    // 반투명 배경
    const bg = this.scene.add.rectangle(w / 2, boxH / 2, w - 40, boxH - 20, 0x000000, 0.85)
      .setStrokeStyle(2, 0xffffff, 0.5);
    // 이름 태그
    this.nameText = this.scene.add.text(100, 10, '', {
      fontSize: '18px', fontFamily: 'Arial Black', color: '#ffdd00',
      stroke: '#000', strokeThickness: 2,
    });
    // 본문
    this.bodyText = this.scene.add.text(100, 38, '', {
      fontSize: '16px', fontFamily: 'Arial', color: '#ffffff',
      wordWrap: { width: w - 180 }, lineSpacing: 6,
    });
    // 초상화
    this.portrait = this.scene.add.image(50, boxH / 2, '__missing').setScale(0.8).setVisible(false);

    this.container.add([bg, this.nameText, this.bodyText, this.portrait]);

    // 클릭으로 다음 대사
    this.scene.input.on('pointerdown', () => {
      if (!this.container.visible) return;
      if (this.isTyping) {
        this.completeTyping();
      } else {
        this.advance();
      }
    });
  }

  // 대화 데이터 등록
  register(id: string, lines: DialogueLine[]) {
    this.dialogues.set(id, lines);
  }

  // 대화 시작
  start(id: string) {
    const lines = this.dialogues.get(id);
    if (!lines) return;
    this.current = { id, index: 0 };
    this.container.setVisible(true);
    this.showLine(lines[0]);
  }

  private showLine(line: DialogueLine) {
    this.nameText.setText(line.speaker);
    this.bodyText.setText('');
    this.fullText = line.text;
    this.charIndex = 0;
    this.isTyping = true;

    if (line.portrait && this.scene.textures.exists(line.portrait)) {
      this.portrait.setTexture(line.portrait).setVisible(true);
    } else {
      this.portrait.setVisible(false);
    }

    line.onShow?.();

    // 타이핑 효과
    const speed = line.speed || 30;
    this.typeTimer = this.scene.time.addEvent({
      delay: speed,
      repeat: this.fullText.length - 1,
      callback: () => {
        this.charIndex++;
        this.bodyText.setText(this.fullText.substring(0, this.charIndex));
        if (this.charIndex >= this.fullText.length) this.isTyping = false;
      },
    });

    // 선택지가 있으면 표시
    if (line.choices) {
      this.scene.time.delayedCall(500, () => this.showChoices(line.choices!));
    }
  }

  private completeTyping() {
    this.typeTimer?.remove();
    this.bodyText.setText(this.fullText);
    this.isTyping = false;
  }

  private advance() {
    if (!this.current) return;
    const lines = this.dialogues.get(this.current.id)!;
    this.current.index++;
    if (this.current.index >= lines.length) {
      this.close();
    } else {
      this.showLine(lines[this.current.index]);
    }
  }

  private showChoices(choices: DialogueLine['choices']) {
    if (!choices) return;
    const filtered = choices.filter(c => !c.condition || c.condition());
    // 선택지 버튼 생성 (간소화)
    filtered.forEach((choice, i) => {
      const btn = this.scene.add.text(200, 80 + i * 30, `> ${choice.text}`, {
        fontSize: '16px', color: '#88ccff',
      }).setInteractive({ useHandCursor: true }).setDepth(1001);
      btn.on('pointerdown', () => {
        this.container.list.filter(o => o !== btn).forEach(() => {});
        btn.destroy();
        if (choice.next) this.start(choice.next);
        else this.advance();
      });
      this.container.add(btn);
    });
  }

  close() {
    this.container.setVisible(false);
    this.current = null;
    this.scene.events.emit('dialogue-end');
  }
}
```

---

## 2. 인벤토리 시스템 (RPG Maker/Diablo 스타일)

```typescript
interface InventoryItem {
  id: string;
  name: string;
  description: string;
  icon: string;
  type: 'weapon' | 'armor' | 'consumable' | 'material' | 'quest';
  rarity: 'common' | 'uncommon' | 'rare' | 'epic' | 'legendary';
  stackable: boolean;
  maxStack: number;
  quantity: number;
  stats?: Record<string, number>;
  usable?: boolean;
  onUse?: () => void;
}

class InventorySystem {
  private slots: (InventoryItem | null)[];
  private maxSlots: number;

  constructor(maxSlots: number = 20) {
    this.maxSlots = maxSlots;
    this.slots = new Array(maxSlots).fill(null);
    this.load();
  }

  addItem(item: InventoryItem): boolean {
    // 스택 가능하면 기존 슬롯에 추가
    if (item.stackable) {
      const existing = this.slots.find(s => s?.id === item.id && (s?.quantity || 0) < (s?.maxStack || 99));
      if (existing) {
        existing.quantity = Math.min((existing.quantity || 0) + item.quantity, existing.maxStack);
        this.save();
        return true;
      }
    }
    // 빈 슬롯 찾기
    const emptyIndex = this.slots.findIndex(s => s === null);
    if (emptyIndex === -1) return false; // 인벤토리 가득 참
    this.slots[emptyIndex] = { ...item };
    this.save();
    return true;
  }

  removeItem(slotIndex: number, quantity: number = 1): InventoryItem | null {
    const item = this.slots[slotIndex];
    if (!item) return null;
    if (item.stackable && item.quantity > quantity) {
      item.quantity -= quantity;
      this.save();
      return { ...item, quantity };
    }
    this.slots[slotIndex] = null;
    this.save();
    return item;
  }

  useItem(slotIndex: number): boolean {
    const item = this.slots[slotIndex];
    if (!item || !item.usable || !item.onUse) return false;
    item.onUse();
    if (item.type === 'consumable') this.removeItem(slotIndex);
    return true;
  }

  // 아이템 정렬 (등급 → 타입 → 이름)
  sort() {
    const rarityOrder = { legendary: 0, epic: 1, rare: 2, uncommon: 3, common: 4 };
    const items = this.slots.filter(Boolean) as InventoryItem[];
    items.sort((a, b) => rarityOrder[a.rarity] - rarityOrder[b.rarity] || a.type.localeCompare(b.type));
    this.slots = [...items, ...new Array(this.maxSlots - items.length).fill(null)];
    this.save();
  }

  getItems(): (InventoryItem | null)[] { return this.slots; }
  getItemCount(id: string): number {
    return this.slots.filter(s => s?.id === id).reduce((sum, s) => sum + (s?.quantity || 0), 0);
  }
  hasItem(id: string): boolean { return this.slots.some(s => s?.id === id); }
  isFull(): boolean { return this.slots.every(s => s !== null); }

  save() { localStorage.setItem('inventory', JSON.stringify(this.slots)); }
  load() {
    const d = localStorage.getItem('inventory');
    if (d) this.slots = JSON.parse(d);
  }
}

// 크래프팅 시스템
interface CraftingRecipe {
  id: string;
  name: string;
  materials: { itemId: string; quantity: number }[];
  result: { itemId: string; quantity: number };
}

class CraftingSystem {
  private recipes: CraftingRecipe[] = [];

  register(recipe: CraftingRecipe) { this.recipes.push(recipe); }

  canCraft(recipeId: string, inventory: InventorySystem): boolean {
    const recipe = this.recipes.find(r => r.id === recipeId);
    if (!recipe) return false;
    return recipe.materials.every(m => inventory.getItemCount(m.itemId) >= m.quantity);
  }

  craft(recipeId: string, inventory: InventorySystem): boolean {
    if (!this.canCraft(recipeId, inventory)) return false;
    const recipe = this.recipes.find(r => r.id === recipeId)!;
    // 재료 소비
    for (const mat of recipe.materials) {
      let remaining = mat.quantity;
      for (let i = 0; i < inventory.getItems().length && remaining > 0; i++) {
        const slot = inventory.getItems()[i];
        if (slot?.id === mat.itemId) {
          const take = Math.min(slot.quantity, remaining);
          inventory.removeItem(i, take);
          remaining -= take;
        }
      }
    }
    // 결과물 추가
    return inventory.addItem({ id: recipe.result.itemId, quantity: recipe.result.quantity } as any);
  }

  getAvailableRecipes(inventory: InventorySystem): CraftingRecipe[] {
    return this.recipes.filter(r => this.canCraft(r.id, inventory));
  }
}
```

---

## 3. 날씨 & 낮/밤 시스템 (Stardew Valley/Terraria 스타일)

```typescript
class DayNightSystem {
  private timeOfDay = 0; // 0~1 (0=자정, 0.25=새벽, 0.5=정오, 0.75=저녁)
  private daySpeed = 0.0001; // 1 게임분 = 약 1초
  private overlay: Phaser.GameObjects.Rectangle;
  private ambientLight: number = 0xffffff;

  constructor(private scene: Phaser.Scene) {
    this.overlay = scene.add.rectangle(
      scene.scale.width / 2, scene.scale.height / 2,
      scene.scale.width, scene.scale.height, 0x000033, 0
    ).setDepth(900).setBlendMode(Phaser.BlendModes.MULTIPLY);
  }

  update(delta: number) {
    this.timeOfDay = (this.timeOfDay + this.daySpeed * delta) % 1;

    // 시간대별 색상/밝기
    let color: number, alpha: number;
    if (this.timeOfDay < 0.2) { // 밤 (0~5시)
      color = 0x1a1a44; alpha = 0.6;
    } else if (this.timeOfDay < 0.3) { // 새벽 (5~7시)
      const t = (this.timeOfDay - 0.2) / 0.1;
      color = this.lerpColor(0x1a1a44, 0xff8844, t); alpha = 0.6 * (1 - t) + 0.1 * t;
    } else if (this.timeOfDay < 0.4) { // 아침 (7~10시)
      const t = (this.timeOfDay - 0.3) / 0.1;
      color = this.lerpColor(0xff8844, 0xffffff, t); alpha = 0.1 * (1 - t);
    } else if (this.timeOfDay < 0.7) { // 낮 (10~17시)
      color = 0xffffff; alpha = 0;
    } else if (this.timeOfDay < 0.8) { // 석양 (17~19시)
      const t = (this.timeOfDay - 0.7) / 0.1;
      color = this.lerpColor(0xffffff, 0xff6622, t); alpha = t * 0.2;
    } else { // 밤 (19~24시)
      const t = (this.timeOfDay - 0.8) / 0.2;
      color = this.lerpColor(0xff6622, 0x1a1a44, t); alpha = 0.2 + t * 0.4;
    }

    this.overlay.setFillStyle(color, alpha);
    this.ambientLight = color;
  }

  getTimeString(): string {
    const hours = Math.floor(this.timeOfDay * 24);
    const minutes = Math.floor((this.timeOfDay * 24 - hours) * 60);
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;
  }

  isNight(): boolean { return this.timeOfDay < 0.25 || this.timeOfDay > 0.8; }
  isDay(): boolean { return this.timeOfDay > 0.3 && this.timeOfDay < 0.7; }

  private lerpColor(c1: number, c2: number, t: number): number {
    const r1 = (c1 >> 16) & 0xff, g1 = (c1 >> 8) & 0xff, b1 = c1 & 0xff;
    const r2 = (c2 >> 16) & 0xff, g2 = (c2 >> 8) & 0xff, b2 = c2 & 0xff;
    const r = Math.round(r1 + (r2 - r1) * t);
    const g = Math.round(g1 + (g2 - g1) * t);
    const b = Math.round(b1 + (b2 - b1) * t);
    return (r << 16) | (g << 8) | b;
  }
}

class WeatherSystem {
  private currentWeather: 'clear' | 'rain' | 'snow' | 'fog' | 'storm' = 'clear';
  private emitter?: Phaser.GameObjects.Particles.ParticleEmitter;

  constructor(private scene: Phaser.Scene) {}

  setWeather(weather: typeof this.currentWeather) {
    this.emitter?.destroy();
    this.currentWeather = weather;

    const w = this.scene.scale.width;
    const h = this.scene.scale.height;

    switch (weather) {
      case 'rain':
        // 프로시저럴 빗방울 텍스처
        const rg = this.scene.make.graphics({ add: false });
        rg.fillStyle(0x8888ff, 0.6);
        rg.fillRect(0, 0, 2, 8);
        rg.generateTexture('raindrop', 2, 8);
        rg.destroy();

        this.emitter = this.scene.add.particles(0, 0, 'raindrop', {
          x: { min: 0, max: w }, y: -10,
          speedY: { min: 300, max: 500 }, speedX: { min: -30, max: -10 },
          lifespan: 2000, frequency: 5, quantity: 3,
          alpha: { min: 0.3, max: 0.7 },
        }).setDepth(800);
        break;

      case 'snow':
        const sg = this.scene.make.graphics({ add: false });
        sg.fillStyle(0xffffff);
        sg.fillCircle(3, 3, 3);
        sg.generateTexture('snowflake', 6, 6);
        sg.destroy();

        this.emitter = this.scene.add.particles(0, 0, 'snowflake', {
          x: { min: 0, max: w }, y: -10,
          speedY: { min: 30, max: 80 }, speedX: { min: -20, max: 20 },
          lifespan: 5000, frequency: 30, quantity: 2,
          scale: { min: 0.3, max: 1 }, alpha: { min: 0.5, max: 1 },
          rotate: { min: 0, max: 360 },
        }).setDepth(800);
        break;

      case 'fog':
        // 안개 오버레이
        const fog = this.scene.add.rectangle(w / 2, h / 2, w, h, 0xcccccc, 0.3).setDepth(800);
        this.scene.tweens.add({ targets: fog, alpha: { from: 0.2, to: 0.4 }, duration: 3000, yoyo: true, repeat: -1 });
        break;
    }
  }

  getWeather() { return this.currentWeather; }

  // 랜덤 날씨 변화 (선택)
  randomizeWeather() {
    const weathers: typeof this.currentWeather[] = ['clear', 'clear', 'clear', 'rain', 'rain', 'snow', 'fog', 'storm'];
    this.setWeather(weathers[Math.floor(Math.random() * weathers.length)]);
  }
}
```

---

## 4. 게임패드/컨트롤러 지원 (Construct 3 스타일)

```typescript
class GamepadManager {
  private gamepad: Gamepad | null = null;
  private deadzone = 0.15;
  private prevButtons: boolean[] = [];
  private inputMode: 'keyboard' | 'gamepad' = 'keyboard';

  constructor(private scene: Phaser.Scene) {
    window.addEventListener('gamepadconnected', (e) => {
      this.gamepad = (e as GamepadEvent).gamepad;
      this.inputMode = 'gamepad';
      console.log(`🎮 Gamepad connected: ${this.gamepad.id}`);
    });
    window.addEventListener('gamepaddisconnected', () => {
      this.gamepad = null;
      this.inputMode = 'keyboard';
    });
    // 키보드 입력 감지 시 모드 전환
    scene.input.keyboard!.on('keydown', () => { this.inputMode = 'keyboard'; });
  }

  update(): GamepadInput {
    const gp = navigator.getGamepads()?.[0];
    if (!gp) return this.getKeyboardInput();
    this.gamepad = gp;
    this.inputMode = 'gamepad';

    const input: GamepadInput = {
      moveX: this.applyDeadzone(gp.axes[0]),
      moveY: this.applyDeadzone(gp.axes[1]),
      aimX: this.applyDeadzone(gp.axes[2]),
      aimY: this.applyDeadzone(gp.axes[3]),
      attack: gp.buttons[0]?.pressed || false,     // A / Cross
      dash: gp.buttons[1]?.pressed || false,        // B / Circle
      interact: gp.buttons[2]?.pressed || false,    // X / Square
      special: gp.buttons[3]?.pressed || false,     // Y / Triangle
      pause: this.justPressed(gp, 9),               // Start
      back: this.justPressed(gp, 8),                // Select
    };

    this.prevButtons = gp.buttons.map(b => b.pressed);
    return input;
  }

  private getKeyboardInput(): GamepadInput {
    const k = this.scene.input.keyboard!;
    return {
      moveX: (k.addKey('D').isDown ? 1 : 0) - (k.addKey('A').isDown ? 1 : 0),
      moveY: (k.addKey('S').isDown ? 1 : 0) - (k.addKey('W').isDown ? 1 : 0),
      aimX: 0, aimY: 0,
      attack: k.addKey('SPACE').isDown,
      dash: k.addKey('SHIFT').isDown,
      interact: k.addKey('E').isDown,
      special: k.addKey('Q').isDown,
      pause: Phaser.Input.Keyboard.JustDown(k.addKey('ESC')),
      back: false,
    };
  }

  private applyDeadzone(value: number): number {
    return Math.abs(value) < this.deadzone ? 0 : value;
  }

  private justPressed(gp: Gamepad, index: number): boolean {
    return gp.buttons[index]?.pressed && !this.prevButtons[index];
  }

  getInputMode(): 'keyboard' | 'gamepad' { return this.inputMode; }

  // 버튼 프롬프트 아이콘 (키보드↔게임패드 자동 전환)
  getButtonPrompt(action: string): string {
    const prompts: Record<string, { keyboard: string; gamepad: string }> = {
      attack: { keyboard: 'SPACE', gamepad: 'A' },
      dash: { keyboard: 'SHIFT', gamepad: 'B' },
      interact: { keyboard: 'E', gamepad: 'X' },
      special: { keyboard: 'Q', gamepad: 'Y' },
      pause: { keyboard: 'ESC', gamepad: 'START' },
    };
    const p = prompts[action];
    return p ? p[this.inputMode] : action;
  }
}

interface GamepadInput {
  moveX: number; moveY: number;
  aimX: number; aimY: number;
  attack: boolean; dash: boolean;
  interact: boolean; special: boolean;
  pause: boolean; back: boolean;
}
```

---

## 5. 성능 프로파일러 (GameMaker 스타일)

```typescript
class PerformanceProfiler {
  private fpsHistory: number[] = [];
  private drawCalls = 0;
  private entityCount = 0;
  private memoryUsage = 0;
  private overlay?: Phaser.GameObjects.Text;
  private visible = false;

  constructor(private scene: Phaser.Scene) {
    // F3으로 토글
    scene.input.keyboard!.on('keydown-F3', () => this.toggle());
  }

  update() {
    const fps = Math.round(this.scene.game.loop.actualFps);
    this.fpsHistory.push(fps);
    if (this.fpsHistory.length > 60) this.fpsHistory.shift();

    if ((performance as any).memory) {
      this.memoryUsage = Math.round((performance as any).memory.usedJSHeapSize / 1048576);
    }

    // 렌더러 통계
    const renderer = this.scene.game.renderer as any;
    this.drawCalls = renderer?.gl ? renderer.currentPipeline?.drawCalls || 0 : 0;

    if (this.visible) this.updateOverlay();
  }

  private toggle() {
    this.visible = !this.visible;
    if (this.visible && !this.overlay) {
      this.overlay = this.scene.add.text(5, 5, '', {
        fontSize: '12px', fontFamily: 'monospace',
        color: '#00ff00', backgroundColor: '#000000aa',
        padding: { x: 6, y: 4 },
      }).setDepth(9999).setScrollFactor(0);
    }
    this.overlay?.setVisible(this.visible);
  }

  private updateOverlay() {
    const fps = this.fpsHistory[this.fpsHistory.length - 1] || 0;
    const avgFps = Math.round(this.fpsHistory.reduce((a, b) => a + b, 0) / this.fpsHistory.length);
    const minFps = Math.min(...this.fpsHistory);
    const fpsColor = fps >= 55 ? '#00ff00' : fps >= 30 ? '#ffaa00' : '#ff0000';

    this.overlay?.setText([
      `FPS: ${fps} (avg:${avgFps} min:${minFps})`,
      `Memory: ${this.memoryUsage}MB`,
      `Entities: ${this.scene.children.length}`,
      `Textures: ${this.scene.textures.getTextureKeys().length}`,
      `Draw Calls: ${this.drawCalls}`,
    ].join('\n'));
    this.overlay?.setColor(fpsColor);
  }

  // 커스텀 타이머
  private timers = new Map<string, number>();
  startTimer(label: string) { this.timers.set(label, performance.now()); }
  endTimer(label: string): number {
    const start = this.timers.get(label);
    if (!start) return 0;
    const elapsed = performance.now() - start;
    this.timers.delete(label);
    return elapsed;
  }
}
```

---

## 6. 반응형 UI 스케일링 (Construct 3 스타일)

```typescript
class ResponsiveUI {
  // 안전 영역 계산 (노치/상태바 대응)
  static getSafeArea(): { top: number; bottom: number; left: number; right: number } {
    const style = getComputedStyle(document.documentElement);
    return {
      top: parseInt(style.getPropertyValue('--sat') || '0') || (window.screen.height > 800 ? 44 : 0),
      bottom: parseInt(style.getPropertyValue('--sab') || '0') || 0,
      left: parseInt(style.getPropertyValue('--sal') || '0') || 0,
      right: parseInt(style.getPropertyValue('--sar') || '0') || 0,
    };
  }

  // 기기별 최적 해상도
  static getOptimalResolution(): { width: number; height: number } {
    const dpr = Math.min(window.devicePixelRatio, 2); // 최대 2x
    const w = window.innerWidth * dpr;
    const h = window.innerHeight * dpr;
    // 성능을 위해 최대 1920x1080 제한
    const maxW = 1920, maxH = 1080;
    const scale = Math.min(1, maxW / w, maxH / h);
    return { width: Math.floor(w * scale), height: Math.floor(h * scale) };
  }

  // 화면 방향 감지 & 강제
  static enforceOrientation(preferred: 'landscape' | 'portrait') {
    const isLandscape = window.innerWidth > window.innerHeight;
    const needsRotation = (preferred === 'landscape' && !isLandscape) ||
                          (preferred === 'portrait' && isLandscape);

    if (needsRotation) {
      // 회전 안내 오버레이
      const overlay = document.createElement('div');
      overlay.id = 'rotate-overlay';
      overlay.innerHTML = `<div style="position:fixed;inset:0;background:#000;display:flex;align-items:center;justify-content:center;z-index:99999;color:#fff;font-size:20px">📱 화면을 ${preferred === 'landscape' ? '가로' : '세로'}로 돌려주세요</div>`;
      document.body.appendChild(overlay);

      window.addEventListener('resize', () => {
        const ok = preferred === 'landscape' ? window.innerWidth > window.innerHeight : window.innerHeight > window.innerWidth;
        document.getElementById('rotate-overlay')!.style.display = ok ? 'none' : 'flex';
      });
    }
  }
}
```

---

## 7. 타일맵 자동 생성 (Tiled/LDtk 호환)

```typescript
class AutoTiler {
  // 47-tile 비트마스킹 자동 타일링
  static calculateTileIndex(grid: number[][], x: number, y: number): number {
    const isSolid = (tx: number, ty: number) => {
      if (ty < 0 || ty >= grid.length || tx < 0 || tx >= grid[0].length) return false;
      return grid[ty][tx] === 1;
    };

    let bitmask = 0;
    if (isSolid(x, y - 1))     bitmask |= 1;   // 위
    if (isSolid(x + 1, y))     bitmask |= 2;   // 오른쪽
    if (isSolid(x, y + 1))     bitmask |= 4;   // 아래
    if (isSolid(x - 1, y))     bitmask |= 8;   // 왼쪽
    // 대각선 (인접 2변이 모두 solid일 때만)
    if (isSolid(x + 1, y - 1) && (bitmask & 3) === 3)  bitmask |= 16;  // 우상
    if (isSolid(x + 1, y + 1) && (bitmask & 6) === 6)  bitmask |= 32;  // 우하
    if (isSolid(x - 1, y + 1) && (bitmask & 12) === 12) bitmask |= 64; // 좌하
    if (isSolid(x - 1, y - 1) && (bitmask & 9) === 9)  bitmask |= 128; // 좌상

    return bitmask;
  }

  // Tiled JSON 맵 로드 (Phaser)
  static loadTiledMap(scene: Phaser.Scene, key: string, tilesetKey: string): Phaser.Tilemaps.Tilemap {
    const map = scene.make.tilemap({ key });
    const tileset = map.addTilesetImage(map.tilesets[0].name, tilesetKey);
    if (!tileset) throw new Error('Tileset not found');

    // 모든 레이어 자동 생성
    map.layers.forEach(layerData => {
      const layer = map.createLayer(layerData.name, tileset);
      if (layerData.name.includes('collision') || layerData.name.includes('wall')) {
        layer?.setCollisionByExclusion([-1, 0]);
      }
    });

    return map;
  }

  // 패럴랙스 배경 자동 설정
  static setupParallax(scene: Phaser.Scene, layers: { key: string; scrollFactor: number; y?: number }[]) {
    layers.forEach(({ key, scrollFactor, y }) => {
      const img = scene.add.tileSprite(
        scene.scale.width / 2, y || scene.scale.height / 2,
        scene.scale.width, scene.scale.height, key
      ).setScrollFactor(scrollFactor, scrollFactor).setDepth(-10 + scrollFactor * 10);
    });
  }
}
```

---

## 8. 스킬 트리 시스템 (Path of Exile 스타일)

```typescript
interface SkillNode {
  id: string;
  name: string;
  description: string;
  icon: string;
  cost: number; // 스킬 포인트
  maxLevel: number;
  currentLevel: number;
  prerequisites: string[]; // 선행 스킬 ID
  effects: { stat: string; value: number; perLevel: number }[];
  position: { x: number; y: number }; // UI 위치
  tier: 'minor' | 'major' | 'keystone';
}

class SkillTreeSystem {
  private nodes = new Map<string, SkillNode>();
  private skillPoints = 0;

  addNode(node: SkillNode) { this.nodes.set(node.id, node); }

  canUnlock(nodeId: string): boolean {
    const node = this.nodes.get(nodeId);
    if (!node) return false;
    if (node.currentLevel >= node.maxLevel) return false;
    if (this.skillPoints < node.cost) return false;
    return node.prerequisites.every(pre => {
      const preNode = this.nodes.get(pre);
      return preNode && preNode.currentLevel > 0;
    });
  }

  unlock(nodeId: string): boolean {
    if (!this.canUnlock(nodeId)) return false;
    const node = this.nodes.get(nodeId)!;
    node.currentLevel++;
    this.skillPoints -= node.cost;
    this.save();
    return true;
  }

  getTotalStats(): Record<string, number> {
    const stats: Record<string, number> = {};
    for (const node of this.nodes.values()) {
      if (node.currentLevel > 0) {
        for (const effect of node.effects) {
          const value = effect.value + effect.perLevel * (node.currentLevel - 1);
          stats[effect.stat] = (stats[effect.stat] || 0) + value;
        }
      }
    }
    return stats;
  }

  addSkillPoints(amount: number) { this.skillPoints += amount; this.save(); }
  getSkillPoints(): number { return this.skillPoints; }
  getNodes(): SkillNode[] { return [...this.nodes.values()]; }

  // 리셋 (비용 있음)
  reset(refundRate: number = 1.0) {
    let refunded = 0;
    for (const node of this.nodes.values()) {
      refunded += node.currentLevel * node.cost;
      node.currentLevel = 0;
    }
    this.skillPoints += Math.floor(refunded * refundRate);
    this.save();
  }

  save() {
    localStorage.setItem('skilltree', JSON.stringify({
      points: this.skillPoints,
      nodes: [...this.nodes.entries()].map(([id, n]) => [id, n.currentLevel]),
    }));
  }
  load() {
    const d = localStorage.getItem('skilltree');
    if (d) {
      const p = JSON.parse(d);
      this.skillPoints = p.points;
      for (const [id, level] of p.nodes) {
        const node = this.nodes.get(id);
        if (node) node.currentLevel = level;
      }
    }
  }
}
```
