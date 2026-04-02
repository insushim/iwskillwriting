# Godot 4 Best Practices

## 프로젝트 초기화

```gdscript
# project.godot 필수 설정
[application]
config/name="GameName"
run/main_scene="res://scenes/main.tscn"
config/features=PackedStringArray("4.3", "GL Compatibility")

[display]
window/size/viewport_width=1280
window/size/viewport_height=720
window/stretch/mode="canvas_items"
window/stretch/aspect="expand"

[autoload]
GameManager="*res://autoload/game_manager.gd"
EventBus="*res://autoload/event_bus.gd"
AudioManager="*res://autoload/audio_manager.gd"

[input]
move_left={ "events": [Object(InputEventKey, "keycode": 65), Object(InputEventKey, "keycode": 4194319)] }
move_right={ "events": [Object(InputEventKey, "keycode": 68), Object(InputEventKey, "keycode": 4194321)] }
move_up={ "events": [Object(InputEventKey, "keycode": 87), Object(InputEventKey, "keycode": 4194320)] }
move_down={ "events": [Object(InputEventKey, "keycode": 83), Object(InputEventKey, "keycode": 4194322)] }
```

---

## 핵심 패턴

### 이벤트 버스
```gdscript
# autoload/event_bus.gd
extends Node

signal player_hit(damage: int)
signal enemy_killed(enemy_type: String, position: Vector2)
signal wave_started(wave_number: int)
signal wave_completed(wave_number: int)
signal score_changed(new_score: int)
signal coins_changed(new_coins: int)
signal game_over()
signal upgrade_selected(upgrade_id: String)
signal quiz_answered(correct: bool)
```

### 게임 매니저
```gdscript
# autoload/game_manager.gd
extends Node

var score: int = 0 :
    set(value):
        score = value
        EventBus.score_changed.emit(score)

var coins: int = 0 :
    set(value):
        coins = value
        EventBus.coins_changed.emit(coins)

var current_wave: int = 1
var player_hp: int = 100
var max_hp: int = 100
var is_paused: bool = false

func reset() -> void:
    score = 0
    coins = 0
    current_wave = 1
    player_hp = max_hp

func save_game() -> void:
    var save_data := {
        "score": score,
        "coins": coins,
        "wave": current_wave,
        "hp": player_hp,
    }
    var file := FileAccess.open("user://save.json", FileAccess.WRITE)
    file.store_string(JSON.stringify(save_data))

func load_game() -> bool:
    if not FileAccess.file_exists("user://save.json"):
        return false
    var file := FileAccess.open("user://save.json", FileAccess.READ)
    var data: Dictionary = JSON.parse_string(file.get_as_text())
    if data:
        score = data.get("score", 0)
        coins = data.get("coins", 0)
        current_wave = data.get("wave", 1)
        player_hp = data.get("hp", 100)
        return true
    return false
```

### 플레이어
```gdscript
# scripts/player.gd
extends CharacterBody2D

@export var speed: float = 200.0
@export var max_hp: int = 100

var hp: int = max_hp
var is_invincible: bool = false

@onready var sprite := $AnimatedSprite2D
@onready var weapon_mount := $WeaponMount
@onready var invincibility_timer := $InvincibilityTimer

func _physics_process(delta: float) -> void:
    var input_dir := Input.get_vector("move_left", "move_right", "move_up", "move_down")
    velocity = input_dir.normalized() * speed
    move_and_slide()

    # 애니메이션
    if velocity.length() > 0:
        sprite.play("walk")
        sprite.flip_h = velocity.x < 0
    else:
        sprite.play("idle")

func take_damage(amount: int) -> void:
    if is_invincible:
        return
    hp -= amount
    GameManager.player_hp = hp
    EventBus.player_hit.emit(amount)

    # 무적 프레임
    is_invincible = true
    invincibility_timer.start()

    # 깜빡임 효과
    var tween := create_tween()
    for i in range(5):
        tween.tween_property(sprite, "modulate:a", 0.3, 0.1)
        tween.tween_property(sprite, "modulate:a", 1.0, 0.1)

    if hp <= 0:
        die()

func die() -> void:
    EventBus.game_over.emit()
    queue_free()

func _on_invincibility_timer_timeout() -> void:
    is_invincible = false
    sprite.modulate.a = 1.0
```

### 적 (뱀 형태 예시)
```gdscript
# scripts/enemy_snake.gd
extends Node2D

@export var segment_count: int = 10
@export var segment_spacing: float = 20.0
@export var speed: float = 100.0
@export var hp_per_segment: int = 10

var segments: Array[CharacterBody2D] = []
var path_points: Array[Vector2] = []
var target: Node2D

func _ready() -> void:
    spawn_segments()

func spawn_segments() -> void:
    for i in range(segment_count):
        var seg := preload("res://scenes/enemy_segment.tscn").instantiate()
        seg.position = position + Vector2(i * segment_spacing, 0)
        seg.hp = hp_per_segment
        seg.is_head = (i == 0)
        add_child(seg)
        segments.append(seg)

func _physics_process(delta: float) -> void:
    if segments.is_empty():
        queue_free()
        return

    # 머리가 타겟 추적
    var head := segments[0]
    if target:
        var dir := (target.global_position - head.global_position).normalized()
        head.velocity = dir * speed
        head.move_and_slide()

    # 나머지 세그먼트는 앞 세그먼트 따라감
    for i in range(1, segments.size()):
        var prev := segments[i - 1]
        var curr := segments[i]
        var dist := curr.global_position.distance_to(prev.global_position)
        if dist > segment_spacing:
            var dir := (prev.global_position - curr.global_position).normalized()
            curr.velocity = dir * speed * 1.1  # 약간 더 빠르게 추적
            curr.move_and_slide()

func remove_segment(seg: CharacterBody2D) -> void:
    var idx := segments.find(seg)
    if idx >= 0:
        segments.remove_at(idx)
        seg.queue_free()
        EventBus.enemy_killed.emit("segment", seg.global_position)
```

### 웨이브 매니저
```gdscript
# scripts/wave_manager.gd
extends Node

signal wave_started(number: int)
signal wave_completed(number: int)
signal all_waves_completed()

@export var waves_data: Array[Dictionary] = []
var current_wave: int = 0
var enemies_alive: int = 0
var is_active: bool = false

func start_waves(data: Array[Dictionary]) -> void:
    waves_data = data
    current_wave = 0
    start_next_wave()

func start_next_wave() -> void:
    current_wave += 1
    if current_wave > waves_data.size():
        all_waves_completed.emit()
        return

    is_active = true
    wave_started.emit(current_wave)
    EventBus.wave_started.emit(current_wave)

    var wave := waves_data[current_wave - 1]
    enemies_alive = wave.get("enemy_count", 10)

    # 적 스폰
    for i in range(enemies_alive):
        var delay := i * wave.get("spawn_interval", 1.0)
        get_tree().create_timer(delay).timeout.connect(
            func(): spawn_enemy(wave)
        )

func spawn_enemy(wave_data: Dictionary) -> void:
    var enemy_scene := load(wave_data.get("enemy_scene", "res://scenes/enemy.tscn"))
    var enemy := enemy_scene.instantiate()
    # 화면 바깥 랜덤 위치에서 스폰
    var angle := randf() * TAU
    var dist := 500.0
    enemy.position = Vector2(cos(angle), sin(angle)) * dist + Vector2(640, 360)
    get_parent().add_child(enemy)

func on_enemy_killed() -> void:
    enemies_alive -= 1
    if enemies_alive <= 0:
        is_active = false
        wave_completed.emit(current_wave)
        EventBus.wave_completed.emit(current_wave)
```

---

## 씬 구조 가이드

### 메인 게임 씬 트리
```
Game (Node2D)
├── Background (Sprite2D 또는 ParallaxBackground)
├── Entities (Node2D)
│   ├── Player (CharacterBody2D)
│   │   ├── Sprite2D / AnimatedSprite2D
│   │   ├── CollisionShape2D
│   │   ├── WeaponMount (Node2D)
│   │   └── InvincibilityTimer (Timer)
│   ├── Enemies (Node2D)
│   └── Projectiles (Node2D)
├── Items (Node2D)
├── Effects (Node2D)
├── WaveManager (Node)
└── UI (CanvasLayer)
    ├── HUD (Control)
    │   ├── HPBar
    │   ├── ScoreLabel
    │   └── WaveLabel
    ├── PauseMenu (Control)
    └── GameOverPanel (Control)
```

---

## 성능 최적화
- `CharacterBody2D.move_and_slide()` 사용 (RigidBody2D 대신)
- 오브젝트 풀링 (`queue_free()` 최소화)
- `@onready` 변수로 노드 캐싱
- 시그널 기반 통신 (폴링 대신)
- `_physics_process`는 물리만, `_process`는 비주얼만
- VisibleOnScreenNotifier2D로 화면 밖 비활성화
