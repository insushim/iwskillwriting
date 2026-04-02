---
description: 마인크래프트 모드/플러그인 개발. "마인크래프트", "마크", "Minecraft", "모드", "Forge", "Fabric" 트리거.
---

# Minecraft 모드/플러그인 개발

## 개발 환경 선택

### Forge (Java Edition 모드)
```bash
# Forge MDK 다운로드 및 설정
# https://files.minecraftforge.net/
```

### Fabric (경량 모드)
```bash
# Fabric 템플릿
# https://fabricmc.net/develop/template/
```

### Bukkit/Spigot/Paper (서버 플러그인)
```bash
# Maven 프로젝트 생성
mvn archetype:generate -DgroupId=com.example -DartifactId=myplugin
```

## 프로젝트 구조

### Forge 모드
```
src/main/java/com/example/mod/
├── ExampleMod.java          # 메인 모드 클래스
├── init/
│   ├── ModItems.java        # 아이템 등록
│   ├── ModBlocks.java       # 블록 등록
│   └── ModEntities.java     # 엔티티 등록
├── items/
├── blocks/
├── entities/
└── client/
    └── renderer/
```

### Fabric 모드
```
src/main/java/com/example/mod/
├── ExampleMod.java          # 메인 (implements ModInitializer)
├── mixin/                   # Mixin 클래스
└── registry/
```

### Bukkit 플러그인
```
src/main/java/com/example/plugin/
├── MyPlugin.java            # extends JavaPlugin
├── commands/
├── listeners/
└── utils/
src/main/resources/
└── plugin.yml               # 플러그인 설정
```

## 핵심 코드 템플릿

### Forge 모드 메인 클래스
```java
@Mod("examplemod")
public class ExampleMod {
    public static final String MOD_ID = "examplemod";
    private static final Logger LOGGER = LogManager.getLogger();

    public ExampleMod() {
        IEventBus modEventBus = FMLJavaModLoadingContext.get().getModEventBus();
        modEventBus.addListener(this::setup);
        ModItems.register(modEventBus);
        ModBlocks.register(modEventBus);
    }

    private void setup(final FMLCommonSetupEvent event) {
        LOGGER.info("ExampleMod initialized!");
    }
}
```

### Fabric 모드 메인 클래스
```java
public class ExampleMod implements ModInitializer {
    public static final String MOD_ID = "examplemod";
    public static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);

    @Override
    public void onInitialize() {
        LOGGER.info("ExampleMod initialized!");
        ModItems.registerItems();
        ModBlocks.registerBlocks();
    }
}
```

### Bukkit 플러그인 메인 클래스
```java
public class MyPlugin extends JavaPlugin {
    @Override
    public void onEnable() {
        getLogger().info("Plugin enabled!");
        saveDefaultConfig();
        getCommand("mycommand").setExecutor(new MyCommand(this));
        getServer().getPluginManager().registerEvents(new MyListener(this), this);
    }

    @Override
    public void onDisable() {
        getLogger().info("Plugin disabled!");
    }
}
```

### plugin.yml (Bukkit)
```yaml
name: MyPlugin
version: 1.0.0
main: com.example.plugin.MyPlugin
api-version: 1.20
commands:
  mycommand:
    description: Example command
    usage: /<command>
permissions:
  myplugin.use:
    default: true
```

## 일반적인 기능 구현

### 커스텀 아이템 (Forge)
```java
public class ModItems {
    public static final DeferredRegister<Item> ITEMS =
        DeferredRegister.create(ForgeRegistries.ITEMS, ExampleMod.MOD_ID);

    public static final RegistryObject<Item> EXAMPLE_ITEM = ITEMS.register("example_item",
        () -> new Item(new Item.Properties()));
}
```

### 커스텀 블록 (Fabric)
```java
public class ModBlocks {
    public static final Block EXAMPLE_BLOCK = new Block(
        FabricBlockSettings.of(Material.METAL).strength(4.0f)
    );

    public static void registerBlocks() {
        Registry.register(Registries.BLOCK, new Identifier("modid", "example_block"), EXAMPLE_BLOCK);
    }
}
```

### 이벤트 리스너 (Bukkit)
```java
public class MyListener implements Listener {
    @EventHandler
    public void onPlayerJoin(PlayerJoinEvent event) {
        event.getPlayer().sendMessage("Welcome!");
    }

    @EventHandler
    public void onBlockBreak(BlockBreakEvent event) {
        if (event.getBlock().getType() == Material.DIAMOND_ORE) {
            event.getPlayer().sendMessage("You found diamonds!");
        }
    }
}
```

## 빌드 및 테스트

### Forge
```bash
./gradlew build
# 결과: build/libs/modid-version.jar
```

### Fabric
```bash
./gradlew build
# 결과: build/libs/modid-version.jar
```

### Bukkit/Paper
```bash
mvn package
# 결과: target/plugin-version.jar
```

## 디버깅
```bash
# Forge/Fabric - 개발 클라이언트 실행
./gradlew runClient

# 서버 실행
./gradlew runServer
```

$ARGUMENTS
