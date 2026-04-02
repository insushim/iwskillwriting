# Phaser 3 Best Practices

## 프로젝트 설정

### Vite + TypeScript 설정
```bash
npm init -y
npm install phaser@3.80 --save
npm install typescript vite @types/node --save-dev
```

### vite.config.ts
```typescript
import { defineConfig } from 'vite';

export default defineConfig({
  base: './',
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
  },
  server: {
    port: 5173,
    open: true,
  },
});
```

### tsconfig.json
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "outDir": "dist",
    "sourceMap": true,
    "lib": ["ES2020", "DOM"]
  },
  "include": ["src/**/*"]
}
```

### package.json scripts
```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  }
}
```

---

## 핵심 패턴

### 게임 초기화
```typescript
// src/main.ts
import Phaser from 'phaser';
import { BootScene } from './scenes/BootScene';
import { MenuScene } from './scenes/MenuScene';
import { GameScene } from './scenes/GameScene';
import { UIScene } from './scenes/UIScene';

const config: Phaser.Types.Core.GameConfig = {
  type: Phaser.AUTO,
  width: 800,
  height: 600,
  parent: 'game-container',
  backgroundColor: '#1a1a2e',
  physics: {
    default: 'arcade',
    arcade: {
      gravity: { x: 0, y: 0 }, // 탑다운이면 0, 플랫포머면 { x: 0, y: 300 }
      debug: false,
    },
  },
  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH,
  },
  scene: [BootScene, MenuScene, GameScene, UIScene],
};

new Phaser.Game(config);
```

### 씬 패턴
```typescript
// src/scenes/GameScene.ts
import Phaser from 'phaser';

export class GameScene extends Phaser.Scene {
  private player!: Phaser.Physics.Arcade.Sprite;
  private enemies!: Phaser.Physics.Arcade.Group;
  private cursors!: Phaser.Types.Input.Keyboard.CursorKeys;
  private score: number = 0;
  private waveNumber: number = 1;

  constructor() {
    super({ key: 'GameScene' });
  }

  create(): void {
    // 배경
    this.add.image(400, 300, 'background');

    // 플레이어
    this.player = this.physics.add.sprite(400, 300, 'player');
    this.player.setCollideWorldBounds(true);

    // 적 그룹 (오브젝트 풀링)
    this.enemies = this.physics.add.group({
      classType: Phaser.Physics.Arcade.Sprite,
      maxSize: 50,
      runChildUpdate: true,
    });

    // 충돌
    this.physics.add.overlap(
      this.player,
      this.enemies,
      this.onPlayerHit,
      undefined,
      this
    );

    // 입력
    this.cursors = this.input.keyboard!.createCursorKeys();

    // UI 씬 병렬 실행
    this.scene.launch('UIScene');
  }

  update(time: number, delta: number): void {
    this.handleMovement(delta);
    this.updateEnemies(delta);
  }

  private handleMovement(delta: number): void {
    const speed = 200;
    this.player.setVelocity(0);

    if (this.cursors.left.isDown) this.player.setVelocityX(-speed);
    if (this.cursors.right.isDown) this.player.setVelocityX(speed);
    if (this.cursors.up.isDown) this.player.setVelocityY(-speed);
    if (this.cursors.down.isDown) this.player.setVelocityY(speed);
  }
}
```

### 오브젝트 풀링
```typescript
// 생성 (미리 풀에 넣어둠)
this.bullets = this.physics.add.group({
  classType: Phaser.Physics.Arcade.Sprite,
  maxSize: 30,
  runChildUpdate: true,
  createCallback: (obj) => {
    const bullet = obj as Phaser.Physics.Arcade.Sprite;
    bullet.setActive(false).setVisible(false);
  },
});

// 발사 (풀에서 가져옴)
fireBullet(x: number, y: number, angle: number): void {
  const bullet = this.bullets.get(x, y, 'bullet');
  if (!bullet) return; // 풀 소진
  bullet.setActive(true).setVisible(true);
  this.physics.velocityFromAngle(angle, 400, bullet.body.velocity);
  // 3초 후 회수
  this.time.delayedCall(3000, () => {
    bullet.setActive(false).setVisible(false);
    bullet.body.reset(-100, -100);
  });
}
```

### 에셋 로딩
```typescript
// src/scenes/BootScene.ts
export class BootScene extends Phaser.Scene {
  constructor() { super({ key: 'BootScene' }); }

  preload(): void {
    // 프로그레스 바
    const width = this.cameras.main.width;
    const height = this.cameras.main.height;
    const progressBar = this.add.graphics();
    const progressBox = this.add.graphics();
    progressBox.fillStyle(0x222222, 0.8);
    progressBox.fillRect(width/4, height/2 - 15, width/2, 30);

    this.load.on('progress', (value: number) => {
      progressBar.clear();
      progressBar.fillStyle(0xffffff, 1);
      progressBar.fillRect(width/4 + 5, height/2 - 10, (width/2 - 10) * value, 20);
    });

    this.load.on('complete', () => {
      progressBar.destroy();
      progressBox.destroy();
    });

    // 에셋 로드
    this.load.image('player', 'assets/img/player.png');
    this.load.image('enemy', 'assets/img/enemy.png');
    this.load.image('background', 'assets/img/background.png');
    this.load.spritesheet('player_walk', 'assets/img/player_walk.png', {
      frameWidth: 64, frameHeight: 64,
    });
    // 오디오
    this.load.audio('bgm', 'assets/audio/bgm.mp3');
    this.load.audio('sfx_hit', 'assets/audio/hit.mp3');
  }

  create(): void {
    // 애니메이션 등록
    this.anims.create({
      key: 'walk',
      frames: this.anims.generateFrameNumbers('player_walk', { start: 0, end: 3 }),
      frameRate: 8,
      repeat: -1,
    });

    this.scene.start('MenuScene');
  }
}
```

### 프로시저럴 사운드 (Web Audio / Tone.js 없이)
```typescript
// src/systems/AudioManager.ts
export class AudioManager {
  private scene: Phaser.Scene;

  constructor(scene: Phaser.Scene) {
    this.scene = scene;
  }

  // Web Audio API로 간단한 효과음 생성
  playSynth(type: 'hit' | 'coin' | 'levelup' | 'explosion'): void {
    const ctx = this.scene.sound.context as AudioContext;
    if (!ctx) return;

    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.connect(gain);
    gain.connect(ctx.destination);

    const now = ctx.currentTime;

    switch (type) {
      case 'hit':
        osc.type = 'square';
        osc.frequency.setValueAtTime(200, now);
        osc.frequency.exponentialRampToValueAtTime(50, now + 0.1);
        gain.gain.setValueAtTime(0.3, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.1);
        osc.start(now);
        osc.stop(now + 0.1);
        break;

      case 'coin':
        osc.type = 'sine';
        osc.frequency.setValueAtTime(800, now);
        osc.frequency.setValueAtTime(1200, now + 0.05);
        gain.gain.setValueAtTime(0.2, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.15);
        osc.start(now);
        osc.stop(now + 0.15);
        break;

      case 'levelup':
        osc.type = 'sine';
        osc.frequency.setValueAtTime(400, now);
        osc.frequency.exponentialRampToValueAtTime(800, now + 0.1);
        osc.frequency.exponentialRampToValueAtTime(1200, now + 0.2);
        gain.gain.setValueAtTime(0.3, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.3);
        osc.start(now);
        osc.stop(now + 0.3);
        break;

      case 'explosion':
        const bufferSize = ctx.sampleRate * 0.2;
        const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
        const data = buffer.getChannelData(0);
        for (let i = 0; i < bufferSize; i++) {
          data[i] = (Math.random() * 2 - 1) * (1 - i / bufferSize);
        }
        const noise = ctx.createBufferSource();
        noise.buffer = buffer;
        const noiseGain = ctx.createGain();
        noise.connect(noiseGain);
        noiseGain.connect(ctx.destination);
        noiseGain.gain.setValueAtTime(0.4, now);
        noiseGain.gain.exponentialRampToValueAtTime(0.01, now + 0.2);
        noise.start(now);
        noise.stop(now + 0.2);
        return; // noise doesn't use osc
    }
  }
}
```

### 세이브/로드
```typescript
// src/systems/SaveSystem.ts
interface SaveData {
  playerLevel: number;
  score: number;
  highScore: number;
  coins: number;
  unlockedWeapons: string[];
  settings: { bgmVolume: number; sfxVolume: number; };
  lastPlayed: string;
}

export class SaveSystem {
  private static KEY = 'game_save_data';

  static save(data: SaveData): void {
    data.lastPlayed = new Date().toISOString();
    localStorage.setItem(this.KEY, JSON.stringify(data));
  }

  static load(): SaveData | null {
    const raw = localStorage.getItem(this.KEY);
    if (!raw) return null;
    try { return JSON.parse(raw); }
    catch { return null; }
  }

  static getDefault(): SaveData {
    return {
      playerLevel: 1, score: 0, highScore: 0, coins: 0,
      unlockedWeapons: ['basic'],
      settings: { bgmVolume: 0.7, sfxVolume: 1.0 },
      lastPlayed: new Date().toISOString(),
    };
  }

  static reset(): void {
    localStorage.removeItem(this.KEY);
  }
}
```

### 모바일 터치 조이스틱
```typescript
// 가상 조이스틱 구현
createVirtualJoystick(): void {
  const zone = this.add.zone(150, this.scale.height - 150, 200, 200);
  zone.setInteractive();

  let pointer: Phaser.Input.Pointer | null = null;
  const baseX = 150, baseY = this.scale.height - 150;
  const maxDist = 50;

  const base = this.add.circle(baseX, baseY, 60, 0x333333, 0.5);
  const stick = this.add.circle(baseX, baseY, 25, 0xffffff, 0.8);

  this.input.on('pointerdown', (p: Phaser.Input.Pointer) => {
    if (p.x < this.scale.width / 2) pointer = p;
  });

  this.input.on('pointermove', (p: Phaser.Input.Pointer) => {
    if (pointer && p.id === pointer.id) {
      const dx = p.x - baseX;
      const dy = p.y - baseY;
      const dist = Math.min(Math.sqrt(dx*dx + dy*dy), maxDist);
      const angle = Math.atan2(dy, dx);
      stick.setPosition(baseX + Math.cos(angle) * dist, baseY + Math.sin(angle) * dist);
      // velocity = dist / maxDist
    }
  });

  this.input.on('pointerup', (p: Phaser.Input.Pointer) => {
    if (pointer && p.id === pointer.id) {
      pointer = null;
      stick.setPosition(baseX, baseY);
    }
  });
}
```

---

## 성능 체크리스트
- [ ] 오브젝트 풀링 (적, 발사체, 파티클)
- [ ] 화면 밖 오브젝트 비활성화
- [ ] 텍스처 아틀라스 사용 (개별 이미지 대신)
- [ ] 물리 바디 최소화 (정적 vs 동적)
- [ ] 타이머 기반 스폰 (매 프레임 X)
- [ ] 이벤트 기반 통신 (this.events.emit)
- [ ] 60fps 유지 확인 (this.game.loop.actualFps)
