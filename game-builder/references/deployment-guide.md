# 게임 배포 가이드 v2.0

> 웹, 모바일, 데스크톱, PWA, itch.io, Steam 배포 전략

---

## 1. 웹 배포 (Phaser / HTML5)

### Vercel 배포
```bash
# Vite 프로젝트
npm run build
npx vercel --prod

# vercel.json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite"
}
```

### Netlify 배포
```bash
npm run build
npx netlify deploy --prod --dir=dist
```

### GitHub Pages 배포
```yaml
# .github/workflows/deploy.yml
name: Deploy Game
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm ci && npm run build
      - uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dist
```

---

## 2. PWA (모바일 앱처럼 설치)

### manifest.json
```json
{
  "name": "Game Name",
  "short_name": "Game",
  "start_url": "/",
  "display": "fullscreen",
  "orientation": "landscape",
  "background_color": "#000000",
  "theme_color": "#1a1a2e",
  "icons": [
    { "src": "/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/icon-512.png", "sizes": "512x512", "type": "image/png" }
  ]
}
```

### Service Worker (오프라인 캐싱)
```javascript
// sw.js
const CACHE_NAME = 'game-v1';
const ASSETS = [
  '/', '/index.html', '/assets/img/player.png',
  '/assets/img/enemy.png', '/assets/img/background.png',
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE_NAME).then(c => c.addAll(ASSETS)));
});

self.addEventListener('fetch', e => {
  e.respondWith(
    caches.match(e.request).then(r => r || fetch(e.request))
  );
});
```

---

## 3. 모바일 앱 (Capacitor)

```bash
# Capacitor 설정
npm install @capacitor/core @capacitor/cli
npx cap init "Game Name" com.example.game

# 플랫폼 추가
npx cap add android
npx cap add ios

# 빌드 → 복사 → 열기
npm run build
npx cap copy
npx cap open android  # Android Studio에서 열기
npx cap open ios      # Xcode에서 열기
```

### capacitor.config.ts
```typescript
import { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.example.game',
  appName: 'Game Name',
  webDir: 'dist',
  server: {
    androidScheme: 'https',
  },
  plugins: {
    SplashScreen: {
      launchAutoHide: false,
      showSpinner: true,
    },
  },
};

export default config;
```

---

## 4. 데스크톱 앱 (Electron)

```bash
npm install electron electron-builder --save-dev
```

### electron/main.js
```javascript
const { app, BrowserWindow } = require('electron');
const path = require('path');

function createWindow() {
  const win = new BrowserWindow({
    width: 1280,
    height: 720,
    fullscreen: false,
    autoHideMenuBar: true,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
    },
  });

  // 프로덕션: 빌드된 파일 로드
  win.loadFile(path.join(__dirname, '../dist/index.html'));
}

app.whenReady().then(createWindow);
app.on('window-all-closed', () => { if (process.platform !== 'darwin') app.quit(); });
```

### package.json (electron-builder)
```json
{
  "build": {
    "appId": "com.example.game",
    "productName": "Game Name",
    "directories": { "output": "release" },
    "win": { "target": ["nsis", "portable"], "icon": "assets/icon.ico" },
    "mac": { "target": "dmg", "icon": "assets/icon.icns" },
    "linux": { "target": ["AppImage"], "icon": "assets/icon.png" }
  }
}
```

---

## 5. itch.io 배포

```bash
# Butler CLI 설치
# https://itch.io/docs/butler/

# 웹 게임 업로드
butler push dist/ username/game-name:html5

# Windows 빌드
butler push release/win-unpacked/ username/game-name:windows

# 버전 관리
butler status username/game-name
```

### itch.io 최적화
```html
<!-- index.html에 추가 -->
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
  body { margin: 0; overflow: hidden; background: #000; }
  canvas { display: block; }
</style>
```

---

## 6. CrazyGames / Poki 배포

### CrazyGames SDK 연동
```typescript
// CrazyGames SDK
declare const CrazyGames: any;

class CrazyGamesIntegration {
  private sdk: any;

  async init() {
    this.sdk = await CrazyGames.SDK.init();
  }

  // 게임 시작/종료 알림 (광고 타이밍)
  gameplayStart() { this.sdk.game.gameplayStart(); }
  gameplayStop() { this.sdk.game.gameplayStop(); }

  // 광고 표시
  async showAd(type: 'midgame' | 'rewarded'): Promise<boolean> {
    try {
      await this.sdk.ad.requestAd(type);
      return true;
    } catch { return false; }
  }

  // 리더보드
  async submitScore(score: number) {
    await this.sdk.game.happytime(); // 행복한 순간 (바이럴 캡처)
  }
}
```

---

## 7. 성능 최적화 체크리스트 (배포 전)

```
빌드 최적화:
  □ Tree-shaking 활성화 (Vite 기본 지원)
  □ 에셋 압축 (PNG → WebP, 50-80% 용량 감소)
  □ 오디오 압축 (WAV → OGG/MP3, 90% 감소)
  □ 코드 minification + gzip
  □ 소스맵 제거 (프로덕션)
  □ 미사용 에셋 정리

에셋 최적화:
  □ 스프라이트 아틀라스 (TexturePacker / free-tex-packer)
  □ 이미지 lazy loading
  □ LOD (Level of Detail) 텍스처
  □ 오디오 스프라이트 (여러 효과음 → 1파일)

런타임 최적화:
  □ 오브젝트 풀링 (적, 발사체, 파티클)
  □ 화면 밖 오브젝트 비활성화
  □ requestAnimationFrame 기반 루프
  □ 물리 계산 최적화 (공간 해싱)
  □ GC 최소화 (객체 재사용)
  □ 60fps (데스크톱) / 30fps (모바일) 타겟
```
