# 🎨 게임 에셋 스킬

## 설명
게임에 필요한 에셋(스프라이트, 오디오, UI)을 구성하고 관리합니다.

## 트리거
- "게임 에셋"
- "스프라이트"
- "효과음"
- "BGM"
- "게임 UI"

## 에셋 구조

```
public/assets/
├── sprites/           # 스프라이트
│   ├── player/
│   │   ├── idle.png
│   │   ├── run.png
│   │   └── jump.png
│   ├── enemies/
│   ├── items/
│   └── effects/
├── audio/
│   ├── bgm/           # 배경음악
│   │   ├── menu.mp3
│   │   ├── game.mp3
│   │   └── boss.mp3
│   └── sfx/           # 효과음
│       ├── jump.mp3
│       ├── coin.mp3
│       ├── hit.mp3
│       └── gameover.mp3
├── ui/                # UI 에셋
│   ├── buttons/
│   ├── icons/
│   └── fonts/
└── tilemap/           # 타일맵
    ├── tileset.png
    └── level1.json
```

## 무료 에셋 소스

### 스프라이트
| 사이트 | URL | 특징 |
|--------|-----|------|
| Kenney | kenney.nl/assets | 고품질, 일관된 스타일 |
| OpenGameArt | opengameart.org | 다양한 스타일 |
| itch.io | itch.io/game-assets | 인디 아티스트 |

### 오디오
| 사이트 | URL | 특징 |
|--------|-----|------|
| Freesound | freesound.org | 효과음 |
| Incompetech | incompetech.com | BGM (Kevin MacLeod) |
| OpenGameArt | opengameart.org | 게임 특화 |

### 폰트
| 사이트 | URL | 특징 |
|--------|-----|------|
| Google Fonts | fonts.google.com | 웹폰트 |
| DaFont | dafont.com | 게임 폰트 |

## 에셋 로딩 코드 (Phaser)

```typescript
// scenes/BootScene.ts
export class BootScene extends Phaser.Scene {
  constructor() {
    super({ key: 'BootScene' });
  }
  
  preload() {
    // 로딩 바
    const progressBar = this.add.graphics();
    this.load.on('progress', (value: number) => {
      progressBar.clear();
      progressBar.fillStyle(0x6366f1, 1);
      progressBar.fillRect(100, 280, 600 * value, 30);
    });
    
    // 스프라이트
    this.load.spritesheet('player', '/assets/sprites/player.png', {
      frameWidth: 32,
      frameHeight: 32,
    });
    this.load.image('background', '/assets/sprites/background.png');
    this.load.image('platform', '/assets/sprites/platform.png');
    
    // 오디오
    this.load.audio('bgm', '/assets/audio/bgm/game.mp3');
    this.load.audio('jump', '/assets/audio/sfx/jump.mp3');
    this.load.audio('coin', '/assets/audio/sfx/coin.mp3');
    this.load.audio('hit', '/assets/audio/sfx/hit.mp3');
    
    // 타일맵
    this.load.tilemapTiledJSON('level1', '/assets/tilemap/level1.json');
    this.load.image('tiles', '/assets/tilemap/tileset.png');
  }
  
  create() {
    this.scene.start('MenuScene');
  }
}
```

## 스프라이트 시트 애니메이션

```typescript
// 애니메이션 정의
this.anims.create({
  key: 'player-idle',
  frames: this.anims.generateFrameNumbers('player', { start: 0, end: 3 }),
  frameRate: 8,
  repeat: -1,
});

this.anims.create({
  key: 'player-run',
  frames: this.anims.generateFrameNumbers('player', { start: 4, end: 11 }),
  frameRate: 12,
  repeat: -1,
});

this.anims.create({
  key: 'player-jump',
  frames: this.anims.generateFrameNumbers('player', { start: 12, end: 14 }),
  frameRate: 6,
  repeat: 0,
});
```

## 오디오 설정

```typescript
// src/game/systems/AudioSystem.ts
export class AudioSystem {
  private scene: Phaser.Scene;
  private bgm: Phaser.Sound.BaseSound | null = null;
  
  constructor(scene: Phaser.Scene) {
    this.scene = scene;
  }
  
  playBGM(key: string, volume: number = 0.3) {
    if (this.bgm) this.bgm.stop();
    this.bgm = this.scene.sound.add(key, { volume, loop: true });
    this.bgm.play();
  }
  
  playSFX(key: string, volume: number = 0.7) {
    this.scene.sound.play(key, { volume });
  }
  
  stopBGM() {
    if (this.bgm) {
      this.bgm.stop();
      this.bgm = null;
    }
  }
  
  setMute(muted: boolean) {
    this.scene.sound.mute = muted;
  }
}
```

## 체크리스트

- [ ] 스프라이트 시트 준비
- [ ] 애니메이션 정의
- [ ] BGM 파일 추가
- [ ] 효과음 파일 추가
- [ ] 로딩 화면 구현
- [ ] 에셋 프리로드
- [ ] 오디오 볼륨 조절
- [ ] 음소거 기능
