---
description: 웹 게임 개발. "게임 개발", "Phaser", "PixiJS", "Three.js", "게임", "2D 게임", "3D 게임" 트리거.
---

# 웹 게임 개발

## Phaser 3 (2D 게임)

### 설치 및 설정
```bash
npm create vite@latest my-game -- --template vanilla-ts
cd my-game
npm install phaser
```

### 기본 게임 구조
```typescript
// src/main.ts
import Phaser from 'phaser';
import { BootScene } from './scenes/BootScene';
import { GameScene } from './scenes/GameScene';
import { UIScene } from './scenes/UIScene';

const config: Phaser.Types.Core.GameConfig = {
  type: Phaser.AUTO,
  width: 800,
  height: 600,
  parent: 'game-container',
  physics: {
    default: 'arcade',
    arcade: {
      gravity: { y: 300, x: 0 },
      debug: false
    }
  },
  scene: [BootScene, GameScene, UIScene]
};

new Phaser.Game(config);
```

### 씬 구현
```typescript
// src/scenes/GameScene.ts
import Phaser from 'phaser';

export class GameScene extends Phaser.Scene {
  private player!: Phaser.Physics.Arcade.Sprite;
  private cursors!: Phaser.Types.Input.Keyboard.CursorKeys;
  private score = 0;
  private scoreText!: Phaser.GameObjects.Text;
  private coins!: Phaser.Physics.Arcade.Group;

  constructor() {
    super({ key: 'GameScene' });
  }

  preload() {
    this.load.image('sky', 'assets/sky.png');
    this.load.image('ground', 'assets/platform.png');
    this.load.image('coin', 'assets/coin.png');
    this.load.spritesheet('player', 'assets/player.png', {
      frameWidth: 32,
      frameHeight: 48
    });
  }

  create() {
    // 배경
    this.add.image(400, 300, 'sky');

    // 플랫폼
    const platforms = this.physics.add.staticGroup();
    platforms.create(400, 568, 'ground').setScale(2).refreshBody();

    // 플레이어
    this.player = this.physics.add.sprite(100, 450, 'player');
    this.player.setBounce(0.2);
    this.player.setCollideWorldBounds(true);

    // 애니메이션
    this.anims.create({
      key: 'left',
      frames: this.anims.generateFrameNumbers('player', { start: 0, end: 3 }),
      frameRate: 10,
      repeat: -1
    });

    this.anims.create({
      key: 'idle',
      frames: [{ key: 'player', frame: 4 }],
      frameRate: 20
    });

    this.anims.create({
      key: 'right',
      frames: this.anims.generateFrameNumbers('player', { start: 5, end: 8 }),
      frameRate: 10,
      repeat: -1
    });

    // 충돌
    this.physics.add.collider(this.player, platforms);

    // 코인
    this.coins = this.physics.add.group({
      key: 'coin',
      repeat: 11,
      setXY: { x: 12, y: 0, stepX: 70 }
    });

    this.coins.children.iterate((child) => {
      const coin = child as Phaser.Physics.Arcade.Sprite;
      coin.setBounceY(Phaser.Math.FloatBetween(0.4, 0.8));
      return true;
    });

    this.physics.add.collider(this.coins, platforms);
    this.physics.add.overlap(this.player, this.coins, this.collectCoin, undefined, this);

    // 점수 UI
    this.scoreText = this.add.text(16, 16, 'Score: 0', {
      fontSize: '32px',
      color: '#000'
    });

    // 입력
    this.cursors = this.input.keyboard!.createCursorKeys();
  }

  update() {
    if (this.cursors.left.isDown) {
      this.player.setVelocityX(-160);
      this.player.anims.play('left', true);
    } else if (this.cursors.right.isDown) {
      this.player.setVelocityX(160);
      this.player.anims.play('right', true);
    } else {
      this.player.setVelocityX(0);
      this.player.anims.play('idle');
    }

    if (this.cursors.up.isDown && this.player.body!.touching.down) {
      this.player.setVelocityY(-330);
    }
  }

  private collectCoin(
    player: Phaser.Types.Physics.Arcade.GameObjectWithBody,
    coin: Phaser.Types.Physics.Arcade.GameObjectWithBody
  ) {
    (coin as Phaser.Physics.Arcade.Sprite).disableBody(true, true);
    this.score += 10;
    this.scoreText.setText('Score: ' + this.score);

    // 모든 코인 수집 시
    if (this.coins.countActive(true) === 0) {
      this.coins.children.iterate((child) => {
        const c = child as Phaser.Physics.Arcade.Sprite;
        c.enableBody(true, c.x, 0, true, true);
        return true;
      });
    }
  }
}
```

## Three.js (3D 게임)

### 기본 설정
```typescript
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';

class Game {
  private scene: THREE.Scene;
  private camera: THREE.PerspectiveCamera;
  private renderer: THREE.WebGLRenderer;
  private controls: OrbitControls;

  constructor() {
    // 씬
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0x87ceeb);

    // 카메라
    this.camera = new THREE.PerspectiveCamera(
      75,
      window.innerWidth / window.innerHeight,
      0.1,
      1000
    );
    this.camera.position.set(0, 5, 10);

    // 렌더러
    this.renderer = new THREE.WebGLRenderer({ antialias: true });
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.renderer.shadowMap.enabled = true;
    document.body.appendChild(this.renderer.domElement);

    // 컨트롤
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);

    // 조명
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    this.scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
    directionalLight.position.set(5, 10, 5);
    directionalLight.castShadow = true;
    this.scene.add(directionalLight);

    // 바닥
    const groundGeometry = new THREE.PlaneGeometry(20, 20);
    const groundMaterial = new THREE.MeshStandardMaterial({ color: 0x228b22 });
    const ground = new THREE.Mesh(groundGeometry, groundMaterial);
    ground.rotation.x = -Math.PI / 2;
    ground.receiveShadow = true;
    this.scene.add(ground);

    // 플레이어 (큐브)
    const playerGeometry = new THREE.BoxGeometry(1, 1, 1);
    const playerMaterial = new THREE.MeshStandardMaterial({ color: 0xff0000 });
    const player = new THREE.Mesh(playerGeometry, playerMaterial);
    player.position.y = 0.5;
    player.castShadow = true;
    this.scene.add(player);

    // 리사이즈
    window.addEventListener('resize', () => {
      this.camera.aspect = window.innerWidth / window.innerHeight;
      this.camera.updateProjectionMatrix();
      this.renderer.setSize(window.innerWidth, window.innerHeight);
    });

    this.animate();
  }

  private animate = () => {
    requestAnimationFrame(this.animate);
    this.controls.update();
    this.renderer.render(this.scene, this.camera);
  };
}

new Game();
```

## 게임 시스템

### 상태 관리
```typescript
// src/systems/GameState.ts
interface GameState {
  score: number;
  level: number;
  lives: number;
  isPlaying: boolean;
  isPaused: boolean;
}

class GameStateManager {
  private state: GameState = {
    score: 0,
    level: 1,
    lives: 3,
    isPlaying: false,
    isPaused: false
  };

  private listeners: Set<(state: GameState) => void> = new Set();

  getState(): Readonly<GameState> {
    return { ...this.state };
  }

  setState(partial: Partial<GameState>) {
    this.state = { ...this.state, ...partial };
    this.notify();
  }

  subscribe(listener: (state: GameState) => void) {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  private notify() {
    this.listeners.forEach(listener => listener(this.state));
  }

  addScore(points: number) {
    this.setState({ score: this.state.score + points });
  }

  loseLife() {
    const newLives = this.state.lives - 1;
    this.setState({ lives: newLives });
    if (newLives <= 0) {
      this.gameOver();
    }
  }

  private gameOver() {
    this.setState({ isPlaying: false });
    // 게임 오버 이벤트 발생
  }
}

export const gameState = new GameStateManager();
```

### 오디오 시스템
```typescript
// src/systems/AudioManager.ts
class AudioManager {
  private sounds: Map<string, HTMLAudioElement> = new Map();
  private bgm: HTMLAudioElement | null = null;
  private sfxVolume = 1;
  private bgmVolume = 0.5;

  preload(key: string, src: string): Promise<void> {
    return new Promise((resolve, reject) => {
      const audio = new Audio(src);
      audio.addEventListener('canplaythrough', () => {
        this.sounds.set(key, audio);
        resolve();
      });
      audio.addEventListener('error', reject);
    });
  }

  playSFX(key: string) {
    const sound = this.sounds.get(key);
    if (sound) {
      const clone = sound.cloneNode() as HTMLAudioElement;
      clone.volume = this.sfxVolume;
      clone.play();
    }
  }

  playBGM(key: string, loop = true) {
    this.stopBGM();
    const sound = this.sounds.get(key);
    if (sound) {
      this.bgm = sound;
      this.bgm.loop = loop;
      this.bgm.volume = this.bgmVolume;
      this.bgm.play();
    }
  }

  stopBGM() {
    if (this.bgm) {
      this.bgm.pause();
      this.bgm.currentTime = 0;
    }
  }

  setVolume(sfx: number, bgm: number) {
    this.sfxVolume = Math.max(0, Math.min(1, sfx));
    this.bgmVolume = Math.max(0, Math.min(1, bgm));
    if (this.bgm) this.bgm.volume = this.bgmVolume;
  }
}

export const audioManager = new AudioManager();
```

### 입력 시스템
```typescript
// src/systems/InputManager.ts
type InputAction = 'left' | 'right' | 'jump' | 'attack' | 'pause';

class InputManager {
  private keyMap: Map<string, InputAction> = new Map([
    ['ArrowLeft', 'left'],
    ['KeyA', 'left'],
    ['ArrowRight', 'right'],
    ['KeyD', 'right'],
    ['Space', 'jump'],
    ['ArrowUp', 'jump'],
    ['KeyZ', 'attack'],
    ['Escape', 'pause']
  ]);

  private activeActions: Set<InputAction> = new Set();
  private justPressed: Set<InputAction> = new Set();

  constructor() {
    window.addEventListener('keydown', (e) => {
      const action = this.keyMap.get(e.code);
      if (action && !this.activeActions.has(action)) {
        this.activeActions.add(action);
        this.justPressed.add(action);
      }
    });

    window.addEventListener('keyup', (e) => {
      const action = this.keyMap.get(e.code);
      if (action) {
        this.activeActions.delete(action);
      }
    });
  }

  isPressed(action: InputAction): boolean {
    return this.activeActions.has(action);
  }

  isJustPressed(action: InputAction): boolean {
    return this.justPressed.has(action);
  }

  update() {
    this.justPressed.clear();
  }
}

export const inputManager = new InputManager();
```

## 빌드 및 배포
```bash
# Vite 빌드
npm run build

# GitHub Pages 배포
npm install gh-pages --save-dev
# package.json scripts에 추가: "deploy": "gh-pages -d dist"
npm run deploy
```

$ARGUMENTS
