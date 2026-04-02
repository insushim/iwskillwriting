# Minecraft Development Skill

> 마인크래프트 모드, 플러그인, 데이터팩, 리소스팩 개발 전문가

## Triggers
- "마인크래프트", "마크", "Minecraft", "모드 만들어", "플러그인 만들어"
- "데이터팩", "리소스팩", "텍스처팩", "스킨"
- "Forge", "Fabric", "Spigot", "Paper", "Bukkit"

## Capabilities

### 1. Java Edition 모드 개발
```yaml
frameworks:
  - Forge (1.12.2 ~ 1.20.x)
  - Fabric (1.14 ~ 1.20.x)
  - NeoForge (1.20.1+)

features:
  - 커스텀 블록/아이템
  - 새로운 몹/엔티티
  - 월드 생성기
  - GUI/인벤토리
  - 네트워킹 패킷
```

### 2. 서버 플러그인 개발
```yaml
platforms:
  - Spigot/Paper (권장)
  - Bukkit
  - BungeeCord/Velocity (프록시)

features:
  - 커스텀 명령어
  - 이벤트 리스너
  - 경제 시스템
  - 권한 관리
  - MySQL/SQLite 연동
```

### 3. 데이터팩 개발
```yaml
components:
  - 커스텀 레시피
  - 전리품 테이블
  - 구조물 생성
  - 함수 (mcfunction)
  - 진행 상황/업적
  - 태그 시스템
```

### 4. 리소스팩 개발
```yaml
assets:
  - 텍스처 (blocks, items, entities)
  - 모델 (JSON)
  - 사운드
  - 셰이더 (OptiFine/Iris)
  - 언어 파일
```

## Project Templates

### Forge Mod (1.20.x)
```java
@Mod("mymod")
public class MyMod {
    public static final String MODID = "mymod";
    private static final Logger LOGGER = LogUtils.getLogger();

    public MyMod() {
        IEventBus modEventBus = FMLJavaModLoadingContext.get().getModEventBus();
        modEventBus.addListener(this::commonSetup);

        ModItems.register(modEventBus);
        ModBlocks.register(modEventBus);

        MinecraftForge.EVENT_BUS.register(this);
    }

    private void commonSetup(final FMLCommonSetupEvent event) {
        LOGGER.info("MyMod initialized!");
    }
}
```

### Spigot Plugin
```java
public class MyPlugin extends JavaPlugin {
    @Override
    public void onEnable() {
        saveDefaultConfig();
        getCommand("mycommand").setExecutor(new MyCommand());
        getServer().getPluginManager().registerEvents(new MyListener(), this);
        getLogger().info("Plugin enabled!");
    }

    @Override
    public void onDisable() {
        getLogger().info("Plugin disabled!");
    }
}
```

### Datapack Function
```mcfunction
# data/mypack/functions/main.mcfunction
scoreboard objectives add timer dummy
execute as @a at @s run function mypack:player_tick
schedule function mypack:main 1t
```

## Build Tools
```bash
# Forge/Fabric
./gradlew build

# Spigot Plugin
mvn clean package

# Datapack
zip -r mypack.zip data pack.mcmeta
```

## Best Practices
1. 버전 호환성 명시
2. 성능 최적화 (틱 최소화)
3. 설정 파일 제공
4. 다국어 지원
5. API 문서화
