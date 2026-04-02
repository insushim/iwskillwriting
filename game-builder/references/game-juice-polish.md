# 게임 주스 & 폴리시 가이드 v3.0

> 게임을 "느낌 좋게" 만드는 핵심 기법. 같은 게임이라도 주스가 있으면 10배 재밌어짐.

---

## 1. 카메라 셰이크 (피격/폭발)

```typescript
class ScreenEffects {
  private scene: Phaser.Scene;

  constructor(scene: Phaser.Scene) { this.scene = scene; }

  // 강도별 셰이크
  shake(intensity: 'light' | 'medium' | 'heavy' | 'extreme' = 'medium') {
    const config = {
      light:   { duration: 50,  intensity: 0.003 },
      medium:  { duration: 100, intensity: 0.008 },
      heavy:   { duration: 200, intensity: 0.015 },
      extreme: { duration: 400, intensity: 0.025 },
    };
    const { duration, intensity: i } = config[intensity];
    this.scene.cameras.main.shake(duration, i);
  }

  // 화면 플래시 (피격)
  flash(color: number = 0xffffff, duration: number = 100) {
    this.scene.cameras.main.flash(duration, (color >> 16) & 0xff, (color >> 8) & 0xff, color & 0xff);
  }

  // 히트스톱 (프레임 멈춤 — 타격감의 핵심)
  hitStop(duration: number = 50) {
    this.scene.physics.world.pause();
    this.scene.time.delayedCall(duration, () => this.scene.physics.world.resume());
  }

  // 슬로모션 (보스 킬, 마지막 적 처치)
  slowMotion(duration: number = 1000, timeScale: number = 0.3) {
    this.scene.time.timeScale = timeScale;
    this.scene.physics.world.timeScale = 1 / timeScale;
    this.scene.time.delayedCall(duration * timeScale, () => {
      this.scene.time.timeScale = 1;
      this.scene.physics.world.timeScale = 1;
    });
  }

  // 줌 펀치 (강한 공격)
  zoomPunch(intensity: number = 1.05, duration: number = 100) {
    const cam = this.scene.cameras.main;
    const originalZoom = cam.zoom;
    this.scene.tweens.add({
      targets: cam, zoom: originalZoom * intensity,
      duration: duration / 2, yoyo: true, ease: 'Quad.easeOut',
    });
  }

  // 크로매틱 어버레이션 (대시/속도감)
  chromaticAberration(sprite: Phaser.GameObjects.Sprite, offset: number = 3) {
    const r = this.scene.add.sprite(sprite.x + offset, sprite.y, sprite.texture.key).setTint(0xff0000).setAlpha(0.3);
    const b = this.scene.add.sprite(sprite.x - offset, sprite.y, sprite.texture.key).setTint(0x0000ff).setAlpha(0.3);
    this.scene.time.delayedCall(50, () => { r.destroy(); b.destroy(); });
  }
}
```

---

## 2. 스쿼시 & 스트레치 (생동감)

```typescript
class SpriteJuice {
  // 점프 시 스쿼시 & 스트레치
  static jumpSquash(sprite: Phaser.GameObjects.Sprite, scene: Phaser.Scene) {
    scene.tweens.add({
      targets: sprite,
      scaleX: 1.3, scaleY: 0.7,
      duration: 80, yoyo: true, ease: 'Quad.easeOut',
    });
  }

  // 착지 시 납작해짐
  static landSquash(sprite: Phaser.GameObjects.Sprite, scene: Phaser.Scene) {
    scene.tweens.add({
      targets: sprite,
      scaleX: 1.4, scaleY: 0.6,
      duration: 60, yoyo: true, ease: 'Bounce.easeOut',
    });
  }

  // 피격 시 깜빡임
  static hitFlash(sprite: Phaser.GameObjects.Sprite, scene: Phaser.Scene) {
    sprite.setTintFill(0xffffff);
    scene.time.delayedCall(60, () => sprite.clearTint());
  }

  // 피격 시 넉백
  static knockback(sprite: Phaser.Physics.Arcade.Sprite, fromX: number, fromY: number, force: number = 300) {
    const angle = Math.atan2(sprite.y - fromY, sprite.x - fromX);
    sprite.setVelocity(Math.cos(angle) * force, Math.sin(angle) * force);
  }

  // 사망 시 연출
  static deathEffect(sprite: Phaser.GameObjects.Sprite, scene: Phaser.Scene) {
    scene.tweens.add({
      targets: sprite,
      alpha: 0, scaleX: 1.5, scaleY: 1.5, angle: 360,
      duration: 300, ease: 'Quad.easeOut',
      onComplete: () => sprite.destroy(),
    });
  }

  // 아이템 획득 시 빨려 들어감
  static magnetPickup(item: Phaser.GameObjects.Sprite, target: Phaser.GameObjects.Sprite, scene: Phaser.Scene) {
    scene.tweens.add({
      targets: item,
      x: target.x, y: target.y, scale: 0, alpha: 0,
      duration: 200, ease: 'Quad.easeIn',
      onComplete: () => item.destroy(),
    });
  }

  // 등장 애니메이션 (팝인)
  static popIn(obj: Phaser.GameObjects.GameObject & { setScale: Function }, scene: Phaser.Scene) {
    obj.setScale(0);
    scene.tweens.add({
      targets: obj, scaleX: 1, scaleY: 1,
      duration: 300, ease: 'Back.easeOut',
    });
  }
}
```

---

## 3. 데미지 넘버 (시각적 피드백)

```typescript
class DamageNumbers {
  static show(scene: Phaser.Scene, x: number, y: number, amount: number, isCrit: boolean = false) {
    const color = isCrit ? '#ffff00' : amount > 0 ? '#ff4444' : '#44ff44';
    const size = isCrit ? 28 : 20;
    const prefix = isCrit ? '!' : '';

    const text = scene.add.text(x, y, `${prefix}${Math.abs(amount)}`, {
      fontSize: `${size}px`,
      fontFamily: 'Arial Black',
      color,
      stroke: '#000000',
      strokeThickness: 3,
    }).setOrigin(0.5);

    // 위로 떠오르면서 사라짐
    scene.tweens.add({
      targets: text,
      y: y - 60 - Math.random() * 20,
      x: x + (Math.random() - 0.5) * 40,
      alpha: 0,
      scale: isCrit ? 1.5 : 1.0,
      duration: 800,
      ease: 'Quad.easeOut',
      onComplete: () => text.destroy(),
    });

    // 크리티컬이면 잠깐 커졌다 작아짐
    if (isCrit) {
      text.setScale(0.5);
      scene.tweens.add({
        targets: text, scale: 1.5,
        duration: 150, ease: 'Back.easeOut',
      });
    }
  }

  // 콤보 카운터
  static showCombo(scene: Phaser.Scene, x: number, y: number, combo: number) {
    if (combo < 3) return;
    const text = scene.add.text(x, y - 40, `${combo} COMBO!`, {
      fontSize: '24px', fontFamily: 'Arial Black',
      color: combo >= 10 ? '#ff00ff' : combo >= 5 ? '#ffaa00' : '#ffffff',
      stroke: '#000000', strokeThickness: 4,
    }).setOrigin(0.5).setScale(0);

    scene.tweens.add({
      targets: text, scale: 1.2, duration: 200, ease: 'Back.easeOut', yoyo: true,
      hold: 300,
      onComplete: () => {
        scene.tweens.add({ targets: text, alpha: 0, y: y - 80, duration: 300, onComplete: () => text.destroy() });
      },
    });
  }
}
```

---

## 4. UI 폴리시

```typescript
class UIJuice {
  // 버튼 호버/프레스 효과
  static makeInteractive(button: Phaser.GameObjects.Image | Phaser.GameObjects.Text, scene: Phaser.Scene, onClick: () => void) {
    button.setInteractive({ useHandCursor: true });

    button.on('pointerover', () => {
      scene.tweens.add({ targets: button, scale: 1.1, duration: 100, ease: 'Quad.easeOut' });
      button.setTint(0xdddddd);
    });

    button.on('pointerout', () => {
      scene.tweens.add({ targets: button, scale: 1.0, duration: 100, ease: 'Quad.easeOut' });
      button.clearTint();
    });

    button.on('pointerdown', () => {
      scene.tweens.add({ targets: button, scale: 0.95, duration: 50, ease: 'Quad.easeIn' });
    });

    button.on('pointerup', () => {
      scene.tweens.add({ targets: button, scale: 1.1, duration: 100, ease: 'Back.easeOut' });
      onClick();
    });
  }

  // HP 바 스무스 감소
  static smoothBar(scene: Phaser.Scene, bar: Phaser.GameObjects.Graphics,
    x: number, y: number, w: number, h: number,
    current: number, max: number, color: number = 0x44ff44) {

    const ratio = Math.max(0, current / max);
    bar.clear();

    // 배경
    bar.fillStyle(0x222222, 0.8);
    bar.fillRect(x, y, w, h);

    // 빨간색 지연 바 (데미지 시각화)
    bar.fillStyle(0xff4444, 0.6);
    bar.fillRect(x, y, w * ratio + 10, h); // 살짝 더 넓게

    // 실제 HP 바
    const barColor = ratio > 0.5 ? 0x44ff44 : ratio > 0.25 ? 0xffaa00 : 0xff4444;
    bar.fillStyle(barColor);
    bar.fillRect(x, y, w * ratio, h);

    // 테두리
    bar.lineStyle(1, 0xffffff, 0.5);
    bar.strokeRect(x, y, w, h);
  }

  // 토스트 알림
  static toast(scene: Phaser.Scene, message: string, icon?: string) {
    const y = scene.scale.height - 80;
    const bg = scene.add.rectangle(scene.scale.width / 2, y + 50, 300, 40, 0x000000, 0.8)
      .setDepth(1000);
    const text = scene.add.text(scene.scale.width / 2, y + 50, `${icon || ''} ${message}`, {
      fontSize: '16px', color: '#ffffff',
    }).setOrigin(0.5).setDepth(1001);

    // 아래에서 위로 슬라이드
    scene.tweens.add({
      targets: [bg, text], y: y,
      duration: 300, ease: 'Back.easeOut',
    });

    // 2초 후 사라짐
    scene.time.delayedCall(2000, () => {
      scene.tweens.add({
        targets: [bg, text], alpha: 0, y: y - 20,
        duration: 200, onComplete: () => { bg.destroy(); text.destroy(); },
      });
    });
  }
}
```

---

## 5. 파티클 프리셋

```typescript
class GameParticles {
  static explosion(scene: Phaser.Scene, x: number, y: number) {
    const emitter = scene.add.particles(x, y, 'particle', {
      speed: { min: 100, max: 300 },
      scale: { start: 1, end: 0 },
      alpha: { start: 1, end: 0 },
      lifespan: 400,
      quantity: 20,
      tint: [0xff4444, 0xff8800, 0xffff00],
      emitting: false,
    });
    emitter.explode(20);
    scene.time.delayedCall(500, () => emitter.destroy());
  }

  static coinPickup(scene: Phaser.Scene, x: number, y: number) {
    const emitter = scene.add.particles(x, y, 'particle', {
      speed: { min: 50, max: 150 },
      scale: { start: 0.5, end: 0 },
      lifespan: 300,
      quantity: 8,
      tint: [0xffdd00, 0xffaa00],
      gravityY: -100,
      emitting: false,
    });
    emitter.explode(8);
    scene.time.delayedCall(400, () => emitter.destroy());
  }

  static levelUp(scene: Phaser.Scene, x: number, y: number) {
    const emitter = scene.add.particles(x, y, 'particle', {
      speed: { min: 80, max: 200 },
      scale: { start: 0.8, end: 0 },
      lifespan: 800,
      quantity: 30,
      tint: [0xffff00, 0x00ff00, 0xffffff],
      angle: { min: 0, max: 360 },
      emitting: false,
    });
    emitter.explode(30);
    scene.time.delayedCall(1000, () => emitter.destroy());
  }

  static heal(scene: Phaser.Scene, x: number, y: number) {
    const emitter = scene.add.particles(x, y, 'particle', {
      speed: { min: 30, max: 80 },
      scale: { start: 0.6, end: 0 },
      lifespan: 600,
      quantity: 12,
      tint: [0x00ff88, 0x88ffbb],
      gravityY: -150,
      emitting: false,
    });
    emitter.explode(12);
    scene.time.delayedCall(700, () => emitter.destroy());
  }

  // 프로시저럴 파티클 텍스처 생성 (에셋 없이)
  static createParticleTexture(scene: Phaser.Scene, key: string = 'particle', size: number = 8) {
    const g = scene.make.graphics({ add: false });
    g.fillStyle(0xffffff);
    g.fillCircle(size / 2, size / 2, size / 2);
    g.generateTexture(key, size, size);
    g.destroy();
  }
}
```

---

## 6. 이벤트 트리거 가이드

```
이벤트              → 적용할 주스
────────────────────────────────────────
적 피격             → hitFlash + knockback + shake(light) + 데미지넘버 + hit SFX
적 처치             → deathEffect + explosion파티클 + shake(medium) + coin파티클 + kill SFX
플레이어 피격       → flash(red) + shake(heavy) + hitStop(80ms) + playerHit SFX
플레이어 사망       → slowMotion + shake(extreme) + 화면 어두워짐 + gameOver SFX
레벨업              → levelUp파티클 + zoomPunch + toast("Level Up!") + levelUp SFX
아이템 획득         → magnetPickup + coinPickup파티클 + coin SFX
보스 등장           → slowMotion + shake(heavy) + 화면 어두워짐 + boss SFX
보스 처치           → slowMotion(2초) + explosion(대형) + 화면 밝아짐 + victory SFX
웨이브 시작         → toast("Wave N") + warning SFX
웨이브 클리어       → toast("Wave Clear!") + 짧은 슬로모 + clear SFX
크리티컬 히트       → hitStop(100ms) + zoomPunch + 크리티컬 데미지넘버 + crit SFX
콤보 3+             → showCombo + 콤보별 SFX 피치 증가
UI 버튼 호버        → scale 1.1 + hover SFX
UI 버튼 클릭        → scale 0.95→1.1 + click SFX
```
