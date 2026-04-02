# 접근성 & 국제화 가이드

---

## 1. 접근성 (Accessibility)

### 색각이상 (색맹) 지원
```typescript
class ColorblindFilter {
  static MODES = {
    normal: { name: '기본', matrix: null },
    deuteranopia: {
      name: '적록색맹 (제2형)',
      matrix: [0.625, 0.375, 0, 0, 0, 0.7, 0.3, 0, 0, 0, 0, 0.3, 0.7, 0, 0, 0, 0, 0, 1, 0]
    },
    protanopia: {
      name: '적록색맹 (제1형)',
      matrix: [0.567, 0.433, 0, 0, 0, 0.558, 0.442, 0, 0, 0, 0, 0.242, 0.758, 0, 0, 0, 0, 0, 1, 0]
    },
    tritanopia: {
      name: '청황색맹',
      matrix: [0.95, 0.05, 0, 0, 0, 0, 0.433, 0.567, 0, 0, 0, 0.475, 0.525, 0, 0, 0, 0, 0, 1, 0]
    },
  };

  // Phaser에서 적용
  static apply(scene: Phaser.Scene, mode: string): void {
    const config = this.MODES[mode];
    if (!config?.matrix) {
      scene.cameras.main.resetPostPipeline();
      return;
    }
    // WebGL ColorMatrix 필터 적용
    scene.cameras.main.setPostPipeline('ColorMatrix');
  }

  // 색상 대신 패턴/아이콘으로 구분
  static safeColors = {
    danger: { color: '#ff4444', icon: '⚠', pattern: 'diagonal' },
    safe: { color: '#44ff44', icon: '✓', pattern: 'dots' },
    neutral: { color: '#4444ff', icon: '○', pattern: 'solid' },
    special: { color: '#ffff44', icon: '★', pattern: 'cross' },
  };
}
```

### 텍스트 크기 조절
```typescript
class TextScaling {
  static SCALES = {
    small: 0.8,
    normal: 1.0,
    large: 1.3,
    xlarge: 1.6,
    xxlarge: 2.0,
  };

  private scale: number = 1.0;

  setScale(preset: keyof typeof TextScaling.SCALES): void {
    this.scale = TextScaling.SCALES[preset];
    // 모든 텍스트 오브젝트 업데이트
    this.updateAllText();
  }

  createText(scene: Phaser.Scene, x: number, y: number, text: string, baseSize: number = 16): Phaser.GameObjects.Text {
    return scene.add.text(x, y, text, {
      fontSize: `${Math.round(baseSize * this.scale)}px`,
      fontFamily: 'sans-serif',
    });
  }
}
```

### 키 리매핑
```typescript
class InputRemapper {
  private bindings: Map<string, string> = new Map([
    ['move_up', 'KeyW'],
    ['move_down', 'KeyS'],
    ['move_left', 'KeyA'],
    ['move_right', 'KeyD'],
    ['attack', 'Space'],
    ['pause', 'Escape'],
    ['interact', 'KeyE'],
  ]);

  rebind(action: string, newKey: string): void {
    this.bindings.set(action, newKey);
    this.save();
  }

  isPressed(action: string, keyboard: Phaser.Input.Keyboard.KeyboardPlugin): boolean {
    const key = this.bindings.get(action);
    if (!key) return false;
    return keyboard.addKey(key).isDown;
  }

  save(): void {
    localStorage.setItem('keybindings', JSON.stringify(Object.fromEntries(this.bindings)));
  }

  load(): void {
    const saved = localStorage.getItem('keybindings');
    if (saved) {
      const data = JSON.parse(saved);
      for (const [action, key] of Object.entries(data)) {
        this.bindings.set(action, key as string);
      }
    }
  }
}
```

### 난이도 옵션
```typescript
interface DifficultyOptions {
  // 전투
  damageMultiplier: number;      // 받는 데미지 배율
  enemyHpMultiplier: number;     // 적 HP 배율
  enemySpeedMultiplier: number;  // 적 속도 배율

  // 보조 기능
  autoAim: boolean;              // 자동 조준
  slowMotion: boolean;           // 슬로우 모션 (50% 속도)
  invincibilityFrames: number;   // 무적 프레임 (초)

  // 시각적
  damageNumbers: boolean;        // 데미지 숫자 표시
  healthBarsOnEnemies: boolean;  // 적 HP바 표시
  minimapEnabled: boolean;       // 미니맵

  // 교육 게임 전용
  hintDelay: number;             // 힌트 표시까지 대기 시간 (초)
  wrongAnswerPenalty: number;    // 오답 패널티 (HP 감소량)
  timeLimit: number;             // 문제 제한 시간 (0 = 무제한)
}

const DIFFICULTY_PRESETS: Record<string, DifficultyOptions> = {
  story: {
    damageMultiplier: 0.5, enemyHpMultiplier: 0.5, enemySpeedMultiplier: 0.7,
    autoAim: true, slowMotion: false, invincibilityFrames: 1.0,
    damageNumbers: true, healthBarsOnEnemies: true, minimapEnabled: true,
    hintDelay: 5, wrongAnswerPenalty: 0, timeLimit: 0,
  },
  normal: {
    damageMultiplier: 1.0, enemyHpMultiplier: 1.0, enemySpeedMultiplier: 1.0,
    autoAim: false, slowMotion: false, invincibilityFrames: 0.5,
    damageNumbers: true, healthBarsOnEnemies: true, minimapEnabled: true,
    hintDelay: 15, wrongAnswerPenalty: 5, timeLimit: 30,
  },
  hard: {
    damageMultiplier: 1.5, enemyHpMultiplier: 1.5, enemySpeedMultiplier: 1.2,
    autoAim: false, slowMotion: false, invincibilityFrames: 0.2,
    damageNumbers: false, healthBarsOnEnemies: false, minimapEnabled: false,
    hintDelay: 0, wrongAnswerPenalty: 15, timeLimit: 15,
  },
};
```

---

## 2. 국제화 (i18n)

### 간단한 i18n 시스템
```typescript
class I18n {
  private locale: string = 'ko';
  private translations: Record<string, Record<string, string>> = {};

  constructor() {
    this.translations = {
      ko: {
        'menu.play': '시작',
        'menu.settings': '설정',
        'menu.quit': '종료',
        'game.score': '점수',
        'game.wave': '웨이브',
        'game.hp': '체력',
        'game.coins': '코인',
        'game.pause': '일시정지',
        'game.resume': '계속하기',
        'game.retry': '다시하기',
        'game.gameover': '게임 오버',
        'game.victory': '승리!',
        'upgrade.choose': '업그레이드를 선택하세요',
        'upgrade.reroll': '다시 뽑기',
      },
      en: {
        'menu.play': 'Play',
        'menu.settings': 'Settings',
        'menu.quit': 'Quit',
        'game.score': 'Score',
        'game.wave': 'Wave',
        'game.hp': 'HP',
        'game.coins': 'Coins',
        'game.pause': 'Paused',
        'game.resume': 'Resume',
        'game.retry': 'Retry',
        'game.gameover': 'Game Over',
        'game.victory': 'Victory!',
        'upgrade.choose': 'Choose an upgrade',
        'upgrade.reroll': 'Reroll',
      },
      ja: {
        'menu.play': 'スタート',
        'menu.settings': '設定',
        'menu.quit': '終了',
        'game.score': 'スコア',
        'game.wave': 'ウェーブ',
        'game.hp': 'HP',
        'game.coins': 'コイン',
        'game.pause': 'ポーズ',
        'game.resume': '続ける',
        'game.retry': 'リトライ',
        'game.gameover': 'ゲームオーバー',
        'game.victory': '勝利！',
        'upgrade.choose': 'アップグレードを選択',
        'upgrade.reroll': 'リロール',
      },
    };
  }

  setLocale(locale: string): void {
    this.locale = locale;
    localStorage.setItem('locale', locale);
  }

  t(key: string, params?: Record<string, string | number>): string {
    let text = this.translations[this.locale]?.[key]
            || this.translations['en']?.[key]
            || key;

    if (params) {
      for (const [k, v] of Object.entries(params)) {
        text = text.replace(`{${k}}`, String(v));
      }
    }
    return text;
  }

  // CJK 폰트 자동 선택
  getFont(): string {
    const fonts: Record<string, string> = {
      ko: '"Noto Sans KR", "Malgun Gothic", sans-serif',
      ja: '"Noto Sans JP", "Meiryo", sans-serif',
      zh: '"Noto Sans SC", "Microsoft YaHei", sans-serif',
      en: '"Inter", "Arial", sans-serif',
    };
    return fonts[this.locale] || fonts.en;
  }
}

// 사용
const i18n = new I18n();
const text = i18n.t('game.score'); // "점수"
```
