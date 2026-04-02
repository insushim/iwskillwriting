# 소셜 & 참여 시스템 가이드 v3.0

> 업적, 데일리 리워드, 튜토리얼, 스크린샷 공유, 레벨 에디터

---

## 1. 업적 시스템

```typescript
interface Achievement {
  id: string;
  title: string;
  description: string;
  icon: string;
  rarity: 'common' | 'rare' | 'epic' | 'legendary';
  progress: number;
  maxProgress: number;
  unlocked: boolean;
  reward?: { type: string; amount: number };
}

class AchievementSystem {
  private achievements = new Map<string, Achievement>();

  register(id: string, title: string, desc: string, max: number, rarity: Achievement['rarity'] = 'common', reward?: Achievement['reward']) {
    this.achievements.set(id, { id, title, description: desc, icon: '', rarity, progress: 0, maxProgress: max, unlocked: false, reward });
  }

  progress(id: string, amount: number = 1): boolean {
    const a = this.achievements.get(id);
    if (!a || a.unlocked) return false;
    a.progress = Math.min(a.progress + amount, a.maxProgress);
    if (a.progress >= a.maxProgress) {
      a.unlocked = true;
      this.save();
      return true; // 해금됨! → 토스트 표시
    }
    this.save();
    return false;
  }

  // 기본 업적 세트
  static defaultAchievements(sys: AchievementSystem) {
    sys.register('first_kill', '첫 사냥', '적 1마리 처치', 1);
    sys.register('kill_100', '학살자', '적 100마리 처치', 100, 'rare', { type: 'coins', amount: 500 });
    sys.register('kill_1000', '전설의 사냥꾼', '적 1000마리 처치', 1000, 'epic', { type: 'coins', amount: 5000 });
    sys.register('survive_10min', '생존 전문가', '10분 생존', 1, 'rare');
    sys.register('level_10', '성장의 증거', '레벨 10 달성', 1);
    sys.register('no_damage', '무적', '데미지 없이 웨이브 클리어', 1, 'legendary');
    sys.register('all_weapons', '무기 수집가', '모든 무기 획득', 1, 'epic');
  }

  save() { localStorage.setItem('achievements', JSON.stringify([...this.achievements.values()])); }
  load() {
    const d = localStorage.getItem('achievements');
    if (d) JSON.parse(d).forEach((a: Achievement) => this.achievements.set(a.id, a));
  }
}
```

---

## 2. 데일리 리워드 (출석 보상)

```typescript
class DailyReward {
  private static REWARDS = [
    { day: 1, type: 'coins', amount: 100 },
    { day: 2, type: 'coins', amount: 150 },
    { day: 3, type: 'gems', amount: 10 },
    { day: 4, type: 'coins', amount: 200 },
    { day: 5, type: 'coins', amount: 250 },
    { day: 6, type: 'gems', amount: 25 },
    { day: 7, type: 'coins', amount: 500, bonus: true }, // 주간 보너스
  ];

  static canClaim(): boolean {
    const last = localStorage.getItem('daily_last');
    return !last || last !== new Date().toDateString();
  }

  static claim(): { type: string; amount: number; day: number; streak: number } | null {
    if (!this.canClaim()) return null;

    const today = new Date().toDateString();
    const yesterday = new Date(Date.now() - 86400000).toDateString();
    const last = localStorage.getItem('daily_last');
    let streak = parseInt(localStorage.getItem('daily_streak') || '0');

    streak = (last === yesterday) ? streak + 1 : 1;
    if (streak > 7) streak = 1; // 주간 리셋

    const reward = this.REWARDS[(streak - 1) % 7];
    localStorage.setItem('daily_last', today);
    localStorage.setItem('daily_streak', streak.toString());

    return { ...reward, day: reward.day, streak };
  }

  static getCalendar(): { day: number; type: string; amount: number; claimed: boolean; current: boolean }[] {
    const streak = parseInt(localStorage.getItem('daily_streak') || '0');
    return this.REWARDS.map((r, i) => ({
      ...r, claimed: i < streak, current: i === streak,
    }));
  }
}
```

---

## 3. 스크린샷 캡처 & 공유

```typescript
class ShareSystem {
  // Phaser 게임 스크린샷 캡처
  static capture(game: Phaser.Game): Promise<string> {
    return new Promise(resolve => {
      game.renderer.snapshot((img: HTMLImageElement) => {
        const canvas = document.createElement('canvas');
        canvas.width = img.width;
        canvas.height = img.height;
        canvas.getContext('2d')!.drawImage(img, 0, 0);
        resolve(canvas.toDataURL('image/png'));
      });
    });
  }

  // Web Share API (모바일 최적)
  static async share(title: string, text: string, dataURL?: string) {
    const shareData: ShareData = { title, text, url: location.href };

    if (dataURL && navigator.canShare) {
      const blob = await (await fetch(dataURL)).blob();
      const file = new File([blob], 'screenshot.png', { type: 'image/png' });
      if (navigator.canShare({ files: [file] })) {
        shareData.files = [file];
      }
    }

    if (navigator.share) {
      await navigator.share(shareData);
    } else {
      // 폴백: Twitter/Facebook 링크
      window.open(`https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(location.href)}`);
    }
  }
}
```

---

## 4. 튜토리얼 시스템

```typescript
class TutorialManager {
  private steps: { id: string; text: string; target?: string; action?: string }[] = [];
  private current = 0;
  private overlay: HTMLElement | null = null;

  addStep(id: string, text: string, target?: string, action?: string) {
    this.steps.push({ id, text, target, action });
  }

  start() {
    if (localStorage.getItem('tutorial_done')) return;
    this.current = 0;
    this.showStep();
  }

  private showStep() {
    if (this.current >= this.steps.length) {
      this.complete();
      return;
    }
    const step = this.steps[this.current];

    // 오버레이 생성
    if (this.overlay) this.overlay.remove();
    this.overlay = document.createElement('div');
    this.overlay.className = 'tutorial-overlay';
    this.overlay.innerHTML = `
      <div class="tutorial-box">
        <p>${step.text}</p>
        <div>
          <button onclick="this.closest('.tutorial-overlay').dispatchEvent(new Event('skip'))">건너뛰기</button>
          <button onclick="this.closest('.tutorial-overlay').dispatchEvent(new Event('next'))">다음</button>
        </div>
      </div>
    `;
    this.overlay.addEventListener('next', () => { this.current++; this.showStep(); });
    this.overlay.addEventListener('skip', () => this.complete());
    document.body.appendChild(this.overlay);

    // 타겟 요소 하이라이트
    if (step.target) {
      const el = document.querySelector(step.target) as HTMLElement;
      el?.classList.add('tutorial-highlight');
    }
  }

  private complete() {
    this.overlay?.remove();
    document.querySelectorAll('.tutorial-highlight').forEach(el => el.classList.remove('tutorial-highlight'));
    localStorage.setItem('tutorial_done', 'true');
  }

  // 기본 튜토리얼 세트
  static gameDefaults(tm: TutorialManager) {
    tm.addStep('move', 'WASD 또는 화살표로 이동하세요!');
    tm.addStep('attack', '자동으로 가장 가까운 적을 공격합니다.');
    tm.addStep('levelup', '레벨업 시 3개 중 1개를 선택하세요!');
    tm.addStep('shop', '상점에서 무기를 강화할 수 있습니다.');
  }
}
```

---

## 5. 히트맵 수집 (사망 위치 분석)

```typescript
class DeathHeatmap {
  private data: { x: number; y: number; wave: number; cause: string }[] = [];

  recordDeath(x: number, y: number, wave: number, cause: string) {
    this.data.push({ x, y, wave, cause });
    // 10% 샘플링으로 서버 전송
    if (Math.random() < 0.1 && this.data.length >= 10) this.flush();
  }

  // Canvas에 히트맵 시각화 (디버그용)
  render(ctx: CanvasRenderingContext2D, width: number, height: number) {
    for (const d of this.data) {
      const alpha = Math.min(0.8, this.data.filter(
        p => Math.abs(p.x - d.x) < 50 && Math.abs(p.y - d.y) < 50
      ).length * 0.1);
      ctx.fillStyle = `rgba(255, 0, 0, ${alpha})`;
      ctx.beginPath();
      ctx.arc(d.x, d.y, 20, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  private async flush() {
    const batch = [...this.data];
    this.data = [];
    try { await fetch('/api/heatmap', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(batch) }); }
    catch { this.data.unshift(...batch); } // 실패 시 복구
  }
}
```

---

## 6. A/B 테스트 프레임워크

```typescript
class ABTest {
  private experiments = new Map<string, { variants: string[]; weights: number[]; assigned?: string }>();

  register(id: string, variants: string[], weights?: number[]) {
    const w = weights || variants.map(() => 1 / variants.length);
    const saved = localStorage.getItem(`ab_${id}`);
    this.experiments.set(id, { variants, weights: w, assigned: saved || undefined });
  }

  getVariant(id: string): string {
    const exp = this.experiments.get(id);
    if (!exp) return 'control';
    if (exp.assigned) return exp.assigned;

    // 가중 랜덤 할당
    let r = Math.random();
    for (let i = 0; i < exp.variants.length; i++) {
      r -= exp.weights[i];
      if (r <= 0) {
        exp.assigned = exp.variants[i];
        localStorage.setItem(`ab_${id}`, exp.assigned);
        return exp.assigned;
      }
    }
    exp.assigned = exp.variants[0];
    localStorage.setItem(`ab_${id}`, exp.assigned);
    return exp.assigned;
  }

  // 사용 예
  static setup(ab: ABTest) {
    ab.register('upgrade_ui', ['cards', 'list', 'grid']); // 업그레이드 UI 실험
    ab.register('difficulty_curve', ['linear', 'exponential', 'adaptive']); // 난이도 곡선
    ab.register('reward_amount', ['low', 'medium', 'high']); // 보상 양
  }
}
```

---

## 7. 배틀패스 시스템

```typescript
interface BattlePassTier {
  level: number;
  xpRequired: number;
  freeReward: { type: string; amount: number; name: string } | null;
  premiumReward: { type: string; amount: number; name: string } | null;
}

class BattlePass {
  tiers: BattlePassTier[] = [];
  currentXP = 0;
  currentLevel = 0;
  isPremium = false;
  seasonEnd: Date;

  constructor(tierCount: number = 30) {
    this.seasonEnd = new Date(Date.now() + 30 * 86400000); // 30일 시즌
    for (let i = 1; i <= tierCount; i++) {
      this.tiers.push({
        level: i,
        xpRequired: 100 * i, // 점진적 증가
        freeReward: i % 3 === 0 ? { type: 'coins', amount: i * 50, name: `${i * 50} 코인` } : null,
        premiumReward: { type: i % 5 === 0 ? 'skin' : 'coins', amount: i * 100, name: i % 5 === 0 ? `시즌 스킨 ${Math.ceil(i / 5)}` : `${i * 100} 코인` },
      });
    }
    this.load();
  }

  addXP(amount: number): BattlePassTier[] {
    const rewards: BattlePassTier[] = [];
    this.currentXP += amount;
    while (this.currentLevel < this.tiers.length) {
      const tier = this.tiers[this.currentLevel];
      if (this.currentXP >= tier.xpRequired) {
        this.currentXP -= tier.xpRequired;
        this.currentLevel++;
        rewards.push(tier);
      } else break;
    }
    this.save();
    return rewards; // 해금된 보상 목록
  }

  getRemainingDays(): number {
    return Math.max(0, Math.ceil((this.seasonEnd.getTime() - Date.now()) / 86400000));
  }

  getProgress(): { level: number; xp: number; xpNeeded: number; percent: number } {
    const tier = this.tiers[this.currentLevel];
    return {
      level: this.currentLevel,
      xp: this.currentXP,
      xpNeeded: tier?.xpRequired || 0,
      percent: tier ? (this.currentXP / tier.xpRequired) * 100 : 100,
    };
  }

  save() { localStorage.setItem('battlepass', JSON.stringify({ xp: this.currentXP, level: this.currentLevel, premium: this.isPremium })); }
  load() {
    const d = localStorage.getItem('battlepass');
    if (d) { const p = JSON.parse(d); this.currentXP = p.xp; this.currentLevel = p.level; this.isPremium = p.premium; }
  }
}
```
