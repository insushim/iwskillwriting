# 프로시저럴 사운드 생성 가이드

## 개요

게임 에셋 중 사운드는 AI 이미지 생성만큼 자동화가 어렵습니다.
이 가이드에서는 외부 API 없이 코드만으로 게임 사운드를 생성하는 방법을 다룹니다.

---

## 방법 1: Web Audio API (Phaser / HTML5)

### 효과음 생성기 클래스

```typescript
// src/systems/SoundSynth.ts
export class SoundSynth {
  private ctx: AudioContext;

  constructor() {
    this.ctx = new AudioContext();
  }

  private playTone(
    freq: number, duration: number, type: OscillatorType = 'sine',
    volume: number = 0.3, freqEnd?: number
  ): void {
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.connect(gain);
    gain.connect(this.ctx.destination);
    const now = this.ctx.currentTime;
    osc.type = type;
    osc.frequency.setValueAtTime(freq, now);
    if (freqEnd) osc.frequency.exponentialRampToValueAtTime(freqEnd, now + duration);
    gain.gain.setValueAtTime(volume, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + duration);
    osc.start(now);
    osc.stop(now + duration);
  }

  private playNoise(duration: number, volume: number = 0.3): void {
    const bufferSize = this.ctx.sampleRate * duration;
    const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
    const data = buffer.getChannelData(0);
    for (let i = 0; i < bufferSize; i++) {
      data[i] = (Math.random() * 2 - 1) * (1 - i / bufferSize);
    }
    const source = this.ctx.createBufferSource();
    source.buffer = buffer;
    const gain = this.ctx.createGain();
    source.connect(gain);
    gain.connect(this.ctx.destination);
    gain.gain.setValueAtTime(volume, this.ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + duration);
    source.start();
    source.stop(this.ctx.currentTime + duration);
  }

  // ═══ 게임 효과음 프리셋 ═══

  /** 기본 공격 (슈팅) */
  shoot(): void {
    this.playTone(600, 0.08, 'square', 0.2, 200);
  }

  /** 적 피격 */
  hit(): void {
    this.playTone(200, 0.1, 'square', 0.25, 50);
  }

  /** 적 사망 */
  kill(): void {
    this.playTone(300, 0.05, 'square', 0.2, 100);
    setTimeout(() => this.playTone(500, 0.08, 'sine', 0.15, 200), 50);
  }

  /** 코인/아이템 획득 */
  coin(): void {
    this.playTone(800, 0.05, 'sine', 0.2);
    setTimeout(() => this.playTone(1200, 0.1, 'sine', 0.15), 50);
  }

  /** 레벨업 */
  levelUp(): void {
    const notes = [523, 659, 784, 1047]; // C5-E5-G5-C6
    notes.forEach((freq, i) => {
      setTimeout(() => this.playTone(freq, 0.15, 'sine', 0.2), i * 100);
    });
  }

  /** 폭발 */
  explosion(): void {
    this.playNoise(0.3, 0.4);
    this.playTone(80, 0.3, 'sine', 0.3, 20);
  }

  /** 플레이어 피격 */
  playerHit(): void {
    this.playTone(150, 0.15, 'sawtooth', 0.3, 50);
    this.playNoise(0.05, 0.15);
  }

  /** 게임 오버 */
  gameOver(): void {
    const notes = [392, 349, 330, 262]; // G4-F4-E4-C4 (하강)
    notes.forEach((freq, i) => {
      setTimeout(() => this.playTone(freq, 0.3, 'sine', 0.25), i * 250);
    });
  }

  /** UI 클릭 */
  click(): void {
    this.playTone(1000, 0.03, 'sine', 0.1);
  }

  /** UI 호버 */
  hover(): void {
    this.playTone(800, 0.02, 'sine', 0.05);
  }

  /** 보물상자 열기 */
  chestOpen(): void {
    const notes = [262, 330, 392, 523, 659]; // C4-E4-G4-C5-E5
    notes.forEach((freq, i) => {
      setTimeout(() => this.playTone(freq, 0.12, 'sine', 0.15 + i * 0.02), i * 80);
    });
  }

  /** 카드 선택 / 업그레이드 */
  cardSelect(): void {
    this.playTone(440, 0.05, 'sine', 0.15);
    setTimeout(() => this.playTone(880, 0.1, 'sine', 0.2), 50);
  }

  /** 웨이브 시작 경고 */
  waveWarning(): void {
    for (let i = 0; i < 3; i++) {
      setTimeout(() => this.playTone(600, 0.1, 'square', 0.2), i * 200);
    }
  }

  /** 보스 등장 */
  bossAppear(): void {
    this.playTone(100, 0.5, 'sawtooth', 0.3, 50);
    setTimeout(() => this.playNoise(0.3, 0.2), 300);
    setTimeout(() => this.playTone(80, 0.8, 'sine', 0.4, 30), 500);
  }

  /** 퀴즈 정답 */
  quizCorrect(): void {
    this.playTone(523, 0.08, 'sine', 0.2);
    setTimeout(() => this.playTone(659, 0.08, 'sine', 0.2), 80);
    setTimeout(() => this.playTone(784, 0.15, 'sine', 0.25), 160);
  }

  /** 퀴즈 오답 */
  quizWrong(): void {
    this.playTone(200, 0.15, 'square', 0.2, 100);
    setTimeout(() => this.playTone(150, 0.2, 'square', 0.2, 80), 150);
  }

  /** 치유 / 회복 */
  heal(): void {
    const notes = [392, 440, 494, 523]; // G4-A4-B4-C5
    notes.forEach((freq, i) => {
      setTimeout(() => this.playTone(freq, 0.1, 'sine', 0.12), i * 60);
    });
  }

  /** 스킬/마법 시전 */
  magic(): void {
    for (let i = 0; i < 8; i++) {
      const freq = 300 + Math.random() * 1200;
      setTimeout(() => this.playTone(freq, 0.04, 'sine', 0.08), i * 30);
    }
  }
}
```

### Phaser에서 사용

```typescript
// GameScene.ts
import { SoundSynth } from '../systems/SoundSynth';

export class GameScene extends Phaser.Scene {
  private synth!: SoundSynth;

  create(): void {
    this.synth = new SoundSynth();

    // 이벤트 연결
    this.events.on('enemy-hit', () => this.synth.hit());
    this.events.on('enemy-kill', () => this.synth.kill());
    this.events.on('player-hit', () => this.synth.playerHit());
    this.events.on('coin-collect', () => this.synth.coin());
    this.events.on('level-up', () => this.synth.levelUp());
  }

  fireWeapon(): void {
    this.synth.shoot();
    // ... 발사 로직
  }
}
```

---

## 방법 2: 간단한 BGM 생성 (루프 음악)

### 프로시저럴 배경음악

```typescript
export class BGMGenerator {
  private ctx: AudioContext;
  private gainNode: GainNode;
  private isPlaying: boolean = false;

  constructor() {
    this.ctx = new AudioContext();
    this.gainNode = this.ctx.createGain();
    this.gainNode.connect(this.ctx.destination);
    this.gainNode.gain.value = 0.15;
  }

  /** 판타지/모험 테마 BGM */
  playFantasyLoop(): void {
    if (this.isPlaying) return;
    this.isPlaying = true;

    // C 마이너 스케일 기반 멜로디
    const melody = [
      { note: 262, dur: 0.4 },  // C4
      { note: 311, dur: 0.4 },  // Eb4
      { note: 349, dur: 0.2 },  // F4
      { note: 392, dur: 0.6 },  // G4
      { note: 349, dur: 0.3 },  // F4
      { note: 311, dur: 0.3 },  // Eb4
      { note: 262, dur: 0.8 },  // C4
      { note: 0, dur: 0.4 },    // rest
      { note: 392, dur: 0.4 },  // G4
      { note: 466, dur: 0.4 },  // Bb4
      { note: 523, dur: 0.6 },  // C5
      { note: 466, dur: 0.2 },  // Bb4
      { note: 392, dur: 0.4 },  // G4
      { note: 349, dur: 0.4 },  // F4
      { note: 311, dur: 0.8 },  // Eb4
      { note: 0, dur: 0.4 },    // rest
    ];

    const loopDuration = melody.reduce((sum, n) => sum + n.dur, 0);

    const playLoop = () => {
      if (!this.isPlaying) return;
      let time = this.ctx.currentTime;

      melody.forEach(({ note, dur }) => {
        if (note > 0) {
          const osc = this.ctx.createOscillator();
          const env = this.ctx.createGain();
          osc.connect(env);
          env.connect(this.gainNode);
          osc.type = 'sine';
          osc.frequency.value = note;
          env.gain.setValueAtTime(0.001, time);
          env.gain.exponentialRampToValueAtTime(0.3, time + 0.02);
          env.gain.exponentialRampToValueAtTime(0.001, time + dur - 0.02);
          osc.start(time);
          osc.stop(time + dur);
        }
        time += dur;
      });

      // 다음 루프 예약
      setTimeout(playLoop, loopDuration * 1000);
    };

    playLoop();
  }

  /** 전투 BGM (빠른 템포) */
  playBattleLoop(): void {
    if (this.isPlaying) return;
    this.isPlaying = true;

    const bpm = 140;
    const beat = 60 / bpm;

    // 베이스 + 드럼 패턴
    const playBeat = () => {
      if (!this.isPlaying) return;
      const now = this.ctx.currentTime;

      for (let i = 0; i < 8; i++) {
        const t = now + i * beat;

        // 킥 드럼 (매 비트)
        if (i % 2 === 0) {
          const osc = this.ctx.createOscillator();
          const gain = this.ctx.createGain();
          osc.connect(gain);
          gain.connect(this.gainNode);
          osc.frequency.setValueAtTime(150, t);
          osc.frequency.exponentialRampToValueAtTime(30, t + 0.1);
          gain.gain.setValueAtTime(0.5, t);
          gain.gain.exponentialRampToValueAtTime(0.001, t + 0.1);
          osc.start(t);
          osc.stop(t + 0.1);
        }

        // 하이햇 (매 비트)
        const bufSize = this.ctx.sampleRate * 0.03;
        const buf = this.ctx.createBuffer(1, bufSize, this.ctx.sampleRate);
        const data = buf.getChannelData(0);
        for (let j = 0; j < bufSize; j++) {
          data[j] = (Math.random() * 2 - 1) * (1 - j / bufSize);
        }
        const noise = this.ctx.createBufferSource();
        noise.buffer = buf;
        const nGain = this.ctx.createGain();
        noise.connect(nGain);
        nGain.connect(this.gainNode);
        nGain.gain.setValueAtTime(0.1, t);
        nGain.gain.exponentialRampToValueAtTime(0.001, t + 0.03);
        noise.start(t);
        noise.stop(t + 0.03);

        // 베이스 라인
        const bassNotes = [131, 131, 156, 131, 175, 175, 156, 131]; // C3 패턴
        const bass = this.ctx.createOscillator();
        const bGain = this.ctx.createGain();
        bass.connect(bGain);
        bGain.connect(this.gainNode);
        bass.type = 'sawtooth';
        bass.frequency.value = bassNotes[i];
        bGain.gain.setValueAtTime(0.15, t);
        bGain.gain.exponentialRampToValueAtTime(0.001, t + beat * 0.8);
        bass.start(t);
        bass.stop(t + beat * 0.8);
      }

      setTimeout(playBeat, 8 * beat * 1000);
    };

    playBeat();
  }

  stop(): void {
    this.isPlaying = false;
  }

  setVolume(value: number): void {
    this.gainNode.gain.value = Math.max(0, Math.min(1, value));
  }
}
```

---

## 방법 3: Godot GDScript 사운드

```gdscript
# autoload/audio_manager.gd
extends Node

var sfx_volume: float = 1.0
var bgm_volume: float = 0.7

# 프로시저럴 효과음
func play_synth_sfx(type: String) -> void:
    var player := AudioStreamPlayer.new()
    add_child(player)

    var gen := AudioStreamGenerator.new()
    gen.mix_rate = 44100.0
    gen.buffer_length = 0.5
    player.stream = gen
    player.volume_db = linear_to_db(sfx_volume)
    player.play()

    var playback: AudioStreamGeneratorPlayback = player.get_stream_playback()

    match type:
        "shoot":
            _generate_tone(playback, 600, 0.08, 200)
        "hit":
            _generate_tone(playback, 200, 0.1, 50)
        "coin":
            _generate_tone(playback, 800, 0.05)
            _generate_tone(playback, 1200, 0.1)
        "explosion":
            _generate_noise(playback, 0.3)

    # 자동 정리
    await get_tree().create_timer(1.0).timeout
    player.queue_free()

func _generate_tone(playback: AudioStreamGeneratorPlayback,
                     freq: float, duration: float,
                     freq_end: float = -1.0) -> void:
    var sample_rate := 44100.0
    var samples := int(sample_rate * duration)
    var current_freq := freq

    for i in range(samples):
        var t := float(i) / sample_rate
        var progress := float(i) / float(samples)

        if freq_end > 0:
            current_freq = lerp(freq, freq_end, progress)

        var sample := sin(TAU * current_freq * t) * (1.0 - progress) * 0.3
        playback.push_frame(Vector2(sample, sample))

func _generate_noise(playback: AudioStreamGeneratorPlayback,
                      duration: float) -> void:
    var samples := int(44100.0 * duration)
    for i in range(samples):
        var progress := float(i) / float(samples)
        var sample := (randf() * 2.0 - 1.0) * (1.0 - progress) * 0.4
        playback.push_frame(Vector2(sample, sample))
```

---

## 외부 오디오 API (선택사항)

코드 생성 사운드가 만족스럽지 않을 경우:

| API | 용도 | 비용 |
|-----|------|------|
| ElevenLabs SFX | 효과음 생성 | 유료 |
| Stable Audio | BGM 생성 | 유료 |
| Freesound.org | 무료 효과음 다운로드 | 무료 |
| Kenny.nl Audio | 게임용 무료 사운드팩 | 무료 |
| OpenGameArt.org | 무료 게임 오디오 | 무료 |

### 무료 사운드 다운로드 스크립트

```bash
# Kenny.nl 게임 사운드팩 다운로드 (CC0 라이선스)
mkdir -p assets/audio
# 수동 다운로드: https://kenney.nl/assets/category:Audio
# 추천 팩: "Interface Sounds", "Impact Sounds", "Digital Audio"
```

---

## 추천 조합

| 게임 유형 | BGM | SFX |
|-----------|-----|-----|
| 아케이드/캐주얼 | 프로시저럴 루프 | 프로시저럴 Web Audio |
| RPG/어드벤처 | 무료 음원(Freesound) | 프로시저럴 + 무료 |
| 교육/퀴즈 | 프로시저럴 차분한 BGM | 정답/오답 프로시저럴 |
| 디펜스/서바이벌 | 프로시저럴 전투 BGM | 프로시저럴 전투 SFX |
