# 멀티플레이어 & 백엔드 가이드

> Colyseus, Socket.io, Supabase, Firebase 기반 게임 백엔드

---

## 1. 리더보드 (Supabase)

```typescript
// Supabase 리더보드
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

class Leaderboard {
  async submitScore(playerName: string, score: number, gameMode: string = 'default') {
    const { error } = await supabase.from('leaderboard').upsert({
      player_name: playerName,
      score,
      game_mode: gameMode,
      created_at: new Date().toISOString(),
    }, { onConflict: 'player_name,game_mode' });
    return !error;
  }

  async getTopScores(limit: number = 10, gameMode: string = 'default') {
    const { data } = await supabase
      .from('leaderboard')
      .select('player_name, score, created_at')
      .eq('game_mode', gameMode)
      .order('score', { ascending: false })
      .limit(limit);
    return data || [];
  }

  async getPlayerRank(playerName: string, gameMode: string = 'default') {
    const { data } = await supabase.rpc('get_player_rank', {
      p_name: playerName,
      p_mode: gameMode,
    });
    return data;
  }
}

// SQL 함수 (Supabase에서 생성)
/*
CREATE TABLE leaderboard (
  id BIGSERIAL PRIMARY KEY,
  player_name TEXT NOT NULL,
  score INTEGER NOT NULL DEFAULT 0,
  game_mode TEXT NOT NULL DEFAULT 'default',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(player_name, game_mode)
);

CREATE INDEX idx_leaderboard_score ON leaderboard(game_mode, score DESC);

CREATE OR REPLACE FUNCTION get_player_rank(p_name TEXT, p_mode TEXT)
RETURNS INTEGER AS $$
  SELECT COUNT(*)::INTEGER + 1
  FROM leaderboard
  WHERE game_mode = p_mode AND score > (
    SELECT score FROM leaderboard WHERE player_name = p_name AND game_mode = p_mode
  );
$$ LANGUAGE SQL;
*/
```

---

## 2. 실시간 멀티플레이어 (Colyseus)

```typescript
// 서버 (colyseus)
import { Room, Client } from 'colyseus';
import { Schema, type, MapSchema } from '@colyseus/schema';

class Player extends Schema {
  @type("number") x: number = 0;
  @type("number") y: number = 0;
  @type("number") hp: number = 100;
  @type("string") name: string = "";
}

class GameState extends Schema {
  @type({ map: Player }) players = new MapSchema<Player>();
  @type("number") wave: number = 1;
}

class CoopGameRoom extends Room<GameState> {
  maxClients = 4;

  onCreate() {
    this.setState(new GameState());
    this.setSimulationInterval((dt) => this.update(dt));
  }

  onJoin(client: Client, options: any) {
    const player = new Player();
    player.name = options.name || `Player${this.clients.length}`;
    this.state.players.set(client.sessionId, player);
  }

  onMessage(client: Client, type: string, message: any) {
    const player = this.state.players.get(client.sessionId);
    if (!player) return;

    switch (type) {
      case 'move':
        player.x = message.x;
        player.y = message.y;
        break;
      case 'attack':
        this.broadcast('attack', { from: client.sessionId, ...message });
        break;
    }
  }

  onLeave(client: Client) {
    this.state.players.delete(client.sessionId);
  }

  update(dt: number) {
    // 서버 측 게임 로직
  }
}
```

---

## 3. 클라우드 세이브 (Firebase)

```typescript
import { initializeApp } from 'firebase/app';
import { getFirestore, doc, setDoc, getDoc } from 'firebase/firestore';
import { getAuth, signInAnonymously } from 'firebase/auth';

class CloudSave {
  private db;
  private auth;

  constructor(config: any) {
    const app = initializeApp(config);
    this.db = getFirestore(app);
    this.auth = getAuth(app);
  }

  async init() {
    await signInAnonymously(this.auth);
    return this.auth.currentUser?.uid;
  }

  async save(data: any) {
    const uid = this.auth.currentUser?.uid;
    if (!uid) return;
    await setDoc(doc(this.db, 'saves', uid), {
      ...data,
      updatedAt: Date.now(),
    });
  }

  async load(): Promise<any | null> {
    const uid = this.auth.currentUser?.uid;
    if (!uid) return null;
    const snap = await getDoc(doc(this.db, 'saves', uid));
    return snap.exists() ? snap.data() : null;
  }
}
```

---

## 4. 게임 분석 (커스텀)

```typescript
class GameAnalytics {
  private events: AnalyticsEvent[] = [];
  private sessionId = crypto.randomUUID();
  private endpoint = '/api/analytics'; // 또는 Supabase

  trackEvent(name: string, data: Record<string, any> = {}) {
    this.events.push({
      event: name,
      session: this.sessionId,
      timestamp: Date.now(),
      data,
    });

    // 10개 모이면 배치 전송
    if (this.events.length >= 10) this.flush();
  }

  // 주요 이벤트
  trackGameStart(mode: string) { this.trackEvent('game_start', { mode }); }
  trackGameEnd(score: number, wave: number, duration: number) {
    this.trackEvent('game_end', { score, wave, duration });
  }
  trackLevelUp(level: number, choice: string) {
    this.trackEvent('level_up', { level, choice });
  }
  trackDeath(cause: string, wave: number) {
    this.trackEvent('death', { cause, wave });
  }
  trackPurchase(item: string, cost: number) {
    this.trackEvent('purchase', { item, cost });
  }

  async flush() {
    if (this.events.length === 0) return;
    const batch = [...this.events];
    this.events = [];

    try {
      await fetch(this.endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(batch),
      });
    } catch {
      // 실패하면 다시 큐에 넣기
      this.events.unshift(...batch);
    }
  }
}
```
